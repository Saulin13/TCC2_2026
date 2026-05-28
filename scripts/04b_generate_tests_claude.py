import argparse
import os
import re
from pathlib import Path

import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv

from dataset_config import (
    BASE_DIR,
    add_dataset_argument,
    resolve_dataset,
    resolve_module_path_from_row,
)

PROMPT_TEMPLATE_PATH = BASE_DIR / "prompts" / "prompt_generate_tests.txt"

DEFAULT_CLAUDE_MODEL = "claude-3-5-sonnet-latest"
MAX_TOKENS = 4096
TEMPERATURE = 0.2


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
    """Substitui placeholders do template; {file_code} por ultimo."""
    return (
        template.replace("{func_name}", func_name)
        .replace("{module_path}", module_path)
        .replace("{file_code}", file_code)
    )


def _extract_claude_text(response: object) -> str:
    content = getattr(response, "content", None)
    if not content:
        return ""

    parts: list[str] = []
    for item in content:
        if getattr(item, "type", None) == "text":
            parts.append(getattr(item, "text", ""))
    return "\n".join(parts).strip()


def generate_test_with_claude(
    client: Anthropic,
    model_name: str,
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
    response = client.messages.create(
        model=model_name,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = _extract_claude_text(response)
    return prompt, _strip_llm_markdown_code(raw)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gera testes com Claude a partir de uma amostra de funcoes."
    )
    add_dataset_argument(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    input_sample = cfg.sample_csv
    repo_path = cfg.repo_path
    output_tests_dir = cfg.tests_dir("claude")
    output_prompts_dir = cfg.prompts_dir("claude")

    load_dotenv(BASE_DIR / ".env")

    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    model_name = os.getenv("CLAUDE_MODEL", "").strip() or DEFAULT_CLAUDE_MODEL

    if not api_key:
        print("Erro: ANTHROPIC_API_KEY não encontrado no .env.")
        return

    if not input_sample.exists():
        print(f"Erro: arquivo não encontrado: {input_sample}")
        return

    if not PROMPT_TEMPLATE_PATH.exists():
        print(f"Erro: template de prompt não encontrado: {PROMPT_TEMPLATE_PATH}")
        return

    if not repo_path.exists():
        print(f"Erro: repositório não encontrado: {repo_path}")
        return

    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    df = pd.read_csv(input_sample)

    output_tests_dir.mkdir(parents=True, exist_ok=True)
    output_prompts_dir.mkdir(parents=True, exist_ok=True)

    client = Anthropic(api_key=api_key)
    total = len(df)

    for pos, (_, row) in enumerate(df.iterrows(), start=1):
        func_name = str(row.get("function_name", "")).strip()
        file_path = str(row.get("file_path", "")).strip()
        file_code = str(row.get("source_code", ""))

        if not func_name or not file_path:
            print(f"[{pos}/{total}] linha inválida (sem function_name/file_path), pulando.")
            continue

        module_path = resolve_module_path_from_row(row, dataset_key=cfg.key)
        stem = f"{pos:03d}_{func_name}"
        prompt_path = output_prompts_dir / f"prompt_{stem}.txt"
        test_path = output_tests_dir / f"test_{stem}.py"

        print(f"[{pos}/{total}] Gerando teste para {func_name}...")
        try:
            prompt, test_code = generate_test_with_claude(
                client,
                model_name,
                template,
                func_name=func_name,
                module_path=module_path,
                file_code=file_code,
            )
            prompt_path.write_text(prompt, encoding="utf-8")
            test_path.write_text(test_code, encoding="utf-8")
        except Exception as e:  # noqa: BLE001
            print(f"[{pos}/{total}] Erro ao gerar {func_name}: {e}")
            continue

    print(f"\nDataset: {cfg.key}")
    print(f"Sucesso! Prompts em: {output_prompts_dir}")
    print(f"Testes em: {output_tests_dir}")
    print(f"Modelo Claude usado: {model_name}")


if __name__ == "__main__":
    main()
