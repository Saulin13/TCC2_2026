"""
Gera gráficos finais do piloto e resumo de métricas.
Usa test_strength_score como métrica heurística complementar (não mutation testing).
"""

from __future__ import annotations

import unicodedata
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_COVERAGE = BASE_DIR / "data" / "results" / "coverage_results.csv"
INPUT_EVAL = BASE_DIR / "data" / "results" / "evaluation_results.csv"
INPUT_STRENGTH = BASE_DIR / "data" / "results" / "test_strength_results.csv"
OUTPUT_DIR = BASE_DIR / "data" / "results" / "plots"

COMPLEXITY_ORDER = ("baixa", "media", "alta")
STATUS_ORDER = ("ok", "tests_failed", "pytest_error", "timeout")
FIG_DPI = 150
MERGE_KEYS = ("function_name", "test_file")


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


def _prepare_coverage(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["complexity_level"] = out["complexity_level"].apply(normalize_complexity_level)
    out["passed"] = out["passed"].apply(_parse_passed)
    out["coverage_percent"] = pd.to_numeric(out["coverage_percent"], errors="coerce")
    return out


def _save_fig(path: Path) -> None:
    plt.savefig(path, dpi=FIG_DPI, bbox_inches="tight")
    plt.close()
    print(f"  Salvo: {path.name}")


def _status_colors(labels: list[str]) -> list[str]:
    palette = {
        "ok": "#2ecc71",
        "tests_failed": "#e74c3c",
        "pytest_error": "#f39c12",
        "timeout": "#9b59b6",
    }
    return [palette.get(lbl, "#95a5a6") for lbl in labels]


def plot_01_execucao_por_status(df_cov: pd.DataFrame) -> None:
    counts = df_cov["execution_status"].value_counts()
    known = [s for s in STATUS_ORDER if s in counts.index]
    others = [s for s in counts.index if s not in STATUS_ORDER]
    order = known + sorted(others)
    values = [int(counts[s]) for s in order]
    colors = _status_colors(order)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(order, values, color=colors, edgecolor="#333333", linewidth=0.6)
    ax.set_title("Quantidade de testes por status de execução (piloto)")
    ax.set_xlabel("execution_status")
    ax.set_ylabel("Quantidade de testes")
    ax.tick_params(axis="x", rotation=25)
    total = sum(values) or 1
    for bar, val in zip(bars, values):
        ax.annotate(
            f"{val}\n({val / total * 100:.1f}%)",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.set_ylim(0, max(values) * 1.2 if values else 1)
    fig.tight_layout()
    _save_fig(OUTPUT_DIR / "01_execucao_por_status.png")


def plot_02_cobertura_media_por_complexidade(df_cov: pd.DataFrame) -> None:
    means = (
        df_cov.groupby("complexity_level", observed=True)["coverage_percent"]
        .mean()
        .reindex(COMPLEXITY_ORDER)
        .dropna()
    )
    labels = list(means.index)
    values = means.values

    fig, ax = plt.subplots(figsize=(7, 5))
    bars = ax.bar(labels, values, color=["#3498db", "#9b59b6", "#e67e22"][: len(labels)])
    ax.set_title("Cobertura média por nível de complexidade")
    ax.set_xlabel("complexity_level")
    ax.set_ylabel("coverage_percent (média, %)")
    ax.set_ylim(0, 100)
    for bar, val in zip(bars, values):
        ax.annotate(f"{val:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, val), ha="center", va="bottom")
    fig.tight_layout()
    _save_fig(OUTPUT_DIR / "02_cobertura_media_por_complexidade.png")


def _boxplot_by_complexity(
    df: pd.DataFrame,
    value_col: str,
    title: str,
    ylabel: str,
    filename: str,
) -> None:
    data = []
    labels = []
    for level in COMPLEXITY_ORDER:
        subset = df.loc[df["complexity_level"] == level, value_col].dropna()
        if len(subset) > 0:
            data.append(subset.values)
            labels.append(level)
    if not data:
        print(f"  Ignorado {filename}: sem dados.")
        return

    fig, ax = plt.subplots(figsize=(7, 5))
    bp = ax.boxplot(data, tick_labels=labels, patch_artist=True)
    colors = ["#3498db", "#9b59b6", "#e67e22"]
    for patch, color in zip(bp["boxes"], colors[: len(bp["boxes"])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)
    ax.set_title(title)
    ax.set_xlabel("complexity_level")
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    _save_fig(OUTPUT_DIR / filename)


def plot_03_nota_llm_por_complexidade(df_eval: pd.DataFrame) -> None:
    df = df_eval.copy()
    df["complexity_level"] = df["complexity_level"].apply(normalize_complexity_level)
    df["overall_score"] = pd.to_numeric(df["overall_score"], errors="coerce")
    _boxplot_by_complexity(
        df,
        "overall_score",
        "Nota geral da LLM (overall_score) por complexidade",
        "overall_score",
        "03_nota_llm_por_complexidade.png",
    )


def _scatter_with_trend(
    x: pd.Series,
    y: pd.Series,
    *,
    title: str,
    xlabel: str,
    ylabel: str,
    filename: str,
    color_by: pd.Series | None = None,
) -> None:
    valid = pd.DataFrame({"x": x, "y": y}).dropna()
    if valid.empty:
        print(f"  Ignorado {filename}: sem pares válidos.")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    if color_by is not None:
        colors = color_by.reindex(valid.index).map(
            {"ok": "#2ecc71", "tests_failed": "#e74c3c", "pytest_error": "#f39c12"}
        ).fillna("#7f8c8d")
        ax.scatter(valid["x"], valid["y"], c=colors, alpha=0.85, s=70, edgecolors="white", linewidths=0.5)
    else:
        ax.scatter(valid["x"], valid["y"], alpha=0.85, s=70, c="#2980b9", edgecolors="white", linewidths=0.5)

    if len(valid) >= 2:
        coef = np.polyfit(valid["x"], valid["y"], 1)
        poly = np.poly1d(coef)
        x_line = np.linspace(valid["x"].min(), valid["x"].max(), 50)
        ax.plot(x_line, poly(x_line), "--", color="#c0392b", linewidth=1.5, label="Tendência (regressão linear)")
        ax.legend(loc="best", fontsize=9)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    _save_fig(OUTPUT_DIR / filename)


def plot_04_cobertura_vs_nota_llm(df_eval: pd.DataFrame) -> None:
    df = df_eval.copy()
    df["coverage_percent"] = pd.to_numeric(df["coverage_percent"], errors="coerce")
    df["overall_score"] = pd.to_numeric(df["overall_score"], errors="coerce")
    _scatter_with_trend(
        df["coverage_percent"],
        df["overall_score"],
        title="Cobertura vs. qualidade avaliada pela LLM",
        xlabel="coverage_percent (%)",
        ylabel="overall_score (LLM)",
        filename="04_cobertura_vs_nota_llm.png",
        color_by=df.get("execution_status"),
    )


def plot_05_test_strength_por_complexidade(df_str: pd.DataFrame) -> None:
    df = df_str.copy()
    df["complexity_level"] = df["complexity_level"].apply(normalize_complexity_level)
    df["test_strength_score"] = pd.to_numeric(df["test_strength_score"], errors="coerce")
    _boxplot_by_complexity(
        df,
        "test_strength_score",
        "test_strength_score (heurístico) por complexidade",
        "test_strength_score (0–10)",
        "05_test_strength_por_complexidade.png",
    )


def plot_06_test_strength_vs_coverage(df_str: pd.DataFrame) -> None:
    df = df_str.copy()
    df["coverage_percent"] = pd.to_numeric(df["coverage_percent"], errors="coerce")
    df["test_strength_score"] = pd.to_numeric(df["test_strength_score"], errors="coerce")
    _scatter_with_trend(
        df["coverage_percent"],
        df["test_strength_score"],
        title="Cobertura vs. test_strength_score (métrica heurística)",
        xlabel="coverage_percent (%)",
        ylabel="test_strength_score",
        filename="06_test_strength_vs_coverage.png",
    )


def _enrich_strength_with_test_file(df_str: pd.DataFrame, df_cov: pd.DataFrame) -> pd.DataFrame:
    """test_strength_results não traz test_file; obtém de coverage_results."""
    keys = ["function_name", "test_file"]
    lookup = df_cov[keys].drop_duplicates(subset=["function_name"])
    if "test_file" in df_str.columns:
        return df_str
    return df_str.merge(lookup, on="function_name", how="left")


def plot_07_test_strength_vs_llm_score(
    df_str: pd.DataFrame,
    df_eval: pd.DataFrame,
    df_cov: pd.DataFrame,
) -> None:
    enriched = _enrich_strength_with_test_file(df_str, df_cov)
    missing_file = enriched["test_file"].isna().sum()
    if missing_file:
        print(f"  Aviso: {missing_file} registro(s) sem test_file para o gráfico 07.")

    left = enriched[list(MERGE_KEYS) + ["test_strength_score"]].copy()
    right = df_eval[list(MERGE_KEYS) + ["overall_score"]].copy()
    left["test_strength_score"] = pd.to_numeric(left["test_strength_score"], errors="coerce")
    right["overall_score"] = pd.to_numeric(right["overall_score"], errors="coerce")

    merged = left.merge(right, on=list(MERGE_KEYS), how="inner")
    if merged.empty:
        print("  Ignorado 07_test_strength_vs_llm_score.png: merge vazio.")
        return

    _scatter_with_trend(
        merged["test_strength_score"],
        merged["overall_score"],
        title="test_strength_score (heurístico) vs. overall_score (LLM)",
        xlabel="test_strength_score",
        ylabel="overall_score (LLM)",
        filename="07_test_strength_vs_llm_score.png",
    )


def build_summary_metrics(
    df_cov: pd.DataFrame,
    df_eval: pd.DataFrame | None,
    df_str: pd.DataFrame | None,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    n = len(df_cov)
    passed_count = int(df_cov["passed"].sum())
    rows.append({"metric": "total_testes", "value": n})
    rows.append({"metric": "taxa_sucesso_geral", "value": round(passed_count / n, 4) if n else 0})
    rows.append(
        {
            "metric": "media_cobertura_geral",
            "value": round(df_cov["coverage_percent"].mean(), 4),
        }
    )

    if df_str is not None and not df_str.empty:
        rows.append(
            {
                "metric": "media_test_strength_score",
                "value": round(pd.to_numeric(df_str["test_strength_score"], errors="coerce").mean(), 4),
            }
        )

    if df_eval is not None and not df_eval.empty:
        overall = pd.to_numeric(df_eval["overall_score"], errors="coerce")
        rows.append({"metric": "media_overall_score_llm", "value": round(overall.mean(), 4)})

    for status, count in df_cov["execution_status"].value_counts().items():
        rows.append({"metric": f"status_{status}", "value": int(count)})

    for level in COMPLEXITY_ORDER:
        sub = df_cov[df_cov["complexity_level"] == level]
        if sub.empty:
            continue
        rows.append(
            {
                "metric": f"media_cobertura_{level}",
                "value": round(sub["coverage_percent"].mean(), 4),
            }
        )

    if df_str is not None and not df_str.empty:
        df_s = df_str.copy()
        df_s["complexity_level"] = df_s["complexity_level"].apply(normalize_complexity_level)
        df_s["test_strength_score"] = pd.to_numeric(df_s["test_strength_score"], errors="coerce")
        for level in COMPLEXITY_ORDER:
            sub = df_s[df_s["complexity_level"] == level]
            if sub.empty:
                continue
            rows.append(
                {
                    "metric": f"media_test_strength_{level}",
                    "value": round(sub["test_strength_score"].mean(), 4),
                }
            )

    if df_eval is not None and not df_eval.empty:
        df_e = df_eval.copy()
        df_e["complexity_level"] = df_e["complexity_level"].apply(normalize_complexity_level)
        df_e["overall_score"] = pd.to_numeric(df_e["overall_score"], errors="coerce")
        for level in COMPLEXITY_ORDER:
            sub = df_e[df_e["complexity_level"] == level]
            if sub.empty:
                continue
            rows.append(
                {
                    "metric": f"media_overall_score_{level}",
                    "value": round(sub["overall_score"].mean(), 4),
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    print("Gerando gráficos finais do piloto...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.labelsize": 12,
            "axes.titlesize": 13,
            "figure.titlesize": 14,
        }
    )

    if not INPUT_COVERAGE.exists():
        print(f"Erro: arquivo obrigatório não encontrado: {INPUT_COVERAGE}")
        return

    df_cov = _prepare_coverage(pd.read_csv(INPUT_COVERAGE))

    df_eval: pd.DataFrame | None = None
    if INPUT_EVAL.exists():
        df_eval = pd.read_csv(INPUT_EVAL)
        df_eval["complexity_level"] = df_eval["complexity_level"].apply(normalize_complexity_level)
        print(f"Avaliação LLM carregada: {len(df_eval)} registros.")
    else:
        print(f"Aviso: {INPUT_EVAL.name} não encontrado — gráficos 03, 04 e 07 serão omitidos.")

    df_str: pd.DataFrame | None = None
    if INPUT_STRENGTH.exists():
        df_str = pd.read_csv(INPUT_STRENGTH)
        df_str["complexity_level"] = df_str["complexity_level"].apply(normalize_complexity_level)
        print(f"test_strength_results carregado: {len(df_str)} registros.")
    else:
        print(f"Aviso: {INPUT_STRENGTH.name} não encontrado — gráficos 05, 06 e 07 serão omitidos.")

    print("\nGráficos:")
    plot_01_execucao_por_status(df_cov)
    plot_02_cobertura_media_por_complexidade(df_cov)

    if df_eval is not None:
        plot_03_nota_llm_por_complexidade(df_eval)
        plot_04_cobertura_vs_nota_llm(df_eval)
    if df_str is not None:
        plot_05_test_strength_por_complexidade(df_str)
        plot_06_test_strength_vs_coverage(df_str)
    if df_str is not None and df_eval is not None:
        plot_07_test_strength_vs_llm_score(df_str, df_eval, df_cov)

    summary = build_summary_metrics(df_cov, df_eval, df_str)
    summary_path = OUTPUT_DIR / "summary_metrics.csv"
    summary.to_csv(summary_path, index=False, encoding="utf-8")
    print(f"\nResumo salvo: {summary_path}")
    print(f"\nConcluído. Gráficos em: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
