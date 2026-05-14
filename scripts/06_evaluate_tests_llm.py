import json
import math
import re
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Raiz do projeto; todos os caminhos são relativos a ela
BASE_DIR = Path(__file__).resolve().parent.parent
PROMPT_TEMPLATE_PATH = BASE_DIR / "prompts" / "prompt_evaluate_tests.txt"
INPUT_COVERAGE = BASE_DIR / "data" / "results" / "coverage_results.csv"
SAMPLE_FILE = BASE_DIR / "data" / "selected_functions" / "pilot_sample_30.csv"
OUTPUT_EVAL = BASE_DIR / "data" / "results" / "evaluation_results.csv"

MODEL_NAME = "gpt-4o"
MAX_EVALUATIONS = 10
EXEC_LOG_MAX_CHARS = 4000

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
    cov_row: pd.Series,
    sample_row: pd.Series,
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
        "function_name": cov_row["function_name"],
        "file_path": cov_row["file_path"],
        "complexity_score": cov_row.get("complexity_score", sample_row.get("complexity_score")),
        "complexity_level": cov_row.get("complexity_level", sample_row.get("complexity_level")),
        "test_file": cov_row["test_file"],
        "execution_status": cov_row["execution_status"],
        "passed": _parse_passed(cov_row["passed"]),
        "return_code": _parse_return_code(cov_row["return_code"]),
        "coverage_percent": float(cov_row["coverage_percent"]) if pd.notna(cov_row["coverage_percent"]) else 0.0,
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


def evaluate_one(client: OpenAI, template: str, cov_row: pd.Series, sample_row: pd.Series) -> dict[str, object]:
    test_rel = Path(str(cov_row["test_file"]))
    test_path = (BASE_DIR / test_rel).resolve() if not test_rel.is_absolute() else test_rel

    source_code = sample_row["source_code"]
    if test_path.is_file():
        test_code = test_path.read_text(encoding="utf-8")
    else:
        test_code = f"(arquivo de teste não encontrado: {cov_row['test_file']})"

    prompt = _fill_prompt(template, cov_row, source_code=source_code, test_code=test_code)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.2,
    )
    raw = response.choices[0].message.content or ""
    scores, parse_err = _parse_scores(raw)
    return _row_from_evaluation(cov_row, sample_row, scores, parse_err)


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

    df_cov = pd.read_csv(INPUT_COVERAGE).head(MAX_EVALUATIONS).reset_index(drop=True)
    df_sample = pd.read_csv(SAMPLE_FILE).reset_index(drop=True)

    n = len(df_cov)
    if n == 0:
        print("Nenhuma linha em coverage_results.csv para avaliar.")
        return
    if len(df_sample) < n:
        print(f"Aviso: pilot_sample tem menos linhas ({len(df_sample)}) que o lote ({n}).")
        n = min(n, len(df_sample))
        df_cov = df_cov.iloc[:n].reset_index(drop=True)

    rows: list[dict[str, object]] = []
    print(f"Iniciando avaliação LLM das primeiras {n} entradas...")

    for i in range(n):
        cov_row = df_cov.iloc[i]
        sample_row = df_sample.iloc[i]
        name = cov_row["function_name"]
        print(f"[{i + 1}/{n}] {name}...")

        try:
            row_out = evaluate_one(client, template, cov_row, sample_row)
        except Exception as e:
            row_out = _row_from_evaluation(
                cov_row,
                sample_row,
                {},
                f"Erro na API: {e}",
            )
        rows.append(row_out)

    out_df = pd.DataFrame(rows)[OUTPUT_COLUMNS]
    out_df.to_csv(OUTPUT_EVAL, index=False, encoding="utf-8")
    print(f"Avaliação concluída. Resultados: {OUTPUT_EVAL}")


if __name__ == "__main__":
    main()
