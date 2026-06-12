"""
Gera gráficos finais do piloto e resumo de métricas.
test_strength_score é derivado de mutation testing (mutation_score_percent / 10).
"""

from __future__ import annotations

import argparse
import shutil
import unicodedata
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from dataset_config import add_dataset_argument, resolve_dataset

OUTPUT_DIR = Path(".")

COMPLEXITY_ORDER = ("baixa", "media", "alta")
STATUS_ORDER = ("ok", "tests_failed", "pytest_error", "timeout")
FIG_DPI = 150
INSPECTION_DIR_NAME = "inspecao"
CROSS_EVAL_DIR_NAME = "cross_evaluation"
PRESENTATION_PLOT_NAMES: tuple[str, ...] = (
    "01_execucao_por_status.png",
    "02_cobertura_media_por_complexidade.png",
    "05_test_strength_por_complexidade.png",
    "05b_distribuicao_mutation_score.png",
)
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


def _is_execution_ok(status: object) -> bool:
    return str(status).strip().lower() == "ok"


def _is_execution_failed(status: object) -> bool:
    return not _is_execution_ok(status)


def _load_coverage_frames(df_cov: pd.DataFrame, *, cfg) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {"GPT": df_cov}
    claude_path = cfg.result_csv("cobertura_testes_gerados_claude")
    if claude_path.exists():
        frames["Claude"] = _prepare_coverage(pd.read_csv(claude_path))
    return frames


def _normalize_generator_label(value: object) -> str:
    text = str(value).strip().lower()
    if text == "claude":
        return "Claude"
    return "GPT"


def _prepare_mutation_strength_df(df_str: pd.DataFrame) -> pd.DataFrame:
    """Prepara mutation_score_percent e flags de status (ok/failed) para os gráficos 05."""
    df = df_str.copy()
    df["complexity_level"] = df["complexity_level"].apply(normalize_complexity_level)

    if "mutation_score_percent" in df.columns:
        df["mutation_score_percent"] = pd.to_numeric(df["mutation_score_percent"], errors="coerce")
    else:
        df["mutation_score_percent"] = pd.NA

    missing_score = df["mutation_score_percent"].isna()
    if missing_score.any() and "test_strength_score" in df.columns:
        derived = pd.to_numeric(df.loc[missing_score, "test_strength_score"], errors="coerce") * 10.0
        df.loc[missing_score, "mutation_score_percent"] = derived

    if "mutation_status" in df.columns:
        df["mutation_status"] = df["mutation_status"].astype(str).str.strip().str.lower()
    else:
        df["mutation_status"] = "ok"

    failed_mask = df["mutation_status"] == "failed"
    df.loc[failed_mask, "mutation_score_percent"] = 0.0
    df["mutation_failed"] = failed_mask

    if "generator" in df.columns:
        df["generator"] = df["generator"].map(_normalize_generator_label)
    else:
        df["generator"] = "GPT"

    return df.dropna(subset=["mutation_score_percent"])


def _load_strength_frames(df_str: pd.DataFrame | None, *, cfg) -> pd.DataFrame:
    if df_str is None or df_str.empty:
        return pd.DataFrame(
            columns=[
                "complexity_level",
                "mutation_score_percent",
                "generator",
                "mutation_status",
                "mutation_failed",
            ]
        )
    return _prepare_mutation_strength_df(df_str)


def plot_01_execucao_por_status(df_cov: pd.DataFrame, *, cfg=None) -> None:
    """Barras agrupadas GPT vs Claude (OK e FAILED), com fallback para um único gerador."""
    if cfg is None:
        frames = {"GPT": df_cov}
    else:
        frames = _load_coverage_frames(df_cov, cfg=cfg)

    if len(frames) > 1:
        labels = list(frames.keys())
        x = np.arange(len(labels))
        width = 0.35
        ok_vals = [int(frames[l]["execution_status"].map(_is_execution_ok).sum()) for l in labels]
        fail_vals = [int(frames[l]["execution_status"].map(_is_execution_failed).sum()) for l in labels]

        fig, ax = plt.subplots(figsize=(8, 5))
        ok_bars = ax.bar(x - width / 2, ok_vals, width, label="OK", color="#2ecc71", edgecolor="#333333", linewidth=0.6)
        fail_bars = ax.bar(
            x + width / 2, fail_vals, width, label="FAILED", color="#e74c3c", edgecolor="#333333", linewidth=0.6
        )
        ax.set_xlabel("Modelo gerador")
        ax.set_ylabel("Quantidade de testes")
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()
        for bars in (ok_bars, fail_bars):
            for bar in bars:
                h = bar.get_height()
                ax.annotate(f"{int(h)}", xy=(bar.get_x() + bar.get_width() / 2, h), ha="center", va="bottom", fontsize=9)
        ymax = max(ok_vals + fail_vals + [1])
        ax.set_ylim(0, ymax * 1.15)
        fig.tight_layout()
        _save_fig(OUTPUT_DIR / "01_execucao_por_status.png")
        return

    counts = df_cov["execution_status"].value_counts()
    known = [s for s in STATUS_ORDER if s in counts.index]
    others = [s for s in counts.index if s not in STATUS_ORDER]
    order = known + sorted(others)
    values = [int(counts[s]) for s in order]
    colors = _status_colors(order)

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(order, values, color=colors, edgecolor="#333333", linewidth=0.6)
    ax.set_xlabel("execution_status")
    ax.set_ylabel("Quantidade de testes")
    ax.tick_params(axis="x", rotation=25)
    for bar, val in zip(bars, values):
        ax.annotate(
            f"{val}",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha="center",
            va="bottom",
            fontsize=9,
        )
    ax.set_ylim(0, max(values) * 1.2 if values else 1)
    fig.tight_layout()
    _save_fig(OUTPUT_DIR / "01_execucao_por_status.png")


def plot_02_cobertura_media_por_complexidade(df_cov: pd.DataFrame, *, cfg=None) -> None:
    if cfg is None:
        frames = {"GPT": df_cov}
    else:
        frames = _load_coverage_frames(df_cov, cfg=cfg)

    levels = [lvl for lvl in COMPLEXITY_ORDER if any(lvl in f["complexity_level"].values for f in frames.values())]
    if not levels:
        print("  Ignorado 02_cobertura_media_por_complexidade.png: sem níveis.")
        return

    generators = list(frames.keys())
    x = np.arange(len(levels))
    width = 0.35 if len(generators) > 1 else 0.6
    colors = {"GPT": "#3498db", "Claude": "#e67e22"}
    offset_map = {"GPT": -width / 2, "Claude": width / 2} if len(generators) > 1 else {"GPT": 0.0}

    fig, ax = plt.subplots(figsize=(8, 5))
    all_values: list[float] = []
    for gen in generators:
        means = (
            frames[gen]
            .groupby("complexity_level", observed=True)["coverage_percent"]
            .mean()
            .reindex(levels)
        )
        offsets = x + offset_map.get(gen, 0.0)
        bars = ax.bar(
            offsets,
            means.values,
            width,
            label=gen,
            color=colors.get(gen, "#95a5a6"),
            edgecolor="#333333",
            linewidth=0.6,
        )
        for bar, val in zip(bars, means.values):
            if pd.notna(val):
                all_values.append(float(val))
                ax.annotate(f"{val:.1f}%", xy=(bar.get_x() + bar.get_width() / 2, val), ha="center", va="bottom")

    ax.set_xlabel("complexity_level")
    ax.set_ylabel("coverage_percent (média, %)")
    ax.set_xticks(x)
    ax.set_xticklabels(levels)
    ax.set_ylim(0, 100)
    if len(generators) > 1:
        ax.legend()
    fig.tight_layout()
    _save_fig(OUTPUT_DIR / "02_cobertura_media_por_complexidade.png")


def plot_03_nota_llm_por_complexidade(df_eval: pd.DataFrame) -> None:
    df = df_eval.copy()
    df["complexity_level"] = df["complexity_level"].apply(normalize_complexity_level)
    df["overall_score"] = pd.to_numeric(df["overall_score"], errors="coerce")
    data = []
    labels = []
    for level in COMPLEXITY_ORDER:
        subset = df.loc[df["complexity_level"] == level, "overall_score"].dropna()
        if len(subset) > 0:
            data.append(subset.values)
            labels.append(level)
    if not data:
        print("  Ignorado 03_nota_llm_por_complexidade.png: sem dados.")
        return

    fig, ax = plt.subplots(figsize=(7, 5))
    bp = ax.boxplot(data, tick_labels=labels, patch_artist=True)
    colors = ["#3498db", "#9b59b6", "#e67e22"]
    for patch, color in zip(bp["boxes"], colors[: len(bp["boxes"])]):
        patch.set_facecolor(color)
        patch.set_alpha(0.65)
    ax.set_xlabel("complexity_level")
    ax.set_ylabel("overall_score")
    fig.tight_layout()
    _save_fig(OUTPUT_DIR / "03_nota_llm_por_complexidade.png")


def _scatter_with_trend(
    x: pd.Series,
    y: pd.Series,
    *,
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
        xlabel="coverage_percent (%)",
        ylabel="overall_score (LLM)",
        filename="04_cobertura_vs_nota_llm.png",
        color_by=df.get("execution_status"),
    )


def _barplot_mutation_score_mean_by_complexity(df: pd.DataFrame, *, filename: str) -> None:
    levels = [lvl for lvl in COMPLEXITY_ORDER if lvl in df["complexity_level"].values]
    generators = [g for g in ("GPT", "Claude") if g in df["generator"].values]
    if not levels or not generators:
        print(f"  Ignorado {filename}: sem dados.")
        return

    x = np.arange(len(levels))
    width = 0.35 if len(generators) > 1 else 0.6
    colors = {"GPT": "#3498db", "Claude": "#e67e22"}
    offset_map = {"GPT": -width / 2, "Claude": width / 2} if len(generators) > 1 else {"GPT": 0.0}

    fig, ax = plt.subplots(figsize=(8, 5))
    for gen in generators:
        means = (
            df.loc[df["generator"] == gen]
            .groupby("complexity_level", observed=True)["mutation_score_percent"]
            .mean()
            .reindex(levels)
        )
        offsets = x + offset_map.get(gen, 0.0)
        bars = ax.bar(
            offsets,
            means.values,
            width,
            label=gen,
            color=colors.get(gen, "#95a5a6"),
            edgecolor="#333333",
            linewidth=0.6,
        )
        for bar, val in zip(bars, means.values):
            if pd.notna(val):
                ax.annotate(
                    f"{val:.1f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, val),
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

    ax.set_xlabel("complexity_level")
    ax.set_ylabel("Mutation Score Médio (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(levels)
    ax.set_ylim(0, 100)
    if len(generators) > 1:
        ax.legend()
    fig.tight_layout()
    _save_fig(OUTPUT_DIR / filename)


def _stripplot_mutation_score_distribution(df: pd.DataFrame, *, filename: str) -> None:
    levels = [lvl for lvl in COMPLEXITY_ORDER if lvl in df["complexity_level"].values]
    generators = [g for g in ("GPT", "Claude") if g in df["generator"].values]
    if not levels or not generators:
        print(f"  Ignorado {filename}: sem dados.")
        return

    colors = {"GPT": "#3498db", "Claude": "#e67e22"}
    offsets = {"GPT": -0.18, "Claude": 0.18} if len(generators) > 1 else {"GPT": 0.0}
    rng = np.random.default_rng(42)

    fig, ax = plt.subplots(figsize=(9, 5))
    for gen in generators:
        for idx, level in enumerate(levels):
            subset = df.loc[
                (df["generator"] == gen) & (df["complexity_level"] == level),
                "mutation_score_percent",
            ].dropna()
            if subset.empty:
                continue
            jitter = rng.uniform(-0.10, 0.10, len(subset))
            x_vals = idx + offsets.get(gen, 0.0) + jitter
            ax.scatter(
                x_vals,
                subset.values,
                s=70,
                alpha=0.85,
                c=colors.get(gen, "#95a5a6"),
                edgecolors="white",
                linewidths=0.5,
                label=gen if idx == 0 else None,
            )

    ax.set_xticks(np.arange(len(levels)))
    ax.set_xticklabels(levels)
    ax.set_xlabel("complexity_level")
    ax.set_ylabel("mutation_score_percent (%)")
    ax.set_ylim(0, 100)
    ax.legend(title="Gerador", loc="best")
    fig.tight_layout()
    _save_fig(OUTPUT_DIR / filename)


def _boxplot_mutation_score_by_complexity(df: pd.DataFrame, *, filename: str) -> None:
    levels = [lvl for lvl in COMPLEXITY_ORDER if lvl in df["complexity_level"].values]
    generators = [g for g in ("GPT", "Claude") if g in df["generator"].values]
    if not levels or not generators:
        print(f"  Ignorado {filename}: sem dados.")
        return

    colors = {"GPT": "#3498db", "Claude": "#e67e22"}
    offsets = {"GPT": -0.2, "Claude": 0.2} if len(generators) > 1 else {"GPT": 0.0}
    fig, ax = plt.subplots(figsize=(8, 5))
    legend_handles: list[plt.Rectangle] = []

    for gen in generators:
        box_data: list[np.ndarray] = []
        positions: list[float] = []
        for idx, level in enumerate(levels):
            subset = df.loc[
                (df["complexity_level"] == level) & (df["generator"] == gen),
                "mutation_score_percent",
            ].dropna()
            if len(subset) > 0:
                box_data.append(subset.values)
                positions.append(idx + offsets.get(gen, 0.0))
        if not box_data:
            continue
        bp = ax.boxplot(box_data, positions=positions, widths=0.35, patch_artist=True, manage_ticks=False)
        color = colors.get(gen, "#95a5a6")
        for patch in bp["boxes"]:
            patch.set_facecolor(color)
            patch.set_alpha(0.65)
        legend_handles.append(plt.Rectangle((0, 0), 1, 1, fc=color, alpha=0.65, ec="#333333"))

        for idx, level in enumerate(levels):
            failed_subset = df.loc[
                (df["complexity_level"] == level)
                & (df["generator"] == gen)
                & (df["mutation_failed"]),
                "mutation_score_percent",
            ]
            if failed_subset.empty:
                continue
            ax.scatter(
                [idx + offsets.get(gen, 0.0)] * len(failed_subset),
                failed_subset.values,
                marker="x",
                c="#c0392b",
                s=36,
                zorder=3,
            )

    ax.set_xticks(np.arange(len(levels)))
    ax.set_xticklabels(levels)
    ax.set_xlabel("complexity_level")
    ax.set_ylabel("mutation_score_percent (%)")
    ax.set_ylim(0, 100)
    failed_handle = plt.Line2D(
        [0],
        [0],
        marker="x",
        color="#c0392b",
        linestyle="",
        markersize=7,
        label="mutation_status=failed",
    )
    ax.legend(legend_handles + [failed_handle], [*generators, "mutation_status=failed"], loc="best")
    fig.tight_layout()
    _save_fig(OUTPUT_DIR / filename)


def plot_05_test_strength_por_complexidade(df_str: pd.DataFrame) -> None:
    df = _prepare_mutation_strength_df(df_str)
    _barplot_mutation_score_mean_by_complexity(
        df,
        filename="05_test_strength_por_complexidade.png",
    )
    _stripplot_mutation_score_distribution(
        df,
        filename="05b_distribuicao_mutation_score.png",
    )


def plot_05_test_strength_inspection(df_str: pd.DataFrame) -> None:
    """Gráficos secundários de mutation testing (inspeção, fora do núcleo principal)."""
    global OUTPUT_DIR
    df = _prepare_mutation_strength_df(df_str)
    inspection_dir = OUTPUT_DIR / INSPECTION_DIR_NAME
    inspection_dir.mkdir(parents=True, exist_ok=True)
    previous = OUTPUT_DIR
    OUTPUT_DIR = inspection_dir
    try:
        _boxplot_mutation_score_by_complexity(
            df,
            filename="05_test_strength_por_complexidade_boxplot.png",
        )
    finally:
        OUTPUT_DIR = previous


def write_mutation_strength_summary_txt(df_str: pd.DataFrame, output_path: Path) -> None:
    df = _prepare_mutation_strength_df(df_str)
    failed_count = int(df["mutation_failed"].sum())
    ok_count = int((~df["mutation_failed"]).sum())

    lines = [
        "Resumo do mutation_score_percent (gráficos)",
        "=" * 48,
        f"Total de registros: {len(df)}",
        f"mutation_status ok: {ok_count}",
        f"mutation_status failed: {failed_count}",
        "",
        "Média de mutation_score_percent por modelo gerador:",
    ]
    for generator, group in df.groupby("generator", observed=True):
        lines.append(f"  {generator}: {group['mutation_score_percent'].mean():.2f}%")

    lines.append("")
    lines.append("Média de mutation_score_percent por complexidade e modelo:")
    for level in COMPLEXITY_ORDER:
        level_df = df[df["complexity_level"] == level]
        if level_df.empty:
            continue
        lines.append(f"  {level}:")
        for generator, group in level_df.groupby("generator", observed=True):
            lines.append(f"    {generator}: {group['mutation_score_percent'].mean():.2f}%")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  Resumo mutation score: {output_path}")


def plot_06_test_strength_vs_coverage(df_str: pd.DataFrame) -> None:
    global OUTPUT_DIR
    inspection_dir = OUTPUT_DIR / INSPECTION_DIR_NAME
    inspection_dir.mkdir(parents=True, exist_ok=True)
    df = df_str.copy()
    df["coverage_percent"] = pd.to_numeric(df["coverage_percent"], errors="coerce")
    df["test_strength_score"] = pd.to_numeric(df["test_strength_score"], errors="coerce")
    previous = OUTPUT_DIR
    OUTPUT_DIR = inspection_dir
    try:
        _scatter_with_trend(
            df["coverage_percent"],
            df["test_strength_score"],
            xlabel="coverage_percent (%)",
            ylabel="test_strength_score",
            filename="06_test_strength_vs_coverage.png",
        )
    finally:
        OUTPUT_DIR = previous


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
    global OUTPUT_DIR
    inspection_dir = OUTPUT_DIR / INSPECTION_DIR_NAME
    inspection_dir.mkdir(parents=True, exist_ok=True)
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

    previous = OUTPUT_DIR
    OUTPUT_DIR = inspection_dir
    try:
        _scatter_with_trend(
            merged["test_strength_score"],
            merged["overall_score"],
            xlabel="test_strength_score",
            ylabel="overall_score (LLM)",
            filename="07_test_strength_vs_llm_score.png",
        )
    finally:
        OUTPUT_DIR = previous


def _execution_ok_failed_totals(df_cov: pd.DataFrame, *, cfg) -> tuple[int, int]:
    frames = _load_coverage_frames(df_cov, cfg=cfg)
    ok_total = sum(int(f["execution_status"].map(_is_execution_ok).sum()) for f in frames.values())
    fail_total = sum(int(f["execution_status"].map(_is_execution_failed).sum()) for f in frames.values())
    return ok_total, fail_total


def _coverage_means_by_generator(df_cov: pd.DataFrame, *, cfg) -> dict[str, float]:
    frames = _load_coverage_frames(df_cov, cfg=cfg)
    return {gen: float(frame["coverage_percent"].mean()) for gen, frame in frames.items()}


def _mutation_means_by_generator(df_str: pd.DataFrame) -> dict[str, float]:
    mutation_df = _prepare_mutation_strength_df(df_str)
    return {
        str(gen): float(group["mutation_score_percent"].mean())
        for gen, group in mutation_df.groupby("generator", observed=True)
    }


def _complexity_observations(
    df_cov: pd.DataFrame,
    df_str: pd.DataFrame,
    *,
    cfg,
) -> list[str]:
    lines: list[str] = []
    cov_frames = _load_coverage_frames(df_cov, cfg=cfg)
    mutation_df = _prepare_mutation_strength_df(df_str)

    for level in COMPLEXITY_ORDER:
        cov_parts: list[str] = []
        mut_parts: list[str] = []
        for gen, frame in cov_frames.items():
            sub_cov = frame[frame["complexity_level"] == level]
            if not sub_cov.empty:
                cov_parts.append(f"{gen}={sub_cov['coverage_percent'].mean():.1f}%")
        for gen, group in mutation_df.groupby("generator", observed=True):
            sub_mut = group[group["complexity_level"] == level]
            if not sub_mut.empty:
                mut_parts.append(f"{gen}={sub_mut['mutation_score_percent'].mean():.1f}%")
        if cov_parts or mut_parts:
            detail = []
            if cov_parts:
                detail.append(f"cobertura [{', '.join(cov_parts)}]")
            if mut_parts:
                detail.append(f"mutation score [{', '.join(mut_parts)}]")
            lines.append(f"  {level}: {'; '.join(detail)}.")
    return lines


def write_cross_evaluation_readme(
    df_cov: pd.DataFrame,
    df_str: pd.DataFrame,
    *,
    cfg,
    output_path: Path,
) -> None:
    ok_total, fail_total = _execution_ok_failed_totals(df_cov, cfg=cfg)
    coverage_means = _coverage_means_by_generator(df_cov, cfg=cfg)
    mutation_means = _mutation_means_by_generator(df_str)

    best_coverage = max(coverage_means, key=coverage_means.get) if coverage_means else "N/A"
    best_mutation = max(mutation_means, key=mutation_means.get) if mutation_means else "N/A"

    lines = [
        "README — Resultados principais para apresentação",
        "=" * 52,
        "",
        "Execução dos testes gerados",
        f"  OK: {ok_total}",
        f"  FAILED: {fail_total}",
        "",
        "Cobertura média por modelo gerador",
    ]
    for gen, value in coverage_means.items():
        lines.append(f"  {gen}: {value:.2f}%")
    lines.append(f"  Melhor modelo em cobertura: {best_coverage}")

    lines.extend(["", "Mutation score médio por modelo gerador"])
    for gen, value in mutation_means.items():
        lines.append(f"  {gen}: {value:.2f}%")
    lines.append(f"  Melhor modelo em mutation testing: {best_mutation}")

    lines.extend(["", "Observações por nível de complexidade"])
    observations = _complexity_observations(df_cov, df_str, cfg=cfg)
    lines.extend(observations if observations else ["  (sem dados suficientes)"])

    lines.extend(
        [
            "",
            "Notas",
            "  - Gráficos principais desta pasta: execução, cobertura e mutation testing.",
            "  - mutation_score_percent reflete mutantes mortos pelos testes (0–100%).",
            "  - Gráficos 06/07 e boxplot de mutation ficam em plots/<dataset>/inspecao/.",
        ]
    )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  README apresentação: {output_path}")


def sync_cross_evaluation_presentation() -> list[Path]:
    cross_dir = OUTPUT_DIR / CROSS_EVAL_DIR_NAME
    cross_dir.mkdir(parents=True, exist_ok=True)
    copied: list[Path] = []
    for filename in PRESENTATION_PLOT_NAMES:
        source = OUTPUT_DIR / filename
        if not source.exists():
            print(f"  Aviso: {filename} não encontrado — não copiado para {CROSS_EVAL_DIR_NAME}/.")
            continue
        destination = cross_dir / filename
        shutil.copy2(source, destination)
        copied.append(destination.resolve())
        print(f"  Copiado para {CROSS_EVAL_DIR_NAME}: {filename}")
    return copied


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
        mutation_df = _prepare_mutation_strength_df(df_str)
        rows.append(
            {
                "metric": "media_mutation_score_percent",
                "value": round(mutation_df["mutation_score_percent"].mean(), 4),
            }
        )
        rows.append(
            {
                "metric": "mutation_status_failed_count",
                "value": int(mutation_df["mutation_failed"].sum()),
            }
        )
        for generator, group in mutation_df.groupby("generator", observed=True):
            rows.append(
                {
                    "metric": f"media_mutation_score_percent_{generator.lower()}",
                    "value": round(group["mutation_score_percent"].mean(), 4),
                }
            )
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
        mutation_df = _prepare_mutation_strength_df(df_str)
        for level in COMPLEXITY_ORDER:
            sub = mutation_df[mutation_df["complexity_level"] == level]
            if sub.empty:
                continue
            for generator, group in sub.groupby("generator", observed=True):
                rows.append(
                    {
                        "metric": f"media_mutation_score_{level}_{generator.lower()}",
                        "value": round(group["mutation_score_percent"].mean(), 4),
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gera gráficos finais do experimento.")
    add_dataset_argument(parser)
    return parser.parse_args()


def main() -> None:
    global OUTPUT_DIR

    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    input_coverage = cfg.result_csv("cobertura_testes_gerados_gpt")
    input_eval = cfg.result_csv("avaliacao_gpt_sobre_testes_gpt")
    input_strength = cfg.result_csv("forca_heuristica_testes")
    OUTPUT_DIR = cfg.plots_dir

    print(f"Dataset: {cfg.key}")
    print("Gerando gráficos finais...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update(
        {
            "font.size": 11,
            "axes.labelsize": 12,
        }
    )

    if not input_coverage.exists():
        print(f"Erro: arquivo obrigatório não encontrado: {input_coverage}")
        return

    df_cov = _prepare_coverage(pd.read_csv(input_coverage))

    df_eval: pd.DataFrame | None = None
    if input_eval.exists():
        df_eval = pd.read_csv(input_eval)
        df_eval["complexity_level"] = df_eval["complexity_level"].apply(normalize_complexity_level)
        print(f"Avaliação LLM carregada: {len(df_eval)} registros.")
    else:
        print(f"Aviso: {input_eval.name} não encontrado — gráficos 03, 04 e 07 serão omitidos.")

    df_str: pd.DataFrame | None = None
    if input_strength.exists():
        df_str = pd.read_csv(input_strength)
        df_str["complexity_level"] = df_str["complexity_level"].apply(normalize_complexity_level)
        print(f"test_strength_results carregado: {len(df_str)} registros.")
    else:
        print(f"Aviso: {input_strength.name} não encontrado — gráficos 05, 06 e 07 serão omitidos.")

    print("\nGráficos:")
    plot_01_execucao_por_status(df_cov, cfg=cfg)
    plot_02_cobertura_media_por_complexidade(df_cov, cfg=cfg)

    if df_eval is not None:
        plot_03_nota_llm_por_complexidade(df_eval)
        plot_04_cobertura_vs_nota_llm(df_eval)
    if df_str is not None:
        plot_05_test_strength_por_complexidade(df_str)
        write_mutation_strength_summary_txt(df_str, OUTPUT_DIR / "resumo_mutation_score.txt")

    print("\nPasta cross_evaluation (apresentação):")
    sync_cross_evaluation_presentation()
    if df_str is not None:
        write_cross_evaluation_readme(
            df_cov,
            df_str,
            cfg=cfg,
            output_path=OUTPUT_DIR / CROSS_EVAL_DIR_NAME / "README_RESULTADOS.txt",
        )

    print("\nGráficos de inspeção (secundários, pasta inspecao/):")
    if df_str is not None:
        plot_05_test_strength_inspection(df_str)
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
