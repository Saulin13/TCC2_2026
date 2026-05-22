"""
Avalia testes gerados com Claude (Anthropic), alinhado à amostra já avaliada pelo GPT.
"""

from __future__ import annotations

import ast
import json
import math
import os
import re
import unicodedata
from pathlib import Path

import pandas as pd
from anthropic import Anthropic
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_PATH = BASE_DIR / "repos" / "Python"
TESTS_DIR = BASE_DIR / "tests" / "generated"
PROMPT_TEMPLATE_PATH = BASE_DIR / "prompts" / "prompt_evaluate_tests.txt"
INPUT_COVERAGE = BASE_DIR / "data" / "results" / "coverage_results.csv"
INPUT_EVAL_GPT = BASE_DIR / "data" / "results" / "evaluation_results.csv"
INPUT_EVAL_GPT_ALT = BASE_DIR / "data" / "results" / "evaluation_results_gpt.csv"
SAMPLE_FILE = BASE_DIR / "data" / "selected_functions" / "pilot_sample_30.csv"
OUTPUT_EVAL = BASE_DIR / "data" / "results" / "evaluation_results_claude.csv"

DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 1200
TEMPERATURE = 0.0
EXEC_LOG_MAX_CHARS = 4000
RANDOM_SEED = 42
SAMPLE_BY_LEVEL = {"baixa": 4, "media": 3, "alta": 3}
MERGE_KEYS = ("function_name", "file_path")
SELECT_KEYS = ("function_name", "test_file")

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


def resolve_claude_model() -> str:
    return (os.getenv("CLAUDE_MODEL") or DEFAULT_CLAUDE_MODEL).strip()


def _normalize_text(value: str) -> str:
    if not isinstance(value, str):
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    without_accents = "".join(ch for ch in normalized if not unicodedata.combining(ch))
    return without_accents.strip().lower()


def normalize_complexity_level(value: object) -> str:
    norm = _normalize_text(str(value) if value is not None else "")
    if norm in {"baixa", "low"}:
        return "baixa"
    if norm in {"media", "medium"}:
        return "media"
    if norm in {"alta", "high"}:
        return "alta"
    return norm


def select_balanced_sample(df: pd.DataFrame) -> pd.DataFrame:
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


def select_from_prior_eval(df_cov: pd.DataFrame, df_prior: pd.DataFrame) -> pd.DataFrame:
    keys = df_prior[list(SELECT_KEYS)].drop_duplicates()
    merged = df_cov.merge(keys, on=list(SELECT_KEYS), how="inner")
    if merged.empty:
        print("Aviso: merge com avaliação GPT retornou vazio; usando amostra balanceada.")
        return select_balanced_sample(df_cov)
    return merged.reset_index(drop=True)


def _parse_passed(val: object) -> bool:
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in ("true", "1", "yes")


def _parse_return_code(val: object) -> int:
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return -1
    try:
        return int(float(val))
    except (TypeError, ValueError):
        return -1


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


def _extract_json_object(raw: str) -> str:
    cleaned = _strip_json_fences(raw)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        return cleaned[start : end + 1]
    return cleaned


def _parse_scores(raw: str) -> tuple[dict[str, object], str | None]:
    try:
        data = json.loads(_extract_json_object(raw))
    except json.JSONDecodeError as e:
        return {}, f"JSON inválido: {e}"
    if not isinstance(data, dict):
        return {}, "Resposta não é um objeto JSON"
    return data, None


def _log_excerpt(row: pd.Series, field: str) -> str:
    text = str(row.get(field) or "").strip()
    if not text:
        return ""
    return text[:EXEC_LOG_MAX_CHARS]


def _build_execution_summary(row: pd.Series) -> str:
    lines = [
        f"execution_status: {row['execution_status']}",
        f"passed: {row['passed']}",
        f"return_code: {_parse_return_code(row['return_code'])}",
    ]
    stderr = _log_excerpt(row, "stderr")
    stdout = _log_excerpt(row, "stdout")
    if stderr:
        lines.extend(["", "stderr (trecho):", stderr])
    if stdout:
        lines.extend(["", "stdout (trecho):", stdout])
    return "\n".join(lines)


def _coverage_str(row: pd.Series) -> str:
    cov = row.get("coverage_percent")
    if pd.isna(cov):
        return ""
    return str(float(cov))


def _fill_prompt(template: str, row: pd.Series, *, source_code: str, test_code: str) -> str:
    execution_status = str(row.get("execution_status", ""))
    coverage_percent = _coverage_str(row)
    execution_summary = _build_execution_summary(row)

    prompt = template
    replacements = {
        "<<<FUNCTION_CODE>>>": source_code,
        "<<<TEST_CODE>>>": test_code,
        "<<<EXECUTION_SUMMARY>>>": execution_summary,
        "<<<COVERAGE_PERCENT>>>": coverage_percent,
        "{function_code}": source_code,
        "{test_code}": test_code,
        "{execution_status}": execution_status,
        "{coverage_percent}": coverage_percent,
    }
    for key, value in replacements.items():
        prompt = prompt.replace(key, value)

    template_lower = template.lower()
    if "stdout" not in template_lower:
        stdout = _log_excerpt(row, "stdout")
        if stdout:
            prompt += f"\n\nstdout (trecho):\n{stdout}"
    if "stderr" not in template_lower:
        stderr = _log_excerpt(row, "stderr")
        if stderr:
            prompt += f"\n\nstderr (trecho):\n{stderr}"

    if "json" not in prompt.lower():
        prompt += (
            "\n\nResponda exclusivamente com um objeto JSON válido, sem markdown, "
            "no formato solicitado no template."
        )
    return prompt


def _extract_function_from_repo(function_name: str, file_path: str) -> str | None:
    source_file = REPO_PATH / Path(str(file_path).replace("\\", "/"))
    if not source_file.is_file():
        return None
    try:
        full_source = source_file.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        full_source = source_file.read_text(encoding="latin-1")
    except OSError:
        return None

    try:
        tree = ast.parse(full_source, filename=str(source_file))
    except SyntaxError:
        return None

    lines = full_source.splitlines()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
            end = getattr(node, "end_lineno", node.lineno)
            return "\n".join(lines[node.lineno - 1 : end])
    return None


def load_function_source(row: pd.Series) -> str:
    from_sample = row.get("source_code")
    if isinstance(from_sample, str) and from_sample.strip():
        return from_sample

    extracted = _extract_function_from_repo(
        str(row["function_name"]),
        str(row["file_path"]),
    )
    if extracted:
        return extracted

    source_file = REPO_PATH / Path(str(row["file_path"]).replace("\\", "/"))
    if source_file.is_file():
        try:
            return source_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return source_file.read_text(encoding="latin-1")
        except OSError:
            pass
    return f"(código-fonte não encontrado para {row['function_name']})"


def load_test_code(test_file: object) -> str:
    rel = Path(str(test_file))
    path = (BASE_DIR / rel).resolve() if not rel.is_absolute() else rel
    if path.is_file():
        return path.read_text(encoding="utf-8")
    alt = TESTS_DIR / rel.name
    if alt.is_file():
        return alt.read_text(encoding="utf-8")
    return f"(arquivo de teste não encontrado: {test_file})"


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


def evaluate_one(client: Anthropic, template: str, row: pd.Series, *, model: str) -> dict[str, object]:
    source_code = load_function_source(row)
    test_code = load_test_code(row["test_file"])
    prompt = _fill_prompt(template, row, source_code=source_code, test_code=test_code)

    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        messages=[{"role": "user", "content": prompt}],
    )

    parts: list[str] = []
    for block in response.content:
        if getattr(block, "type", None) == "text":
            parts.append(getattr(block, "text", "") or "")
    raw = "".join(parts).strip()
    scores, parse_err = _parse_scores(raw)
    return _row_from_evaluation(row, scores, parse_err)


def _load_prior_gpt_eval() -> pd.DataFrame | None:
    for path in (INPUT_EVAL_GPT, INPUT_EVAL_GPT_ALT):
        if path.exists():
            print(f"Usando avaliação GPT de referência: {path.name}")
            return pd.read_csv(path)
    return None


def main() -> None:
    load_dotenv(BASE_DIR / ".env")

    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("Erro: ANTHROPIC_API_KEY não definida no .env")
        return

    if not INPUT_COVERAGE.exists():
        print(f"Erro: arquivo não encontrado: {INPUT_COVERAGE}")
        return
    if not PROMPT_TEMPLATE_PATH.exists():
        print(f"Erro: template não encontrado: {PROMPT_TEMPLATE_PATH}")
        return

    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    model = resolve_claude_model()
    client = Anthropic(api_key=api_key)

    df_cov = pd.read_csv(INPUT_COVERAGE)
    df_prior = _load_prior_gpt_eval()
    if df_prior is not None:
        df_selected = select_from_prior_eval(df_cov, df_prior)
    else:
        print("Aviso: evaluation_results.csv não encontrado; usando amostra balanceada.")
        df_selected = select_balanced_sample(df_cov)

    n = len(df_selected)
    if n == 0:
        print("Nenhuma linha elegível para avaliar.")
        return

    if SAMPLE_FILE.exists():
        df_sample = pd.read_csv(SAMPLE_FILE)
        df_eval = df_selected.merge(
            df_sample[list(MERGE_KEYS) + ["source_code"]],
            on=list(MERGE_KEYS),
            how="left",
        )
        missing = df_eval["source_code"].isna().sum()
        if missing:
            print(f"Aviso: {missing} função(ões) sem source_code no pilot_sample; usando repos/Python.")
    else:
        df_eval = df_selected.copy()
        print(f"Aviso: {SAMPLE_FILE.name} não encontrado; usando apenas repos/Python.")

    print(f"Modelo Claude: {model}")
    print(f"Iniciando avaliação de {n} testes...")
    print(
        "Distribuição: "
        + ", ".join(f"{lvl}={cnt}" for lvl, cnt in df_eval["complexity_level"].value_counts().items())
    )

    rows: list[dict[str, object]] = []
    for i in range(n):
        row = df_eval.iloc[i]
        name = row["function_name"]
        level = row.get("complexity_level", "")
        print(f"[{i + 1}/{n}] {name} ({level})...")

        try:
            row_out = evaluate_one(client, template, row, model=model)
        except Exception as e:
            row_out = _row_from_evaluation(row, {}, f"Erro na API: {e}")
        rows.append(row_out)

    out_df = pd.DataFrame(rows)[OUTPUT_COLUMNS]
    OUTPUT_EVAL.parent.mkdir(parents=True, exist_ok=True)
    out_df.to_csv(OUTPUT_EVAL, index=False, encoding="utf-8")
    errors = int((out_df["evaluation_error"] != "").sum())
    print(f"\nAvaliação concluída: {OUTPUT_EVAL}")
    print(f"Sucesso: {n - errors}/{n} | Com erro: {errors}/{n}")


if __name__ == "__main__":
    main()
