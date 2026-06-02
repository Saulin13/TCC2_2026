from __future__ import annotations

import ast
import random
import textwrap
from pathlib import Path

import pandas as pd
from radon.complexity import cc_rank, cc_visit

from dataset_config import (
    file_path_to_sklearn_module_path,
    function_importable,
)

BASE_DIR = Path(__file__).resolve().parent.parent
BASE_REPO_PATH = BASE_DIR / "repos" / "scikit-learn"
OUTPUT_CSV_PATH = (
    BASE_DIR / "data" / "selected_functions" / "sample_real_project_15.csv"
)

REPOSITORY_NAME = "scikit-learn"
RANDOM_STATE = 42

SAMPLE_COUNTS = {"baixa": 5, "media": 5, "alta": 5}

PREFERRED_PATH_PREFIXES = (
    "sklearn/metrics/",
    "sklearn/preprocessing/",
    "sklearn/model_selection/",
    "sklearn/utils/",
)

SCAN_ROOT = "sklearn"

IGNORED_DIR_KEYWORDS = (
    "test",
    "tests",
    "benchmark",
    "benchmarks",
    "examples",
    "doc",
    "docs",
    "asv_benchmarks",
    "maint_tools",
    "build_tools",
    "externals",
    "__check_build",
    "_build",
)

IGNORED_FILE_PREFIXES = ("test_", "conftest")
IGNORED_FILE_NAMES = frozenset({"setup.py", "conftest.py"})

MIN_USEFUL_LINES = 3
MAX_TOTAL_LINES = 120

FORBIDDEN_SOURCE_PATTERNS = (
    "cimport",
    "cython",
    ".pyx",
    "fetch_openml",
    "fetch_california_housing",
    "fetch_lfw",
    "fetch_20newsgroups",
    "fetch_covtype",
    "fetch_kddcup",
    "fetch_rcv1",
    "fetch_species_distributions",
    "load_files",
    "load_sample_images",
    "urllib.request",
    "urllib.urlopen",
    "import requests",
    "from requests",
    "import httpx",
    "from httpx",
    "http.client",
    "import socket",
    "from socket",
    "subprocess.",
    "import subprocess",
    "joblib.load",
    "pickle.load",
    "np.load(",
    "numpy.load(",
    "pd.read_csv",
    "pd.read_table",
    "read_csv(",
    "read_table(",
    "import matplotlib",
    "from matplotlib",
    "matplotlib.pyplot",
    "plt.show",
    "open(",
    "Path(",
    "datasets.fetch_",
    "from sklearn.datasets import fetch",
    "import sklearn.datasets",
)

OUTPUT_COLUMNS = [
    "function_name",
    "file_path",
    "module_path",
    "start_line",
    "end_line",
    "source_code",
    "complexity_score",
    "radon_rank",
    "complexity_level",
    "repository",
]


def normalize_path(path: str) -> str:
    return str(path).replace("\\", "/")


def classify_complexity_level(score: int) -> str:
    if score <= 5:
        return "baixa"
    if score <= 10:
        return "media"
    return "alta"


def measure_complexity(source_code: str) -> tuple[int, str, str]:
    if not isinstance(source_code, str) or not source_code.strip():
        score = 0
        return score, cc_rank(score), classify_complexity_level(score)

    try:
        clean_code = textwrap.dedent(source_code).strip()
        blocks = cc_visit(clean_code)
        score = max((block.complexity for block in blocks), default=0)
        return score, cc_rank(score), classify_complexity_level(score)
    except Exception:
        score = 0
        return score, cc_rank(score), classify_complexity_level(score)


def count_useful_lines(source_code: str) -> int:
    if not isinstance(source_code, str):
        return 0

    useful = 0
    for line in source_code.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        useful += 1
    return useful


def should_ignore_file(file_path: Path) -> bool:
    if file_path.name in IGNORED_FILE_NAMES:
        return True
    if any(file_path.name.startswith(prefix) for prefix in IGNORED_FILE_PREFIXES):
        return True

    dir_parts = [part.lower() for part in file_path.parts[:-1]]
    return any(keyword in dir_parts for keyword in IGNORED_DIR_KEYWORDS)


def is_preferred_path(file_path: str) -> bool:
    normalized = normalize_path(file_path)
    return any(normalized.startswith(prefix) for prefix in PREFERRED_PATH_PREFIXES)


def _source_has_forbidden_patterns(source_code: str) -> bool:
    lowered = (source_code or "").lower()
    return any(pattern.lower() in lowered for pattern in FORBIDDEN_SOURCE_PATTERNS)


def _is_likely_top_level_function(source_code: str) -> bool:
    if not isinstance(source_code, str) or not source_code.strip():
        return False

    for raw in source_code.splitlines():
        line = raw.rstrip("\n")
        stripped = line.lstrip(" \t")
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("@"):
            continue
        if stripped.startswith("def ") or stripped.startswith("async def "):
            leading = len(line) - len(line.lstrip(" \t"))
            return leading == 0
        return False
    return False


def get_source_segment(lines: list[str], start_line: int, end_line: int) -> str:
    return "\n".join(lines[start_line - 1 : end_line])


def extract_module_level_functions(file_path: Path, base_path: Path) -> list[dict]:
    try:
        source_code = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source_code = file_path.read_text(encoding="latin-1")

    source_lines = source_code.splitlines()
    tree = ast.parse(source_code, filename=str(file_path))

    records: list[dict] = []
    for node in tree.body:
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue

        start_line = node.lineno
        end_line = getattr(node, "end_lineno", node.lineno)
        records.append(
            {
                "function_name": node.name,
                "file_path": normalize_path(file_path.relative_to(base_path)),
                "start_line": start_line,
                "end_line": end_line,
                "source_code": get_source_segment(
                    source_lines, start_line=start_line, end_line=end_line
                ),
            }
        )

    return records


def extract_functions(base_repo_path: Path) -> pd.DataFrame:
    scan_root = base_repo_path / SCAN_ROOT
    if not scan_root.exists():
        raise FileNotFoundError(f"Diretorio sklearn nao encontrado: {scan_root}")

    all_records: list[dict] = []
    for py_file in scan_root.rglob("*.py"):
        if should_ignore_file(py_file):
            continue

        try:
            all_records.extend(extract_module_level_functions(py_file, base_repo_path))
        except (SyntaxError, ValueError):
            continue

    return pd.DataFrame(
        all_records,
        columns=["function_name", "file_path", "start_line", "end_line", "source_code"],
    )


def filter_candidates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["module_path"] = df["file_path"].map(file_path_to_sklearn_module_path)
    df["total_lines"] = df["source_code"].fillna("").apply(lambda s: len(str(s).splitlines()))
    df["useful_lines"] = df["source_code"].fillna("").apply(count_useful_lines)
    df["is_preferred"] = df["file_path"].map(is_preferred_path)
    df["importable"] = df.apply(
        lambda row: function_importable(str(row["module_path"]), str(row["function_name"])),
        axis=1,
    )

    fn = df["function_name"].fillna("")

    mask = (
        (~fn.str.startswith("_"))
        & (~fn.str.startswith("test_"))
        & (df["useful_lines"] >= MIN_USEFUL_LINES)
        & (df["total_lines"] <= MAX_TOTAL_LINES)
        & (~df["source_code"].fillna("").map(_source_has_forbidden_patterns))
        & (df["source_code"].fillna("").map(_is_likely_top_level_function))
        & (df["file_path"].map(is_preferred_path))
        & df["importable"]
    )

    return df[mask].copy()


def select_with_file_diversity(
    df_level: pd.DataFrame, target_n: int, rng: random.Random
) -> pd.DataFrame:
    if df_level.empty:
        return df_level.copy()

    df_level = df_level.sort_values(
        by=["importable", "is_preferred", "complexity_score", "file_path", "function_name"],
        ascending=[False, False, True, True, True],
    )

    file_to_indices: dict[str, list[int]] = {}
    for file_path, group in df_level.groupby("file_path"):
        indices = group.index.tolist()
        rng.shuffle(indices)
        file_to_indices[file_path] = indices

    files = list(file_to_indices.keys())
    preferred_files = [f for f in files if is_preferred_path(f)]
    other_files = [f for f in files if f not in preferred_files]
    rng.shuffle(preferred_files)
    rng.shuffle(other_files)
    files = preferred_files + other_files

    selected_indices: list[int] = []
    while len(selected_indices) < target_n:
        picked_in_round = False
        for file_path in files:
            candidates = file_to_indices.get(file_path, [])
            if not candidates:
                continue
            selected_indices.append(candidates.pop(0))
            picked_in_round = True
            if len(selected_indices) >= target_n:
                break
        if not picked_in_round:
            break

    return df_level.loc[selected_indices].copy()


def build_sample(df: pd.DataFrame) -> pd.DataFrame:
    rng = random.Random(RANDOM_STATE)
    selected_parts: list[pd.DataFrame] = []

    for level, target_n in SAMPLE_COUNTS.items():
        level_df = df[df["complexity_level"] == level].copy()
        level_selected = select_with_file_diversity(level_df, target_n, rng)
        selected_parts.append(level_selected)

        if len(level_selected) < target_n:
            print(
                f"Aviso: nivel '{level}' possui apenas {len(level_selected)} "
                f"funcoes elegiveis (alvo: {target_n})."
            )

    selected = pd.concat(selected_parts, ignore_index=True)
    selected["repository"] = REPOSITORY_NAME

    return selected.sort_values(
        by=["complexity_level", "file_path", "function_name"]
    ).reset_index(drop=True)


def main() -> None:
    if not BASE_REPO_PATH.exists():
        raise FileNotFoundError(f"Repositorio nao encontrado: {BASE_REPO_PATH}")

    extracted = extract_functions(BASE_REPO_PATH)
    analyzed_total = len(extracted)

    if analyzed_total == 0:
        raise RuntimeError("Nenhuma funcao encontrada no repositorio scikit-learn.")

    complexity_data = extracted["source_code"].apply(measure_complexity)
    extracted["complexity_score"] = complexity_data.apply(lambda item: item[0])
    extracted["radon_rank"] = complexity_data.apply(lambda item: item[1])
    extracted["complexity_level"] = complexity_data.apply(lambda item: item[2])

    candidates = filter_candidates(extracted)
    importable_count = len(candidates)
    selected = build_sample(candidates)

    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    selected[OUTPUT_COLUMNS].to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8")

    print(f"Total de funcoes analisadas: {analyzed_total}")
    print(f"Candidatos importaveis (sklearn pip): {importable_count}")
    print(f"Total selecionado: {len(selected)}")
    print("Distribuicao por complexidade:")
    if selected.empty:
        print("(nenhuma funcao selecionada)")
    else:
        print(selected["complexity_level"].value_counts().to_string())
    print(f"Arquivo salvo em: {OUTPUT_CSV_PATH.relative_to(BASE_DIR).as_posix()}")


if __name__ == "__main__":
    main()
