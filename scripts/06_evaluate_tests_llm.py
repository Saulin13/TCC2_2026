import json
import math
import os
import re
import unicodedata
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Raiz do projeto; todos os caminhos são relativos a ela
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_TEMPLATE_PATH = BASE_DIR / "prompts" / "prompt_evaluate_tests.txt"
INPUT_COVERAGE = BASE_DIR / "data" / "results" / "coverage_results.csv"
SAMPLE_FILE = BASE_DIR / "data" / "selected_functions" / "pilot_sample_30.csv"
OUTPUT_EVAL = BASE_DIR / "data" / "results" / "evaluation_results_gpt.csv"

MODEL_NAME = "gpt-4o"  # padrão; sobrescrito por OPENAI_MODEL no .env
EXEC_LOG_MAX_CHARS = 4000
RANDOM_SEED = 42
SAMPLE_BY_LEVEL = {"baixa": 4, "media": 3, "alta": 3}
MERGE_KEYS = ("function_name", "file_path")


def resolve_model_name() -> str:
    """Modelo OpenAI: variável de ambiente OPENAI_MODEL ou padrão do script."""
    return (os.getenv("OPENAI_MODEL") or os.getenv("MODEL_NAME") or MODEL_NAME).strip()


def _normalize_text(value: str) -> str:
    if not isinstance(value, str):
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    without_accents = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return without_accents.strip().lower()


def normalize_complexity_level(value: object) -> str:
    """Mapeia rótulos de complexidade para baixa/media/alta."""
    norm = _normalize_text(str(value) if value is not None else "")
    if norm in {"baixa", "low"}:
        return "baixa"
    if norm in {"media", "medium"}:
        return "media"
    if norm in {"alta", "high"}:
        return "alta"
    return norm


def select_balanced_sample(df: pd.DataFrame) -> pd.DataFrame:
    """Seleciona amostra balanceada: 4 baixa, 3 média, 3 alta."""
    work = df.copy()
    work["complexity_level"] = work["complexity_level"].apply(normalize_complexity_level)
    parts: list[pd.DataFrame] = []
    for level, target in SAMPLE_BY_LEVEL.items():
        pool = work[work["complexity_level"] == level]
        available = len(pool)
        if available < target:
            print(f"Aviso: apenas {available} registro(s) em '{level}' (alvo: {target}).")
        k = min(target, available)
        if k == 0:
            continue
        parts.append(pool.sample(n=k, random_state=RANDOM_SEED))
    if not parts:
        return work.iloc[0:0]
    return pd.concat(parts, ignore_index=True)


def _parse_passed(val: object) -> bool:
    if isinstance(val, bool):
        return val
    s = str(val).strip().lower()
    return s in ("true", "1", "yes")


def _parse_return_code(val: object) -> int:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return -1
    try:
        return int(float(val))
    except (TypeError, ValueError):
        return -1


OUTPUT_COLUMNS = [
    "function_name",
    "file_path",
    "complexity_score",
    "complexity_level",
    "test_file",
    "execution_status",
    "passed",
    "return_code",
    "coverage_percent",
    "correctness_score",
    "scenario_coverage_score",
    "edge_cases_score",
    "clarity_score",
    "overall_score",
    "strengths",
    "missing_cases",
    "potential_problems",
    "evaluation_error",
]


def _strip_json_fences(text: str) -> str:
    t = (text or "").strip()
    m = re.match(
        r"^```(?:json)?\s*\r?\n(.*)\r?\n```\s*$",
        t,
        re.DOTALL | re.IGNORECASE,
    )
    if m:
        return m.group(1).strip()
    t = re.sub(r"^```(?:json)?\s*\r?\n?", "", t, flags=re.IGNORECASE)
    t = re.sub(r"\r?\n?```\s*$", "", t)
    return t.strip()


def _build_execution_summary(row: pd.Series) -> str:
    lines = [
        f"execution_status: {row['execution_status']}",
        f"passed: {row['passed']}",
        f"return_code: {_parse_return_code(row['return_code'])}",
    ]
    stdout = str(row.get("stdout") or "")
    stderr = str(row.get("stderr") or "")
    if stderr.strip():
        lines.append("")
        lines.append("stderr (trecho):")
        lines.append(stderr[:EXEC_LOG_MAX_CHARS])
    if stdout.strip():
        lines.append("")
        lines.append("stdout (trecho):")
        lines.append(stdout[:EXEC_LOG_MAX_CHARS])
    return "\n".join(lines)


def _fill_prompt(template: str, row: pd.Series, *, source_code: str, test_code: str) -> str:
    cov_pct = row["coverage_percent"]
    if pd.isna(cov_pct):
        cov_str = ""
    else:
        cov_str = str(float(cov_pct))
    return (
        template.replace("<<<FUNCTION_CODE>>>", str(source_code))
        .replace("<<<TEST_CODE>>>", str(test_code))
        .replace("<<<EXECUTION_SUMMARY>>>", _build_execution_summary(row))
        .replace("<<<COVERAGE_PERCENT>>>", cov_str)
    )


def _parse_scores(raw: str) -> tuple[dict[str, object], str | None]:
    cleaned = _strip_json_fences(raw)
    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        return {}, f"JSON inválido: {e}"
    if not isinstance(data, dict):
        return {}, "Resposta não é um objeto JSON"
    return data, None


def _row_from_evaluation(
    row: pd.Series,
    scores: dict[str, object],
    err: str | None,
) -> dict[str, object]:
    def fnum(key: str) -> float:
        if err:
            return math.nan
        v = scores.get(key)
        if v is None:
            return math.nan
        try:
            return float(v)
        except (TypeError, ValueError):
            return math.nan

    def fstr(key: str) -> str:
        if err:
            return ""
        v = scores.get(key)
        return "" if v is None else str(v)

    return {
        "function_name": row["function_name"],
        "file_path": row["file_path"],
        "complexity_score": row.get("complexity_score"),
        "complexity_level": row.get("complexity_level"),
        "test_file": row["test_file"],
        "execution_status": row["execution_status"],
        "passed": _parse_passed(row["passed"]),
        "return_code": _parse_return_code(row["return_code"]),
        "coverage_percent": float(row["coverage_percent"]) if pd.notna(row["coverage_percent"]) else 0.0,
        "correctness_score": fnum("correctness_score"),
        "scenario_coverage_score": fnum("scenario_coverage_score"),
        "edge_cases_score": fnum("edge_cases_score"),
        "clarity_score": fnum("clarity_score"),
        "overall_score": fnum("overall_score"),
        "strengths": fstr("strengths"),
        "missing_cases": fstr("missing_cases"),
        "potential_problems": fstr("potential_problems"),
        "evaluation_error": err or "",
    }


def evaluate_one(
    client: OpenAI,
    template: str,
    row: pd.Series,
    *,
    model: str,
) -> dict[str, object]:
    test_rel = Path(str(row["test_file"]))
    test_path = (BASE_DIR / test_rel).resolve() if not test_rel.is_absolute() else test_rel

    source_code = row.get("source_code")
    if not isinstance(source_code, str) or not source_code.strip():
        source_code = "(código-fonte não encontrado no pilot_sample_30.csv)"

    if test_path.is_file():
        test_code = test_path.read_text(encoding="utf-8")
    else:
        test_code = f"(arquivo de teste não encontrado: {row['test_file']})"

    prompt = _fill_prompt(template, row, source_code=source_code, test_code=test_code)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    raw = response.choices[0].message.content or ""
    scores, parse_err = _parse_scores(raw)
    return _row_from_evaluation(row, scores, parse_err)


def main():
    load_dotenv(BASE_DIR / ".env")

    if not INPUT_COVERAGE.exists():
        print(f"Erro: arquivo não encontrado: {INPUT_COVERAGE}")
        return
    if not PROMPT_TEMPLATE_PATH.exists():
        print(f"Erro: template não encontrado: {PROMPT_TEMPLATE_PATH}")
        return
    if not SAMPLE_FILE.exists():
        print(f"Erro: arquivo não encontrado: {SAMPLE_FILE}")
        return

    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    client = OpenAI()
    model = resolve_model_name()

    df_cov = pd.read_csv(INPUT_COVERAGE)
    df_selected = select_balanced_sample(df_cov)
    n = len(df_selected)
    if n == 0:
        print("Nenhuma linha elegível em coverage_results.csv para avaliar.")
        return

    df_sample = pd.read_csv(SAMPLE_FILE)
    df_eval = df_selected.merge(
        df_sample[list(MERGE_KEYS) + ["source_code"]],
        on=list(MERGE_KEYS),
        how="left",
    )
    missing_source = df_eval["source_code"].isna().sum()
    if missing_source:
        print(f"Aviso: {missing_source} função(ões) sem source_code no pilot_sample_30.csv.")

    expected = sum(SAMPLE_BY_LEVEL.values())
    print(
        f"Amostra balanceada: {n} de {expected} "
        f"({', '.join(f'{level}={count}' for level, count in df_eval['complexity_level'].value_counts().items())})"
    )
    print(f"Modelo OpenAI: {model}")
    print(f"Iniciando avaliação LLM de {n} entradas...")

    rows: list[dict[str, object]] = []
    for i in range(n):
        row = df_eval.iloc[i]
        name = row["function_name"]
        level = row["complexity_level"]
        print(f"[{i + 1}/{n}] {name} ({level})...")

        try:
            row_out = evaluate_one(client, template, row, model=model)
        except Exception as e:
            row_out = _row_from_evaluation(row, {}, f"Erro na API: {e}")
        rows.append(row_out)

    out_df = pd.DataFrame(rows)[OUTPUT_COLUMNS]
    out_df.to_csv(OUTPUT_EVAL, index=False, encoding="utf-8")
    print(f"Avaliação concluída. Resultados: {OUTPUT_EVAL}")


if __name__ == "__main__":
    main()
