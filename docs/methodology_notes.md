# Notas de Metodologia do Experimento

## Objetivo Geral

- Investigar a geração automática de testes unitários com LLMs.
- Avaliar qualidade dos testes gerados com métricas quantitativas e revisão assistida por outro LLM.
- Comparar resultados de geração e avaliação para identificar pontos fortes e limitações da abordagem.

## Base de Código do Estudo

- Repositório de origem: `TheAlgorithms/Python`.
- Justificativa: grande volume de funções independentes, diversidade de domínios e complexidades, e fácil reprodução do experimento.

## Fluxo Metodológico (Visão Geral)

1. Extrair funções Python do repositório selecionado.
2. Medir e classificar a complexidade de cada função com Radon.
3. Selecionar uma amostra piloto de 30 funções.
4. Gerar testes unitários para a amostra com ChatGPT-5.
5. Executar os testes com pytest e medir cobertura com coverage.
6. Avaliar parte dos testes gerados com Claude Code.
7. Comparar geração e avaliação com métricas quantitativas.

## Etapas Detalhadas

### 1) Extração de funções Python

- Percorrer os arquivos `.py` do repositório.
- Identificar funções candidatas (preferencialmente funções puras e com dependências controladas).
- Registrar metadados básicos: caminho do arquivo, nome da função, assinatura e código-fonte.

### 2) Classificação por complexidade com Radon

- Aplicar Radon para obter métricas de complexidade ciclomática por função.
- Categorizar funções por faixas de complexidade (baixa, média, alta).
- Usar essa classificação para balancear a amostra piloto.

### 3) Seleção de amostra piloto (30 funções)

- Definir amostra de 30 funções com representatividade entre níveis de complexidade.
- Evitar funções com forte acoplamento externo que inviabilizem execução simples dos testes.
- Consolidar a amostra em arquivo estruturado para uso nas etapas seguintes.

### 4) Geração de testes com ChatGPT-5

- Usar prompt padronizado para reduzir variação de instrução entre funções.
- Gerar testes focados em: casos típicos, casos de borda e tratamento de erro.
- Armazenar saídas com rastreabilidade (função de origem, prompt, resposta e versão do modelo).

### 5) Execução com pytest e medição de cobertura

- Executar testes gerados via pytest.
- Coletar taxa de sucesso/falha e tipos de erro de execução.
- Medir cobertura de código com coverage (por função e agregado da amostra).

### 6) Avaliação parcial com Claude Code

- Selecionar um subconjunto dos testes para avaliação qualitativa assistida.
- Solicitar análise de adequação dos testes (clareza, completude, relevância dos cenários).
- Registrar observações estruturadas para confronto com métricas numéricas.

### 7) Comparação com métricas quantitativas

- Comparar geração e avaliação por indicadores objetivos.
- Métricas sugeridas:
  - taxa de testes executáveis;
  - taxa de aprovação no pytest;
  - cobertura média por função;
  - distribuição de cobertura por faixa de complexidade;
  - proporção de testes com casos de borda.
- Relacionar achados quantitativos com a avaliação parcial do Claude Code.

## Resultados Esperados

- Entender como a complexidade da função afeta a qualidade dos testes gerados.
- Identificar limitações recorrentes na geração automática de testes.
- Produzir insumos para refinar prompts e melhorar o pipeline de geração/avaliação.

## Observações Práticas

- Manter versionamento dos prompts para reprodutibilidade.
- Fixar dependências e ambiente para reduzir variação experimental.
- Registrar logs de execução e falhas para análise posterior.
