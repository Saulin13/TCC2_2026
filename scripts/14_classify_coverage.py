"""
Classifica a cobertura do coverage.py em categorias interpretáveis.
Entrada: data/results/cobertura_testes_gerados_gpt.csv
Saídas:
  - data/results/classificacao_cobertura.csv
  - data/results/resumo_classificacao_cobertura.txt
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from csv_columns import prepare_csv_for_save, standardize_function_column, validate_required_columns
from dataset_config import add_dataset_argument, resolve_dataset

# Faixas de classificação (fáceis de ajustar após revisão da literatura)
LOW_COVERAGE_MAX_EXCLUSIVE = 50.0
MEDIUM_COVERAGE_MAX_EXCLUSIVE = 80.0

CLASS_LOW = "cobertura_baixa"
CLASS_MEDIUM = "cobertura_media"
CLASS_HIGH = "cobertura_alta"

REQUIRED_COLUMNS = [
    "function_name",
    "file_path",
    "complexity_level",
    "test_file",
    "execution_status",
    "coverage_percent",
]

OUTPUT_COLUMNS = REQUIRED_COLUMNS + ["coverage_classification"]


def classify_coverage(coverage_percent: float) -> str:
    if pd.isna(coverage_percent):
        return ""
    if coverage_percent < LOW_COVERAGE_MAX_EXCLUSIVE:
        return CLASS_LOW
    if coverage_percent < MEDIUM_COVERAGE_MAX_EXCLUSIVE:
        return CLASS_MEDIUM
    return CLASS_HIGH


def format_series_mean(series: pd.Series, decimals: int = 2) -> str:
    numeric = pd.to_numeric(series, errors="coerce")
    if numeric.dropna().empty:
        return "N/A"
    return f"{numeric.mean():.{decimals}f}"


def build_summary_text(df: pd.DataFrame) -> str:
    lines: list[str] = []
    total_rows = len(df)

    lines.append("Resumo da classificação de cobertura")
    lines.append("")
    lines.append(f"Total de registros: {total_rows}")
    lines.append("")

    lines.append("Total por categoria:")
    category_counts = (
        df["coverage_classification"]
        .value_counts(dropna=False)
        .reindex([CLASS_LOW, CLASS_MEDIUM, CLASS_HIGH], fill_value=0)
    )
    for category, count in category_counts.items():
        lines.append(f"- {category}: {int(count)}")
    lines.append("")

    lines.append("Percentual por categoria:")
    for category, count in category_counts.items():
        pct = (count / total_rows * 100.0) if total_rows else 0.0
        lines.append(f"- {category}: {pct:.2f}%")
    lines.append("")

    lines.append(f"Média de cobertura geral: {format_series_mean(df['coverage_percent'])}")
    lines.append("")

    lines.append("Média de cobertura por complexity_level:")
    by_complexity = (
        df.groupby("complexity_level", dropna=False, observed=True)["coverage_percent"]
        .mean()
        .sort_index()
    )
    if by_complexity.empty:
        lines.append("- N/A")
    else:
        for level, mean_val in by_complexity.items():
            level_label = str(level) if pd.notna(level) else "N/A"
            lines.append(f"- {level_label}: {mean_val:.2f}")
    lines.append("")

    lines.append("Média de cobertura por execution_status:")
    by_status = (
        df.groupby("execution_status", dropna=False, observed=True)["coverage_percent"]
        .mean()
        .sort_index()
    )
    if by_status.empty:
        lines.append("- N/A")
    else:
        for status, mean_val in by_status.items():
            status_label = str(status) if pd.notna(status) else "N/A"
            lines.append(f"- {status_label}: {mean_val:.2f}")

    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classifica cobertura do coverage.py em categorias interpretáveis."
    )
    add_dataset_argument(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    input_coverage = cfg.result_csv("cobertura_testes_gerados_gpt")
    output_classification = cfg.result_csv("classificacao_cobertura")
    output_summary = cfg.result_txt("resumo_classificacao_cobertura")

    print(f"Dataset: {cfg.key}")
    print("Classificando cobertura do coverage.py...")

    if not input_coverage.exists():
        print(f"Erro: arquivo de entrada não encontrado: {input_coverage}")
        return

    output_classification.parent.mkdir(parents=True, exist_ok=True)

    df = standardize_function_column(pd.read_csv(input_coverage))
    try:
        validate_required_columns(df, REQUIRED_COLUMNS, input_coverage.name)
    except ValueError as exc:
        print(exc)
        return

    out = df[REQUIRED_COLUMNS].copy()
    out["coverage_percent"] = pd.to_numeric(out["coverage_percent"], errors="coerce")
    out["coverage_classification"] = out["coverage_percent"].apply(classify_coverage)
    out = out[OUTPUT_COLUMNS]

    prepare_csv_for_save(out).to_csv(output_classification, index=False, encoding="utf-8")
    print(f"CSV salvo: {output_classification}")

    summary_text = build_summary_text(out)
    output_summary.write_text(summary_text, encoding="utf-8")
    print(f"Resumo salvo: {output_summary}")

    print("Concluído.")


if __name__ == "__main__":
    main()
