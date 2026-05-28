"""
Padronização de colunas em CSVs da pipeline do experimento.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

import pandas as pd

FUNCTION_ALIASES = ("function", "nome_funcao", "target_function")
TEST_FILE_ALIASES = ("file_name",)


def _looks_like_test_file(value: object) -> bool:
    text = str(value).replace("\\", "/").strip()
    if not text:
        return False
    name = Path(text).name.lower()
    return name.startswith("test_") or "/test_" in text.lower() or "tests/generated" in text.lower()


def infer_function_name_from_test_file(test_file: object) -> str:
    """Extrai nome da função a partir de test_XXX_<func>.py (compatibilidade retroativa)."""
    stem = Path(str(test_file).replace("\\", "/")).stem
    match = re.match(r"test_\d+_(.+)", stem, flags=re.IGNORECASE)
    if match:
        return match.group(1)
    if stem.lower().startswith("test_"):
        return stem[5:]
    return stem


def standardize_function_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Garante coluna function_name.

    Renomeia aliases conhecidos. Se só existir file_name e os valores
    não parecerem arquivos de teste, trata file_name como function_name.
    Se file_name for caminho de teste, infere function_name a partir do nome do arquivo.
    """
    out = df.copy()

    if "function_name" not in out.columns:
        for alias in FUNCTION_ALIASES:
            if alias in out.columns:
                out = out.rename(columns={alias: "function_name"})
                break

    if "function_name" not in out.columns and "file_name" in out.columns:
        series = out["file_name"].dropna()
        if series.empty:
            out = out.rename(columns={"file_name": "function_name"})
        elif series.map(_looks_like_test_file).mean() >= 0.5:
            out = standardize_test_file_column(out, source_column="file_name")
            if "test_file" in out.columns:
                out["function_name"] = out["test_file"].map(infer_function_name_from_test_file)
        else:
            out = out.rename(columns={"file_name": "function_name"})

    if "function_name" in out.columns:
        out["function_name"] = out["function_name"].astype(str).str.strip()

    return out


def standardize_test_file_column(
    df: pd.DataFrame,
    *,
    source_column: str = "file_name",
) -> pd.DataFrame:
    """Garante coluna test_file (a partir de file_name ou caminhos legados)."""
    out = df.copy()

    if "test_file" not in out.columns:
        for alias in TEST_FILE_ALIASES:
            if alias in out.columns:
                out = out.rename(columns={alias: "test_file"})
                break

    if "test_file" not in out.columns and source_column in out.columns:
        out = out.rename(columns={source_column: "test_file"})

    if "test_file" in out.columns:
        out["test_file"] = out["test_file"].astype(str).str.strip()

    return out


def validate_required_columns(
    df: pd.DataFrame,
    required: Iterable[str],
    source_name: str,
) -> None:
    """Valida presença de colunas obrigatórias; erro amigável se faltar alguma."""
    missing = [col for col in required if col not in df.columns]
    if not missing:
        return

    available = list(df.columns)
    lines = [
        "ERRO:",
        f"CSV {source_name} não possui coluna(s) obrigatória(s): {', '.join(missing)}.",
        "Colunas encontradas:",
        str(available),
    ]
    raise ValueError("\n".join(lines))


def log_dataframe_info(label: str, df: pd.DataFrame, *, source: str | Path | None = None) -> None:
    """Log padronizado de dataframe carregado."""
    src = f" ({source})" if source is not None else ""
    print(f"[OK] {label} carregado{src}")
    print(f"Linhas: {len(df)}")
    print(f"Colunas: {list(df.columns)}")
    print()


def prepare_csv_for_save(df: pd.DataFrame) -> pd.DataFrame:
    """Padroniza colunas antes de salvar CSV na pipeline."""
    return standardize_test_file_column(standardize_function_column(df))
