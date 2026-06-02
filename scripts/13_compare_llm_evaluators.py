"""Comparação GPT vs Claude nos cenários de avaliação cruzada."""

from __future__ import annotations

import argparse
import unicodedata
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from csv_columns import prepare_csv_for_save, standardize_function_column
from dataset_config import add_dataset_argument, resolve_dataset

PLOTS_DIR = Path(".")
FIG_DPI = 150
MERGE_KEYS = ("function_name", "test_file")
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


def _save_fig(path: Path) -> None:
    plt.savefig(path, dpi=FIG_DPI, bbox_inches="tight")
    plt.close()
    print(f"  Salvo: {path.name}")


def _annotate_bars(ax: plt.Axes, bars, *, decimals: int = 2) -> None:
    for bar in bars:
        height = bar.get_height()
        if pd.isna(height):
            continue
        ax.annotate(
            f"{height:.{decimals}f}",
            xy=(bar.get_x() + bar.get_width() / 2, height),
            ha="center",
            va="bottom",
        )


def _prepare_evaluator_df(df: pd.DataFrame, suffix: str) -> pd.DataFrame:
    out = df.copy()
    out["test_file"] = out["test_file"].astype(str)
    out["complexity_level"] = out["complexity_level"].apply(normalize_complexity_level)
    out = out.rename(columns={"overall_score": f"overall_score_{suffix}"})
    keep = [
        "function_name",
        "test_file",
        "file_path",
        "complexity_level",
        "execution_status",
        "coverage_percent",
        f"overall_score_{suffix}",
    ]
    return out[[c for c in keep if c in out.columns]]


def _build_pair(gpt_df: pd.DataFrame, claude_df: pd.DataFrame, *, generator: str) -> pd.DataFrame:
    g = _prepare_evaluator_df(gpt_df, "gpt")
    c = _prepare_evaluator_df(claude_df, "claude")
    merged = g.merge(
        c[list(MERGE_KEYS) + ["overall_score_claude"]],
        on=list(MERGE_KEYS),
        how="inner",
    )
    merged["overall_score_gpt"] = pd.to_numeric(merged["overall_score_gpt"], errors="coerce")
    merged["overall_score_claude"] = pd.to_numeric(merged["overall_score_claude"], errors="coerce")
    merged["generator"] = generator
    return merged


def _plot_scatter(df: pd.DataFrame, *, filename: str) -> None:
    x = df["overall_score_gpt"]
    y = df["overall_score_claude"]
    valid = pd.DataFrame({"x": x, "y": y}).dropna()
    if valid.empty:
        print(f"  Ignorado {filename}: sem dados.")
        return
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(valid["x"], valid["y"], alpha=0.85, s=80, c="#2980b9", edgecolors="white", linewidths=0.5)
    lo = min(valid["x"].min(), valid["y"].min(), 0)
    hi = max(valid["x"].max(), valid["y"].max(), 10)
    ax.plot([lo, hi], [lo, hi], "--", color="#c0392b", linewidth=1.5, label="y = x")
    ax.set_xlim(lo - 0.5, hi + 0.5)
    ax.set_ylim(lo - 0.5, hi + 0.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("overall_score_gpt")
    ax.set_ylabel("overall_score_claude")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    _save_fig(PLOTS_DIR / filename)


def _plot_cross_mean(cross_df: pd.DataFrame) -> None:
    means = (
        cross_df.groupby("scenario", observed=True)["overall_score"]
        .mean()
        .reindex(["GPT→GPT", "GPT→Claude", "Claude→GPT", "Claude→Claude"])
        .dropna()
    )
    if means.empty:
        print("  Ignorado overall_score_cross_evaluation_mean.png: sem dados.")
        return
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(means.index, means.values, color=["#3498db", "#9b59b6", "#1abc9c", "#e67e22"])
    ax.set_xlabel("cenário")
    ax.set_ylabel("overall_score (média)")
    ax.set_ylim(0, 10)
    _annotate_bars(ax, bars, decimals=2)
    fig.tight_layout()
    _save_fig(PLOTS_DIR / "overall_score_cross_evaluation_mean.png")


def _plot_cross_by_complexity(cross_df: pd.DataFrame) -> None:
    levels = [lvl for lvl in COMPLEXITY_ORDER if lvl in cross_df["complexity_level"].values]
    if not levels:
        print("  Ignorado overall_score_cross_evaluation_by_complexity.png: sem níveis.")
        return
    scenarios = ["GPT→GPT", "GPT→Claude", "Claude→GPT", "Claude→Claude"]
    means = (
        cross_df.groupby(["complexity_level", "scenario"], observed=True)["overall_score"]
        .mean()
        .unstack()
        .reindex(index=levels, columns=scenarios)
    )
    x = np.arange(len(levels))
    width = 0.2
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ["#3498db", "#9b59b6", "#1abc9c", "#e67e22"]
    for idx, scen in enumerate(scenarios):
        vals = means[scen].values if scen in means.columns else np.array([np.nan] * len(levels))
        bars = ax.bar(x + (idx - 1.5) * width, vals, width, label=scen, color=colors[idx])
        _annotate_bars(ax, bars, decimals=2)
    ax.set_xticks(x)
    ax.set_xticklabels(levels)
    ax.set_xlabel("complexity_level")
    ax.set_ylabel("overall_score (média)")
    ax.set_ylim(0, 10)
    ax.legend()
    fig.tight_layout()
    _save_fig(PLOTS_DIR / "overall_score_cross_evaluation_by_complexity.png")


def write_summary(pair_gpt_tests: pd.DataFrame, pair_claude_tests: pd.DataFrame, output_summary: Path) -> None:
    lines = [
        "Resumo da comparação cruzada GPT vs. Claude",
        "=" * 48,
        f"Comparações em testes GPT: {len(pair_gpt_tests)}",
        f"Comparações em testes Claude: {len(pair_claude_tests)}",
        "",
        f"Média GPT→GPT: {pair_gpt_tests['overall_score_gpt'].mean():.2f}",
        f"Média GPT→Claude: {pair_gpt_tests['overall_score_claude'].mean():.2f}",
        f"Média Claude→GPT: {pair_claude_tests['overall_score_gpt'].mean():.2f}",
        f"Média Claude→Claude: {pair_claude_tests['overall_score_claude'].mean():.2f}",
    ]
    output_summary.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compara avaliações GPT e Claude.")
    add_dataset_argument(parser)
    return parser.parse_args()


def main() -> None:
    global PLOTS_DIR

    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    input_gpt_on_gpt = cfg.result_csv("avaliacao_gpt_sobre_testes_gpt")
    input_claude_on_gpt = cfg.result_csv("avaliacao_claude_sobre_testes_gpt")
    input_gpt_on_claude = cfg.result_csv("avaliacao_gpt_sobre_testes_claude")
    input_claude_on_claude = cfg.result_csv("avaliacao_claude_sobre_testes_claude")
    output_comparison = cfg.result_csv("comparacao_avaliadores_gpt_claude")
    output_summary = cfg.result_txt("resumo_comparacao_avaliadores")
    PLOTS_DIR = cfg.plots_dir

    print(f"Dataset: {cfg.key}")
    print("Comparando avaliadores GPT e Claude...")

    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.labelsize": 12,
        }
    )
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        input_gpt_on_gpt,
        input_claude_on_gpt,
        input_gpt_on_claude,
        input_claude_on_claude,
    ]
    missing = [p for p in required if not p.exists()]
    if missing:
        print("Erro: arquivos de avaliação ausentes:")
        for p in missing:
            print(f"  - {p}")
        return

    pair_gpt_tests = _build_pair(
        standardize_function_column(pd.read_csv(input_gpt_on_gpt)),
        standardize_function_column(pd.read_csv(input_claude_on_gpt)),
        generator="gpt",
    )
    pair_claude_tests = _build_pair(
        standardize_function_column(pd.read_csv(input_gpt_on_claude)),
        standardize_function_column(pd.read_csv(input_claude_on_claude)),
        generator="claude",
    )

    pair_gpt_tests["comparison_group"] = "gpt_tests"
    pair_claude_tests["comparison_group"] = "claude_tests"
    comparison = pd.concat([pair_gpt_tests, pair_claude_tests], ignore_index=True)
    prepare_csv_for_save(comparison).to_csv(output_comparison, index=False, encoding="utf-8")
    print(f"\nComparação salva: {output_comparison} ({len(comparison)} linhas)")

    print("\nGráficos:")
    _plot_scatter(pair_gpt_tests, filename="overall_score_gpt_tests_gpt_vs_claude.png")
    _plot_scatter(pair_claude_tests, filename="overall_score_claude_tests_gpt_vs_claude.png")

    cross_rows: list[dict[str, object]] = []
    for _, row in pair_gpt_tests.iterrows():
        cross_rows.append(
            {
                "function_name": row["function_name"],
                "complexity_level": row["complexity_level"],
                "scenario": "GPT→GPT",
                "overall_score": row["overall_score_gpt"],
            }
        )
        cross_rows.append(
            {
                "function_name": row["function_name"],
                "complexity_level": row["complexity_level"],
                "scenario": "GPT→Claude",
                "overall_score": row["overall_score_claude"],
            }
        )
    for _, row in pair_claude_tests.iterrows():
        cross_rows.append(
            {
                "function_name": row["function_name"],
                "complexity_level": row["complexity_level"],
                "scenario": "Claude→GPT",
                "overall_score": row["overall_score_gpt"],
            }
        )
        cross_rows.append(
            {
                "function_name": row["function_name"],
                "complexity_level": row["complexity_level"],
                "scenario": "Claude→Claude",
                "overall_score": row["overall_score_claude"],
            }
        )
    cross_df = pd.DataFrame(cross_rows)
    cross_df["overall_score"] = pd.to_numeric(cross_df["overall_score"], errors="coerce")
    cross_df["complexity_level"] = cross_df["complexity_level"].apply(normalize_complexity_level)
    _plot_cross_mean(cross_df)
    _plot_cross_by_complexity(cross_df)

    write_summary(pair_gpt_tests, pair_claude_tests, output_summary)
    print(f"Resumo: {output_summary}")
    print("\nConcluído.")


if __name__ == "__main__":
    main()
