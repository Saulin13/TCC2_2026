from __future__ import annotations

from pathlib import Path

import pandas as pd
import textwrap
from radon.complexity import cc_rank, cc_visit

INPUT_CSV_PATH = Path("data/raw/functions_extracted.csv")
OUTPUT_CSV_PATH = Path("data/raw/functions_with_complexity.csv")


def classify_complexity_level(score: int) -> str:
    """Classifica o nivel de complexidade com base no escore."""
    if score <= 5:
        return "baixa"
    if score <= 10:
        return "media"
    return "alta"


def measure_complexity(source_code: str) -> tuple[int, str, str]:
    """
    Calcula complexidade ciclomatica para um trecho de codigo de funcao.

    Retorna:
    - complexity_score
    - radon_rank
    - complexity_level
    """
    if not isinstance(source_code, str) or not source_code.strip():
        score = 0
        return score, cc_rank(score), classify_complexity_level(score)

    try:
        clean_code = textwrap.dedent(source_code).strip()
        blocks = cc_visit(clean_code)

        if not blocks:
            score = 0
        else:
            score = max(block.complexity for block in blocks)

        return score, cc_rank(score), classify_complexity_level(score)

    except Exception as e:
        print(f"Erro ao medir complexidade em uma funcao: {e}")
        score = 0
        return score, cc_rank(score), classify_complexity_level(score)


def main() -> None:
    if not INPUT_CSV_PATH.exists():
        raise FileNotFoundError(f"Arquivo de entrada nao encontrado: {INPUT_CSV_PATH}")

    df = pd.read_csv(INPUT_CSV_PATH)

    required_columns = {"function_name", "file_path", "start_line", "end_line", "source_code"}
    missing = required_columns.difference(df.columns)
    if missing:
        raise ValueError(f"Colunas obrigatorias ausentes no CSV: {sorted(missing)}")

    complexity_data = df["source_code"].apply(measure_complexity)
    df["complexity_score"] = complexity_data.apply(lambda item: item[0])
    df["radon_rank"] = complexity_data.apply(lambda item: item[1])
    df["complexity_level"] = complexity_data.apply(lambda item: item[2])

    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8")

    print(f"Funcoes processadas: {len(df)}")
    print(f"Arquivo salvo em: {OUTPUT_CSV_PATH.resolve()}")


if __name__ == "__main__":
    main()
