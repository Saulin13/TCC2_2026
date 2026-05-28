import argparse
import os
import re
from pathlib import Path

import pandas as pd

from csv_columns import (
    infer_function_name_from_test_file,
    prepare_csv_for_save,
    validate_required_columns,
)
from dataset_config import BASE_DIR, add_dataset_argument, resolve_dataset

OUTPUT_COLUMNS = (
    "function_name",
    "test_file",
    "test_loc",
    "assertion_count",
    "assertion_density",
)


def calcular_metricas_codigo(caminho_arquivo: Path) -> tuple[int, int]:
    with open(caminho_arquivo, encoding="utf-8") as f:
        linhas = f.readlines()

    linhas_codigo = [
        l.strip() for l in linhas if l.strip() and not l.strip().startswith("#")
    ]
    total_loc = len(linhas_codigo)

    if total_loc == 0:
        return 0, 0

    conteudo_completo = "".join(linhas_codigo)
    assercoes = re.findall(r"\bassert\b", conteudo_completo)
    return total_loc, len(assercoes)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calcula densidade de asserções nos testes gerados (GPT)."
    )
    parser.add_argument(
        "--generator",
        choices=("gpt", "claude"),
        default="gpt",
        help="Gerador dos testes analisados (padrão: gpt).",
    )
    add_dataset_argument(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    tests_dir = cfg.tests_dir(args.generator)
    output_csv = cfg.result_csv("metrica_densidade_asserts")

    print(f"Dataset: {cfg.key} | Gerador: {args.generator}")
    print("Iniciando cálculo de Densidade de Asserções nos testes Python...")

    if not tests_dir.exists():
        print(f"Erro: Diretório de testes não encontrado em {tests_dir}")
        return

    resultados: list[dict[str, object]] = []

    for root, _, files in os.walk(tests_dir):
        for file in files:
            if file.endswith(".py") and file.startswith("test_"):
                caminho_completo = Path(root) / file
                loc, asserts = calcular_metricas_codigo(caminho_completo)
                densidade = round(asserts / loc, 4) if loc > 0 else 0.0
                try:
                    test_file = str(caminho_completo.relative_to(BASE_DIR))
                except ValueError:
                    test_file = str(caminho_completo)
                resultados.append(
                    {
                        "function_name": infer_function_name_from_test_file(file),
                        "test_file": test_file,
                        "test_loc": loc,
                        "assertion_count": asserts,
                        "assertion_density": densidade,
                    }
                )

    if not resultados:
        print("Nenhum arquivo test_*.py encontrado para análise.")
        return

    df = prepare_csv_for_save(pd.DataFrame(resultados)[list(OUTPUT_COLUMNS)])
    validate_required_columns(df, ("function_name", "test_file"), output_csv.name)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"Métrica de Densidade de Asserções salva em: {output_csv}")


if __name__ == "__main__":
    main()
