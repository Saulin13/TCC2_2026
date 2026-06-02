"""
Análise estatística e visual avançada do experimento TCC.

Gera:
- data/results/summary_statistics.csv
- data/results/correlation_results.csv
- Gráficos em data/results/graficos/
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

from dataset_config import (
    BASE_DIR,
    RESULTS_DIR,
    add_dataset_argument,
    resolve_dataset,
)

GRAFICOS_DIR = RESULTS_DIR / "graficos"
SUMMARY_CSV = RESULTS_DIR / "summary_statistics.csv"
CORRELATION_CSV = RESULTS_DIR / "correlation_results.csv"

FIG_DPI = 300
FIG_SIZE = (10, 6)
MERGE_KEYS = ("function_name", "test_file")

SUMMARY_COLUMNS = [
    "dataset",
    "test_generator",
    "execution_ok_percent",
    "failed_percent",
    "average_coverage",
    "average_overall_score",
    "average_test_strength",
    "max_overall_score",
    "min_overall_score",
    "n_tests",
]

CORRELATION_PAIRS = (
    ("coverage_percent", "overall_score", "coverage_percent vs overall_score"),
    ("test_strength_score", "overall_score", "test_strength_score vs overall_score"),
    ("overall_score_gpt", "overall_score_claude", "overall_score_gpt vs overall_score_claude"),
)


def _parse_passed(val: object) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in ("true", "1", "yes")


def _is_ok(status: object) -> bool:
    return str(status).strip().lower() == "ok"


def _is_failed(status: object) -> bool:
    s = str(status).strip().lower()
    return s in {"tests_failed", "failed"}


def _load_coverage(cfg, generator: str) -> pd.DataFrame | None:
    path = cfg.result_csv(f"cobertura_testes_gerados_{generator}")
    if not path.exists():
        print(f"Aviso: {path.name} não encontrado.")
        return None
    df = pd.read_csv(path)
    df["test_generator"] = generator.upper()
    df["passed"] = df["passed"].apply(_parse_passed)
    df["coverage_percent"] = pd.to_numeric(df["coverage_percent"], errors="coerce")
    return df


def _overall_for_generator(row: pd.Series, generator: str) -> float:
    if generator.lower() == "gpt":
        cols = ["overall_score_gpt_on_gpt", "overall_score_claude_on_gpt"]
    else:
        cols = ["overall_score_gpt_on_claude", "overall_score_claude_on_claude"]
    values = [pd.to_numeric(row.get(c), errors="coerce") for c in cols if c in row.index]
    valid = [v for v in values if pd.notna(v)]
    return float(np.mean(valid)) if valid else float("nan")


def _build_analysis_frame(cfg) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Monta frames por gerador e frame consolidado para correlações."""
    parts: list[pd.DataFrame] = []
    for gen in ("gpt", "claude"):
        cov = _load_coverage(cfg, gen)
        if cov is None:
            continue
        work = cov.copy()

        final_path = cfg.result_csv("resultados_finais")
        if final_path.exists():
            final = pd.read_csv(final_path)
            score_cols = [c for c in final.columns if c.startswith("overall_score_")]
            if score_cols:
                final_subset = final[["function_name", *score_cols]].drop_duplicates(
                    subset=["function_name"], keep="first"
                )
                work = work.merge(final_subset, on="function_name", how="left")
                work["overall_score"] = work.apply(
                    lambda row: _overall_for_generator(row, gen), axis=1
                )
            else:
                work["overall_score"] = np.nan
        else:
            if gen == "gpt":
                eval_paths = (
                    cfg.result_csv("avaliacao_gpt_sobre_testes_gpt"),
                    cfg.result_csv("avaliacao_claude_sobre_testes_gpt"),
                )
            else:
                eval_paths = (
                    cfg.result_csv("avaliacao_gpt_sobre_testes_claude"),
                    cfg.result_csv("avaliacao_claude_sobre_testes_claude"),
                )

            score_frames: list[pd.Series] = []
            for path in eval_paths:
                if path.exists():
                    ev = pd.read_csv(path)
                    if "overall_score" in ev.columns:
                        score_frames.append(
                            pd.to_numeric(
                                ev.set_index("function_name")["overall_score"],
                                errors="coerce",
                            )
                        )
            if score_frames:
                merged_scores = pd.concat(score_frames, axis=1).mean(axis=1, skipna=True)
                work = work.merge(
                    merged_scores.rename("overall_score"),
                    left_on="function_name",
                    right_index=True,
                    how="left",
                )
            else:
                work["overall_score"] = np.nan

        strength_path = cfg.result_csv("forca_heuristica_testes")
        if strength_path.exists():
            strength = pd.read_csv(strength_path)[["function_name", "test_strength_score"]]
            strength["test_strength_score"] = pd.to_numeric(
                strength["test_strength_score"], errors="coerce"
            )
            work = work.merge(strength.drop_duplicates("function_name"), on="function_name", how="left")
        else:
            work["test_strength_score"] = np.nan

        parts.append(work)

    if not parts:
        return pd.DataFrame(), pd.DataFrame()

    combined = pd.concat(parts, ignore_index=True)
    return combined, combined


def _summary_row(df: pd.DataFrame, *, dataset: str, generator: str) -> dict[str, object]:
    sub = df[df["test_generator"] == generator.upper()].copy()
    n = len(sub)
    if n == 0:
        return {col: "" for col in SUMMARY_COLUMNS}

    ok_count = int(sub["execution_status"].map(_is_ok).sum())
    failed_count = int(sub["execution_status"].map(_is_failed).sum())
    overall = pd.to_numeric(sub.get("overall_score"), errors="coerce")
    strength = pd.to_numeric(sub.get("test_strength_score"), errors="coerce")
    coverage = pd.to_numeric(sub.get("coverage_percent"), errors="coerce")

    return {
        "dataset": dataset,
        "test_generator": generator.upper(),
        "execution_ok_percent": round(ok_count / n * 100, 2),
        "failed_percent": round(failed_count / n * 100, 2),
        "average_coverage": round(coverage.mean(), 2) if coverage.notna().any() else "",
        "average_overall_score": round(overall.mean(), 2) if overall.notna().any() else "",
        "average_test_strength": round(strength.mean(), 2) if strength.notna().any() else "",
        "max_overall_score": round(overall.max(), 2) if overall.notna().any() else "",
        "min_overall_score": round(overall.min(), 2) if overall.notna().any() else "",
        "n_tests": n,
    }


def build_summary_statistics(df: pd.DataFrame, *, dataset: str) -> pd.DataFrame:
    rows = [
        _summary_row(df, dataset=dataset, generator="gpt"),
        _summary_row(df, dataset=dataset, generator="claude"),
    ]
    return pd.DataFrame(rows, columns=SUMMARY_COLUMNS)


def _correlation_row(
    x: pd.Series,
    y: pd.Series,
    *,
    dataset: str,
    label: str,
) -> dict[str, object] | None:
    pair = pd.DataFrame({"x": x, "y": y}).dropna()
    n = len(pair)
    if n < 2:
        return None
    pearson_r, pearson_p = stats.pearsonr(pair["x"], pair["y"])
    spearman_r, spearman_p = stats.spearmanr(pair["x"], pair["y"])
    return {
        "dataset": dataset,
        "comparison": label,
        "variable_x": label.split(" vs ")[0],
        "variable_y": label.split(" vs ")[1],
        "n": n,
        "pearson_r": round(float(pearson_r), 4),
        "pearson_p": round(float(pearson_p), 4),
        "spearman_r": round(float(spearman_r), 4),
        "spearman_p": round(float(spearman_p), 4),
    }


def build_correlation_results(df: pd.DataFrame, *, dataset: str) -> pd.DataFrame:
    rows: list[dict[str, object]] = []

    for x_col, y_col, label in CORRELATION_PAIRS:
        if x_col == "overall_score_gpt" and y_col == "overall_score_claude":
            gpt_eval = df[df["test_generator"] == "GPT"].copy()
            if gpt_eval.empty:
                continue
            x = pd.to_numeric(gpt_eval.get("overall_score_gpt_on_gpt"), errors="coerce")
            y = pd.to_numeric(gpt_eval.get("overall_score_claude_on_gpt"), errors="coerce")
            if x.isna().all() or y.isna().all():
                x = pd.to_numeric(
                    gpt_eval.get("overall_score") if "overall_score" in gpt_eval else x,
                    errors="coerce",
                )
                comp_path = resolve_dataset(dataset).result_csv("comparacao_avaliadores_gpt_claude")
                if comp_path.exists():
                    comp = pd.read_csv(comp_path)
                    comp = comp[comp.get("comparison_group", comp.get("generator", "")) == "gpt_tests"]
                    if comp.empty and "generator" not in comp.columns:
                        comp = pd.read_csv(comp_path).head(len(gpt_eval))
                    if "overall_score_gpt" in comp.columns:
                        x = pd.to_numeric(comp["overall_score_gpt"], errors="coerce")
                        y = pd.to_numeric(comp["overall_score_claude"], errors="coerce")
            row = _correlation_row(x, y, dataset=dataset, label=label)
        else:
            work = df.copy()
            if x_col not in work.columns or y_col not in work.columns:
                continue
            row = _correlation_row(
                pd.to_numeric(work[x_col], errors="coerce"),
                pd.to_numeric(work[y_col], errors="coerce"),
                dataset=dataset,
                label=label,
            )
        if row:
            rows.append(row)

    return pd.DataFrame(rows)


def _save_fig(path: Path, *, title: str, ax: plt.Axes) -> None:
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    fig = ax.figure
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=FIG_DPI, bbox_inches="tight")
    plt.close(fig)
    print(f"  Salvo: {path.relative_to(BASE_DIR).as_posix()}")


def plot_execution_status_grouped(df_gpt: pd.DataFrame, df_claude: pd.DataFrame, out_dir: Path) -> None:
    def counts(df: pd.DataFrame) -> tuple[int, int]:
        ok = int(df["execution_status"].map(_is_ok).sum())
        failed = int(df["execution_status"].map(_is_failed).sum())
        return ok, failed

    ok_gpt, fail_gpt = counts(df_gpt)
    ok_claude, fail_claude = counts(df_claude)

    labels = ["GPT", "Claude"]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ok_bars = ax.bar(x - width / 2, [ok_gpt, ok_claude], width, label="OK", color="#2ecc71", edgecolor="#333")
    fail_bars = ax.bar(
        x + width / 2, [fail_gpt, fail_claude], width, label="FAILED", color="#e74c3c", edgecolor="#333"
    )

    ax.set_xlabel("Modelo gerador de testes", fontsize=12)
    ax.set_ylabel("Quantidade de testes", fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.legend(fontsize=11)
    ax.grid(True, axis="y", alpha=0.3)

    for bars in (ok_bars, fail_bars):
        for bar in bars:
            h = bar.get_height()
            ax.annotate(
                f"{int(h)}",
                xy=(bar.get_x() + bar.get_width() / 2, h),
                ha="center",
                va="bottom",
                fontsize=10,
            )

    ymax = max(ok_gpt, ok_claude, fail_gpt, fail_claude, 1)
    ax.set_ylim(0, ymax * 1.15)
    _save_fig(
        out_dir / "execution_status_gpt_vs_claude.png",
        title="Comparação de status de execução por modelo gerador",
        ax=ax,
    )


def plot_correlation_heatmap(df: pd.DataFrame, out_dir: Path, *, dataset: str) -> None:
    numeric_cols = [
        c
        for c in (
            "coverage_percent",
            "test_strength_score",
            "overall_score",
            "overall_score_gpt_on_gpt",
            "overall_score_claude_on_gpt",
        )
        if c in df.columns
    ]
    if len(numeric_cols) < 2:
        print("  Ignorado heatmap_correlacao.png: colunas insuficientes.")
        return

    work = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    corr = work.corr(method="pearson")

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=35, ha="right", fontsize=10)
    ax.set_yticklabels(corr.index, fontsize=10)
    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=9)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="Coeficiente de Pearson")
    _save_fig(
        out_dir / f"heatmap_correlacao_{dataset}.png",
        title=f"Mapa de calor de correlações ({dataset})",
        ax=ax,
    )


def _scatter_with_trend(
    x: pd.Series,
    y: pd.Series,
    *,
    xlabel: str,
    ylabel: str,
    title: str,
    filename: str,
    out_dir: Path,
    diagonal: bool = False,
) -> None:
    valid = pd.DataFrame({"x": x, "y": y}).dropna()
    if len(valid) < 2:
        print(f"  Ignorado {filename}: poucos pontos válidos.")
        return

    fig, ax = plt.subplots(figsize=FIG_SIZE)
    ax.scatter(valid["x"], valid["y"], alpha=0.8, s=70, c="#2980b9", edgecolors="white", linewidths=0.5)

    slope, intercept, _, _, _ = stats.linregress(valid["x"], valid["y"])
    x_line = np.linspace(valid["x"].min(), valid["x"].max(), 100)
    ax.plot(x_line, slope * x_line + intercept, color="#c0392b", linewidth=2, label="Tendência linear")

    if diagonal:
        lo = min(valid["x"].min(), valid["y"].min(), 0)
        hi = max(valid["x"].max(), valid["y"].max(), 10)
        ax.plot([lo, hi], [lo, hi], "--", color="#7f8c8d", linewidth=1.5, label="y = x")
        ax.set_xlim(lo - 0.5, hi + 0.5)
        ax.set_ylim(lo - 0.5, hi + 0.5)
        ax.set_aspect("equal", adjustable="box")

    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    _save_fig(out_dir / filename, title=title, ax=ax)


def generate_plots(df: pd.DataFrame, df_gpt: pd.DataFrame, df_claude: pd.DataFrame, out_dir: Path, *, dataset: str) -> None:
    out_dir = out_dir / dataset
    out_dir.mkdir(parents=True, exist_ok=True)

    print("\nGráficos estatísticos:")
    if not df_gpt.empty and not df_claude.empty:
        plot_execution_status_grouped(df_gpt, df_claude, out_dir)

    _scatter_with_trend(
        pd.to_numeric(df["coverage_percent"], errors="coerce"),
        pd.to_numeric(df["overall_score"], errors="coerce"),
        xlabel="Cobertura de código (%)",
        ylabel="Overall score (LLM)",
        title="Relação entre cobertura e qualidade avaliada pelos LLMs",
        filename="scatter_coverage_vs_overall_score.png",
        out_dir=out_dir,
    )

    _scatter_with_trend(
        pd.to_numeric(df["test_strength_score"], errors="coerce"),
        pd.to_numeric(df["overall_score"], errors="coerce"),
        xlabel="Test strength score",
        ylabel="Overall score (LLM)",
        title="Relação entre robustez heurística e qualidade avaliada pelos LLMs",
        filename="scatter_test_strength_vs_overall_score.png",
        out_dir=out_dir,
    )

    gpt_tests = df_gpt.copy()
    x_gpt = pd.to_numeric(gpt_tests.get("overall_score_gpt_on_gpt"), errors="coerce")
    y_claude = pd.to_numeric(gpt_tests.get("overall_score_claude_on_gpt"), errors="coerce")
    if x_gpt.isna().all() or y_claude.isna().all():
        comp_path = resolve_dataset(dataset).result_csv("comparacao_avaliadores_gpt_claude")
        if comp_path.exists():
            comp = pd.read_csv(comp_path)
            mask = comp.get("comparison_group", comp.get("generator", pd.Series())) == "gpt_tests"
            if mask.any():
                sub = comp[mask]
            else:
                sub = comp.iloc[: len(gpt_tests)]
            x_gpt = pd.to_numeric(sub.get("overall_score_gpt"), errors="coerce")
            y_claude = pd.to_numeric(sub.get("overall_score_claude"), errors="coerce")

    _scatter_with_trend(
        x_gpt,
        y_claude,
        xlabel="Overall score (avaliador GPT)",
        ylabel="Overall score (avaliador Claude)",
        title="Concordância entre avaliadores GPT e Claude (testes gerados por GPT)",
        filename="scatter_gpt_vs_claude_overall_score.png",
        out_dir=out_dir,
        diagonal=True,
    )

    plot_correlation_heatmap(df, out_dir, dataset=dataset)


def _append_or_write_csv(path: Path, df: pd.DataFrame, *, dedup_cols: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        existing = pd.read_csv(path)
        combined = pd.concat([existing, df], ignore_index=True)
        subset = [c for c in dedup_cols if c in combined.columns]
        if subset:
            combined = combined.drop_duplicates(subset=subset, keep="last")
        combined.to_csv(path, index=False, encoding="utf-8")
    else:
        df.to_csv(path, index=False, encoding="utf-8")


def run_for_dataset(dataset_key: str) -> None:
    cfg = resolve_dataset(dataset_key)
    print(f"\nDataset: {cfg.key}")

    df, _ = _build_analysis_frame(cfg)
    if df.empty:
        print("Sem dados para análise estatística.")
        return

    df_gpt = df[df["test_generator"] == "GPT"].copy()
    df_claude = df[df["test_generator"] == "CLAUDE"].copy()

    summary = build_summary_statistics(df, dataset=cfg.key)
    correlations = build_correlation_results(df, dataset=cfg.key)

    _append_or_write_csv(SUMMARY_CSV, summary, dedup_cols=["dataset", "test_generator"])
    _append_or_write_csv(CORRELATION_CSV, correlations, dedup_cols=["dataset", "comparison"])

    print(f"Resumo: {SUMMARY_CSV}")
    print(f"Correlações: {CORRELATION_CSV}")

    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.labelsize": 12,
            "axes.titlesize": 13,
            "figure.dpi": FIG_DPI,
        }
    )
    generate_plots(df, df_gpt, df_claude, GRAFICOS_DIR, dataset=cfg.key)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Análise estatística e gráficos avançados.")
    add_dataset_argument(parser)
    parser.add_argument(
        "--all-datasets",
        action="store_true",
        help="Processa thealgorithms e real em sequência.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    datasets = ["thealgorithms", "real"] if args.all_datasets else [args.dataset]
    for ds in datasets:
        run_for_dataset(ds)
    print(f"\nConcluído. Gráficos em: {GRAFICOS_DIR}")


if __name__ == "__main__":
    main()
