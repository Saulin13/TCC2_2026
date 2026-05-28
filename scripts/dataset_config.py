"""
Configuração de caminhos por dataset do experimento (TheAlgorithms vs. scikit-learn).
"""

from __future__ import annotations

import argparse
import importlib
import inspect
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SELECTED_DIR = BASE_DIR / "data" / "selected_functions"
RESULTS_DIR = BASE_DIR / "data" / "results"
GENERATED_TESTS_ROOT = BASE_DIR / "tests" / "generated"
PROMPTS_ROOT = BASE_DIR / "data" / "results" / "generated_prompts"

DATASET_THEALGORITHMS = "thealgorithms"
DATASET_REAL = "real"
DEFAULT_DATASET = DATASET_THEALGORITHMS
DATASET_CHOICES = (DATASET_THEALGORITHMS, DATASET_REAL)


@dataclass(frozen=True)
class DatasetConfig:
    """Paths e metadados de um dataset do experimento."""

    key: str
    suffix: str
    sample_filename: str
    repo_relative: Path
    pilot_sample_filename: str | None = None

    @property
    def sample_csv(self) -> Path:
        return SELECTED_DIR / self.sample_filename

    @property
    def pilot_sample_csv(self) -> Path | None:
        if self.pilot_sample_filename is None:
            return None
        return SELECTED_DIR / self.pilot_sample_filename

    @property
    def repo_path(self) -> Path:
        return BASE_DIR / self.repo_relative

    @property
    def results_dir(self) -> Path:
        return RESULTS_DIR

    @property
    def plots_dir(self) -> Path:
        return RESULTS_DIR / "plots" / self.key

    def resolve_sample(self, *, pilot: bool = False) -> Path:
        if pilot:
            if self.pilot_sample_csv is None:
                raise ValueError(f"Dataset '{self.key}' não possui amostra piloto.")
            return self.pilot_sample_csv
        return self.sample_csv

    def tests_dir(self, generator: str) -> Path:
        return GENERATED_TESTS_ROOT / self.key / generator

    def prompts_dir(self, generator: str) -> Path:
        return PROMPTS_ROOT / self.key / generator

    def result_csv(self, stem: str) -> Path:
        """Ex.: result_csv('cobertura_testes_gerados_gpt') -> .../cobertura_testes_gerados_gpt_thealgorithms.csv"""
        return self.results_dir / f"{stem}{self.suffix}.csv"

    def result_txt(self, stem: str) -> Path:
        return self.results_dir / f"{stem}{self.suffix}.txt"


_DATASETS: dict[str, DatasetConfig] = {
    DATASET_THEALGORITHMS: DatasetConfig(
        key=DATASET_THEALGORITHMS,
        suffix="_thealgorithms",
        sample_filename="sample_thealgorithms_60.csv",
        repo_relative=Path("repos/Python"),
        pilot_sample_filename="pilot_sample_30.csv",
    ),
    DATASET_REAL: DatasetConfig(
        key=DATASET_REAL,
        suffix="_real",
        sample_filename="sample_real_project_10.csv",
        repo_relative=Path("repos/scikit-learn"),
        pilot_sample_filename=None,
    ),
}


def resolve_dataset(name: str | None = None) -> DatasetConfig:
    key = (name or DEFAULT_DATASET).strip().lower()
    if key not in _DATASETS:
        valid = ", ".join(DATASET_CHOICES)
        raise ValueError(f"Dataset inválido: {name!r}. Opções: {valid}")
    return _DATASETS[key]


def file_path_to_sklearn_module_path(file_path: str) -> str:
    """sklearn/utils/validation.py -> sklearn.utils.validation"""
    normalized = str(file_path).replace("\\", "/").lstrip("/")
    if normalized.endswith(".py"):
        normalized = normalized[:-3]
    parts = [p for p in normalized.split("/") if p]
    if not parts:
        return "sklearn"
    if parts[0] != "sklearn":
        parts = ["sklearn", *parts]
    return ".".join(parts)


def file_path_to_module_path(file_path: str, *, dataset_key: str) -> str:
    if dataset_key == DATASET_REAL:
        return file_path_to_sklearn_module_path(file_path)
    p = Path(str(file_path).replace("\\", "/"))
    return ".".join(p.with_suffix("").parts)


def resolve_module_path_from_row(row: object, *, dataset_key: str) -> str:
    """Usa module_path do CSV ou deriva a partir de file_path."""
    if hasattr(row, "get"):
        module_path = row.get("module_path")  # type: ignore[union-attr]
        file_path = row.get("file_path", "")  # type: ignore[union-attr]
    else:
        module_path = getattr(row, "module_path", None)
        file_path = getattr(row, "file_path", "")

    if isinstance(module_path, str) and module_path.strip():
        return module_path.strip()
    return file_path_to_module_path(str(file_path), dataset_key=dataset_key)


def function_importable(module_path: str, function_name: str) -> bool:
    """Verifica se a função existe no pacote sklearn instalado (pip)."""
    try:
        module = importlib.import_module(module_path)
    except Exception:
        return False
    obj = getattr(module, function_name, None)
    return callable(obj)


def resolve_installed_module_file(module_path: str) -> Path | None:
    """Caminho do .py do módulo sklearn instalado via pip."""
    try:
        module = importlib.import_module(module_path)
        source = inspect.getsourcefile(module) or inspect.getfile(module)
        return Path(source).resolve()
    except (TypeError, OSError, ValueError):
        return None
    except Exception:
        return None


def add_dataset_argument(
    parser: argparse.ArgumentParser,
    *,
    help_suffix: str = "",
) -> None:
    extra = f" {help_suffix}".rstrip()
    parser.add_argument(
        "--dataset",
        choices=DATASET_CHOICES,
        default=DEFAULT_DATASET,
        help=(
            f"Dataset do experimento: {DATASET_THEALGORITHMS} (padrão) ou {DATASET_REAL}."
            f"{extra}"
        ),
    )
