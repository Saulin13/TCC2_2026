import argparse
import json
import os
import subprocess
from pathlib import Path
import sys

import pandas as pd

from csv_columns import prepare_csv_for_save
from dataset_config import (
    BASE_DIR,
    DatasetConfig,
    add_dataset_argument,
    function_importable,
    resolve_dataset,
    resolve_installed_module_file,
    resolve_module_path_from_row,
)

DATASET_THEALGORITHMS = "thealgorithms"
DATASET_REAL = "real"

COVERAGE_JSON = BASE_DIR / "coverage.json"
DOT_COVERAGE = BASE_DIR / ".coverage"

MERGE_KEYS = ("function_name", "file_path")

RESULT_COLUMNS = [
    "function_name",
    "file_path",
    "complexity_score",
    "complexity_level",
    "test_file",
    "execution_status",
    "passed",
    "return_code",
    "coverage_percent",
    "stdout",
    "stderr",
    "coverage_error",
    "coverage_status",
    "coverage_return_code",
    "module_path",
    "source_file",
    "error_type",
    "error_message",
]

EXECUTION_COLUMNS = [
    "function_name",
    "file_path",
    "complexity_level",
    "test_file",
    "execution_status",
    "passed",
    "return_code",
    "stdout",
    "stderr",
]


def _cleanup_coverage_artifacts() -> None:
    """Remove artefatos do coverage.py antes de cada execução."""
    for p in (COVERAGE_JSON, DOT_COVERAGE):
        if p.exists():
            try:
                p.unlink()
            except OSError:
                pass


def _coverage_percent_for_source(cov: dict, source_file: Path) -> float:
    """Percentual coberto do arquivo fonte no relatório JSON do coverage."""
    files = cov.get("files") or {}
    if not files:
        return float(cov.get("totals", {}).get("percent_covered", 0.0) or 0.0)

    try:
        want = source_file.resolve()
    except OSError:
        want = source_file

    def resolve_key(key: str) -> Path:
        p = Path(str(key).replace("\\", "/"))
        try:
            if p.is_absolute():
                return p.resolve()
            return (BASE_DIR / p).resolve()
        except OSError:
            return p

    resolved_pairs = []
    for key, meta in files.items():
        try:
            kp = resolve_key(key)
            if kp == want:
                return float(meta["summary"]["percent_covered"])
            resolved_pairs.append((kp, meta))
        except (OSError, KeyError, TypeError, ValueError):
            continue

    # Uma única entrada no relatório costuma ser o arquivo medido
    if len(resolved_pairs) == 1:
        return float(resolved_pairs[0][1]["summary"]["percent_covered"])

    for kp, meta in resolved_pairs:
        if kp.name == want.name and kp.parent.name == want.parent.name:
            return float(meta["summary"]["percent_covered"])

    return float(cov.get("totals", {}).get("percent_covered", 0.0) or 0.0)


def _decode_subprocess_output(raw: object) -> str:
    if raw is None:
        return ""
    if isinstance(raw, str):
        return raw
    return bytes(raw).decode("utf-8", errors="replace")


def _execution_status(return_code: int) -> str:
    if return_code == 0:
        return "ok"
    if return_code == 1:
        return "tests_failed"
    if return_code >= 2:
        return "pytest_error"
    return "error"


def _prepare_run_env(cfg: DatasetConfig) -> dict[str, str]:
    """Para dataset real, não injeta repos/scikit-learn no PYTHONPATH."""
    env = os.environ.copy()
    repo = os.fspath(cfg.repo_path)

    if cfg.key == DATASET_REAL:
        pythonpath = env.get("PYTHONPATH", "")
        if pythonpath:
            parts = [p for p in pythonpath.split(os.pathsep) if p and os.path.normpath(p) != os.path.normpath(repo)]
            if parts:
                env["PYTHONPATH"] = os.pathsep.join(parts)
            else:
                env.pop("PYTHONPATH", None)
    else:
        env["PYTHONPATH"] = repo
    return env


def _build_pytest_cmd(test_arg: str) -> list[str]:
    return [sys.executable, "-m", "pytest", "-q", test_arg]


def _build_coverage_run_cmd(
    *,
    test_arg: str,
    module_path: str,
    coverage_target: Path,
) -> list[str]:
    source_dir = os.fspath(coverage_target.resolve().parent)
    return [
        sys.executable,
        "-m",
        "coverage",
        "run",
        "--source",
        source_dir,
        "-m",
        "pytest",
        "-q",
        test_arg,
    ]


def _build_real_coverage_run_cmd(*, test_arg: str, module_path: str) -> list[str]:
    source_pkg = module_path.split(".", 1)[0] if module_path else module_path
    return [
        sys.executable,
        "-m",
        "coverage",
        "run",
        "--source",
        source_pkg,
        "--include",
        module_path.replace(".", "/") + ".py",
        "-m",
        "pytest",
        "-q",
        test_arg,
    ]


def _read_coverage_percent(coverage_target: Path | None) -> tuple[float, str]:
    """Lê .coverage existente. Retorna (coverage_percent, coverage_error)."""
    errors: list[str] = []

    if not DOT_COVERAGE.exists():
        return 0.0, ".coverage não foi gerado após coverage run"

    json_completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "coverage",
            "json",
            "-o",
            os.fspath(COVERAGE_JSON),
        ],
        cwd=str(BASE_DIR),
        capture_output=True,
    )
    jerr = _decode_subprocess_output(json_completed.stderr)
    if jerr.strip():
        errors.append(f"[coverage-json] {jerr.strip()}")
    if json_completed.returncode != 0:
        errors.append(
            f"[coverage-json] código de saída {json_completed.returncode}"
        )

    if not COVERAGE_JSON.exists():
        return 0.0, "\n".join(errors) if errors else "coverage.json não foi gerado"

    try:
        with COVERAGE_JSON.open("r", encoding="utf-8") as f:
            cov_data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        errors.append(f"[coverage-parse] {e}")
        return 0.0, "\n".join(errors)

    if coverage_target is not None and coverage_target.exists():
        return _coverage_percent_for_source(cov_data, coverage_target), "\n".join(errors)

    if errors:
        return 0.0, "\n".join(errors)
    return 0.0, "arquivo fonte do módulo instalado não encontrado para mapear cobertura"


def _run_real_coverage(
    *,
    test_arg: str,
    module_path: str,
    coverage_target: Path | None,
    env: dict[str, str],
    timeout: int = 30,
) -> tuple[float, str, str, int]:
    """Segundo passo (dataset real): coverage isolado; não altera status de execução."""
    _cleanup_coverage_artifacts()
    errors: list[str] = []

    try:
        completed = subprocess.run(
            _build_real_coverage_run_cmd(test_arg=test_arg, module_path=module_path),
            env=env,
            cwd=str(BASE_DIR),
            capture_output=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        _cleanup_coverage_artifacts()
        return 0.0, "coverage run excedeu timeout", "timeout", -3
    except OSError as e:
        _cleanup_coverage_artifacts()
        return 0.0, f"erro ao executar coverage: {e}", "error", -2

    cov_stdout = _decode_subprocess_output(completed.stdout)
    cov_stderr = _decode_subprocess_output(completed.stderr)
    if completed.returncode != 0:
        errors.append(f"coverage run retornou código {completed.returncode}")
    if cov_stderr.strip():
        errors.append(cov_stderr.strip())
    if cov_stdout.strip():
        errors.append(cov_stdout.strip())

    cov_pct, read_err = _read_coverage_percent(coverage_target)
    if read_err.strip():
        errors.append(read_err.strip())

    _cleanup_coverage_artifacts()
    error_text = "\n".join(errors).strip()
    if completed.returncode != 0:
        coverage_status = "failed"
    elif cov_pct > 0:
        coverage_status = "ok"
    elif error_text:
        coverage_status = "no_data"
    else:
        coverage_status = "ok"
    return cov_pct, error_text, coverage_status, int(completed.returncode)


def _summarize_error(stdout: str, stderr: str, coverage_error: str) -> tuple[str, str]:
    text = "\n".join(part for part in (stderr, coverage_error, stdout) if part).strip()
    if not text:
        return "", ""
    lowered = text.lower()
    if "modulenotfounderror" in lowered or "importerror" in lowered:
        etype = "import_error"
    elif "assert" in lowered or "failed" in lowered:
        etype = "assertion_failure"
    elif "timeout" in lowered:
        etype = "timeout"
    elif "syntaxerror" in lowered:
        etype = "syntax_error"
    else:
        etype = "runtime_error"
    first_line = next((ln.strip() for ln in text.splitlines() if ln.strip()), "")
    return etype, first_line[:500]


def _load_sample_unique(sample_csv: Path) -> pd.DataFrame:
    df = pd.read_csv(sample_csv)
    before = len(df)
    df = df.drop_duplicates(subset=list(MERGE_KEYS), keep="first").reset_index(drop=True)
    removed = before - len(df)
    if removed > 0:
        print(f"Aviso: {removed} linha(s) duplicada(s) removida(s) da amostra.")
    return df


def run_tests_for_generator(
    *,
    cfg: DatasetConfig,
    generator_name: str,
    tests_dir: Path,
    output_coverage_csv: Path,
    output_execution_csv: Path,
) -> None:
    sample_csv = cfg.sample_csv
    repo_path = cfg.repo_path

    if not sample_csv.exists():
        print(f"Arquivo não encontrado: {sample_csv}")
        return

    cfg.results_dir.mkdir(parents=True, exist_ok=True)
    tests_dir.mkdir(parents=True, exist_ok=True)
    df = _load_sample_unique(sample_csv)

    env = _prepare_run_env(cfg)
    use_installed_sklearn = cfg.key == DATASET_REAL

    rows_out: list[dict] = []
    debug_rows: list[dict] = []
    n = len(df)

    print(f"Dataset: {cfg.key}")
    if use_installed_sklearn:
        print(
            "Modo real: pytest puro classifica execução; coverage em passo separado "
            "(sklearn via pip, sem PYTHONPATH do clone)."
        )
    print(
        f"Iniciando execução ({generator_name}): {n} teste(s) "
        f"(cobertura + execução por arquivo)..."
    )

    for pos, (_, row) in enumerate(df.iterrows()):
        func_name = str(row["function_name"])
        file_path_cell = row["file_path"]
        module_path = resolve_module_path_from_row(row, dataset_key=cfg.key)

        seq = pos + 1
        test_path = tests_dir / f"test_{seq:03d}_{func_name}.py"
        test_rel = test_path.relative_to(BASE_DIR).as_posix()

        print(f"[{seq}/{n}] {func_name}...", end=" ", flush=True)

        if not test_path.exists():
            row_payload = {
                "function_name": func_name,
                "file_path": file_path_cell,
                "complexity_score": row["complexity_score"],
                "complexity_level": row["complexity_level"],
                "test_file": test_rel,
                "execution_status": "missing_test_file",
                "passed": False,
                "return_code": -1,
                "coverage_percent": 0.0,
                "stdout": "",
                "stderr": "",
                "coverage_error": "",
                "coverage_status": "not_run",
                "coverage_return_code": -1,
                "module_path": module_path,
                "source_file": "",
                "error_type": "missing_test_file",
                "error_message": "Arquivo de teste não encontrado.",
            }
            rows_out.append(row_payload)
            debug_rows.append(row_payload.copy())
            print("sem arquivo de teste")
            continue

        coverage_target: Path | None = None

        if use_installed_sklearn:
            if not function_importable(module_path, func_name):
                row_payload = {
                    "function_name": func_name,
                    "file_path": file_path_cell,
                    "complexity_score": row["complexity_score"],
                    "complexity_level": row["complexity_level"],
                    "test_file": test_rel,
                    "execution_status": "missing_source_module",
                    "passed": False,
                    "return_code": -2,
                    "coverage_percent": 0.0,
                    "stdout": "",
                    "stderr": (
                        f"Função não importável no sklearn instalado: "
                        f"{module_path}.{func_name}"
                    ),
                    "coverage_error": "",
                    "coverage_status": "not_run",
                    "coverage_return_code": -1,
                    "module_path": module_path,
                    "source_file": "",
                    "error_type": "missing_source_module",
                    "error_message": f"{module_path}.{func_name} não importável no sklearn instalado.",
                }
                rows_out.append(row_payload)
                debug_rows.append(row_payload.copy())
                print("módulo/função ausente no pip")
                continue
            coverage_target = resolve_installed_module_file(module_path)
        else:
            source_file = repo_path / Path(str(file_path_cell).replace("\\", "/"))
            if not source_file.exists():
                try:
                    disp = source_file.relative_to(BASE_DIR).as_posix()
                except ValueError:
                    disp = os.fspath(source_file)
                row_payload = {
                    "function_name": func_name,
                    "file_path": file_path_cell,
                    "complexity_score": row["complexity_score"],
                    "complexity_level": row["complexity_level"],
                    "test_file": test_rel,
                    "execution_status": "missing_source_file",
                    "passed": False,
                    "return_code": -2,
                    "coverage_percent": 0.0,
                    "stdout": "",
                    "stderr": f"Arquivo fonte não encontrado: {disp}",
                    "coverage_error": "",
                    "coverage_status": "not_run",
                    "coverage_return_code": -1,
                    "module_path": module_path,
                    "source_file": os.fspath(source_file),
                    "error_type": "missing_source_file",
                    "error_message": f"Arquivo fonte não encontrado: {disp}",
                }
                rows_out.append(row_payload)
                debug_rows.append(row_payload.copy())
                print("fonte ausente")
                continue
            coverage_target = source_file

        test_arg = os.fspath(test_path.resolve())

        if use_installed_sklearn:
            try:
                pytest_completed = subprocess.run(
                    _build_pytest_cmd(test_arg),
                    env=env,
                    cwd=str(BASE_DIR),
                    capture_output=True,
                    timeout=30,
                )
            except subprocess.TimeoutExpired as e:
                stdout = _decode_subprocess_output(e.stdout)
                stderr = _decode_subprocess_output(e.stderr)
                if not stderr.strip():
                    stderr = f"pytest excedeu timeout de {e.timeout}s"
                else:
                    stderr = f"{stderr}\n(timeout de {e.timeout}s)".strip()
                error_type, error_message = _summarize_error(
                    stdout, stderr, "não executado: timeout no pytest"
                )
                row_payload = {
                    "function_name": func_name,
                    "file_path": file_path_cell,
                    "complexity_score": row["complexity_score"],
                    "complexity_level": row["complexity_level"],
                    "test_file": test_rel,
                    "execution_status": "timeout",
                    "passed": False,
                    "return_code": -3,
                    "coverage_percent": 0.0,
                    "stdout": stdout,
                    "stderr": stderr,
                    "coverage_error": "não executado: timeout no pytest",
                    "coverage_status": "not_run",
                    "coverage_return_code": -1,
                    "module_path": module_path,
                    "source_file": os.fspath(coverage_target) if coverage_target else "",
                    "error_type": error_type or "timeout",
                    "error_message": error_message or "pytest excedeu timeout",
                }
                rows_out.append(row_payload)
                debug_rows.append(row_payload.copy())
                print("timeout")
                continue

            stdout = _decode_subprocess_output(pytest_completed.stdout)
            stderr = _decode_subprocess_output(pytest_completed.stderr)
            rc = int(pytest_completed.returncode)
            passed = rc == 0
            status = _execution_status(rc)

            cov_pct, coverage_error, coverage_status, coverage_return_code = _run_real_coverage(
                test_arg=test_arg,
                module_path=module_path,
                coverage_target=coverage_target,
                env=env,
            )
            error_type, error_message = _summarize_error(stdout, stderr, coverage_error)
            row_payload = {
                "function_name": func_name,
                "file_path": file_path_cell,
                "complexity_score": row["complexity_score"],
                "complexity_level": row["complexity_level"],
                "test_file": test_rel,
                "execution_status": status,
                "passed": passed,
                "return_code": rc,
                "coverage_percent": cov_pct,
                "stdout": stdout,
                "stderr": stderr,
                "coverage_error": coverage_error,
                "coverage_status": coverage_status,
                "coverage_return_code": coverage_return_code,
                "module_path": module_path,
                "source_file": os.fspath(coverage_target) if coverage_target else "",
                "error_type": error_type,
                "error_message": error_message,
            }
            rows_out.append(row_payload)
            debug_rows.append(row_payload.copy())
            print(f"{status} | cobertura {cov_pct:.1f}%")
            continue

        _cleanup_coverage_artifacts()
        cmd_run = _build_coverage_run_cmd(
            test_arg=test_arg,
            module_path=module_path,
            coverage_target=coverage_target,
        )

        try:
            completed = subprocess.run(
                cmd_run,
                env=env,
                cwd=str(BASE_DIR),
                capture_output=True,
                timeout=30,
            )
        except subprocess.TimeoutExpired as e:
            stdout = _decode_subprocess_output(e.stdout)
            stderr = _decode_subprocess_output(e.stderr)
            if not stderr.strip():
                stderr = f"coverage/pytest excedeu timeout de {e.timeout}s"
            else:
                stderr = f"{stderr}\n(timeout de {e.timeout}s)".strip()
            _cleanup_coverage_artifacts()
            error_type, error_message = _summarize_error(stdout, stderr, "")
            row_payload = {
                "function_name": func_name,
                "file_path": file_path_cell,
                "complexity_score": row["complexity_score"],
                "complexity_level": row["complexity_level"],
                "test_file": test_rel,
                "execution_status": "timeout",
                "passed": False,
                "return_code": -3,
                "coverage_percent": 0.0,
                "stdout": stdout,
                "stderr": stderr,
                "coverage_error": "",
                "coverage_status": "not_run",
                "coverage_return_code": -1,
                "module_path": module_path,
                "source_file": os.fspath(coverage_target) if coverage_target else "",
                "error_type": error_type or "timeout",
                "error_message": error_message or "coverage/pytest excedeu timeout",
            }
            rows_out.append(row_payload)
            debug_rows.append(row_payload.copy())
            print("timeout")
            continue

        stdout = _decode_subprocess_output(completed.stdout)
        stderr = _decode_subprocess_output(completed.stderr)
        rc = int(completed.returncode)
        passed = rc == 0
        status = _execution_status(rc)

        cov_pct, coverage_error = _read_coverage_percent(coverage_target)
        if coverage_error.strip():
            stderr = f"{stderr}\n{coverage_error}".strip()

        _cleanup_coverage_artifacts()

        error_type, error_message = _summarize_error(stdout, stderr, coverage_error)
        row_payload = {
            "function_name": func_name,
            "file_path": file_path_cell,
            "complexity_score": row["complexity_score"],
            "complexity_level": row["complexity_level"],
            "test_file": test_rel,
            "execution_status": status,
            "passed": passed,
            "return_code": rc,
            "coverage_percent": cov_pct,
            "stdout": stdout,
            "stderr": stderr,
            "coverage_error": coverage_error,
            "coverage_status": "ok" if not coverage_error.strip() else "failed",
            "coverage_return_code": rc,
            "module_path": module_path,
            "source_file": os.fspath(coverage_target) if coverage_target else "",
            "error_type": error_type,
            "error_message": error_message,
        }
        rows_out.append(row_payload)
        debug_rows.append(row_payload.copy())
        print(f"{status} | cobertura {cov_pct:.1f}%")

    result_df = pd.DataFrame(rows_out)
    result_df = result_df.drop_duplicates(subset=list(MERGE_KEYS), keep="last")

    prepare_csv_for_save(result_df)[RESULT_COLUMNS].to_csv(
        output_coverage_csv, index=False, encoding="utf-8"
    )
    prepare_csv_for_save(result_df)[EXECUTION_COLUMNS].to_csv(
        output_execution_csv, index=False, encoding="utf-8"
    )
    debug_df = pd.DataFrame(debug_rows).drop_duplicates(subset=list(MERGE_KEYS), keep="last")
    debug_dir = cfg.results_dir / cfg.key
    debug_dir.mkdir(parents=True, exist_ok=True)
    debug_csv = debug_dir / f"test_execution_debug_{generator_name}.csv"
    debug_df["generator"] = generator_name
    prepare_csv_for_save(debug_df).to_csv(debug_csv, index=False, encoding="utf-8")
    merged_debug_csv = debug_dir / "test_execution_debug.csv"
    if merged_debug_csv.exists():
        prev = pd.read_csv(merged_debug_csv)
        merged = pd.concat([prev, debug_df], ignore_index=True)
        merged = merged.drop_duplicates(subset=["generator", *MERGE_KEYS], keep="last")
    else:
        merged = debug_df.copy()
    prepare_csv_for_save(merged).to_csv(merged_debug_csv, index=False, encoding="utf-8")

    print(f"\nCobertura salva em: {output_coverage_csv}")
    print(f"Execução salva em: {output_execution_csv}")
    print(f"Debug salvo em: {debug_csv}")
    print(f"Debug consolidado salvo em: {merged_debug_csv}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Executa testes gerados e calcula cobertura por arquivo."
    )
    parser.add_argument(
        "--generator",
        choices=("gpt", "claude"),
        required=True,
        help="Gerador de testes a executar (gpt ou claude).",
    )
    add_dataset_argument(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    generator = args.generator
    run_tests_for_generator(
        cfg=cfg,
        generator_name=generator,
        tests_dir=cfg.tests_dir(generator),
        output_coverage_csv=cfg.result_csv(f"cobertura_testes_gerados_{generator}"),
        output_execution_csv=cfg.result_csv(f"execucao_testes_{generator}"),
    )


if __name__ == "__main__":
    main()
