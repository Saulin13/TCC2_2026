"""
Consolida métricas do experimento piloto em final_results.csv e final_summary.txt.
Não usa mutation_score.
"""

from __future__ import annotations

import unicodedata
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "data" / "results"

INPUT_COVERAGE = RESULTS_DIR / "coverage_results.csv"
INPUT_DENSITY = RESULTS_DIR / "metric_assertion_density.csv"
INPUT_SUCCESS = RESULTS_DIR / "metric_execution_success.csv"
INPUT_STRENGTH = RESULTS_DIR / "test_strength_results.csv"
INPUT_EVAL_GPT = RESULTS_DIR / "evaluation_results_gpt.csv"
INPUT_EVAL_CLAUDE = RESULTS_DIR / "evaluation_results_claude.csv"

OUTPUT_FINAL = RESULTS_DIR / "final_results.csv"
OUTPUT_SUMMARY = RESULTS_DIR / "final_summary.txt"

MERGE_KEYS = ("function_name", "test_file")
FINAL_COLUMNS = [
    "function_name",
    "test_file",
    "complexity_level",
    "execution_status",
    "coverage_percent",
    "assertion_density",
    "execution_success_rate",
    "test_strength_score",
    "overall_score_gpt",
    "overall_score_claude",
]

COMPLEXITY_ORDER = ("baixa", "media", "alta")


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


def _test_file_basename(test_file: object) -> str:
    return Path(str(test_file)).name


def _category_to_success_rate(category: object) -> float | None:
    if category is None or (isinstance(category, float) and pd.isna(category)):
        return None
    text = str(category).lower()
    if "sucesso" in text or "pass rate" in text or "success" in text:
        return 1.0
    return 0.0


def _load_required(path: Path, label: str) -> pd.DataFrame | None:
    if not path.exists():
        print(f"Erro: {label} não encontrado: {path}")
        return None
    return pd.read_csv(path)


def _load_optional(path: Path) -> pd.DataFrame | None:
    if path.exists():
        return pd.read_csv(path)
    print(f"Aviso: opcional ausente — {path.name}")
    return None


def _prepare_coverage(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["complexity_level"] = out["complexity_level"].apply(normalize_complexity_level)
    out["coverage_percent"] = pd.to_numeric(out["coverage_percent"], errors="coerce")
    out["test_file"] = out["test_file"].astype(str)
    out["test_file_key"] = out["test_file"].map(_test_file_basename)
    out["passed_bool"] = out["passed"].apply(_parse_passed)
    return out


def _prepare_density(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["test_file_key"] = out["file_name"].astype(str).map(lambda x: Path(x).name)
    out["assertion_density"] = pd.to_numeric(out["assertion_density"], errors="coerce")
    return out[["test_file_key", "assertion_density"]].drop_duplicates(subset=["test_file_key"])


def _prepare_success(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    if "execution_category" not in out.columns:
        return pd.DataFrame(columns=["function_name", "execution_success_rate"])
    out["execution_success_rate"] = out["execution_category"].map(_category_to_success_rate)
    return out[["function_name", "execution_success_rate"]].drop_duplicates(subset=["function_name"])


def _prepare_strength(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["complexity_level"] = out["complexity_level"].apply(normalize_complexity_level)
    out["test_strength_score"] = pd.to_numeric(out["test_strength_score"], errors="coerce")
    return out[["function_name", "test_strength_score"]].drop_duplicates(subset=["function_name"])


def _prepare_eval(df: pd.DataFrame, score_column: str) -> pd.DataFrame:
    out = df.copy()
    out["test_file"] = out["test_file"].astype(str)
    out[score_column] = pd.to_numeric(out["overall_score"], errors="coerce")
    return out[list(MERGE_KEYS) + [score_column]].drop_duplicates(subset=list(MERGE_KEYS))


def consolidate() -> pd.DataFrame | None:
    df_cov = _load_required(INPUT_COVERAGE, "coverage_results.csv")
    df_density = _load_required(INPUT_DENSITY, "metric_assertion_density.csv")
    df_success = _load_required(INPUT_SUCCESS, "metric_execution_success.csv")
    df_strength = _load_required(INPUT_STRENGTH, "test_strength_results.csv")

    if any(x is None for x in (df_cov, df_density, df_success, df_strength)):
        return None

    base = _prepare_coverage(df_cov)
    final = base[list(MERGE_KEYS) + ["complexity_level", "execution_status", "coverage_percent", "test_file_key", "passed_bool"]].copy()

    final = final.merge(_prepare_density(df_density), on="test_file_key", how="left")

    final = final.merge(_prepare_success(df_success), on="function_name", how="left")
    final["execution_success_rate"] = final["execution_success_rate"].where(
        final["execution_success_rate"].notna(),
        final["passed_bool"].astype(float),
    )

    final = final.merge(_prepare_strength(df_strength), on="function_name", how="left")

    df_gpt = _load_optional(INPUT_EVAL_GPT)
    if df_gpt is not None:
        final = final.merge(_prepare_eval(df_gpt, "overall_score_gpt"), on=list(MERGE_KEYS), how="left")
    else:
        final["overall_score_gpt"] = pd.NA

    df_claude = _load_optional(INPUT_EVAL_CLAUDE)
    if df_claude is not None:
        final = final.merge(_prepare_eval(df_claude, "overall_score_claude"), on=list(MERGE_KEYS), how="left")
    else:
        final["overall_score_claude"] = pd.NA

    for col in ("overall_score_gpt", "overall_score_claude"):
        if col not in final.columns:
            final[col] = pd.NA

    return final[FINAL_COLUMNS]


def _format_distribution(series: pd.Series, title: str) -> list[str]:
    lines = [title]
    counts = series.dropna().astype(int)
    if counts.empty:
        lines.append("  (sem dados)")
        return lines
    total = int(counts.sum())
    for label, count in counts.items():
        pct = count / total * 100 if total else 0
        lines.append(f"  {label}: {count} ({pct:.1f}%)")
    return lines


def write_summary(df: pd.DataFrame) -> None:
    lines: list[str] = [
        "Resumo consolidado do experimento piloto",
        "=" * 50,
        f"Total de testes: {len(df)}",
        "",
        "Médias gerais",
        f"  Cobertura (%): {df['coverage_percent'].mean():.2f}",
        f"  test_strength_score: {df['test_strength_score'].mean():.2f}",
        f"  execution_success_rate: {df['execution_success_rate'].mean():.2f}",
    ]

    if df["overall_score_gpt"].notna().any():
        lines.append(f"  overall_score_gpt: {df['overall_score_gpt'].mean():.2f} (n={int(df['overall_score_gpt'].notna().sum())})")
    else:
        lines.append("  overall_score_gpt: (não disponível)")

    if df["overall_score_claude"].notna().any():
        lines.append(
            f"  overall_score_claude: {df['overall_score_claude'].mean():.2f} "
            f"(n={int(df['overall_score_claude'].notna().sum())})"
        )
    else:
        lines.append("  overall_score_claude: (não disponível)")

    lines.append("")
    complexity_counts = df["complexity_level"].value_counts()
    ordered = pd.Series(
        {level: complexity_counts.get(level, 0) for level in COMPLEXITY_ORDER},
        dtype=int,
    )
    lines.extend(_format_distribution(ordered, "Distribuição por complexidade"))

    lines.append("")
    lines.extend(_format_distribution(df["execution_status"].value_counts(), "Distribuição por status de execução"))

    if df["overall_score_gpt"].notna().any():
        lines.append("")
        lines.append("Média overall_score_gpt por complexidade:")
        for level in COMPLEXITY_ORDER:
            sub = df[df["complexity_level"] == level]["overall_score_gpt"].dropna()
            if not sub.empty:
                lines.append(f"  {level}: {sub.mean():.2f} (n={len(sub)})")

    if df["overall_score_claude"].notna().any():
        lines.append("")
        lines.append("Média overall_score_claude por complexidade:")
        for level in COMPLEXITY_ORDER:
            sub = df[df["complexity_level"] == level]["overall_score_claude"].dropna()
            if not sub.empty:
                lines.append(f"  {level}: {sub.mean():.2f} (n={len(sub)})")

    lines.append("")
    lines.append("Média de cobertura por complexidade:")
    for level in COMPLEXITY_ORDER:
        sub = df[df["complexity_level"] == level]["coverage_percent"]
        if not sub.empty:
            lines.append(f"  {level}: {sub.mean():.2f}% (n={len(sub)})")

    lines.append("")
    lines.append("Média de test_strength_score por complexidade:")
    for level in COMPLEXITY_ORDER:
        sub = df[df["complexity_level"] == level]["test_strength_score"]
        if not sub.empty:
            lines.append(f"  {level}: {sub.mean():.2f} (n={len(sub)})")

    OUTPUT_SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    print("Consolidando resultados finais do experimento...")

    final = consolidate()
    if final is None or final.empty:
        print("Consolidação abortada: dados insuficientes.")
        return

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    final.to_csv(OUTPUT_FINAL, index=False, encoding="utf-8")
    write_summary(final)

    print(f"\nArquivo consolidado: {OUTPUT_FINAL}")
    print(f"Resumo textual: {OUTPUT_SUMMARY}")
    print(f"Linhas consolidadas: {len(final)}")
    print("\nColunas:")
    for col in final.columns:
        non_null = final[col].notna().sum()
        print(f"  - {col}: {non_null}/{len(final)} preenchidos")


if __name__ == "__main__":
    main()
