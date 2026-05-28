"""
Compara avaliações de testes gerados feitas por GPT e Claude sobre a mesma amostra.
"""

from __future__ import annotations

import unicodedata
from pathlib import Path

import argparse
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from csv_columns import prepare_csv_for_save, standardize_function_column
from dataset_config import add_dataset_argument, resolve_dataset

PLOTS_DIR = Path(".")

MERGE_KEYS = ("function_name", "test_file")
COMPLEXITY_ORDER = ("baixa", "media", "alta")
FIG_DPI = 150

SCORE_COLUMNS = (
    "correctness_score",
    "scenario_coverage_score",
    "edge_cases_score",
    "clarity_score",
    "overall_score",
)

META_COLUMNS = (
    "function_name",
    "test_file",
    "file_path",
    "complexity_score",
    "complexity_level",
    "execution_status",
    "passed",
    "return_code",
    "coverage_percent",
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


def _save_fig(path: Path) -> None:
    plt.savefig(path, dpi=FIG_DPI, bbox_inches="tight")
    plt.close()
    print(f"  Salvo: {path.name}")


def _pearson_r(x: pd.Series, y: pd.Series) -> float | None:
    pair = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(pair) < 2:
        return None
    return float(pair["x"].corr(pair["y"]))


def _load_gpt_eval(gpt_eval_path: Path) -> pd.DataFrame:
    if gpt_eval_path.exists():
        print(f"GPT: {gpt_eval_path.name}")
        return standardize_function_column(pd.read_csv(gpt_eval_path))
    raise FileNotFoundError(f"Arquivo GPT não encontrado: {gpt_eval_path.name}.")


def _prepare_evaluator_df(df: pd.DataFrame, suffix: str) -> pd.DataFrame:
    out = df.copy()
    out["test_file"] = out["test_file"].astype(str)
    out["complexity_level"] = out["complexity_level"].apply(normalize_complexity_level)

    rename_map: dict[str, str] = {}
    for col in SCORE_COLUMNS:
        if col in out.columns:
            rename_map[col] = f"{col}_{suffix}"

    out = out.rename(columns=rename_map)

    keep = [c for c in META_COLUMNS if c in out.columns]
    keep += [f"{c}_{suffix}" for c in SCORE_COLUMNS if f"{c}_{suffix}" in out.columns]
    if f"evaluation_error_{suffix}" not in out.columns and "evaluation_error" in df.columns:
        out = out.rename(columns={"evaluation_error": f"evaluation_error_{suffix}"})
        keep.append(f"evaluation_error_{suffix}")

    return out[keep + [c for c in out.columns if c.startswith("strengths") or c.startswith("missing") or c.startswith("potential")]]


def build_comparison(df_gpt: pd.DataFrame, df_claude: pd.DataFrame) -> pd.DataFrame:
    gpt = _prepare_evaluator_df(df_gpt, "gpt")
    claude = _prepare_evaluator_df(df_claude, "claude")

    meta_cols = [c for c in META_COLUMNS if c in gpt.columns]
    gpt_meta = gpt[meta_cols + [c for c in gpt.columns if c.endswith("_gpt")]].copy()
    claude_scores = claude[list(MERGE_KEYS) + [c for c in claude.columns if c.endswith("_claude")]].copy()

    merged = gpt_meta.merge(claude_scores, on=list(MERGE_KEYS), how="inner")

    merged["overall_score_gpt"] = pd.to_numeric(merged["overall_score_gpt"], errors="coerce")
    merged["overall_score_claude"] = pd.to_numeric(merged["overall_score_claude"], errors="coerce")
    merged["score_difference"] = merged["overall_score_gpt"] - merged["overall_score_claude"]
    merged["abs_score_difference"] = merged["score_difference"].abs()

    return merged


def plot_08_scatter_overall(df: pd.DataFrame) -> None:
    x = df["overall_score_gpt"]
    y = df["overall_score_claude"]
    valid = pd.DataFrame({"x": x, "y": y}).dropna()
    if valid.empty:
        print("  Ignorado 08_gpt_vs_claude_overall_score.png: sem dados.")
        return

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(valid["x"], valid["y"], alpha=0.85, s=80, c="#2980b9", edgecolors="white", linewidths=0.5)

    lo = min(valid["x"].min(), valid["y"].min(), 0)
    hi = max(valid["x"].max(), valid["y"].max(), 10)
    ax.plot([lo, hi], [lo, hi], "--", color="#c0392b", linewidth=1.5, label="y = x")

    ax.set_xlim(lo - 0.5, hi + 0.5)
    ax.set_ylim(lo - 0.5, hi + 0.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("Comparação: overall_score GPT vs. Claude")
    ax.set_xlabel("overall_score_gpt")
    ax.set_ylabel("overall_score_claude")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    _save_fig(PLOTS_DIR / "08_gpt_vs_claude_overall_score.png")


def plot_09_media_avaliadores(df: pd.DataFrame) -> None:
    means = pd.Series(
        {
            "GPT": df["overall_score_gpt"].mean(),
            "Claude": df["overall_score_claude"].mean(),
        }
    ).dropna()

    fig, ax = plt.subplots(figsize=(6, 5))
    colors = ["#3498db", "#9b59b6"]
    bars = ax.bar(means.index, means.values, color=colors, edgecolor="#333333", linewidth=0.6)
    ax.set_title("Média de overall_score por avaliador")
    ax.set_ylabel("overall_score (média)")
    ax.set_ylim(0, 10)
    for bar, val in zip(bars, means.values):
        ax.annotate(f"{val:.2f}", xy=(bar.get_x() + bar.get_width() / 2, val), ha="center", va="bottom")
    fig.tight_layout()
    _save_fig(PLOTS_DIR / "09_media_notas_por_avaliador.png")


def plot_10_diferenca_por_funcao(df: pd.DataFrame) -> None:
    work = df.sort_values("abs_score_difference", ascending=False)
    names = work["function_name"].tolist()
    values = work["abs_score_difference"].tolist()

    fig, ax = plt.subplots(figsize=(10, max(5, len(names) * 0.45)))
    y_pos = np.arange(len(names))
    ax.barh(y_pos, values, color="#e67e22", edgecolor="#333333", linewidth=0.5)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(names, fontsize=9)
    ax.invert_yaxis()
    ax.set_title("|overall_score_gpt − overall_score_claude| por função")
    ax.set_xlabel("abs_score_difference")
    fig.tight_layout()
    _save_fig(PLOTS_DIR / "10_diferenca_notas_por_funcao.png")


def plot_11_media_por_complexidade(df: pd.DataFrame) -> None:
    levels = [lvl for lvl in COMPLEXITY_ORDER if lvl in df["complexity_level"].values]
    if not levels:
        print("  Ignorado 11_media_notas_avaliador_por_complexidade.png: sem níveis.")
        return

    gpt_means = []
    claude_means = []
    for lvl in levels:
        sub = df[df["complexity_level"] == lvl]
        gpt_means.append(sub["overall_score_gpt"].mean())
        claude_means.append(sub["overall_score_claude"].mean())

    x = np.arange(len(levels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width / 2, gpt_means, width, label="GPT", color="#3498db")
    ax.bar(x + width / 2, claude_means, width, label="Claude", color="#9b59b6")
    ax.set_xticks(x)
    ax.set_xticklabels(levels)
    ax.set_ylim(0, 10)
    ax.set_title("Média de overall_score por avaliador e complexidade")
    ax.set_xlabel("complexity_level")
    ax.set_ylabel("overall_score (média)")
    ax.legend()
    fig.tight_layout()
    _save_fig(PLOTS_DIR / "11_media_notas_avaliador_por_complexidade.png")


def plot_12_gpt_vs_claude_diagonal(df: pd.DataFrame) -> None:
    valid = df[["overall_score_gpt", "overall_score_claude"]].dropna()
    if valid.empty:
        print("  Ignorado 12_gpt_vs_claude_diagonal.png: sem dados.")
        return

    r = _pearson_r(valid["overall_score_gpt"], valid["overall_score_claude"])
    r_text = f"r = {r:.3f}" if r is not None else "r = N/A"

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(
        valid["overall_score_gpt"],
        valid["overall_score_claude"],
        alpha=0.85,
        s=80,
        c="#2980b9",
        edgecolors="white",
        linewidths=0.5,
    )

    lo = min(valid["overall_score_gpt"].min(), valid["overall_score_claude"].min(), 0)
    hi = max(valid["overall_score_gpt"].max(), valid["overall_score_claude"].max(), 10)
    ax.plot([lo, hi], [lo, hi], "--", color="#c0392b", linewidth=1.5, label="Concordância perfeita (y = x)")

    ax.set_xlim(lo - 0.5, hi + 0.5)
    ax.set_ylim(lo - 0.5, hi + 0.5)
    ax.set_aspect("equal", adjustable="box")
    ax.set_title("GPT vs. Claude: overall_score\n" + r_text)
    ax.set_xlabel("overall_score (GPT)")
    ax.set_ylabel("overall_score (Claude)")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    _save_fig(PLOTS_DIR / "12_gpt_vs_claude_diagonal.png")


def plot_13_diferenca_notas_distribuicao(df: pd.DataFrame) -> None:
    diff = df["score_difference"].dropna()
    if diff.empty:
        print("  Ignorado 13_diferenca_notas_distribuicao.png: sem dados.")
        return

    mean_diff = diff.mean()
    if mean_diff > 0.05:
        rigor_hint = "GPT tende a ser mais rigoroso (notas menores em média)."
    elif mean_diff < -0.05:
        rigor_hint = "Claude tende a ser mais rigoroso (notas menores em média)."
    else:
        rigor_hint = "Avaliadores com rigor similar em média."

    fig, ax = plt.subplots(figsize=(8, 5))
    bins = min(10, max(4, len(diff)))
    ax.hist(diff, bins=bins, color="#e67e22", edgecolor="#333333", linewidth=0.6, alpha=0.9)
    ax.axvline(0, color="#2c3e50", linestyle="--", linewidth=1.2, label="Diferença zero")
    ax.axvline(mean_diff, color="#c0392b", linestyle="-", linewidth=1.2, label=f"Média = {mean_diff:+.2f}")
    ax.set_title(f"Distribuição: GPT − Claude (overall_score)\n{rigor_hint}")
    ax.set_xlabel("overall_score_gpt − overall_score_claude")
    ax.set_ylabel("Frequência")
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    _save_fig(PLOTS_DIR / "13_diferenca_notas_distribuicao.png")


def plot_14_boxplot_gpt_vs_claude(df: pd.DataFrame) -> None:
    gpt = df["overall_score_gpt"].dropna().tolist()
    claude = df["overall_score_claude"].dropna().tolist()
    if not gpt and not claude:
        print("  Ignorado 14_boxplot_gpt_vs_claude.png: sem dados.")
        return

    fig, ax = plt.subplots(figsize=(6, 5))
    bp = ax.boxplot(
        [gpt, claude],
        tick_labels=["GPT", "Claude"],
        patch_artist=True,
        widths=0.5,
    )
    colors = ["#3498db", "#9b59b6"]
    for patch, color in zip(bp["boxes"], colors):
        patch.set_facecolor(color)
        patch.set_alpha(0.75)
    ax.set_ylim(0, 10)
    ax.set_title("Distribuição de overall_score por avaliador")
    ax.set_ylabel("overall_score")
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    _save_fig(PLOTS_DIR / "14_boxplot_gpt_vs_claude.png")


def plot_15_cobertura_vs_avaliadores(df: pd.DataFrame) -> None:
    work = df[["coverage_percent", "overall_score_gpt", "overall_score_claude"]].copy()
    work["coverage_percent"] = pd.to_numeric(work["coverage_percent"], errors="coerce")
    work = work.dropna(subset=["coverage_percent"])
    if work.empty:
        print("  Ignorado 15_cobertura_vs_avaliadores.png: sem dados de cobertura.")
        return

    fig, ax = plt.subplots(figsize=(8, 6))
    gpt_valid = work.dropna(subset=["overall_score_gpt"])
    claude_valid = work.dropna(subset=["overall_score_claude"])

    if not gpt_valid.empty:
        ax.scatter(
            gpt_valid["coverage_percent"],
            gpt_valid["overall_score_gpt"],
            alpha=0.85,
            s=70,
            c="#3498db",
            label="GPT",
            edgecolors="white",
            linewidths=0.5,
        )
    if not claude_valid.empty:
        ax.scatter(
            claude_valid["coverage_percent"],
            claude_valid["overall_score_claude"],
            alpha=0.85,
            s=70,
            c="#9b59b6",
            label="Claude",
            edgecolors="white",
            linewidths=0.5,
        )

    ax.set_title("Cobertura de código vs. overall_score por avaliador")
    ax.set_xlabel("coverage_percent (%)")
    ax.set_ylabel("overall_score")
    ax.set_ylim(0, 10)
    ax.legend(loc="best")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    _save_fig(PLOTS_DIR / "15_cobertura_vs_avaliadores.png")


def plot_16_avaliador_por_complexidade(df: pd.DataFrame) -> None:
    levels = [lvl for lvl in COMPLEXITY_ORDER if lvl in df["complexity_level"].values]
    if not levels:
        print("  Ignorado 16_avaliador_por_complexidade.png: sem níveis.")
        return

    gpt_means = []
    claude_means = []
    for lvl in levels:
        sub = df[df["complexity_level"] == lvl]
        gpt_means.append(sub["overall_score_gpt"].mean())
        claude_means.append(sub["overall_score_claude"].mean())

    x = np.arange(len(levels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(x - width / 2, gpt_means, width, label="GPT", color="#3498db", edgecolor="#333333", linewidth=0.5)
    ax.bar(x + width / 2, claude_means, width, label="Claude", color="#9b59b6", edgecolor="#333333", linewidth=0.5)
    ax.set_xticks(x)
    ax.set_xticklabels([lvl.capitalize() for lvl in levels])
    ax.set_ylim(0, 10)
    ax.set_title("Média de overall_score por complexidade e avaliador")
    ax.set_xlabel("Nível de complexidade")
    ax.set_ylabel("overall_score (média)")
    ax.legend()
    ax.grid(True, alpha=0.3, axis="y")
    fig.tight_layout()
    _save_fig(PLOTS_DIR / "16_avaliador_por_complexidade.png")


def write_summary(df: pd.DataFrame, output_summary: Path) -> None:
    n = len(df)
    mean_gpt = df["overall_score_gpt"].mean()
    mean_claude = df["overall_score_claude"].mean()
    mean_diff = df["score_difference"].mean()
    corr = df["overall_score_gpt"].corr(df["overall_score_claude"])

    if mean_gpt > mean_claude:
        rigor = "Claude foi mais rigoroso em média (notas menores)."
    elif mean_claude > mean_gpt:
        rigor = "GPT foi mais rigoroso em média (notas menores)."
    else:
        rigor = "GPT e Claude tiveram a mesma média de overall_score."

    lines = [
        "Resumo da comparação GPT vs. Claude",
        "=" * 45,
        f"Total de testes comparados: {n}",
        f"Média overall_score_gpt: {mean_gpt:.2f}",
        f"Média overall_score_claude: {mean_claude:.2f}",
        f"Diferença média (GPT − Claude): {mean_diff:.2f}",
        f"Correlação (overall_score_gpt × overall_score_claude): {corr:.3f}",
        rigor,
        "",
        "Maiores divergências (|diferença|):",
    ]
    top = df.nlargest(5, "abs_score_difference")
    for _, row in top.iterrows():
        lines.append(
            f"  {row['function_name']}: GPT={row['overall_score_gpt']:.1f}, "
            f"Claude={row['overall_score_claude']:.1f}, "
            f"diff={row['score_difference']:+.1f}"
        )

    output_summary.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compara avaliações GPT e Claude.")
    add_dataset_argument(parser)
    return parser.parse_args()


def main() -> None:
    global PLOTS_DIR

    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    input_gpt = cfg.result_csv("avaliacao_gpt_sobre_testes_gpt")
    input_claude = cfg.result_csv("avaliacao_claude_sobre_testes_gpt")
    output_comparison = cfg.result_csv("comparacao_avaliadores_gpt_claude")
    output_summary = cfg.result_txt("resumo_comparacao_avaliadores")
    PLOTS_DIR = cfg.plots_dir

    print(f"Dataset: {cfg.key}")
    print("Comparando avaliadores GPT e Claude...")

    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.labelsize": 12,
            "axes.titlesize": 13,
        }
    )
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    if not input_claude.exists():
        print(f"Erro: arquivo não encontrado: {input_claude}")
        return

    try:
        df_gpt = _load_gpt_eval(input_gpt)
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return

    df_claude = standardize_function_column(pd.read_csv(input_claude))
    print(f"Claude: {input_claude.name} ({len(df_claude)} linhas)")

    comparison = build_comparison(df_gpt, df_claude)
    if comparison.empty:
        print("Erro: merge GPT × Claude retornou vazio. Verifique function_name e test_file.")
        return

    prepare_csv_for_save(comparison).to_csv(output_comparison, index=False, encoding="utf-8")
    print(f"\nComparação salva: {output_comparison} ({len(comparison)} testes)")

    print("\nGráficos:")
    plot_08_scatter_overall(comparison)
    plot_09_media_avaliadores(comparison)
    plot_10_diferenca_por_funcao(comparison)
    plot_11_media_por_complexidade(comparison)
    plot_12_gpt_vs_claude_diagonal(comparison)
    plot_13_diferenca_notas_distribuicao(comparison)
    plot_14_boxplot_gpt_vs_claude(comparison)
    plot_15_cobertura_vs_avaliadores(comparison)
    plot_16_avaliador_por_complexidade(comparison)

    write_summary(comparison, output_summary)
    print(f"Resumo: {output_summary}")
    print("\nConcluído.")


if __name__ == "__main__":
    main()
