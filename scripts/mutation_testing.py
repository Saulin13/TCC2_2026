"""
Execução de mutation testing por par função/teste.

Usa os operadores de mutação do mutmut (libcst) sem depender do CLI do mutmut,
que exige fork/WSL e não roda nativamente no Windows.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as FuturesTimeoutError
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import mutmut.configuration as mutmut_configuration
from mutmut.configuration import Config
from mutmut.mutation.file_mutation import Mutation, create_mutations

from dataset_config import BASE_DIR

MUTATION_TOOL = "mutmut_libcst"


@dataclass(frozen=True)
class MutationRunResult:
    mutation_score_percent: float
    test_strength_score: float
    mutation_status: str
    mutation_error: str
    mutants_total: int
    mutants_killed: int
    mutation_tool: str = MUTATION_TOOL


def _normalize_text(value: str) -> str:
    if not isinstance(value, str):
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    without_accents = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return without_accents.strip().lower()


def _ensure_mutmut_config(source_file: Path) -> None:
    """Inicializa Config do mutmut sem depender de setup.cfg/pyproject.toml."""
    mutmut_configuration._config = Config(
        also_copy=[],
        only_mutate=[],
        do_not_mutate=[],
        do_not_mutate_patterns=[],
        max_stack_depth=-1,
        debug=False,
        source_paths=[source_file.parent],
        pytest_add_cli_args=[],
        pytest_add_cli_args_test_selection=[],
        mutate_only_covered_lines=False,
        timeout_multiplier=15.0,
        timeout_constant=1.0,
        type_check_command=[],
        use_setproctitle=False,
    )


def _failed_result(message: str) -> MutationRunResult:
    return MutationRunResult(
        mutation_score_percent=0.0,
        test_strength_score=0.0,
        mutation_status="failed",
        mutation_error=message,
        mutants_total=0,
        mutants_killed=0,
    )


def _timeout_result() -> MutationRunResult:
    return MutationRunResult(
        mutation_score_percent=0.0,
        test_strength_score=0.0,
        mutation_status="timeout",
        mutation_error="function timeout",
        mutants_total=0,
        mutants_killed=0,
    )


def _deadline_exceeded(deadline: float | None) -> bool:
    return deadline is not None and time.monotonic() >= deadline


def _seconds_until_deadline(deadline: float | None) -> int | None:
    if deadline is None:
        return None
    return max(0, int(deadline - time.monotonic()))


def _ok_result(*, killed: int, total: int) -> MutationRunResult:
    if total <= 0:
        return _failed_result("nenhum mutante gerado para a função alvo")
    score_percent = round((killed / total) * 100.0, 4)
    strength = round(score_percent / 10.0, 4)
    return MutationRunResult(
        mutation_score_percent=score_percent,
        test_strength_score=strength,
        mutation_status="ok",
        mutation_error="",
        mutants_total=total,
        mutants_killed=killed,
    )


def _resolve_path(path: Path | str) -> Path:
    resolved = Path(path)
    if resolved.is_absolute():
        return resolved.resolve()
    return (BASE_DIR / resolved).resolve()


def _function_line_range(
    source_file: Path,
    function_name: str,
    *,
    start_line: int | None,
    end_line: int | None,
) -> tuple[int, int]:
    if start_line is not None and end_line is not None and start_line > 0 and end_line >= start_line:
        return int(start_line), int(end_line)

    import ast

    tree = ast.parse(source_file.read_text(encoding="utf-8"), filename=str(source_file))
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            end = getattr(node, "end_lineno", None) or node.lineno
            return int(node.lineno), int(end)
    raise ValueError(f"função '{function_name}' não encontrada em {source_file}")


def _mutation_target_names(function_name: str) -> list[str]:
    names = [function_name]
    if not function_name.startswith("_"):
        names.append(f"_{function_name}")
    return names


def _filter_mutations_for_function(
    mutations: list[Mutation],
    *,
    function_name: str,
) -> list[Mutation]:
    targets = set(_mutation_target_names(function_name))
    selected: list[Mutation] = []
    for mutation in mutations:
        container = mutation.contained_by_top_level_function
        if container is None or container.name.value not in targets:
            continue
        selected.append(mutation)
    return selected


def _is_sklearn_source(source_file: Path) -> bool:
    return "sklearn" in source_file.parts


def _sklearn_shadow_path(source_file: Path, work_root: Path) -> Path:
    parts = source_file.parts
    if "sklearn" not in parts:
        raise ValueError(f"arquivo fora do pacote sklearn: {source_file}")
    sklearn_idx = parts.index("sklearn")
    relative = Path(*parts[sklearn_idx:])
    return work_root / relative


def _repo_relative_shadow_path(
    source_file: Path,
    work_root: Path,
    repo_root: Path,
) -> Path:
    source_resolved = source_file.resolve()
    repo_resolved = repo_root.resolve()
    try:
        relative = source_resolved.relative_to(repo_resolved)
    except ValueError as exc:
        raise ValueError(
            f"arquivo fora do repositório {repo_resolved}: {source_resolved}"
        ) from exc
    return work_root / relative


def _resolve_shadow_path(
    source_file: Path,
    work_root: Path,
    *,
    repo_root: Path | None = None,
) -> Path:
    if _is_sklearn_source(source_file):
        return _sklearn_shadow_path(source_file, work_root)
    if repo_root is None:
        raise ValueError(
            f"repo_root obrigatório para arquivos fora do sklearn: {source_file}"
        )
    return _repo_relative_shadow_path(source_file, work_root, repo_root)


def _copy_package_init_chain(
    source_file: Path,
    shadow_source: Path,
    repo_root: Path,
) -> None:
    """Copia __init__.py dos pacotes ancestrais para o shadow tree."""
    repo_resolved = repo_root.resolve()
    try:
        rel_parent = source_file.resolve().parent.relative_to(repo_resolved)
    except ValueError:
        return

    work_root = shadow_source.parents[len(rel_parent.parts)]
    partial = Path()
    for part in rel_parent.parts:
        partial = partial / part
        init_src = repo_resolved / partial / "__init__.py"
        if init_src.is_file():
            shadow_init = work_root / partial / "__init__.py"
            shadow_init.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(init_src, shadow_init)


def _setup_shadow_source(
    source_file: Path,
    shadow_source: Path,
    *,
    repo_root: Path | None,
) -> None:
    shadow_source.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_file, shadow_source)
    if repo_root is not None and not _is_sklearn_source(source_file):
        _copy_package_init_chain(source_file, shadow_source, repo_root)


def _terminate_process(proc: subprocess.Popen[Any]) -> None:
    if proc.poll() is not None:
        return
    proc.kill()
    try:
        proc.communicate(timeout=5)
    except subprocess.TimeoutExpired:
        pass


def _run_pytest_on_mutant(
    *,
    test_file: Path,
    shadow_source: Path,
    work_root: Path,
    mutant_source: str,
    env: dict[str, str],
    timeout_seconds: int,
) -> bool:
    shadow_source.parent.mkdir(parents=True, exist_ok=True)
    shadow_source.write_text(mutant_source, encoding="utf-8")

    merged_env = env.copy()
    pythonpath = os.fspath(work_root)
    existing = merged_env.get("PYTHONPATH", "")
    merged_env["PYTHONPATH"] = (
        f"{pythonpath}{os.pathsep}{existing}" if existing else pythonpath
    )

    proc = subprocess.Popen(
        [sys.executable, "-m", "pytest", "-q", os.fspath(test_file)],
        cwd=os.fspath(BASE_DIR),
        env=merged_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        proc.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        _terminate_process(proc)
        raise
    return proc.returncode != 0


def _prepare_scoped_mutations(
    source_file: Path,
    function_name: str,
    *,
    max_mutants: int,
) -> tuple[Any, list[Mutation], str]:
    _ensure_mutmut_config(source_file)
    original_code = source_file.read_text(encoding="utf-8")
    module, mutations, _, _ = create_mutations(str(source_file), original_code, None)
    scoped = _filter_mutations_for_function(list(mutations), function_name=function_name)
    if not scoped:
        raise ValueError("nenhum mutante gerado para a função alvo")
    if len(scoped) > max_mutants:
        scoped = scoped[:max_mutants]
    return module, scoped, original_code


def run_mutation_testing(
    *,
    source_file: Path,
    function_name: str,
    test_file: Path,
    env: dict[str, str],
    repo_root: Path | None = None,
    start_line: int | None = None,
    end_line: int | None = None,
    max_mutants: int = 25,
    timeout_seconds: int = 90,
    function_timeout_seconds: int | None = None,
) -> MutationRunResult:
    source_file = _resolve_path(source_file)
    test_file = _resolve_path(test_file)

    if not source_file.is_file():
        return _failed_result(f"arquivo fonte não encontrado: {source_file}")
    if not test_file.is_file():
        return _failed_result(f"arquivo de teste não encontrado: {test_file}")

    deadline: float | None = None
    if function_timeout_seconds is not None and function_timeout_seconds > 0:
        deadline = time.monotonic() + function_timeout_seconds

    if _deadline_exceeded(deadline):
        return _timeout_result()

    prep_timeout = _seconds_until_deadline(deadline)
    try:
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                _prepare_scoped_mutations,
                source_file,
                function_name,
                max_mutants=max_mutants,
            )
            module, scoped, original_code = future.result(timeout=prep_timeout)
    except FuturesTimeoutError:
        return _timeout_result()
    except Exception as exc:  # noqa: BLE001
        return _failed_result(str(exc))

    work_root = Path(tempfile.mkdtemp(prefix="tcc_mutation_"))
    try:
        shadow_source = _resolve_shadow_path(
            source_file,
            work_root,
            repo_root=repo_root,
        )
    except Exception as exc:  # noqa: BLE001
        shutil.rmtree(work_root, ignore_errors=True)
        return _failed_result(str(exc))

    killed = 0

    try:
        _setup_shadow_source(
            source_file,
            shadow_source,
            repo_root=repo_root,
        )

        for mutation in scoped:
            if _deadline_exceeded(deadline):
                return _timeout_result()

            try:
                mutant_module = module.deep_replace(mutation.original_node, mutation.mutated_node)
                mutant_source = mutant_module.code
            except Exception:  # noqa: BLE001
                continue

            remaining = _seconds_until_deadline(deadline)
            if remaining is not None and remaining <= 0:
                return _timeout_result()
            per_mutant_timeout = (
                min(timeout_seconds, remaining) if remaining is not None else timeout_seconds
            )
            if per_mutant_timeout <= 0:
                return _timeout_result()

            try:
                if _run_pytest_on_mutant(
                    test_file=test_file,
                    shadow_source=shadow_source,
                    work_root=work_root,
                    mutant_source=mutant_source,
                    env=env,
                    timeout_seconds=per_mutant_timeout,
                ):
                    killed += 1
            except subprocess.TimeoutExpired:
                killed += 1
                if _deadline_exceeded(deadline):
                    return _timeout_result()
            except Exception:  # noqa: BLE001
                continue
            finally:
                shadow_source.write_text(original_code, encoding="utf-8")
    finally:
        shutil.rmtree(work_root, ignore_errors=True)

    return _ok_result(killed=killed, total=len(scoped))
