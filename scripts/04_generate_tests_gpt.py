import re
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Raiz do projeto; todos os caminhos são relativos a ela
BASE_DIR = Path(__file__).resolve().parent.parent

PROMPT_TEMPLATE_PATH = BASE_DIR / "prompts" / "prompt_generate_tests.txt"
INPUT_SAMPLE = BASE_DIR / "data" / "selected_functions" / "pilot_sample_30.csv"
OUTPUT_PROMPTS_DIR = BASE_DIR / "data" / "results" / "generated_prompts"
OUTPUT_TESTS_DIR = BASE_DIR / "tests" / "generated"

MODEL_NAME = "gpt-4o"


def _file_path_to_module_path(file_path: str) -> str:
    """Ex.: ciphers/foo.py -> ciphers.foo"""
    p = Path(str(file_path).replace("\\", "/"))
    return ".".join(p.with_suffix("").parts)


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


def main():
    load_dotenv(BASE_DIR / ".env")

    if not INPUT_SAMPLE.exists():
        print(f"Erro: arquivo não encontrado: {INPUT_SAMPLE}")
        return

    if not PROMPT_TEMPLATE_PATH.exists():
        print(f"Erro: template de prompt não encontrado: {PROMPT_TEMPLATE_PATH}")
        return

    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    client = OpenAI()

    df = pd.read_csv(INPUT_SAMPLE)
    OUTPUT_PROMPTS_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_TESTS_DIR.mkdir(parents=True, exist_ok=True)

    n = len(df)
    for pos, (_, row) in enumerate(df.iterrows()):
        seq = pos + 1
        func_name = str(row["function_name"])
        module_path = _file_path_to_module_path(str(row["file_path"]))
        file_code = str(row["source_code"])

        stem = f"{seq:03d}_{func_name}"
        prompt_path = OUTPUT_PROMPTS_DIR / f"prompt_{stem}.txt"
        test_path = OUTPUT_TESTS_DIR / f"test_{stem}.py"

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

    print(f"\nSucesso! Prompts em: {OUTPUT_PROMPTS_DIR}")
    print(f"Testes em: {OUTPUT_TESTS_DIR}")


if __name__ == "__main__":
    main()
