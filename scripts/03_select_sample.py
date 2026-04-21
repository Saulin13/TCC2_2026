from __future__ import annotations

import random
import unicodedata
from pathlib import Path

import pandas as pd

INPUT_CSV_PATH = Path("data/raw/functions_with_complexity.csv")
OUTPUT_CSV_PATH = Path("data/selected_functions/pilot_sample_30.csv")

TARGET_PER_LEVEL = 10
RANDOM_SEED = 42


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

    rng = random.Random(RANDOM_SEED)

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


def main() -> None:
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

    filtered = df[
        (~df["function_name"].fillna("").str.startswith("_"))
        & (~df["function_name"].fillna("").str.startswith("test_"))
        & (df["useful_lines"] >= 3)
        & (df["total_lines"] <= 80)
    ].copy()

    selected_parts: list[pd.DataFrame] = []
    for level in ("baixa", "media", "alta"):
        level_candidates = filtered[filtered["complexity_level"] == level].copy()
        level_selected = select_with_file_diversity(level_candidates, TARGET_PER_LEVEL)
        selected_parts.append(level_selected)

        if len(level_selected) < TARGET_PER_LEVEL:
            print(
                f"Aviso: nivel '{level}' possui apenas {len(level_selected)} "
                f"funcoes elegiveis (alvo: {TARGET_PER_LEVEL})."
            )

    selected = pd.concat(selected_parts, ignore_index=True)
    selected = selected.sort_values(
        by=["complexity_level", "file_path", "function_name"]
    ).reset_index(drop=True)

    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    selected.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8")

    print(f"Total selecionado: {len(selected)}")
    print("Distribuicao por nivel:")
    print(selected["complexity_level"].value_counts().to_string())
    print(f"Arquivo salvo em: {OUTPUT_CSV_PATH.resolve()}")


if __name__ == "__main__":
    main()
