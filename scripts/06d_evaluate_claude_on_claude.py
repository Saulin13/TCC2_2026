"""
Avalia testes gerados pelo Claude usando Claude como avaliador.
"""

from __future__ import annotations

import argparse
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

from csv_columns import prepare_csv_for_save
from dataset_config import BASE_DIR, add_dataset_argument, resolve_dataset

PROMPT_TEMPLATE_PATH = BASE_DIR / "prompts" / "prompt_evaluate_tests.txt"

DEFAULT_CLAUDE_MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 1200
TEMPERATURE = 0.0
EXEC_LOG_MAX_CHARS = 4000
EVAL_SAMPLE_PER_LEVEL = 10
RANDOM_STATE = 42
SAMPLE_BY_LEVEL = {"baixa": EVAL_SAMPLE_PER_LEVEL, "media": EVAL_SAMPLE_PER_LEVEL, "alta": EVAL_SAMPLE_PER_LEVEL}
COMPLEXITY_ORDER = ("baixa", "media", "alta")
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
        k = min(target, len(pool))
        if k > 0:
            parts.append(pool.sample(n=k, random_state=RANDOM_STATE))
    if not parts:
        return work.iloc[0:0]
    return pd.concat(parts, ignore_index=True)


def select_from_prior_eval(df_cov: pd.DataFrame, df_prior: pd.DataFrame) -> pd.DataFrame:
    keys = df_prior[list(SELECT_KEYS)].drop_duplicates()
    merged = df_cov.merge(keys, on=list(SELECT_KEYS), how="inner")
    if merged.empty:
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
    m = re.match(r"^```(?:json)?\s*\r?\n(.*)\r?\n```\s*$", t, re.DOTALL | re.IGNORECASE)
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
    prompt = (
        template.replace("<<<FUNCTION_CODE>>>", source_code)
        .replace("<<<TEST_CODE>>>", test_code)
        .replace("<<<EXECUTION_SUMMARY>>>", _build_execution_summary(row))
        .replace("<<<COVERAGE_PERCENT>>>", _coverage_str(row))
    )
    if "json" not in prompt.lower():
        prompt += "\n\nResponda exclusivamente com um objeto JSON válido, sem markdown."
    return prompt


def _extract_function_from_repo(function_name: str, file_path: str, *, repo_path: Path) -> str | None:
    source_file = repo_path / Path(str(file_path).replace("\\", "/"))
    if not source_file.is_file():
        return None
    full_source = source_file.read_text(encoding="utf-8", errors="replace")
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


def load_function_source(row: pd.Series, *, repo_path: Path) -> str:
    from_sample = row.get("source_code")
    if isinstance(from_sample, str) and from_sample.strip():
        return from_sample
    extracted = _extract_function_from_repo(str(row["function_name"]), str(row["file_path"]), repo_path=repo_path)
    if extracted:
        return extracted
    return f"(código-fonte não encontrado para {row['function_name']})"


def load_test_code(test_file: object) -> str:
    rel = Path(str(test_file))
    path = (BASE_DIR / rel).resolve() if not rel.is_absolute() else rel
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return f"(arquivo de teste não encontrado: {test_file})"


def _row_from_evaluation(row: pd.Series, scores: dict[str, object], err: str | None) -> dict[str, object]:
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


def evaluate_one(client: Anthropic, template: str, row: pd.Series, *, model: str, repo_path: Path) -> dict[str, object]:
    source_code = load_function_source(row, repo_path=repo_path)
    test_code = load_test_code(row["test_file"])
    prompt = _fill_prompt(template, row, source_code=source_code, test_code=test_code)
    response = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = "".join((getattr(block, "text", "") or "") for block in response.content if getattr(block, "type", None) == "text")
    scores, parse_err = _parse_scores(raw)
    return _row_from_evaluation(row, scores, parse_err)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Avalia testes Claude com avaliador Claude.")
    add_dataset_argument(parser)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cfg = resolve_dataset(args.dataset)
    sample_file = cfg.sample_csv
    repo_path = cfg.repo_path
    input_coverage = cfg.result_csv("cobertura_testes_gerados_claude")
    input_prior = cfg.result_csv("avaliacao_gpt_sobre_testes_claude")
    output_eval = cfg.result_csv("avaliacao_claude_sobre_testes_claude")

    load_dotenv(BASE_DIR / ".env")
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("Erro: ANTHROPIC_API_KEY não definida no .env")
        return
    if not input_coverage.exists():
        print(f"Erro: arquivo não encontrado: {input_coverage}")
        return
    if not PROMPT_TEMPLATE_PATH.exists():
        print(f"Erro: template não encontrado: {PROMPT_TEMPLATE_PATH}")
        return

    template = PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")
    model = resolve_claude_model()
    client = Anthropic(api_key=api_key)

    df_cov = pd.read_csv(input_coverage)
    if input_prior.exists():
        df_selected = select_from_prior_eval(df_cov, pd.read_csv(input_prior))
    else:
        df_selected = select_balanced_sample(df_cov)

    if sample_file.exists():
        df_sample = pd.read_csv(sample_file)
        df_eval = df_selected.merge(
            df_sample[list(MERGE_KEYS) + ["source_code"]],
            on=list(MERGE_KEYS),
            how="left",
        )
    else:
        df_eval = df_selected.copy()

    rows: list[dict[str, object]] = []
    for i in range(len(df_eval)):
        row = df_eval.iloc[i]
        print(f"[{i + 1}/{len(df_eval)}] {row['function_name']}...")
        try:
            rows.append(evaluate_one(client, template, row, model=model, repo_path=repo_path))
        except Exception as e:
            rows.append(_row_from_evaluation(row, {}, f"Erro na API: {e}"))

    out_df = prepare_csv_for_save(pd.DataFrame(rows)[OUTPUT_COLUMNS])
    out_df.to_csv(output_eval, index=False, encoding="utf-8")
    print(f"Avaliação concluída: {output_eval}")


if __name__ == "__main__":
    main()
