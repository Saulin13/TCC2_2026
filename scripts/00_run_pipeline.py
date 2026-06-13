"""
Orquestrador da pipeline do experimento TCC.

Executa, em ordem, os scripts de geração, execução, métricas, avaliação,
consolidação e gráficos para um ou mais datasets.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from dataset_config import (
    DATASET_CHOICES,
    DATASET_REAL,
    DATASET_THEALGORITHMS,
    resolve_dataset,
)

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
LOGS_DIR = BASE_DIR / "data" / "results" / "logs"

REAL_COVERAGE_WARNING = (
    "Atenção: no dataset real (scikit-learn), a cobertura pode ser limitada "
    "porque os testes executam contra o pacote sklearn instalado via pip."
)

DATASET_ALL = "all"
DATASET_OPTIONS = (*DATASET_CHOICES, DATASET_ALL)


@dataclass(frozen=True)
class PipelineStep:
    name: str
    script: str
    extra_args: list[str]


def _build_steps(
    dataset: str,
    *,
    skip_generation: bool,
    skip_evaluation: bool,
    only_plots: bool,
) -> list[PipelineStep]:
    ds_args = ["--dataset", dataset]

    all_steps: list[tuple[PipelineStep, bool]] = [
        (
            PipelineStep(
                "Geração de testes com GPT",
                "04_generate_tests_gpt.py",
                ds_args,
            ),
            skip_generation,
        ),
        (
            PipelineStep(
                "Geração de testes com Claude",
                "04b_generate_tests_claude.py",
                ds_args,
            ),
            skip_generation,
        ),
        (
            PipelineStep(
                "Execução/cobertura dos testes gerados pelo GPT",
                "05_run_tests.py",
                [*ds_args, "--generator", "gpt"],
            ),
            only_plots,
        ),
        (
            PipelineStep(
                "Execução/cobertura dos testes gerados pelo Claude",
                "05_run_tests.py",
                [*ds_args, "--generator", "claude"],
            ),
            only_plots,
        ),
        (
            PipelineStep(
                "Classificação da cobertura",
                "14_classify_coverage.py",
                ds_args,
            ),
            only_plots,
        ),
        (
            PipelineStep(
                "Métrica de densidade de asserts",
                "08_calculate_assertion_density.py",
                ds_args,
            ),
            only_plots,
        ),
        (
            PipelineStep(
                "Avaliação GPT sobre testes GPT",
                "06_evaluate_tests_llm.py",
                ds_args,
            ),
            only_plots or skip_evaluation,
        ),
        (
            PipelineStep(
                "Avaliação Claude sobre testes GPT",
                "06b_evaluate_tests_claude.py",
                ds_args,
            ),
            only_plots or skip_evaluation,
        ),
        (
            PipelineStep(
                "Avaliação GPT sobre testes Claude",
                "06c_evaluate_gpt_on_claude.py",
                ds_args,
            ),
            only_plots or skip_evaluation,
        ),
        (
            PipelineStep(
                "Avaliação Claude sobre testes Claude",
                "06d_evaluate_claude_on_claude.py",
                ds_args,
            ),
            only_plots or skip_evaluation,
        ),
        (
            PipelineStep(
                "Métrica de sucesso de execução",
                "09_calculate_execution_success.py",
                ds_args,
            ),
            only_plots,
        ),
        (
            PipelineStep(
                "Métrica test_strength_score",
                "10_calculate_test_strength.py",
                ds_args,
            ),
            only_plots,
        ),
        (
            PipelineStep(
                "Consolidação dos resultados",
                "11_consolidate_results.py",
                ds_args,
            ),
            False,
        ),
        (
            PipelineStep(
                "Geração dos gráficos",
                "12_generate_plots.py",
                ds_args,
            ),
            False,
        ),
        (
            PipelineStep(
                "Comparação dos avaliadores",
                "13_compare_llm_evaluators.py",
                ds_args,
            ),
            only_plots or skip_evaluation,
        ),
        (
            PipelineStep(
                "Análise estatística e gráficos avançados",
                "15_statistical_analysis.py",
                ds_args,
            ),
            False,
        ),
    ]

    return [step for step, skip in all_steps if not skip]


def _resolve_datasets(dataset_arg: str) -> list[str]:
    if dataset_arg == DATASET_ALL:
        return [DATASET_THEALGORITHMS, DATASET_REAL]
    return [dataset_arg]


def _log_path(dataset: str) -> Path:
    return LOGS_DIR / f"pipeline_{dataset}.log"


def _append_log(log_file: Path, text: str) -> None:
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(text)
        if not text.endswith("\n"):
            fh.write("\n")


def _run_step(
    step: PipelineStep,
    *,
    log_file: Path,
    step_index: int,
    total_steps: int,
) -> bool:
    script_path = SCRIPTS_DIR / step.script
    cmd = [sys.executable, str(script_path), *step.extra_args]
    cmd_display = " ".join(cmd)

    started_at = datetime.now()
    header = (
        f"\n{'=' * 72}\n"
        f"[{step_index}/{total_steps}] {step.name}\n"
        f"Início: {started_at.isoformat(timespec='seconds')}\n"
        f"Comando: {cmd_display}\n"
        f"{'=' * 72}\n"
    )

    print(header, end="")
    _append_log(log_file, header)

    result = subprocess.run(
        cmd,
        cwd=SCRIPTS_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    finished_at = datetime.now()

    if result.stdout:
        print(result.stdout, end="" if result.stdout.endswith("\n") else "\n")
    if result.stderr:
        print(result.stderr, end="" if result.stderr.endswith("\n") else "\n", file=sys.stderr)

    status = "SUCESSO" if result.returncode == 0 else "FALHA"
    footer = (
        f"Fim: {finished_at.isoformat(timespec='seconds')}\n"
        f"Status: {status}\n"
        f"Código de saída: {result.returncode}\n"
        f"--- stdout ---\n{result.stdout or '(vazio)'}\n"
        f"--- stderr ---\n{result.stderr or '(vazio)'}\n"
    )
    _append_log(log_file, footer)

    if result.returncode != 0:
        print(
            f"\nPipeline interrompida na etapa: {step.name}\n"
            f"Comando: {cmd_display}\n"
            f"Código de erro: {result.returncode}\n",
            file=sys.stderr,
        )
        return False

    print(f"Etapa concluída com sucesso.\n")
    return True


def _run_pipeline_for_dataset(
    dataset: str,
    steps: list[PipelineStep],
) -> bool:
    log_file = _log_path(dataset)
    pipeline_started = datetime.now()

    if dataset == DATASET_REAL:
        print(REAL_COVERAGE_WARNING)

    intro = (
        f"\n{'#' * 72}\n"
        f"# Pipeline — dataset: {dataset}\n"
        f"# Início da pipeline: {pipeline_started.isoformat(timespec='seconds')}\n"
        f"# Log: {log_file}\n"
        f"{'#' * 72}\n"
    )
    print(intro, end="")
    _append_log(log_file, intro)

    total = len(steps)
    for index, step in enumerate(steps, start=1):
        if not _run_step(step, log_file=log_file, step_index=index, total_steps=total):
            pipeline_finished = datetime.now()
            summary = (
                f"\nPipeline do dataset '{dataset}' encerrada com FALHA.\n"
                f"Fim: {pipeline_finished.isoformat(timespec='seconds')}\n"
            )
            print(summary, end="")
            _append_log(log_file, summary)
            return False

    pipeline_finished = datetime.now()
    summary = (
        f"\nPipeline do dataset '{dataset}' concluída com SUCESSO.\n"
        f"Fim: {pipeline_finished.isoformat(timespec='seconds')}\n"
    )
    print(summary, end="")
    _append_log(log_file, summary)
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Orquestra a execução completa do experimento do TCC."
    )
    parser.add_argument(
        "--dataset",
        choices=DATASET_OPTIONS,
        required=True,
        help=(
            "Dataset a processar: thealgorithms (sample_thealgorithms_60.csv), "
            "real (sample_real_project_15.csv) ou all (ambos, nessa ordem)."
        ),
    )
    parser.add_argument(
        "--skip-generation",
        action="store_true",
        help="Pula a geração de testes com GPT e Claude.",
    )
    parser.add_argument(
        "--skip-evaluation",
        action="store_true",
        help="Pula as avaliações por LLM e a comparação dos avaliadores.",
    )
    parser.add_argument(
        "--only-plots",
        action="store_true",
        help="Executa apenas consolidação de resultados e geração de gráficos.",
    )
    return parser.parse_args()


def _print_final_summary(datasets: list[str]) -> None:
    print("\n" + "=" * 72)
    print("Pipeline finalizada com sucesso.")
    print("\nArquivos principais gerados:")

    for dataset in datasets:
        cfg = resolve_dataset(dataset)
        final_csv = cfg.result_csv("resultados_finais")
        final_txt = cfg.result_txt("resumo_resultados_finais")
        plots_dir = cfg.plots_dir
        print(f"\n  [{dataset}]")
        print(f"  - {final_csv.relative_to(BASE_DIR).as_posix()}")
        print(f"  - {final_txt.relative_to(BASE_DIR).as_posix()}")
        print(f"  - {plots_dir.relative_to(BASE_DIR).as_posix()}/")

    print("\nLogs da execução:")
    for dataset in datasets:
        log_file = _log_path(dataset)
        print(f"  - {log_file.relative_to(BASE_DIR).as_posix()}")

    print("\nComandos úteis:")
    print("  python scripts/00_run_pipeline.py --dataset thealgorithms")
    print("  python scripts/00_run_pipeline.py --dataset real")
    print("  python scripts/00_run_pipeline.py --dataset all")
    print(
        "  python scripts/00_run_pipeline.py --dataset all "
        "--skip-generation --skip-evaluation"
    )
    print("=" * 72 + "\n")


def main() -> int:
    args = parse_args()

    if args.only_plots and (args.skip_generation or args.skip_evaluation):
        print(
            "Aviso: --only-plots já restringe a pipeline; "
            "--skip-generation e --skip-evaluation são redundantes.",
            file=sys.stderr,
        )

    datasets = _resolve_datasets(args.dataset)

    for dataset in datasets:
        steps = _build_steps(
            dataset,
            skip_generation=args.skip_generation,
            skip_evaluation=args.skip_evaluation,
            only_plots=args.only_plots,
        )
        if not _run_pipeline_for_dataset(dataset, steps):
            return 1

    _print_final_summary(datasets)
    return 0


if __name__ == "__main__":
    sys.exit(main())
