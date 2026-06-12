"""
Calcula test_strength_score a partir de mutation testing (mutmut/libcst).

mutation_score_percent = percentual de mutantes mortos pelos testes.
test_strength_score = mutation_score_percent / 10  (escala 0–10).

A métrica heurística anterior é preservada em heuristic_test_strength_score.
"""

from __future__ import annotations

import argparse
import ast
import os
import re
import unicodedata
from pathlib import Path

import pandas as pd

from csv_columns import prepare_csv_for_save
from dataset_config import BASE_DIR, add_dataset_argument, resolve_dataset
from mutation_testing import MUTATION_TOOL, MutationRunResult, run_mutation_testing

OUTPUT_COLUMNS = [
    "function_name",
    "generator",
    "test_file",
    "complexity_level",
    "coverage_percent",
    "assert_count",
    "test_function_count",
    "uses_pytest_raises",
    "edge_case_count",
    "execution_status",
    "passed",
    "heuristic_test_strength_score",
    "mutation_score_percent",
    "test_strength_score",
    "mutation_status",
    "mutation_error",
    "mutants_total",
    "mutants_killed",
    "mutation_tool",
]

EDGE_CASE_PATTERNS: dict[str, re.Pattern[str]] = {
    "none": re.compile(r"\bNone\b"),
    "empty_list": re.compile(r"\[\s*\]"),
    "empty_string": re.compile(r'(?:""|\'\')'),
    "negative": re.compile(r"-\d+"),
    "zero": re.compile(r"(?<![.\w])0(?:\.0+)?(?![.\w])"),
}

GENERATORS = ("gpt", "claude")


def _normalize_text(value: str) -> str:
    if not isinstance(value, str):
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    without_accents = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return without_accents.strip().lower()


def normalize_complexity_level(value: object) -> str:
    norm = _normalize_text(str(value) if value is not None else "")
    if norm in {"baixa", "low"}:
        return "baixa"
    if norm in {"media", "medium"}:
        return "media"
    if norm in {"alta", "high"}:
        return "alta"
    return norm


def _parse_passed(val: object) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in ("true", "1", "yes")


class _TestMetricsVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        self.assert_count = 0
        self.test_function_count = 0
        self.uses_pytest_raises = False

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        if node.name.startswith("test_"):
            self.test_function_count += 1
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        if node.name.startswith("test_"):
            self.test_function_count += 1
        self.generic_visit(node)

    def visit_Assert(self, node: ast.Assert) -> None:
        self.assert_count += 1
        self.generic_visit(node)

    def visit_With(self, node: ast.With) -> None:
        for item in node.items:
            if self._is_pytest_raises(item.context_expr):
                self.uses_pytest_raises = True
        self.generic_visit(node)

    @staticmethod
    def _is_pytest_raises(expr: ast.AST) -> bool:
        if not isinstance(expr, ast.Call):
            return False
        func = expr.func
        if isinstance(func, ast.Attribute) and func.attr == "raises":
            if isinstance(func.value, ast.Name) and func.value.id == "pytest":
                return True
        if isinstance(func, ast.Name) and func.id == "raises":
            return True
        return False


def _count_asserts_fallback(source: str) -> int:
    code_lines = [
        line
        for line in source.splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    return len(re.findall(r"\bassert\b", "\n".join(code_lines)))


def _detect_edge_cases(source: str) -> int:
    found = 0
    for pattern in EDGE_CASE_PATTERNS.values():
        if pattern.search(source):
            found += 1
    return found


def analyze_test_file(path: Path) -> dict[str, int | bool]:
    defaults: dict[str, int | bool] = {
        "assert_count": 0,
        "test_function_count": 0,
        "uses_pytest_raises": False,
        "edge_case_count": 0,
    }
    if not path.is_file():
        return defaults

    try:
        source = path.read_text(encoding="utf-8")
    except OSError:
        return defaults

    defaults["edge_case_count"] = _detect_edge_cases(source)

    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError:
        defaults["assert_count"] = _count_asserts_fallback(source)
        return defaults

    visitor = _TestMetricsVisitor()
    visitor.visit(tree)

    assert_count = visitor.assert_count
    if assert_count == 0:
        assert_count = _count_asserts_fallback(source)

    return {
        "assert_count": assert_count,
        "test_function_count": visitor.test_function_count,
        "uses_pytest_raises": visitor.uses_pytest_raises,
        "edge_case_count": defaults["edge_case_count"],
    }


def compute_heuristic_test_strength_score(
    *,
    coverage_percent: float,
    assert_count: int,
    test_function_count: int,
    edge_case_count: int,
    uses_pytest_raises: bool,
    execution_status: str,
    passed: bool,
) -> float:
    """Métrica heurística legada (0–10), preservada para comparação."""
    cov = max(0.0, min(float(coverage_percent), 100.0)) / 100.0
    coverage_pts = cov * 3.0
    assert_pts = min(assert_count / 10.0, 1.0) * 2.0
    diversity_pts = min(test_function_count / 5.0, 1.0) * 1.5
    edge_pts = (max(0, min(edge_case_count, 5)) / 5.0) * 2.0
    raises_pts = 0.5 if uses_pytest_raises else 0.0

    static_score = coverage_pts + assert_pts + diversity_pts + edge_pts + raises_pts

    status = _normalize_text(execution_status)
    if passed:
        exec_factor = 1.0
        exec_bonus = 1.0
    elif status in {"pytest_error", "timeout", "import_error", "collection_error"}:
        exec_factor = 0.35
        exec_bonus = 0.0
    elif status == "tests_failed":
        exec_factor = 0.6
        exec_bonus = 0.15
    else:
        exec_factor = 0.5
        exec_bonus = 0.0

    raw = static_score * exec_factor + exec_bonus
    return round(max(0.0, min(raw, 10.0)), 2)


# Compatibilidade com scripts que ainda importam compute_test_strength_score.
compute_test_strength_score = compute_heuristic_test_strength_score


def _resolve_test_path(test_file: object) -> Path:
    rel = Path(str(test_file))
    if rel.is_absolute():
        return rel
    return (BASE_DIR / rel).resolve()


def _resolve_source_path(row: pd.Series) -> Path | None:
    raw = row.get("source_file")
    if isinstance(raw, str) and raw.strip():
        path = Path(raw.strip())
        return path if path.is_absolute() else (BASE_DIR / path).resolve()
    return None


def _prepare_run_env(cfg) -> dict[str, str]:
    env = os.environ.copy()
    repo = os.fspath(cfg.repo_path)
    if cfg.key == "real":
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


def _parse_line_number(value: object) -> int | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _print_summary(df: pd.DataFrame) -> None:
    total = len(df)
    ok_count = int((df["mutation_status"] == "ok").sum())
    failed_count = int((df["mutation_status"] == "failed").sum())

    print("\n--- Resumo do mutation testing ---")
    print(f"Testes processados: {total}")
    print(f"mutation_status ok: {ok_count}")
    print(f"mutation_status failed: {failed_count}")
    print(f"Ferramenta: {MUTATION_TOOL}")

    if "generator" in df.columns:
        print("\nMédia mutation_score_percent por gerador:")
        for generator, group in df.groupby("generator", observed=True):
            print(f"  {generator}: {group['mutation_score_percent'].mean():.2f}%")

        print("\nMédia test_strength_score por gerador:")
        for generator, group in df.groupby("generator", observed=True):
            print(f"  {generator}: {group['test_strength_score'].mean():.2f}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calcula test_strength_score via mutation testing (mutmut/libcst)."
    )
    parser.add_argument(
        "--generator",
        choices=(*GENERATORS, "all"),
        default="all",
        help="Gerador dos testes (padrão: all = GPT e Claude).",
    )
    parser.add_argument(
        "--max-mutants",
        type=int,
        default=25,
        help="Máximo de mutantes avaliados por par função/teste (padrão: 25).",
    )
    parser.add_argument(
        "--mutation-timeout",
        type=int,
        default=90,
        help="Timeout em segundos por execução de pytest com mutante (padrão: 90).",
    )
    add_dataset_argument(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    output_csv = cfg.result_csv("forca_heuristica_testes")
    output_summary = cfg.result_txt("resumo_mutation_testing")

    generators = list(GENERATORS) if args.generator == "all" else [args.generator]
    env = _prepare_run_env(cfg)

    print(f"Dataset: {cfg.key}")
    print("Calculando test_strength_score via mutation testing...")
    print(f"Ferramenta: {MUTATION_TOOL}")
    print(f"Geradores: {', '.join(generators)}")
    print(f"max_mutants={args.max_mutants} | mutation_timeout={args.mutation_timeout}s\n")

    rows: list[dict[str, object]] = []

    for generator in generators:
        input_coverage = cfg.result_csv(f"cobertura_testes_gerados_{generator}")
        if not input_coverage.exists():
            print(f"Aviso: cobertura ausente para {generator}: {input_coverage}")
            continue

        df_cov = pd.read_csv(input_coverage)
        print(f"Processando {generator}: {len(df_cov)} registro(s)")

        for index, cov_row in df_cov.iterrows():
            function_name = str(cov_row["function_name"])
            test_path = _resolve_test_path(cov_row["test_file"])
            source_path = _resolve_source_path(cov_row)

            metrics = analyze_test_file(test_path)
            coverage = float(cov_row["coverage_percent"]) if pd.notna(cov_row["coverage_percent"]) else 0.0
            passed = _parse_passed(cov_row["passed"])
            status = str(cov_row.get("execution_status", ""))

            heuristic_score = compute_heuristic_test_strength_score(
                coverage_percent=coverage,
                assert_count=int(metrics["assert_count"]),
                test_function_count=int(metrics["test_function_count"]),
                edge_case_count=int(metrics["edge_case_count"]),
                uses_pytest_raises=bool(metrics["uses_pytest_raises"]),
                execution_status=status,
                passed=passed,
            )

            print(f"  [{generator}] {index + 1}/{len(df_cov)} {function_name} — mutation testing...", flush=True)

            if source_path is None or not source_path.is_file():
                mutation_result = MutationRunResult(
                    mutation_score_percent=0.0,
                    test_strength_score=0.0,
                    mutation_status="failed",
                    mutation_error="source_file ausente ou inválido no CSV de cobertura",
                    mutants_total=0,
                    mutants_killed=0,
                )
            else:
                mutation_result = run_mutation_testing(
                    source_file=source_path,
                    function_name=function_name,
                    test_file=test_path,
                    env=env,
                    start_line=_parse_line_number(cov_row.get("start_line")),
                    end_line=_parse_line_number(cov_row.get("end_line")),
                    max_mutants=args.max_mutants,
                    timeout_seconds=args.mutation_timeout,
                )

            rows.append(
                {
                    "function_name": function_name,
                    "generator": generator,
                    "test_file": str(cov_row["test_file"]),
                    "complexity_level": normalize_complexity_level(cov_row.get("complexity_level")),
                    "coverage_percent": round(coverage, 4),
                    "assert_count": metrics["assert_count"],
                    "test_function_count": metrics["test_function_count"],
                    "uses_pytest_raises": metrics["uses_pytest_raises"],
                    "edge_case_count": metrics["edge_case_count"],
                    "execution_status": status,
                    "passed": passed,
                    "heuristic_test_strength_score": heuristic_score,
                    "mutation_score_percent": mutation_result.mutation_score_percent,
                    "test_strength_score": mutation_result.test_strength_score,
                    "mutation_status": mutation_result.mutation_status,
                    "mutation_error": mutation_result.mutation_error,
                    "mutants_total": mutation_result.mutants_total,
                    "mutants_killed": mutation_result.mutants_killed,
                    "mutation_tool": mutation_result.mutation_tool,
                }
            )

            status_label = mutation_result.mutation_status
            print(
                f"    -> {status_label} | mutantes={mutation_result.mutants_killed}/"
                f"{mutation_result.mutants_total} | score={mutation_result.test_strength_score:.2f}",
                flush=True,
            )

    if not rows:
        print("Nenhum registro processado.")
        return

    out_df = prepare_csv_for_save(pd.DataFrame(rows)[OUTPUT_COLUMNS])
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(output_csv, index=False, encoding="utf-8")

    summary_lines = [
        "Resumo do mutation testing",
        "=" * 40,
        f"Dataset: {cfg.key}",
        f"Ferramenta: {MUTATION_TOOL}",
        "",
        "test_strength_score agora é derivado de mutation testing:",
        "  mutation_score_percent = mutantes mortos / mutantes totais * 100",
        "  test_strength_score = mutation_score_percent / 10",
        "",
        f"Testes processados: {len(out_df)}",
        f"mutation_status ok: {int((out_df['mutation_status'] == 'ok').sum())}",
        f"mutation_status failed: {int((out_df['mutation_status'] == 'failed').sum())}",
        "",
        "Média mutation_score_percent por gerador:",
    ]
    for generator, group in out_df.groupby("generator", observed=True):
        summary_lines.append(f"  {generator}: {group['mutation_score_percent'].mean():.2f}%")
    summary_lines.append("")
    summary_lines.append("Média test_strength_score por gerador:")
    for generator, group in out_df.groupby("generator", observed=True):
        summary_lines.append(f"  {generator}: {group['test_strength_score'].mean():.2f}")

    output_summary.write_text("\n".join(summary_lines) + "\n", encoding="utf-8")

    print(f"\nResultados salvos em: {output_csv}")
    print(f"Resumo salvo em: {output_summary}")
    _print_summary(out_df)


if __name__ == "__main__":
    main()
