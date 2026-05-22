"""
Compara avaliações de testes gerados feitas por GPT e Claude sobre a mesma amostra.
"""

from __future__ import annotations

import unicodedata
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = BASE_DIR / "data" / "results"
PLOTS_DIR = RESULTS_DIR / "plots"

INPUT_GPT = RESULTS_DIR / "evaluation_results.csv"
INPUT_GPT_ALT = RESULTS_DIR / "evaluation_results_gpt.csv"
INPUT_CLAUDE = RESULTS_DIR / "evaluation_results_claude.csv"

OUTPUT_COMPARISON = RESULTS_DIR / "evaluator_comparison.csv"
OUTPUT_SUMMARY = RESULTS_DIR / "evaluator_comparison_summary.txt"

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


def _load_gpt_eval() -> pd.DataFrame:
    for path in (INPUT_GPT, INPUT_GPT_ALT):
        if path.exists():
            print(f"GPT: {path.name}")
            return pd.read_csv(path)
    raise FileNotFoundError(
        f"Nenhum arquivo GPT encontrado ({INPUT_GPT.name} ou {INPUT_GPT_ALT.name})."
    )


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


def write_summary(df: pd.DataFrame) -> None:
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

    OUTPUT_SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    print("Comparando avaliadores GPT e Claude...")

    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.labelsize": 12,
            "axes.titlesize": 13,
        }
    )
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)

    if not INPUT_CLAUDE.exists():
        print(f"Erro: arquivo não encontrado: {INPUT_CLAUDE}")
        return

    try:
        df_gpt = _load_gpt_eval()
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        return

    df_claude = pd.read_csv(INPUT_CLAUDE)
    print(f"Claude: {INPUT_CLAUDE.name} ({len(df_claude)} linhas)")

    comparison = build_comparison(df_gpt, df_claude)
    if comparison.empty:
        print("Erro: merge GPT × Claude retornou vazio. Verifique function_name e test_file.")
        return

    comparison.to_csv(OUTPUT_COMPARISON, index=False, encoding="utf-8")
    print(f"\nComparação salva: {OUTPUT_COMPARISON} ({len(comparison)} testes)")

    print("\nGráficos:")
    plot_08_scatter_overall(comparison)
    plot_09_media_avaliadores(comparison)
    plot_10_diferenca_por_funcao(comparison)
    plot_11_media_por_complexidade(comparison)

    write_summary(comparison)
    print(f"Resumo: {OUTPUT_SUMMARY}")
    print("\nConcluído.")


if __name__ == "__main__":
    main()
