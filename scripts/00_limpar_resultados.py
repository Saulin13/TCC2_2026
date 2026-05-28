"""
Reseta outputs experimentais antigos, recria a estrutura oficial e,
opcionalmente, dispara a pipeline do TheAlgorithms.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = BASE_DIR / "scripts"
RESULTS_DIR = BASE_DIR / "data" / "results"
LOGS_DIR = RESULTS_DIR / "logs"
LOGS_GITKEEP = LOGS_DIR / ".gitkeep"
TESTS_GENERATED_DIR = BASE_DIR / "tests" / "generated"
TESTS_LEGACY_DIR = TESTS_GENERATED_DIR / "legacy"

COVERAGE_FILES = [
    BASE_DIR / ".coverage",
    BASE_DIR / "coverage.json",
]

TEST_OUTPUT_DIRS = (
    TESTS_GENERATED_DIR / "thealgorithms" / "gpt",
    TESTS_GENERATED_DIR / "thealgorithms" / "claude",
    TESTS_GENERATED_DIR / "real" / "gpt",
    TESTS_GENERATED_DIR / "real" / "claude",
)

OFFICIAL_DIRS = (
    RESULTS_DIR,
    LOGS_DIR,
    RESULTS_DIR / "plots" / "thealgorithms",
    RESULTS_DIR / "plots" / "real",
    RESULTS_DIR / "generated_prompts" / "thealgorithms" / "gpt",
    RESULTS_DIR / "generated_prompts" / "thealgorithms" / "claude",
    RESULTS_DIR / "generated_prompts" / "real" / "gpt",
    RESULTS_DIR / "generated_prompts" / "real" / "claude",
    *TEST_OUTPUT_DIRS,
)

PLOT_EXTENSIONS = frozenset({".png", ".jpg", ".jpeg", ".svg", ".pdf"})
LOG_EXTENSIONS = frozenset({".log"})


@dataclass
class RemovalStats:
    csvs: int = 0
    plots: int = 0
    logs: int = 0
    tests: int = 0
    other: int = 0
    removed_paths: list[str] = field(default_factory=list)

    def record(self, path: Path, category: str) -> None:
        self.removed_paths.append(_rel(path))
        if category == "csv":
            self.csvs += 1
        elif category == "plot":
            self.plots += 1
        elif category == "log":
            self.logs += 1
        elif category == "test":
            self.tests += 1
        else:
            self.other += 1


def _rel(path: Path) -> str:
    try:
        return path.relative_to(BASE_DIR).as_posix()
    except ValueError:
        return path.as_posix()


def _classify_file(path: Path) -> str:
    suffix = path.suffix.lower()
    rel = _rel(path)
    if suffix == ".csv":
        return "csv"
    if suffix in PLOT_EXTENSIONS:
        return "plot"
    if suffix in LOG_EXTENSIONS or rel.startswith("data/results/logs/"):
        return "log"
    if rel.startswith("tests/generated/") and suffix == ".py":
        return "test"
    if suffix in {".txt", ".json"}:
        return "other"
    return "other"


def _should_preserve_in_results(path: Path) -> bool:
    """Preserva apenas logs/.gitkeep dentro de data/results."""
    try:
        rel = path.relative_to(RESULTS_DIR)
    except ValueError:
        return False
    parts = rel.parts
    if len(parts) == 2 and parts[0] == "logs" and parts[1] == ".gitkeep":
        return True
    return False


def _collect_results_removals() -> list[Path]:
    if not RESULTS_DIR.exists():
        return []
    removals: list[Path] = []
    for item in sorted(RESULTS_DIR.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if _should_preserve_in_results(item):
            continue
        if item.exists():
            removals.append(item)
    return removals


def _collect_test_removals() -> list[Path]:
    removals: list[Path] = []
    for directory in TEST_OUTPUT_DIRS:
        if not directory.exists():
            continue
        for item in sorted(directory.rglob("*"), key=lambda p: len(p.parts), reverse=True):
            if item.name == ".gitkeep":
                continue
            removals.append(item)
    return removals


def _is_under_legacy(path: Path) -> bool:
    try:
        path.relative_to(TESTS_LEGACY_DIR)
        return True
    except ValueError:
        return False


def _collect_pycache_dirs() -> list[Path]:
    roots = [SCRIPTS_DIR, TESTS_GENERATED_DIR]
    found: list[Path] = []
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("__pycache__"):
            if path.is_dir() and not _is_under_legacy(path):
                found.append(path)
    return sorted(set(found), key=lambda p: p.as_posix())


def _remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)


def _recreate_structure() -> None:
    for directory in OFFICIAL_DIRS:
        directory.mkdir(parents=True, exist_ok=True)
    LOGS_GITKEEP.parent.mkdir(parents=True, exist_ok=True)
    if not LOGS_GITKEEP.exists():
        LOGS_GITKEEP.write_text("", encoding="utf-8")


def _print_verbose_removals(stats: RemovalStats) -> None:
    print("\n[OK] removido:")
    if not stats.removed_paths:
        print("- (nenhum item)")
    else:
        for rel_path in stats.removed_paths:
            print(f"- {rel_path}")

    print("\nResumo:")
    print(f"- {stats.csvs} CSVs removidos")
    print(f"- {stats.plots} gráficos removidos")
    print(f"- {stats.logs} logs removidos")
    print(f"- {stats.tests} testes removidos")
    if stats.other:
        print(f"- {stats.other} outros arquivos removidos")


def _run_pipeline_thealgorithms() -> int:
    cmd = [
        sys.executable,
        str(SCRIPTS_DIR / "00_run_pipeline.py"),
        "--dataset",
        "thealgorithms",
    ]
    print("\n" + "=" * 72)
    print("Iniciando pipeline limpa: thealgorithms")
    print("Comando:", " ".join(cmd))
    print("=" * 72 + "\n")
    result = subprocess.run(cmd, cwd=SCRIPTS_DIR)
    return result.returncode


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reseta resultados experimentais e recria a estrutura oficial."
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Confirma a limpeza sem pedir 'SIM'.",
    )
    parser.add_argument(
        "--run-pipeline",
        action="store_true",
        help="Após a limpeza, executa: 00_run_pipeline.py --dataset thealgorithms",
    )
    parser.add_argument(
        "--no-run-pipeline",
        action="store_true",
        help="Apenas limpa; não executa a pipeline.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    run_pipeline = args.run_pipeline and not args.no_run_pipeline

    to_remove: list[Path] = []
    to_remove.extend(_collect_results_removals())
    to_remove.extend(_collect_test_removals())
    to_remove.extend([p for p in COVERAGE_FILES if p.exists()])
    to_remove.extend(_collect_pycache_dirs())

    unique_to_remove = sorted(set(to_remove), key=lambda p: p.as_posix())

    print("Reset experimental — itens que serão removidos:")
    if not unique_to_remove:
        print("- Nenhum arquivo ou pasta gerada encontrada.")
    else:
        for item in unique_to_remove:
            print(f"- {_rel(item)}")

    if not args.yes:
        confirmacao = input("\nDigite SIM para confirmar a limpeza: ").strip()
        if confirmacao != "SIM":
            print("Limpeza cancelada. Nada foi apagado.")
            return 1

    stats = RemovalStats()
    for item in unique_to_remove:
        _remove_path(item)
        if item.is_file():
            stats.record(item, _classify_file(item))
        elif item.is_dir() and item.name != "__pycache__":
            stats.removed_paths.append(_rel(item) + "/")

    _recreate_structure()

    _print_verbose_removals(stats)

    print("\nEstrutura recriada:")
    for directory in OFFICIAL_DIRS:
        print(f"- {_rel(directory)}/")
    print(f"- {_rel(LOGS_GITKEEP)}")

    print(
        "\nAmbiente experimental resetado com sucesso.\n"
        "Pronto para execução limpa da pipeline."
    )

    if run_pipeline:
        return _run_pipeline_thealgorithms()
    return 0


if __name__ == "__main__":
    sys.exit(main())
