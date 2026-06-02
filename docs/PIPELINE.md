# Pipeline do experimento TCC2_2026

Este documento descreve como executar o experimento de geração e avaliação automática de testes com LLMs, sem alterar a lógica experimental dos scripts.

## Ponto de entrada principal

```bash
python scripts/00_run_pipeline.py --dataset all
```

No Windows, também é possível usar:

```powershell
.\run_all.ps1
```

---

## Ordem correta de execução

### Fase A — Preparação da amostra (manual, uma vez por repositório)

Executar **antes** da pipeline principal, quando ainda não existem os CSVs de amostra:

| Ordem | Script | Saída principal |
|------:|--------|-----------------|
| 1 | `01_extract_functions.py` | `data/raw/functions_extracted.csv` |
| 2 | `02_measure_complexity.py` | `data/raw/functions_with_complexity.csv` |
| 3a | `03_select_sample.py` | `data/selected_functions/sample_thealgorithms_60.csv` |
| 3b | `03b_select_real_project_sample.py` | `data/selected_functions/sample_real_project_15.csv` |

Requisitos: clones em `repos/Python` (TheAlgorithms) e `repos/scikit-learn`.

### Fase B — Pipeline experimental (orquestrada por `00_run_pipeline.py`)

Para cada `--dataset` escolhido, a ordem é:

1. `04_generate_tests_gpt.py` — gera testes com GPT  
2. `04b_generate_tests_claude.py` — gera testes com Claude  
3. `05_run_tests.py --generator gpt` — pytest + cobertura (GPT)  
4. `05_run_tests.py --generator claude` — pytest + cobertura (Claude)  
5. `14_classify_coverage.py` — classificação da cobertura  
6. `08_calculate_assertion_density.py` — densidade de asserts  
7. `09_calculate_execution_success.py` — sucesso de execução  
8. `10_calculate_test_strength.py` — `test_strength_score`  
9. `06_evaluate_tests_llm.py` — GPT avalia testes GPT  
10. `06b_evaluate_tests_claude.py` — Claude avalia testes GPT  
11. `06c_evaluate_gpt_on_claude.py` — GPT avalia testes Claude  
12. `06d_evaluate_claude_on_claude.py` — Claude avalia testes Claude  
13. `13_compare_llm_evaluators.py` — compara avaliadores na matriz 2x2  
14. `11_consolidate_results.py` — tabela final consolidada  
15. `12_generate_plots.py` — gráficos principais do dataset  
16. `15_statistical_analysis.py` — estatísticas, correlações e gráficos em `data/results/graficos/`  

---

## Como rodar por dataset

### TheAlgorithms (`thealgorithms`)

Amostra: `data/selected_functions/sample_thealgorithms_60.csv` (60 funções).

```bash
python scripts/00_run_pipeline.py --dataset thealgorithms
```

### scikit-learn (`real`)

Amostra: `data/selected_functions/sample_real_project_15.csv` (15 funções; 5 baixa, 5 média, 5 alta).

> **Atenção:** no dataset real, a cobertura pode ser limitada porque os testes executam contra o pacote `sklearn` instalado via pip, não necessariamente contra o clone em `repos/scikit-learn`.

```bash
python scripts/00_run_pipeline.py --dataset real
```

### Ambos (`all`)

Executa `thealgorithms` e depois `real`:

```bash
python scripts/00_run_pipeline.py --dataset all
```

### Opções úteis

| Flag | Efeito |
|------|--------|
| `--skip-generation` | Pula etapas 04 e 04b (reutiliza testes já gerados) |
| `--skip-evaluation` | Pula avaliações por LLM e comparação (06, 06b, 06c, 06d, 13) |
| `--only-plots` | Apenas consolidação (11) e gráficos (12) |

Exemplo para reprocessar métricas e gráficos sem chamar APIs:

```bash
python scripts/00_run_pipeline.py --dataset all --skip-generation --skip-evaluation
```

---

## Caminhos oficiais

### Amostras (entrada da pipeline)

| Dataset | Arquivo |
|---------|---------|
| TheAlgorithms | `data/selected_functions/sample_thealgorithms_60.csv` |
| scikit-learn | `data/selected_functions/sample_real_project_15.csv` |

### Testes gerados

| Dataset | GPT | Claude |
|---------|-----|--------|
| TheAlgorithms | `tests/generated/thealgorithms/gpt/` | `tests/generated/thealgorithms/claude/` |
| Real | `tests/generated/real/gpt/` | `tests/generated/real/claude/` |

Layout antigo (`tests/generated/gpt/` na raiz) foi arquivado em `tests/generated/legacy/`.

### Prompts enviados às LLMs

| Dataset | GPT | Claude |
|---------|-----|--------|
| TheAlgorithms | `data/results/generated_prompts/thealgorithms/gpt/` | `.../thealgorithms/claude/` |
| Real | `data/results/generated_prompts/real/gpt/` | `.../real/claude/` |

Templates de prompt: `prompts/prompt_generate_tests.txt`, `prompts/prompt_evaluate_tests.txt`.

### Resultados (CSVs e resumos)

Diretório base: `data/results/`

Os arquivos usam sufixo por dataset:

- `_thealgorithms` — TheAlgorithms  
- `_real` — scikit-learn  

Exemplos:

- `cobertura_testes_gerados_gpt_thealgorithms.csv`
- `resultados_finais_real.csv`
- `resumo_resultados_finais_thealgorithms.txt`

### Gráficos

| Dataset | Diretório |
|---------|-----------|
| TheAlgorithms | `data/results/plots/thealgorithms/` |
| Real | `data/results/plots/real/` |

### Logs

`data/results/logs/pipeline_<dataset>.log`

---

## Entradas e saídas por etapa da pipeline

| Etapa | Entradas principais | Saídas principais |
|-------|---------------------|-------------------|
| Geração GPT | amostra CSV, `prompts/` | testes em `tests/generated/<dataset>/gpt/`, prompts em `generated_prompts/.../gpt/` |
| Geração Claude | amostra CSV, `prompts/` | testes em `.../claude/`, prompts em `generated_prompts/.../claude/` |
| Execução testes | testes gerados, amostra | `cobertura_testes_gerados_<gerador>_<dataset>.csv`, `execucao_testes_<gerador>_<dataset>.csv` |
| Classificação cobertura | cobertura GPT | `classificacao_cobertura_<dataset>.csv`, `resumo_classificacao_cobertura_<dataset>.txt` |
| Métricas 08–10 | cobertura / avaliação | `metrica_densidade_asserts_*`, `metrica_sucesso_execucao_*`, `forca_heuristica_testes_*` |
| Avaliações LLM | cobertura, testes | `avaliacao_gpt_sobre_testes_gpt_*`, `avaliacao_claude_sobre_testes_gpt_*`, `avaliacao_gpt_sobre_testes_claude_*` |
| Comparação avaliadores | avaliações GPT e Claude nos dois geradores | `comparacao_avaliadores_gpt_claude_*`, gráficos de cross-evaluation em `plots/<dataset>/` |
| Consolidação | métricas intermediárias | **`resultados_finais_<dataset>.csv`**, **`resumo_resultados_finais_<dataset>.txt`** |
| Gráficos finais | cobertura, avaliação, força heurística | PNGs 01–07 em `plots/<dataset>/`, `summary_metrics.csv` |

---

## Gráficos principais

### Gerados por `12_generate_plots.py` (análise do experimento)

| Arquivo | Conteúdo |
|---------|----------|
| `01_execucao_por_status.png` | Distribuição de status de execução (ok, falha, erro pytest, timeout) |
| `02_cobertura_media_por_complexidade.png` | Cobertura média por nível (baixa/média/alta) |
| `03_nota_llm_por_complexidade.png` | Nota overall do avaliador GPT por complexidade |
| `04_cobertura_vs_nota_llm.png` | Dispersão cobertura × nota LLM |
| `05_test_strength_por_complexidade.png` | `test_strength_score` por complexidade |
| `06_test_strength_vs_coverage.png` | Força heurística × cobertura |
| `07_test_strength_vs_llm_score.png` | Força heurística × nota LLM |

### Gerados por `13_compare_llm_evaluators.py` (comparação GPT × Claude, matriz 2x2)

| Arquivo | Conteúdo |
|---------|----------|
| `overall_score_gpt_tests_gpt_vs_claude.png` | Dispersão GPT→GPT vs GPT→Claude (`y=x`) |
| `overall_score_claude_tests_gpt_vs_claude.png` | Dispersão Claude→GPT vs Claude→Claude (`y=x`) |
| `overall_score_cross_evaluation_mean.png` | Média por cenário (GPT→GPT, GPT→Claude, Claude→GPT, Claude→Claude) |
| `overall_score_cross_evaluation_by_complexity.png` | Média por complexidade e cenário da matriz 2x2 |

### Diagnóstico de execução/cobertura (dataset real)

Arquivos gerados por `05_run_tests.py`:

- `data/results/real/test_execution_debug.csv` (consolidado GPT + Claude)
- `data/results/real/test_execution_debug_gpt.csv`
- `data/results/real/test_execution_debug_claude.csv`

Colunas-chave incluem: `function_name`, `test_file`, `source_file`, `module_path`,
`execution_status`, `return_code`, `error_type`, `error_message`, `coverage_percent`,
`coverage_status`, `coverage_return_code`.

### Análise estatística (`15_statistical_analysis.py`)

| Arquivo | Conteúdo |
|---------|----------|
| `data/results/summary_statistics.csv` | Métricas agregadas por dataset e gerador (GPT / Claude) |
| `data/results/correlation_results.csv` | Pearson e Spearman entre pares de variáveis |
| `data/results/graficos/<dataset>/` | Heatmap, dispersões com tendência, status OK/FAILED agrupado |

O gráfico `01_execucao_por_status.png` (em `plots/<dataset>/`) compara GPT e Claude com barras agrupadas OK vs FAILED.

---

## Scripts auxiliares

| Script | Função |
|--------|--------|
| `00_limpar_resultados.py` | Remove resultados gerados e recria a estrutura de pastas (preserva `tests/generated/legacy/`) |
| `dataset_config.py` | Caminhos e metadados por dataset (importado pelos outros scripts) |
| `csv_columns.py` | Padronização de colunas nos CSVs |
| `scripts/legacy/17_classificar_cobertura.py` | **Obsoleto** — versão antiga sem `--dataset`; use `14_classify_coverage.py` |

---

## Variáveis de ambiente

Configure um arquivo `.env` na raiz do projeto com as chaves das APIs usadas em geração e avaliação (OpenAI, Anthropic), conforme `requirements.txt`.
