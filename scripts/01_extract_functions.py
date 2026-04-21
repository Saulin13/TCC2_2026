from __future__ import annotations

import ast
from pathlib import Path

import pandas as pd

# Configure aqui o caminho base do repositorio a ser analisado.
# Exemplo: BASE_REPO_PATH = Path("repos/Python")
BASE_REPO_PATH = Path("repos/Python")

OUTPUT_CSV_PATH = Path("data/raw/functions_extracted.csv")
IGNORED_DIR_KEYWORDS = ("test", "tests")
IGNORED_FILE_PREFIX = "test_"


def should_ignore_file(file_path: Path) -> bool:
    """Retorna True se o arquivo deve ser ignorado."""
    if file_path.name.startswith(IGNORED_FILE_PREFIX):
        return True

    dir_parts = [part.lower() for part in file_path.parts[:-1]]
    return any(keyword in dir_parts for keyword in IGNORED_DIR_KEYWORDS)


def get_source_segment(lines: list[str], start_line: int, end_line: int) -> str:
    """Extrai trecho de codigo-fonte entre linhas (1-indexado, inclusivo)."""
    return "\n".join(lines[start_line - 1 : end_line])


def extract_functions_from_file(file_path: Path, base_path: Path) -> list[dict]:
    """Extrai funcoes `def` de um arquivo Python usando AST."""
    try:
        source_code = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        source_code = file_path.read_text(encoding="latin-1")

    source_lines = source_code.splitlines()
    tree = ast.parse(source_code, filename=str(file_path))

    records: list[dict] = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start_line = node.lineno
            end_line = getattr(node, "end_lineno", node.lineno)

            records.append(
                {
                    "function_name": node.name,
                    "file_path": str(file_path.relative_to(base_path)),
                    "start_line": start_line,
                    "end_line": end_line,
                    "source_code": get_source_segment(
                        source_lines, start_line=start_line, end_line=end_line
                    ),
                }
            )

    return records


def extract_functions(base_repo_path: Path) -> pd.DataFrame:
    """Percorre todos os .py e retorna DataFrame com funcoes extraidas."""
    all_records: list[dict] = []

    for py_file in base_repo_path.rglob("*.py"):
        if should_ignore_file(py_file):
            continue

        try:
            file_records = extract_functions_from_file(py_file, base_repo_path)
            all_records.extend(file_records)
        except (SyntaxError, ValueError):
            # Ignora arquivos com sintaxe invalida ou caminho inesperado.
            continue

    return pd.DataFrame(
        all_records,
        columns=["function_name", "file_path", "start_line", "end_line", "source_code"],
    )


def main() -> None:
    if not BASE_REPO_PATH.exists():
        raise FileNotFoundError(
            f"Caminho base nao encontrado: {BASE_REPO_PATH.resolve()}"
        )

    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = extract_functions(BASE_REPO_PATH)
    df.to_csv(OUTPUT_CSV_PATH, index=False, encoding="utf-8")

    print(f"Funcoes extraidas: {len(df)}")
    print(f"Arquivo salvo em: {OUTPUT_CSV_PATH.resolve()}")


if __name__ == "__main__":
    main()
