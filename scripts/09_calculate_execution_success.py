import argparse

import pandas as pd

from csv_columns import (
    log_dataframe_info,
    prepare_csv_for_save,
    standardize_function_column,
    validate_required_columns,
)
from dataset_config import add_dataset_argument, resolve_dataset

OUTPUT_COLUMNS = ("function_name", "execution_category")


def categorizar_sucesso(row: pd.Series) -> str:
    status = str(row.get("execution_status", "")).lower()
    passed = row.get("passed", False)
    stderr = str(row.get("stderr", "")).lower()

    if passed is True or passed == "True" or passed == "true" or "success" in status:
        return "Sucesso Direto (Pass Rate)"
    if "syntaxerror" in stderr or "indentationerror" in stderr or "syntax" in stderr:
        return "Erro de Sintaxe/Compilação"
    return "Falha de Execução (Runtime/Assertion Error)"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classifica taxa de sucesso de execução dos testes avaliados pelo GPT."
    )
    add_dataset_argument(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    input_eval = cfg.result_csv("avaliacao_gpt_sobre_testes_gpt")
    output_csv = cfg.result_csv("metrica_sucesso_execucao")

    print(f"Dataset: {cfg.key}")
    print("Iniciando classificação da Taxa de Sucesso e Execução dos testes Python...")

    if not input_eval.exists():
        print(f"Erro: Arquivo base {input_eval} não encontrado.")
        return

    df = standardize_function_column(pd.read_csv(input_eval))
    log_dataframe_info("df_eval (entrada)", df, source=input_eval.name)
    validate_required_columns(
        df,
        ["function_name", "execution_status"],
        input_eval.name,
    )

    df["execution_category"] = df.apply(categorizar_sucesso, axis=1)
    df_resultado = prepare_csv_for_save(
        df[list(OUTPUT_COLUMNS)].drop_duplicates(subset=["function_name"])
    )
    validate_required_columns(df_resultado, OUTPUT_COLUMNS, output_csv.name)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df_resultado.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"Métrica de Taxa de Sucesso salva em: {output_csv}")

    print("\nResumo Geral da Taxa de Sucesso da IA:")
    resumo = df["execution_category"].value_counts(normalize=True) * 100
    for cat, val in resumo.items():
        print(f" - {cat}: {val:.2f}%")


if __name__ == "__main__":
    main()
