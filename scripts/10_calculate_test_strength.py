"""
Calcula test_strength_score — métrica heurística complementar sobre assertividade
dos testes gerados por LLM. Não é mutation testing nem mutation score.
"""

from __future__ import annotations

import ast
import re
import unicodedata
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_COVERAGE = BASE_DIR / "data" / "results" / "coverage_results.csv"
TESTS_DIR = BASE_DIR / "tests" / "generated"
OUTPUT_CSV = BASE_DIR / "data" / "results" / "test_strength_results.csv"

OUTPUT_COLUMNS = [
    "function_name",
    "complexity_level",
    "coverage_percent",
    "assert_count",
    "test_function_count",
    "uses_pytest_raises",
    "edge_case_count",
    "execution_status",
    "passed",
    "test_strength_score",
]

EDGE_CASE_PATTERNS: dict[str, re.Pattern[str]] = {
    "none": re.compile(r"\bNone\b"),
    "empty_list": re.compile(r"\[\s*\]"),
    "empty_string": re.compile(r'(?:""|\'\')'),
    "negative": re.compile(r"-\d+"),
    "zero": re.compile(r"(?<![.\w])0(?:\.0+)?(?![.\w])"),
}


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
            if isinstance(func.value, ast.Attribute) and func.value.attr == "raises":
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


def compute_test_strength_score(
    *,
    coverage_percent: float,
    assert_count: int,
    test_function_count: int,
    edge_case_count: int,
    uses_pytest_raises: bool,
    execution_status: str,
    passed: bool,
) -> float:
    """
    Score heurístico em [0, 10]. Combina cobertura, asserts, diversidade de cenários,
    edge cases e penalização por falhas de execução. Não representa mutation testing.
    """
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


def _resolve_test_path(test_file: object) -> Path:
    rel = Path(str(test_file))
    if rel.is_absolute():
        return rel
    return (BASE_DIR / rel).resolve()


def _print_statistics(df: pd.DataFrame) -> None:
    print("\n--- Estatísticas (test_strength_score — métrica heurística) ---")

    if "complexity_level" in df.columns:
        print("\nMédia por complexidade:")
        by_level = df.groupby("complexity_level", dropna=False)["test_strength_score"].mean()
        for level in ("baixa", "media", "alta"):
            if level in by_level.index:
                print(f"  {level}: {by_level[level]:.2f}")
        for level, val in by_level.items():
            if level not in ("baixa", "media", "alta"):
                print(f"  {level}: {val:.2f}")

    print("\nMédia por status de execução:")
    by_status = df.groupby("execution_status", dropna=False)["test_strength_score"].mean()
    for status, val in by_status.sort_values(ascending=False).items():
        print(f"  {status}: {val:.2f}")

    cols_show = ["function_name", "complexity_level", "test_strength_score", "coverage_percent"]
    top = df.nlargest(5, "test_strength_score")[cols_show]
    bottom = df.nsmallest(5, "test_strength_score")[cols_show]

    print("\nTop 5 melhores testes:")
    for _, row in top.iterrows():
        print(
            f"  {row['function_name']} ({row['complexity_level']}): "
            f"score={row['test_strength_score']:.2f}, cobertura={row['coverage_percent']:.1f}%"
        )

    print("\nTop 5 piores testes:")
    for _, row in bottom.iterrows():
        print(
            f"  {row['function_name']} ({row['complexity_level']}): "
            f"score={row['test_strength_score']:.2f}, cobertura={row['coverage_percent']:.1f}%"
        )


def main() -> None:
    print("Calculando test_strength_score (métrica heurística complementar)...")
    print("Nota: não é mutation testing nem mutation score.\n")

    if not INPUT_COVERAGE.exists():
        print(f"Erro: arquivo não encontrado: {INPUT_COVERAGE}")
        return
    if not TESTS_DIR.is_dir():
        print(f"Erro: diretório não encontrado: {TESTS_DIR}")
        return

    df_cov = pd.read_csv(INPUT_COVERAGE)
    rows: list[dict[str, object]] = []

    for _, cov_row in df_cov.iterrows():
        test_path = _resolve_test_path(cov_row["test_file"])
        metrics = analyze_test_file(test_path)

        coverage = float(cov_row["coverage_percent"]) if pd.notna(cov_row["coverage_percent"]) else 0.0
        passed = _parse_passed(cov_row["passed"])
        status = str(cov_row.get("execution_status", ""))

        score = compute_test_strength_score(
            coverage_percent=coverage,
            assert_count=int(metrics["assert_count"]),
            test_function_count=int(metrics["test_function_count"]),
            edge_case_count=int(metrics["edge_case_count"]),
            uses_pytest_raises=bool(metrics["uses_pytest_raises"]),
            execution_status=status,
            passed=passed,
        )

        rows.append(
            {
                "function_name": cov_row["function_name"],
                "complexity_level": normalize_complexity_level(cov_row.get("complexity_level")),
                "coverage_percent": round(coverage, 4),
                "assert_count": metrics["assert_count"],
                "test_function_count": metrics["test_function_count"],
                "uses_pytest_raises": metrics["uses_pytest_raises"],
                "edge_case_count": metrics["edge_case_count"],
                "execution_status": status,
                "passed": passed,
                "test_strength_score": score,
            }
        )

    if not rows:
        print("Nenhum registro processado.")
        return

    out_df = pd.DataFrame(rows)[OUTPUT_COLUMNS]
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

    print(f"Resultados salvos em: {OUTPUT_CSV}")
    print(f"Total de testes analisados: {len(out_df)}")
    print(f"Média geral do test_strength_score: {out_df['test_strength_score'].mean():.2f}")

    _print_statistics(out_df)


if __name__ == "__main__":
    main()
