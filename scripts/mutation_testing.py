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
import unicodedata
from dataclasses import dataclass
from pathlib import Path

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


def _sklearn_shadow_path(source_file: Path, work_root: Path) -> Path:
    parts = source_file.parts
    if "sklearn" not in parts:
        raise ValueError(f"arquivo fora do pacote sklearn: {source_file}")
    sklearn_idx = parts.index("sklearn")
    relative = Path(*parts[sklearn_idx:])
    return work_root / relative


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

    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", os.fspath(test_file)],
        cwd=os.fspath(BASE_DIR),
        env=merged_env,
        capture_output=True,
        text=True,
        timeout=timeout_seconds,
    )
    return completed.returncode != 0


def run_mutation_testing(
    *,
    source_file: Path,
    function_name: str,
    test_file: Path,
    env: dict[str, str],
    start_line: int | None = None,
    end_line: int | None = None,
    max_mutants: int = 25,
    timeout_seconds: int = 90,
) -> MutationRunResult:
    source_file = _resolve_path(source_file)
    test_file = _resolve_path(test_file)

    if not source_file.is_file():
        return _failed_result(f"arquivo fonte não encontrado: {source_file}")
    if not test_file.is_file():
        return _failed_result(f"arquivo de teste não encontrado: {test_file}")

    try:
        _ensure_mutmut_config(source_file)
        original_code = source_file.read_text(encoding="utf-8")
        module, mutations, _, _ = create_mutations(str(source_file), original_code, None)
        scoped = _filter_mutations_for_function(list(mutations), function_name=function_name)
        if not scoped:
            return _failed_result("nenhum mutante gerado para a função alvo")
        if len(scoped) > max_mutants:
            scoped = scoped[:max_mutants]
    except Exception as exc:  # noqa: BLE001
        return _failed_result(str(exc))

    work_root = Path(tempfile.mkdtemp(prefix="tcc_mutation_"))
    shadow_source = _sklearn_shadow_path(source_file, work_root)
    killed = 0

    try:
        shadow_source.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, shadow_source)

        for mutation in scoped:
            try:
                mutant_module = module.deep_replace(mutation.original_node, mutation.mutated_node)
                mutant_source = mutant_module.code
            except Exception:  # noqa: BLE001
                continue

            try:
                if _run_pytest_on_mutant(
                    test_file=test_file,
                    shadow_source=shadow_source,
                    work_root=work_root,
                    mutant_source=mutant_source,
                    env=env,
                    timeout_seconds=timeout_seconds,
                ):
                    killed += 1
            except subprocess.TimeoutExpired:
                killed += 1
            except Exception:  # noqa: BLE001
                continue
            finally:
                shadow_source.write_text(original_code, encoding="utf-8")
    finally:
        shutil.rmtree(work_root, ignore_errors=True)

    return _ok_result(killed=killed, total=len(scoped))
