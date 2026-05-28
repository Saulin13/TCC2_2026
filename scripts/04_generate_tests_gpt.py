import argparse
import re
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

from dataset_config import (
    BASE_DIR,
    add_dataset_argument,
    resolve_dataset,
    resolve_module_path_from_row,
)

PROMPT_TEMPLATE_PATH = BASE_DIR / "prompts" / "prompt_generate_tests.txt"

MODEL_NAME = "gpt-4o"
CLEAN_PREVIOUS_OUTPUTS = True


def _strip_llm_markdown_code(text: str) -> str:
    """Remove cercas markdown (```python, ```) da resposta da LLM."""
    if not text:
        return ""
    t = text.strip()
    m = re.match(
        r"^```(?:python|py)?\s*\r?\n(.*)\r?\n```\s*$",
        t,
        re.DOTALL,
    )
    if m:
        return m.group(1).strip()
    t = re.sub(r"^```(?:python|py)?\s*\r?\n?", "", t)
    t = re.sub(r"\r?\n?```\s*$", "", t)
    return t.strip()


def _build_prompt(
    template: str, *, func_name: str, module_path: str, file_code: str
) -> str:
    """Substitui placeholders do template; {file_code} por último (pode conter chaves)."""
    return (
        template.replace("{func_name}", func_name)
        .replace("{module_path}", module_path)
        .replace("{file_code}", file_code)
    )


def generate_test_with_gpt(
    client: OpenAI,
    template: str,
    *,
    func_name: str,
    module_path: str,
    file_code: str,
) -> tuple[str, str]:
    prompt = _build_prompt(
        template,
        func_name=func_name,
        module_path=module_path,
        file_code=file_code,
    )
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    raw = response.choices[0].message.content or ""
    return prompt, _strip_llm_markdown_code(raw)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera testes com GPT a partir de uma amostra de funcoes."
    )
    parser.add_argument(
        "--input-sample",
        type=Path,
        default=None,
        help=(
            "Caminho do CSV de entrada. Se nao informado, usa INPUT_SAMPLE "
            "(sample_thealgorithms_60.csv)."
        ),
    )
    parser.add_argument(
        "--pilot",
        action="store_true",
        help="Usa amostra piloto do dataset (apenas thealgorithms).",
    )
    add_dataset_argument(parser)
    return parser.parse_args()


def resolve_input_sample(args: argparse.Namespace, cfg: DatasetConfig) -> Path:
    if args.input_sample is not None:
        return args.input_sample if args.input_sample.is_absolute() else (BASE_DIR / args.input_sample)
    return cfg.resolve_sample(pilot=args.pilot)


def clean_previous_outputs(prompts_dir: Path, tests_dir: Path) -> None:
    if not CLEAN_PREVIOUS_OUTPUTS:
        return

    prompt_files = list(prompts_dir.glob("prompt_*.txt"))
    test_files = list(tests_dir.glob("test_*.py"))

    for file_path in prompt_files + test_files:
        file_path.unlink(missing_ok=True)

    if prompt_files or test_files:
        print(
            "Arquivos anteriores removidos para evitar sobrescrita confusa "
            f"({len(prompt_files)} prompts, {len(test_files)} testes)."
        )


def main():
    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    input_sample = resolve_input_sample(args, cfg)
    output_prompts_dir = cfg.prompts_dir("gpt")
    output_tests_dir = cfg.tests_dir("gpt")

    load_dotenv(BASE_DIR / ".env")

    if not input_sample.exists():
        print(f"Erro: arquivo não encontrado: {input_sample}")
        return

    if not PROMPT_TEMPLATE_PATH.exists():
        print(f"Erro: template de prompt não encontrado: {PROMPT_TEMPLATE_PATH}")
        return

    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    client = OpenAI()

    df = pd.read_csv(input_sample)
    output_prompts_dir.mkdir(parents=True, exist_ok=True)
    output_tests_dir.mkdir(parents=True, exist_ok=True)
    clean_previous_outputs(output_prompts_dir, output_tests_dir)

    n = len(df)
    for pos, (_, row) in enumerate(df.iterrows()):
        seq = pos + 1
        func_name = str(row["function_name"])
        module_path = resolve_module_path_from_row(row, dataset_key=cfg.key)
        file_code = str(row["source_code"])

        stem = f"{seq:03d}_{func_name}"
        prompt_path = output_prompts_dir / f"prompt_{stem}.txt"
        test_path = output_tests_dir / f"test_{stem}.py"

        print(f"Gerando teste {seq}/{n}: {func_name}...")

        prompt, test_code = generate_test_with_gpt(
            client,
            template,
            func_name=func_name,
            module_path=module_path,
            file_code=file_code,
        )
        prompt_path.write_text(prompt, encoding="utf-8")
        test_path.write_text(test_code, encoding="utf-8")

    print(f"\nDataset: {cfg.key}")
    print(f"Amostra usada: {input_sample}")
    print(f"Sucesso! Prompts em: {output_prompts_dir}")
    print(f"Testes em: {output_tests_dir}")


if __name__ == "__main__":
    main()
