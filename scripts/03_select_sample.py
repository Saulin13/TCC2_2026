from __future__ import annotations

import argparse
import random
import unicodedata
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CSV_PATH = BASE_DIR / "data" / "raw" / "functions_with_complexity.csv"
OUTPUT_MAIN_CSV_PATH = BASE_DIR / "data" / "selected_functions" / "sample_thealgorithms_60.csv"
OUTPUT_PILOT_CSV_PATH = BASE_DIR / "data" / "selected_functions" / "pilot_sample_30.csv"

SAMPLE_SIZE_PER_LEVEL = 20
PILOT_SAMPLE_SIZE_PER_LEVEL = 10
RANDOM_STATE = 42

EXCLUDED_PATH_SEGMENTS = frozenset(
    {"computer_vision", "digital_image_processing", "project_euler"}
)

EXCLUDED_FUNCTION_NAMES = frozenset({"solution", "search", "put", "score"})

GENERIC_FUNCTION_NAMES = frozenset(
    {
        "main",
        "run",
        "helper",
        "wrapper",
        "callback",
        "handler",
        "inner",
        "process",
        "execute",
        "validate",
        "default",
        "result",
        "results",
        "utils",
        "util",
        "temp",
        "tmp",
        "foo",
        "bar",
        "demo",
        "example",
        "unknown",
        "misc",
        "value",
        "values",
        "data",
        "item",
        "items",
        "obj",
        "instance",
        "worker",
        "task",
        "job",
        "fn",
        "func",
        "call",
        "go",
        "do",
        "work",
    }
)

FORBIDDEN_SOURCE_SUBSTRINGS = (
    "import cv2",
    "from cv2",
    "import imageio",
    "import tensorflow",
    "import torch",
    "import sklearn",
    "from sklearn",
)


def normalize_text(value: str) -> str:
    """Normaliza texto para comparacoes robustas (sem acentos, minusculo)."""
    if not isinstance(value, str):
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    without_accents = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return without_accents.strip().lower()


def normalize_complexity_level(value: str) -> str:
    """Mapeia variacoes de rotulos para baixa/media/alta."""
    norm = normalize_text(value)
    if norm in {"baixa", "low"}:
        return "baixa"
    if norm in {"media", "medium"}:
        return "media"
    if norm in {"alta", "high"}:
        return "alta"
    return norm


def count_useful_lines(source_code: str) -> int:
    """Conta linhas uteis (nao vazias e que nao sao apenas comentario)."""
    if not isinstance(source_code, str):
        return 0

    useful = 0
    for line in source_code.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        useful += 1
    return useful


def _path_has_excluded_segment(file_path: str) -> bool:
    parts = {p.lower() for p in Path(str(file_path).replace("\\", "/")).parts}
    return bool(EXCLUDED_PATH_SEGMENTS.intersection(parts))


def _source_has_forbidden_imports(source_code: str) -> bool:
    s = (source_code or "").lower()
    return any(sub in s for sub in FORBIDDEN_SOURCE_SUBSTRINGS)


def _is_likely_top_level_function(source_code: str) -> bool:
    """
    Heuristica: a primeira declaracao def/async def util deve estar na coluna 0
    (nao metodo de classe nem funcao aninhada).
    Ignora comentarios e decoradores iniciais.
    """
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


def _is_too_generic_name(function_name: str) -> bool:
    fn = normalize_text(function_name)
    if not fn:
        return True
    if fn in GENERIC_FUNCTION_NAMES:
        return True
    if len(fn) <= 2:
        return True
    return False


def select_with_file_diversity(df_level: pd.DataFrame, target_n: int) -> pd.DataFrame:
    """
    Seleciona funcoes priorizando diversidade de arquivos.

    Estrategia:
    - embaralha linhas por arquivo;
    - faz selecao em rodadas, pegando no maximo uma funcao por arquivo por rodada;
    - repete ate atingir o alvo ou esgotar candidatos.
    """
    if df_level.empty:
        return df_level.copy()

    rng = random.Random(RANDOM_STATE)

    file_to_indices: dict[str, list[int]] = {}
    for file_path, group in df_level.groupby("file_path"):
        indices = group.index.tolist()
        rng.shuffle(indices)
        file_to_indices[file_path] = indices

    files = list(file_to_indices.keys())
    rng.shuffle(files)

    selected_indices: list[int] = []
    while len(selected_indices) < target_n:
        picked_in_round = False
        for file_path in files:
            candidates = file_to_indices[file_path]
            if not candidates:
                continue
            selected_indices.append(candidates.pop(0))
            picked_in_round = True
            if len(selected_indices) >= target_n:
                break

        if not picked_in_round:
            break

    return df_level.loc[selected_indices].copy()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seleciona amostra estratificada por complexidade no TheAlgorithms/Python."
    )
    parser.add_argument(
        "--sample-size-per-level",
        type=int,
        default=SAMPLE_SIZE_PER_LEVEL,
        help=f"Quantidade de funcoes por nivel (padrao: {SAMPLE_SIZE_PER_LEVEL}).",
    )
    parser.add_argument(
        "--pilot",
        action="store_true",
        help=(
            "Gera arquivo piloto pilot_sample_30.csv com tamanho por nivel "
            f"{PILOT_SAMPLE_SIZE_PER_LEVEL}."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    target_per_level = args.sample_size_per_level
    output_csv_path = OUTPUT_MAIN_CSV_PATH

    if args.pilot:
        target_per_level = PILOT_SAMPLE_SIZE_PER_LEVEL
        output_csv_path = OUTPUT_PILOT_CSV_PATH

    if target_per_level <= 0:
        raise ValueError("--sample-size-per-level deve ser maior que zero.")

    if not INPUT_CSV_PATH.exists():
        raise FileNotFoundError(f"Arquivo de entrada nao encontrado: {INPUT_CSV_PATH}")

    df = pd.read_csv(INPUT_CSV_PATH)

    required_columns = {"function_name", "file_path", "source_code", "complexity_level"}
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Colunas obrigatorias ausentes no CSV: {sorted(missing)}")

    df["complexity_level"] = df["complexity_level"].apply(normalize_complexity_level)
    df["total_lines"] = df["source_code"].fillna("").apply(lambda s: len(str(s).splitlines()))
    df["useful_lines"] = df["source_code"].fillna("").apply(count_useful_lines)

    fn_lower = df["function_name"].fillna("").str.strip().str.lower()
    fp_series = df["file_path"].fillna("")

    mask_path = ~fp_series.map(_path_has_excluded_segment)
    mask_names = ~fn_lower.isin(EXCLUDED_FUNCTION_NAMES)
    mask_generic = ~df["function_name"].fillna("").map(
        lambda x: _is_too_generic_name(str(x))
    )
    mask_imports = ~df["source_code"].fillna("").map(_source_has_forbidden_imports)
    mask_top_level = df["source_code"].fillna("").map(_is_likely_top_level_function)

    filtered = df[
        (~df["function_name"].fillna("").str.startswith("_"))
        & (~df["function_name"].fillna("").str.startswith("test_"))
        & (df["useful_lines"] >= 3)
        & (df["total_lines"] <= 80)
        & mask_path
        & mask_names
        & mask_generic
        & mask_imports
        & mask_top_level
    ].copy()

    selected_parts: list[pd.DataFrame] = []
    for level in ("baixa", "media", "alta"):
        level_candidates = filtered[filtered["complexity_level"] == level].copy()
        level_selected = select_with_file_diversity(level_candidates, target_per_level)
        selected_parts.append(level_selected)

        if len(level_selected) < target_per_level:
            print(
                f"Aviso: nivel '{level}' possui apenas {len(level_selected)} "
                f"funcoes elegiveis (alvo: {target_per_level})."
            )

    selected = pd.concat(selected_parts, ignore_index=True)
    selected = selected.sort_values(
        by=["complexity_level", "file_path", "function_name"]
    ).reset_index(drop=True)

    output_csv_path.parent.mkdir(parents=True, exist_ok=True)
    selected.to_csv(output_csv_path, index=False, encoding="utf-8")

    print(f"Total selecionado: {len(selected)}")
    print("Distribuicao por nivel:")
    print(selected["complexity_level"].value_counts().to_string())
    print(f"Arquivo salvo em: {output_csv_path.relative_to(BASE_DIR).as_posix()}")


if __name__ == "__main__":
    main()
