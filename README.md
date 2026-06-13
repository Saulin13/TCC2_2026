# TCC2_2026 — Geração e avaliação de testes com LLMs

Experimento para gerar testes unitários com GPT e Claude, executá-los com pytest, medir cobertura e métricas heurísticas, e comparar avaliações entre modelos.

## Início rápido

```bash
pip install -r requirements.txt
python scripts/00_run_pipeline.py --dataset all
```

Documentação detalhada: [docs/PIPELINE.md](docs/PIPELINE.md)

No Windows:

```powershell
.\run_all.ps1
```

## Estrutura principal

```
scripts/           # Pipeline e utilitários
data/
  raw/             # Extração e complexidade (Radon)
  selected_functions/   # Amostras oficiais
  results/         # CSVs, resumos, plots, logs, prompts
tests/generated/   # Testes gerados por dataset e LLM
repos/             # Clones: Python (TheAlgorithms), scikit-learn
prompts/           # Templates de geração e avaliação
```

## Tabela de scripts

| Script | Função | Quando usar |
|--------|--------|-------------|
| `00_run_pipeline.py` | Orquestra toda a pipeline experimental por dataset | **Execução principal** — gerar testes, métricas, avaliações e gráficos |
| `00_limpar_resultados.py` | Apaga resultados e testes gerados (com confirmação) | Reiniciar o experimento do zero, mantendo amostras e código-fonte |
| `01_extract_functions.py` | Extrai funções Python do repositório TheAlgorithms | Preparação inicial, antes da amostra de 60 funções |
| `02_measure_complexity.py` | Calcula complexidade ciclomática (Radon) | Após extração; alimenta a seleção de amostra |
| `03_select_sample.py` | Seleciona 60 funções balanceadas por complexidade | Preparação do dataset **thealgorithms** |
| `03b_select_real_project_sample.py` | Seleciona 15 funções do scikit-learn (5 por complexidade) | Preparação do dataset **real** |
| `04_generate_tests_gpt.py` | Gera testes com GPT-4o | Etapa da pipeline ou execução isolada com `--dataset` |
| `04b_generate_tests_claude.py` | Gera testes com Claude | Idem, gerador Claude |
| `05_run_tests.py` | Executa pytest e mede cobertura real via `coverage.py` | Após geração; requer `--generator gpt\|claude`; gera também `test_execution_debug*.csv` |
| `06_evaluate_tests_llm.py` | GPT avalia qualidade dos testes GPT | Pipeline ou reavaliação isolada |
| `06b_evaluate_tests_claude.py` | Claude avalia testes GPT | Comparação entre avaliadores |
| `06c_evaluate_gpt_on_claude.py` | GPT avalia testes gerados pelo Claude | Avaliação cruzada de geradores |
| `06d_evaluate_claude_on_claude.py` | Claude avalia testes gerados pelo Claude | Completa matriz 2x2 de avaliação cruzada |
| `08_calculate_assertion_density.py` | Métrica de densidade de asserts | Após execução dos testes |
| `09_calculate_execution_success.py` | Métrica de sucesso de execução | Após avaliação GPT (usa categorias da avaliação) |
| `10_calculate_test_strength.py` | `test_strength_score` via mutation testing (mutmut/libcst) | Após cobertura; ver limites padrão para `thealgorithms` abaixo |
| `11_consolidate_results.py` | Une métricas em `resultados_finais_*.csv` | Penúltima etapa; inclui `overall_score` dos 4 cenários (GPT→GPT, GPT→Claude, Claude→GPT, Claude→Claude) |
| `12_generate_plots.py` | Gráficos 01–07 do experimento | Última etapa analítica por dataset |
| `13_compare_llm_evaluators.py` | Compara GPT vs Claude nos dois geradores (GPT e Claude) | Após avaliações; gera gráficos de dispersão por gerador e médias da matriz 2x2 |
| `15_statistical_analysis.py` | Estatísticas, correlações (Pearson/Spearman) e gráficos avançados | Gera `summary_statistics.csv`, `correlation_results.csv` e PNGs em `data/results/graficos/` |
| `14_classify_coverage.py` | Classifica cobertura em faixas (baixa/média/alta) | Substitui o script legado `17_classificar_cobertura.py` |
| `dataset_config.py` | Configuração de caminhos por dataset | Importado pelos scripts; não executar diretamente |
| `csv_columns.py` | Padronização de colunas CSV | Importado pelos scripts; não executar diretamente |
| `legacy/17_classificar_cobertura.py` | Versão antiga da classificação de cobertura | **Não usar** — apenas referência histórica |

## Datasets

| Chave | Repositório | Amostra |
|-------|-------------|---------|
| `thealgorithms` | TheAlgorithms/Python | 60 funções |
| `real` | scikit-learn | 15 funções (5 baixa, 5 média, 5 alta) |
| `all` | Ambos, em sequência | — |

### Mutation testing (`10_calculate_test_strength.py`)

No dataset **thealgorithms**, o mutation testing usa limites conservadores por padrão devido ao custo computacional de funções com testes lentos (ex.: `visualise`):

| Parâmetro | Padrão (`thealgorithms`) | Padrão (`real`) |
|-----------|--------------------------|-----------------|
| `--max-mutants` | 5 | 25 |
| `--mutation-timeout` | 10s | 90s |
| `--function-timeout` | 120s | 300s |

Opções úteis:

```bash
# Pular funções problemáticas
python scripts/10_calculate_test_strength.py --dataset thealgorithms --skip-functions visualise

# Ajustar limites manualmente
python scripts/10_calculate_test_strength.py --dataset thealgorithms --max-mutants 5 --function-timeout 120
```

Se o script for interrompido (Ctrl+C), os resultados parciais já processados são salvos em `forca_heuristica_testes_*.csv`.

## Scripts obsoletos / duplicados

| Removido da raiz | Substituído por | Localização atual |
|------------------|-----------------|-------------------|
| `17_classificar_cobertura.py` | `14_classify_coverage.py` | `scripts/legacy/` |

Layout antigo de testes (`tests/generated/gpt/` na raiz) arquivado em `tests/generated/legacy/`. Cópias ativas estão em `tests/generated/thealgorithms/`.

## Referências

- [docs/PIPELINE.md](docs/PIPELINE.md) — ordem de execução, entradas, saídas e gráficos  
- [docs/methodology_notes.md](docs/methodology_notes.md) — notas metodológicas do TCC  
