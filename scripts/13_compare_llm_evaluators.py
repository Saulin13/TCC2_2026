"""Comparação GPT vs Claude nos cenários de avaliação cruzada."""

from __future__ import annotations

import argparse
import shutil
import unicodedata
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from csv_columns import prepare_csv_for_save, standardize_function_column
from dataset_config import RESULTS_DIR, add_dataset_argument, resolve_dataset

PLOTS_DIR = Path(".")
FIG_DPI = 150
SCATTER_2X2_DPI = 300
SCORE_AXIS_MAX = 10.0

MERGE_KEYS = ("function_name", "test_file")
COMPLEXITY_ORDER = ("baixa", "media", "alta")

CROSS_EVALUATION_PRESENTATION_FILES: tuple[str, ...] = (
    "01_execucao_por_status.png",
    "02_cobertura_media_por_complexidade.png",
    "05_test_strength_por_complexidade.png",
    "overall_score_cross_evaluation_by_complexity.png",
    "overall_score_cross_evaluation_mean.png",
    "overall_score_cross_evaluation_2x2_by_function.png",
    "overall_score_gpt_tests_gpt_vs_claude_by_function.png",
    "overall_score_evaluator_gpt_by_function.png",
    "overall_score_evaluator_claude_by_function.png",
    "overall_score_claude_tests_claude_vs_gpt_by_function.png",
)

PIPELINE_PLOTS_FOR_CROSS_EVALUATION: tuple[str, ...] = (
    "01_execucao_por_status.png",
    "02_cobertura_media_por_complexidade.png",
    "05_test_strength_por_complexidade.png",
    "05b_distribuicao_mutation_score.png",
)


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


def clean_cross_evaluation_folder(cross_dir: Path) -> None:
    """Remove arquivos gerados anteriormente, preservando README de apresentação."""
    cross_dir.mkdir(parents=True, exist_ok=True)
    preserve = {"README_RESULTADOS.txt"}
    for path in cross_dir.iterdir():
        if path.is_file() and path.name not in preserve:
            path.unlink()


def _copy_pipeline_plots_to_cross_evaluation(plots_dir: Path, cross_dir: Path) -> list[Path]:
    copied: list[Path] = []
    for filename in PIPELINE_PLOTS_FOR_CROSS_EVALUATION:
        source = plots_dir / filename
        if not source.exists():
            print(f"  Aviso: {filename} não encontrado em {plots_dir} — não copiado para cross_evaluation.")
            continue
        destination = cross_dir / filename
        shutil.copy2(source, destination)
        copied.append(destination.resolve())
        print(f"  Copiado para cross_evaluation: {destination}")
    return copied


def _list_cross_evaluation_files(cross_dir: Path) -> list[Path]:
    if not cross_dir.is_dir():
        return []
    return sorted(path.resolve() for path in cross_dir.iterdir() if path.is_file())


def _save_figure(fig: plt.Figure, filename: str, output_dirs: list[Path], *, dpi: int = FIG_DPI) -> list[Path]:
    saved_paths: list[Path] = []
    for out_dir in output_dirs:
        out_dir.mkdir(parents=True, exist_ok=True)
        path = (out_dir / filename).resolve()
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        saved_paths.append(path)
        print(f"  Salvo: {path}")
    plt.close(fig)
    return saved_paths


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


CROSS_SCATTER_PANELS: list[tuple[str, str, str, str, str]] = [
    ("overall_score_gpt_on_gpt", "overall_score_claude_on_gpt", "Testes GPT: GPT vs Claude", "GPT", "Claude"),
    ("overall_score_gpt_on_gpt", "overall_score_gpt_on_claude", "Avaliador GPT", "GPT", "GPT"),
    ("overall_score_claude_on_claude", "overall_score_claude_on_gpt", "Avaliador Claude", "Claude", "Claude"),
    ("overall_score_claude_on_claude", "overall_score_gpt_on_claude", "Testes Claude: Claude vs GPT", "Claude", "GPT"),
]

CROSS_SCATTER_INDIVIDUAL_PANELS: list[tuple[str, str, str, str, str, str]] = [
    (
        "overall_score_gpt_on_gpt",
        "overall_score_claude_on_gpt",
        "Testes GPT",
        "nota GPT",
        "nota Claude",
        "overall_score_gpt_tests_gpt_vs_claude_by_function.png",
    ),
    (
        "overall_score_gpt_on_gpt",
        "overall_score_gpt_on_claude",
        "Avaliador GPT",
        "GPT→GPT",
        "Claude→GPT",
        "overall_score_evaluator_gpt_by_function.png",
    ),
    (
        "overall_score_gpt_on_claude",
        "overall_score_claude_on_claude",
        "Avaliador Claude",
        "GPT→Claude",
        "Claude→Claude",
        "overall_score_evaluator_claude_by_function.png",
    ),
    (
        "overall_score_claude_on_claude",
        "overall_score_gpt_on_claude",
        "Testes Claude",
        "Claude",
        "GPT",
        "overall_score_claude_tests_claude_vs_gpt_by_function.png",
    ),
]


def _cross_scatter_valid_pairs(df: pd.DataFrame, x_col: str, y_col: str) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "x": pd.to_numeric(df[x_col], errors="coerce"),
            "y": pd.to_numeric(df[y_col], errors="coerce"),
        }
    ).dropna()


def _style_cross_scatter_axis(
    ax: plt.Axes,
    valid: pd.DataFrame,
    *,
    title: str,
    xlabel: str,
    ylabel: str,
) -> None:
    if valid.empty:
        ax.text(0.5, 0.5, "Sem dados", transform=ax.transAxes, ha="center", va="center")
    else:
        ax.scatter(
            valid["x"],
            valid["y"],
            alpha=0.85,
            s=80,
            c="#2980b9",
            edgecolors="white",
            linewidths=0.5,
        )

    ax.plot([0, SCORE_AXIS_MAX], [0, SCORE_AXIS_MAX], "--", color="#c0392b", linewidth=1.5)
    ax.set_xlim(0, SCORE_AXIS_MAX)
    ax.set_ylim(0, SCORE_AXIS_MAX)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title(title, fontsize=11, fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)


def _missing_cross_scatter_columns(
    df: pd.DataFrame,
    panels: list[tuple[str, str, str, str, str]] | list[tuple[str, str, str, str, str, str]],
) -> list[str]:
    if panels and len(panels[0]) == 6:
        return sorted(
            {
                col
                for x_col, y_col, _, _, _, _ in panels  # type: ignore[misc]
                for col in (x_col, y_col)
                if col not in df.columns
            }
        )
    return sorted(
        {
            col
            for x_col, y_col, _, _, _ in panels  # type: ignore[misc]
            for col in (x_col, y_col)
            if col not in df.columns
        }
    )


def plot_cross_evaluation_2x2_by_function(df: pd.DataFrame, output_dirs: list[Path]) -> list[Path]:
    """Figura 2x2 de dispersão cruzada (estilo overall_score_gpt_tests_gpt_vs_claude)."""
    missing = _missing_cross_scatter_columns(df, CROSS_SCATTER_PANELS)
    if missing:
        print(
            "  Ignorado overall_score_cross_evaluation_2x2_by_function.png: "
            f"colunas ausentes: {', '.join(missing)}"
        )
        return []

    if df.empty:
        print("  Ignorado overall_score_cross_evaluation_2x2_by_function.png: dataframe vazio.")
        return []

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    for ax, (x_col, y_col, title, xlabel, ylabel) in zip(axes.flatten(), CROSS_SCATTER_PANELS):
        valid = _cross_scatter_valid_pairs(df, x_col, y_col)
        _style_cross_scatter_axis(ax, valid, title=title, xlabel=xlabel, ylabel=ylabel)

    fig.tight_layout()
    return _save_figure(
        fig,
        "overall_score_cross_evaluation_2x2_by_function.png",
        output_dirs,
        dpi=SCATTER_2X2_DPI,
    )


def plot_cross_evaluation_by_function_individual(df: pd.DataFrame, output_dirs: list[Path]) -> list[Path]:
    """Gera os quatro painéis individuais com o mesmo estilo do gráfico 2x2."""
    missing = _missing_cross_scatter_columns(df, CROSS_SCATTER_INDIVIDUAL_PANELS)
    if missing:
        print(
            "  Ignorados gráficos individuais by_function: "
            f"colunas ausentes: {', '.join(missing)}"
        )
        return []

    if df.empty:
        print("  Ignorados gráficos individuais by_function: dataframe vazio.")
        return []

    saved_paths: list[Path] = []
    for x_col, y_col, title, xlabel, ylabel, filename in CROSS_SCATTER_INDIVIDUAL_PANELS:
        valid = _cross_scatter_valid_pairs(df, x_col, y_col)
        fig, ax = plt.subplots(figsize=(6, 6))
        _style_cross_scatter_axis(ax, valid, title=title, xlabel=xlabel, ylabel=ylabel)
        fig.tight_layout()
        saved_paths.extend(_save_figure(fig, filename, output_dirs, dpi=SCATTER_2X2_DPI))

    return saved_paths


def _plot_scatter(df: pd.DataFrame, *, filename: str, output_dirs: list[Path]) -> list[Path]:
    x = df["overall_score_gpt"]
    y = df["overall_score_claude"]
    valid = pd.DataFrame({"x": x, "y": y}).dropna()
    if valid.empty:
        print(f"  Ignorado {filename}: sem dados.")
        return []
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
    return _save_figure(fig, filename, output_dirs)


def _plot_cross_mean(cross_df: pd.DataFrame, output_dirs: list[Path]) -> list[Path]:
    means = (
        cross_df.groupby("scenario", observed=True)["overall_score"]
        .mean()
        .reindex(["GPT→GPT", "GPT→Claude", "Claude→GPT", "Claude→Claude"])
        .dropna()
    )
    if means.empty:
        print("  Ignorado overall_score_cross_evaluation_mean.png: sem dados.")
        return []
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(means.index, means.values, color=["#3498db", "#9b59b6", "#1abc9c", "#e67e22"])
    ax.set_xlabel("cenário")
    ax.set_ylabel("overall_score (média)")
    ax.set_ylim(0, 10)
    _annotate_bars(ax, bars, decimals=2)
    fig.tight_layout()
    return _save_figure(fig, "overall_score_cross_evaluation_mean.png", output_dirs)


def _plot_cross_by_complexity(cross_df: pd.DataFrame, output_dirs: list[Path]) -> list[Path]:
    levels = [lvl for lvl in COMPLEXITY_ORDER if lvl in cross_df["complexity_level"].values]
    if not levels:
        print("  Ignorado overall_score_cross_evaluation_by_complexity.png: sem níveis.")
        return []
    scenarios = ["GPT→GPT", "GPT→Claude", "Claude→GPT", "Claude→Claude"]
    means = (
        cross_df.groupby(["complexity_level", "scenario"], observed=True)["overall_score"]
        .mean()
        .unstack()
        .reindex(index=levels, columns=scenarios)
    )
    x = np.arange(len(levels))
    width = 0.2
    fig, ax = plt.subplots(figsize=(11, 5))
    colors = ["#3498db", "#9b59b6", "#1abc9c", "#e67e22"]
    all_vals: list[float] = []
    for idx, scen in enumerate(scenarios):
        vals = means[scen].values if scen in means.columns else np.array([np.nan] * len(levels))
        bars = ax.bar(x + (idx - 1.5) * width, vals, width, label=scen, color=colors[idx])
        _annotate_bars(ax, bars, decimals=2)
        for val in vals:
            if pd.notna(val):
                all_vals.append(float(val))
    ax.set_xticks(x)
    ax.set_xticklabels(levels)
    ax.set_xlabel("complexity_level")
    ax.set_ylabel("overall_score (média)")
    ymax = max(all_vals + [10.0]) * 1.12
    ax.set_ylim(0, ymax)
    ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5), borderaxespad=0.0)
    fig.subplots_adjust(right=0.78)
    return _save_figure(fig, "overall_score_cross_evaluation_by_complexity.png", output_dirs)


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
    graficos_dir = RESULTS_DIR / "graficos" / cfg.key
    graficos_dir.mkdir(parents=True, exist_ok=True)
    plots_cross_dir = PLOTS_DIR / "cross_evaluation"
    graficos_cross_dir = graficos_dir / "cross_evaluation"
    clean_cross_evaluation_folder(plots_cross_dir)
    clean_cross_evaluation_folder(graficos_cross_dir)
    cross_eval_dirs = [plots_cross_dir, graficos_cross_dir]

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
    saved_paths: list[Path] = []
    saved_paths.extend(
        _plot_scatter(
            pair_gpt_tests,
            filename="overall_score_gpt_tests_gpt_vs_claude.png",
            output_dirs=[PLOTS_DIR],
        )
    )
    saved_paths.extend(
        _plot_scatter(
            pair_claude_tests,
            filename="overall_score_claude_tests_gpt_vs_claude.png",
            output_dirs=[PLOTS_DIR],
        )
    )

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
    saved_paths.extend(_plot_cross_mean(cross_df, [PLOTS_DIR, *cross_eval_dirs]))
    saved_paths.extend(_plot_cross_by_complexity(cross_df, [PLOTS_DIR, *cross_eval_dirs]))

    final_path = cfg.result_csv("resultados_finais")
    function_plot_dirs = [PLOTS_DIR, graficos_dir, *cross_eval_dirs]
    if final_path.exists():
        df_final = pd.read_csv(final_path)
        saved_paths.extend(plot_cross_evaluation_2x2_by_function(df_final, function_plot_dirs))
        saved_paths.extend(plot_cross_evaluation_by_function_individual(df_final, function_plot_dirs))
    else:
        print(
            f"Aviso: {final_path.name} não encontrado — "
            "overall_score_cross_evaluation_2x2_by_function.png e gráficos individuais não gerados."
        )

    print("\nMontando pasta cross_evaluation (apresentação):")
    for cross_dir in cross_eval_dirs:
        _copy_pipeline_plots_to_cross_evaluation(PLOTS_DIR, cross_dir)

    write_summary(pair_gpt_tests, pair_claude_tests, output_summary)
    print(f"Resumo: {output_summary}")

    for label, cross_dir in (("plots", plots_cross_dir), ("graficos", graficos_cross_dir)):
        final_files = _list_cross_evaluation_files(cross_dir)
        print(f"\nArquivos finais em cross_evaluation ({label}):")
        for path in final_files:
            print(f"  {path}")
        expected = len(CROSS_EVALUATION_PRESENTATION_FILES)
        if len(final_files) != expected:
            print(
                f"  Aviso: esperados {expected} arquivos em {cross_dir}, "
                f"encontrados {len(final_files)}."
            )

    print("\nConcluído.")


if __name__ == "__main__":
    main()
