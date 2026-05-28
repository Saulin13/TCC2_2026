"""
Consolida métricas do experimento piloto em resultados_finais.csv e resumo_resultados_finais.txt.
Não usa mutation_score.
"""

from __future__ import annotations

import argparse
import unicodedata
from pathlib import Path

import pandas as pd

from csv_columns import (
    log_dataframe_info,
    standardize_function_column,
    standardize_test_file_column,
    validate_required_columns,
)
from dataset_config import DatasetConfig, add_dataset_argument, resolve_dataset

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
MERGE_COUNT = 0


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


def _load_and_standardize(path: Path, label: str, *, required: bool = True) -> pd.DataFrame | None:
    if not path.exists():
        if required:
            print(f"Erro: {label} não encontrado: {path}")
        else:
            print(f"Aviso: opcional ausente — {path.name}")
        return None

    df = standardize_test_file_column(standardize_function_column(pd.read_csv(path)))
    log_dataframe_info(label, df, source=path.name)
    return df


def _merge_logged(
    left: pd.DataFrame,
    right: pd.DataFrame,
    *,
    on: str | list[str],
    how: str,
    label: str,
) -> pd.DataFrame:
    global MERGE_COUNT
    before = len(left)
    merged = left.merge(right, on=on, how=how)
    MERGE_COUNT += 1
    print(
        f"[MERGE {MERGE_COUNT}] {label} | on={on} | how={how} | "
        f"linhas antes={before} | depois={len(merged)}"
    )
    return merged


def _prepare_coverage(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    validate_required_columns(
        df,
        ["function_name", "test_file", "complexity_level", "execution_status", "coverage_percent", "passed"],
        source_name,
    )
    out = df.copy()
    out["complexity_level"] = out["complexity_level"].apply(normalize_complexity_level)
    out["coverage_percent"] = pd.to_numeric(out["coverage_percent"], errors="coerce")
    out["test_file"] = out["test_file"].astype(str)
    out["test_file_key"] = out["test_file"].map(_test_file_basename)
    out["passed_bool"] = out["passed"].apply(_parse_passed)
    return out


def _prepare_density(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    validate_required_columns(df, ["assertion_density"], source_name)
    out = standardize_test_file_column(df.copy())
    if "test_file" not in out.columns and "file_name" in out.columns:
        out = out.rename(columns={"file_name": "test_file"})
    validate_required_columns(out, ["test_file"], source_name)
    out["test_file_key"] = out["test_file"].astype(str).map(_test_file_basename)
    out["assertion_density"] = pd.to_numeric(out["assertion_density"], errors="coerce")
    return out[["test_file_key", "assertion_density"]].drop_duplicates(subset=["test_file_key"])


def _prepare_success(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    out = standardize_function_column(df.copy())
    validate_required_columns(out, ["function_name"], source_name)
    if "execution_category" not in out.columns:
        print(f"Aviso: {source_name} sem execution_category; execution_success_rate ficará vazio.")
        return pd.DataFrame(columns=["function_name", "execution_success_rate"])
    out["execution_success_rate"] = out["execution_category"].map(_category_to_success_rate)
    return out[["function_name", "execution_success_rate"]].drop_duplicates(subset=["function_name"])


def _prepare_strength(df: pd.DataFrame, source_name: str) -> pd.DataFrame:
    validate_required_columns(
        df,
        ["function_name", "test_strength_score"],
        source_name,
    )
    out = df.copy()
    if "complexity_level" in out.columns:
        out["complexity_level"] = out["complexity_level"].apply(normalize_complexity_level)
    out["test_strength_score"] = pd.to_numeric(out["test_strength_score"], errors="coerce")
    return out[["function_name", "test_strength_score"]].drop_duplicates(subset=["function_name"])


def _prepare_eval(df: pd.DataFrame, score_column: str, source_name: str) -> pd.DataFrame:
    validate_required_columns(df, list(MERGE_KEYS) + ["overall_score"], source_name)
    out = df.copy()
    out["test_file"] = out["test_file"].astype(str)
    out[score_column] = pd.to_numeric(out["overall_score"], errors="coerce")
    return out[list(MERGE_KEYS) + [score_column]].drop_duplicates(subset=list(MERGE_KEYS))


def consolidate(cfg: DatasetConfig) -> pd.DataFrame | None:
    global MERGE_COUNT
    MERGE_COUNT = 0

    input_coverage = cfg.result_csv("cobertura_testes_gerados_gpt")
    input_density = cfg.result_csv("metrica_densidade_asserts")
    input_success = cfg.result_csv("metrica_sucesso_execucao")
    input_strength = cfg.result_csv("forca_heuristica_testes")
    input_eval_gpt = cfg.result_csv("avaliacao_gpt_sobre_testes_gpt")
    input_eval_claude = cfg.result_csv("avaliacao_claude_sobre_testes_gpt")

    print("Carregando CSVs para consolidação...\n")

    df_cov = _load_and_standardize(input_coverage, "df_cov")
    df_density = _load_and_standardize(input_density, "df_density")
    df_success = _load_and_standardize(input_success, "df_success")
    df_strength = _load_and_standardize(input_strength, "df_strength")

    if any(x is None for x in (df_cov, df_density, df_success, df_strength)):
        return None

    base = _prepare_coverage(df_cov, input_coverage.name)
    final = base[
        list(MERGE_KEYS)
        + ["complexity_level", "execution_status", "coverage_percent", "test_file_key", "passed_bool"]
    ].copy()

    final = _merge_logged(
        final,
        _prepare_density(df_density, input_density.name),
        on="test_file_key",
        how="left",
        label="densidade de asserts",
    )

    final = _merge_logged(
        final,
        _prepare_success(df_success, input_success.name),
        on="function_name",
        how="left",
        label="sucesso de execução",
    )
    final["execution_success_rate"] = final["execution_success_rate"].where(
        final["execution_success_rate"].notna(),
        final["passed_bool"].astype(float),
    )

    final = _merge_logged(
        final,
        _prepare_strength(df_strength, input_strength.name),
        on="function_name",
        how="left",
        label="test_strength_score",
    )

    df_gpt = _load_and_standardize(input_eval_gpt, "df_gpt", required=False)
    if df_gpt is not None:
        final = _merge_logged(
            final,
            _prepare_eval(df_gpt, "overall_score_gpt", input_eval_gpt.name),
            on=list(MERGE_KEYS),
            how="left",
            label="avaliação GPT",
        )
    else:
        final["overall_score_gpt"] = pd.NA

    df_claude = _load_and_standardize(input_eval_claude, "df_claude", required=False)
    if df_claude is not None:
        final = _merge_logged(
            final,
            _prepare_eval(df_claude, "overall_score_claude", input_eval_claude.name),
            on=list(MERGE_KEYS),
            how="left",
            label="avaliação Claude",
        )
    else:
        final["overall_score_claude"] = pd.NA

    for col in ("overall_score_gpt", "overall_score_claude"):
        if col not in final.columns:
            final[col] = pd.NA

    print(f"\nTotal de merges realizados: {MERGE_COUNT}\n")
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


def write_summary(df: pd.DataFrame, output_summary: Path, *, dataset_label: str) -> None:
    lines: list[str] = [
        f"Resumo consolidado do experimento ({dataset_label})",
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

    output_summary.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Consolida métricas do experimento.")
    add_dataset_argument(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    output_final = cfg.result_csv("resultados_finais")
    output_summary = cfg.result_txt("resumo_resultados_finais")

    print(f"Dataset: {cfg.key}")
    print("Consolidando resultados finais do experimento...\n")

    try:
        final = consolidate(cfg)
    except ValueError as exc:
        print(exc)
        print("Consolidação abortada.")
        return

    if final is None or final.empty:
        print("Consolidação abortada: dados insuficientes.")
        return

    cfg.results_dir.mkdir(parents=True, exist_ok=True)
    final.to_csv(output_final, index=False, encoding="utf-8")
    write_summary(final, output_summary, dataset_label=cfg.key)

    print(f"\nArquivo consolidado: {output_final}")
    print(f"Resumo textual: {output_summary}")
    print(f"Linhas consolidadas: {len(final)}")
    print("\nColunas:")
    for col in final.columns:
        non_null = final[col].notna().sum()
        print(f"  - {col}: {non_null}/{len(final)} preenchidos")

    unexpected_na = []
    for col in ("function_name", "test_file", "coverage_percent"):
        if final[col].isna().any():
            unexpected_na.append(f"{col} ({int(final[col].isna().sum())} NaN)")
    if unexpected_na:
        print("\nAviso: colunas essenciais com NaN:", ", ".join(unexpected_na))
    else:
        print("\nColunas essenciais (function_name, test_file, coverage_percent) sem NaN indevido.")


if __name__ == "__main__":
    main()
