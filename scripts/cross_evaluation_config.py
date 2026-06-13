"""Arquivos permitidos na pasta cross_evaluation de apresentação."""

from __future__ import annotations

from pathlib import Path

CROSS_EVALUATION_ALLOWED_FILES: tuple[str, ...] = (
    "01_execucao_por_status.png",
    "02_cobertura_media_por_complexidade.png",
    "05_test_strength_por_complexidade.png",
    "overall_score_cross_evaluation_mean.png",
    "overall_score_cross_evaluation_by_complexity.png",
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
)


def clean_cross_evaluation_folder(cross_dir: Path) -> None:
    """Remove todos os arquivos da pasta cross_evaluation."""
    cross_dir.mkdir(parents=True, exist_ok=True)
    for path in cross_dir.iterdir():
        if path.is_file():
            path.unlink()


def prune_cross_evaluation_folder(cross_dir: Path) -> list[str]:
    """Remove arquivos que não pertencem à lista oficial de apresentação."""
    cross_dir.mkdir(parents=True, exist_ok=True)
    allowed = set(CROSS_EVALUATION_ALLOWED_FILES)
    removed: list[str] = []
    for path in cross_dir.iterdir():
        if path.is_file() and path.name not in allowed:
            path.unlink()
            removed.append(path.name)
    return removed
