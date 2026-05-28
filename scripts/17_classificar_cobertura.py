"""
Classifica cobertura de testes em faixas baseadas na literatura.
Entrada: data/results/cobertura_testes_gerados_gpt.csv
Saídas:
  - data/results/classificacao_cobertura.csv
  - data/results/resumo_classificacao_cobertura.txt
  - data/results/plots/17_classificacao_cobertura.png
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_COVERAGE = BASE_DIR / "data" / "results" / "cobertura_testes_gerados_gpt.csv"
OUTPUT_CSV = BASE_DIR / "data" / "results" / "classificacao_cobertura.csv"
OUTPUT_SUMMARY = BASE_DIR / "data" / "results" / "resumo_classificacao_cobertura.txt"
OUTPUT_PLOT = BASE_DIR / "data" / "results" / "plots" / "17_classificacao_cobertura.png"

# Faixas de classificação (ajustáveis após revisão da literatura)
THRESHOLD_INSUFFICIENT_MAX_EXCLUSIVE = 50.0
THRESHOLD_MODERATE_MAX_EXCLUSIVE = 80.0

CLASS_INSUFFICIENT = "insuficiente"
CLASS_MODERATE = "moderada"
CLASS_ADEQUATE = "adequada"

CLASSIFICATION_ORDER = (CLASS_INSUFFICIENT, CLASS_MODERATE, CLASS_ADEQUATE)
CLASSIFICATION_LABELS_PT = {
    CLASS_INSUFFICIENT: "Insuficiente",
    CLASS_MODERATE: "Moderada",
    CLASS_ADEQUATE: "Adequada",
}
CLASSIFICATION_COLORS = {
    CLASS_INSUFFICIENT: "#e74c3c",
    CLASS_MODERATE: "#f39c12",
    CLASS_ADEQUATE: "#2ecc71",
}

FIG_DPI = 150


def classify_coverage(coverage_percent: float) -> str:
    if pd.isna(coverage_percent):
        return ""
    if coverage_percent < THRESHOLD_INSUFFICIENT_MAX_EXCLUSIVE:
        return CLASS_INSUFFICIENT
    if coverage_percent < THRESHOLD_MODERATE_MAX_EXCLUSIVE:
        return CLASS_MODERATE
    return CLASS_ADEQUATE


def category_counts(df: pd.DataFrame) -> pd.Series:
    return (
        df["coverage_classification"]
        .value_counts(dropna=False)
        .reindex(CLASSIFICATION_ORDER, fill_value=0)
    )


def print_terminal_summary(counts: pd.Series, total: int) -> None:
    print("\nResumo da classificação de cobertura")
    print(f"Total de registros: {total}\n")
    print("Quantidade por categoria:")
    for category, count in counts.items():
        print(f"  {category}: {int(count)}")
    print("\nPercentual por categoria:")
    for category, count in counts.items():
        pct = (count / total * 100.0) if total else 0.0
        print(f"  {category}: {pct:.1f}%")


def build_summary_text(counts: pd.Series, total: int) -> str:
    lines = [
        "Resumo da classificação de cobertura",
        "",
        f"Total de registros: {total}",
        "",
        "Quantidade por categoria:",
    ]
    for category, count in counts.items():
        lines.append(f"- {category}: {int(count)}")
    lines.append("")
    lines.append("Percentual por categoria:")
    for category, count in counts.items():
        pct = (count / total * 100.0) if total else 0.0
        lines.append(f"- {category}: {pct:.2f}%")
    lines.append("")
    lines.append("Faixas utilizadas:")
    lines.append(f"- {CLASS_INSUFFICIENT}: coverage_percent < {THRESHOLD_INSUFFICIENT_MAX_EXCLUSIVE:.0f}")
    lines.append(
        f"- {CLASS_MODERATE}: "
        f"{THRESHOLD_INSUFFICIENT_MAX_EXCLUSIVE:.0f} <= coverage_percent < {THRESHOLD_MODERATE_MAX_EXCLUSIVE:.0f}"
    )
    lines.append(f"- {CLASS_ADEQUATE}: coverage_percent >= {THRESHOLD_MODERATE_MAX_EXCLUSIVE:.0f}")
    return "\n".join(lines) + "\n"


def plot_classification_bar(counts: pd.Series) -> None:
    labels = [CLASSIFICATION_LABELS_PT[c] for c in CLASSIFICATION_ORDER]
    values = [int(counts[c]) for c in CLASSIFICATION_ORDER]
    colors = [CLASSIFICATION_COLORS[c] for c in CLASSIFICATION_ORDER]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(labels, values, color=colors, edgecolor="#333333", linewidth=0.6)

    ax.set_title("Classificação da cobertura de testes")
    ax.set_xlabel("Classificação")
    ax.set_ylabel("Quantidade de testes")
    ax.set_ylim(0, max(values) * 1.2 if values else 1)

    for bar, val in zip(bars, values):
        ax.annotate(
            f"{val}",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha="center",
            va="bottom",
            fontsize=10,
        )

    fig.tight_layout()
    OUTPUT_PLOT.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_PLOT, dpi=FIG_DPI, bbox_inches="tight")
    plt.close()
    print(f"\nGráfico salvo: {OUTPUT_PLOT}")


def main() -> None:
    print("Classificando cobertura (faixas da literatura)...")

    if not INPUT_COVERAGE.exists():
        print(f"Erro: arquivo não encontrado: {INPUT_COVERAGE}")
        return

    df = pd.read_csv(INPUT_COVERAGE)
    if "coverage_percent" not in df.columns:
        print("Erro: coluna 'coverage_percent' ausente no CSV de entrada.")
        return

    df["coverage_percent"] = pd.to_numeric(df["coverage_percent"], errors="coerce")
    df["coverage_classification"] = df["coverage_percent"].apply(classify_coverage)

    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"CSV salvo: {OUTPUT_CSV}")

    total = len(df)
    counts = category_counts(df)
    print_terminal_summary(counts, total)

    summary_text = build_summary_text(counts, total)
    OUTPUT_SUMMARY.write_text(summary_text, encoding="utf-8")
    print(f"Resumo salvo: {OUTPUT_SUMMARY}")

    plot_classification_bar(counts)
    print("Concluído.")


if __name__ == "__main__":
    main()
