import json
import os
import subprocess
from pathlib import Path
import sys

import pandas as pd

# Raiz do projeto; todos os caminhos são relativos a ela
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_SAMPLE = BASE_DIR / "data" / "selected_functions" / "pilot_sample_30.csv"
TESTS_DIR = BASE_DIR / "tests" / "generated"
RESULTS_DIR = BASE_DIR / "data" / "results"
REPO_PATH = BASE_DIR / "repos" / "Python"
COVERAGE_JSON = BASE_DIR / "coverage.json"
DOT_COVERAGE = BASE_DIR / ".coverage"
OUTPUT_CSV = RESULTS_DIR / "coverage_results.csv"

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
    if return_code == 5:
        return "no_tests_collected"
    if return_code in (2, 3, 4):
        return "pytest_error"
    return "error"


def main():
    if not INPUT_SAMPLE.exists():
        print(f"Arquivo não encontrado: {INPUT_SAMPLE}")
        return

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    TESTS_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(INPUT_SAMPLE)

    env = os.environ.copy()
    env["PYTHONPATH"] = os.fspath(REPO_PATH)

    rows_out = []
    n = len(df)

    print(" Iniciando execução individual dos testes com cobertura por arquivo...")

    for pos, (_, row) in enumerate(df.iterrows()):
        func_name = row["function_name"]
        file_path_cell = row["file_path"]
        source_file = REPO_PATH / Path(str(file_path_cell).replace("\\", "/"))

        seq = pos + 1
        test_path = TESTS_DIR / f"test_{seq:03d}_{func_name}.py"
        test_rel = test_path.relative_to(BASE_DIR).as_posix()

        print(f"[{pos + 1}/{n}] {func_name}...", end=" ")

        if not test_path.exists():
            rows_out.append(
                {
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
                }
            )
            print("sem arquivo de teste")
            continue

        if not source_file.exists():
            try:
                disp = source_file.relative_to(BASE_DIR).as_posix()
            except ValueError:
                disp = os.fspath(source_file)
            rows_out.append(
                {
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
                }
            )
            print("fonte ausente")
            continue

        # Remove artefatos de cobertura antes de executar este teste
        _cleanup_coverage_artifacts()

        test_arg = os.fspath(test_path.resolve())
        source_dir = os.fspath(source_file.resolve().parent)

        cmd_run = [
            sys.executable,
            "-m",
            "coverage",
            "run",
            "--source",
            source_dir,
            "-m",
            "pytest",
            test_arg,
        ]

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
            rows_out.append(
                {
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
                }
            )
            print("timeout")
            continue

        stdout = _decode_subprocess_output(completed.stdout)
        stderr = _decode_subprocess_output(completed.stderr)
        rc = completed.returncode
        passed = rc == 0
        status = _execution_status(rc)

        cov_pct = 0.0
        if DOT_COVERAGE.exists():
            json_completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "coverage",
                    "json",
                    "-o",
                    os.fspath(COVERAGE_JSON),
                ],
                env=env,
                cwd=str(BASE_DIR),
                capture_output=True,
            )
            jerr = _decode_subprocess_output(json_completed.stderr)
            if jerr.strip():
                stderr = f"{stderr}\n[coverage-json] {jerr}".strip()
            if json_completed.returncode != 0:
                stderr = (
                    f"{stderr}\n[coverage-json] código de saída {json_completed.returncode}"
                ).strip()
            if COVERAGE_JSON.exists():
                try:
                    with COVERAGE_JSON.open("r", encoding="utf-8") as f:
                        cov_data = json.load(f)
                    cov_pct = _coverage_percent_for_source(cov_data, source_file)
                except (json.JSONDecodeError, OSError, KeyError) as e:
                    stderr = f"{stderr}\n[coverage-parse] {e}".strip()
        else:
            stderr = f"{stderr}\n[coverage] .coverage não foi gerado após coverage run".strip()

        _cleanup_coverage_artifacts()

        rows_out.append(
            {
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
            }
        )
        print(f"{status} | cobertura {cov_pct:.1f}%")

    pd.DataFrame(rows_out)[RESULT_COLUMNS].to_csv(
        OUTPUT_CSV, index=False, encoding="utf-8"
    )
    print(f"\n Resultados salvos em: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
