import pandas as pd
from pathlib import Path

# Configuração de caminhos
BASE_DIR = Path(__file__).parent.parent.absolute()
INPUT_EVAL = BASE_DIR / "data" / "results" / "evaluation_results.csv"
OUTPUT_DIR = BASE_DIR / "data" / "results"

def categorizar_sucesso(row):
    # Obtém o status e mensagens de erro do CSV original
    # Convertemos para string para evitar quebras com valores nulos (NaN)
    status = str(row.get('execution_status', '')).lower()
    passed = row.get('passed', False)
    stderr = str(row.get('stderr', '')).lower()
    stdout = str(row.get('stdout', '')).lower()
    
    # 1. Caso de Sucesso Direto
    if passed is True or passed == "True" or passed == "true" or "success" in status:
        return "Sucesso Direto (Pass Rate)"
        
    # 2. Caso de Erro de Sintaxe / Compilação do Python
    elif "syntaxerror" in stderr or "indentationerror" in stderr or "syntax" in stderr:
        return "Erro de Sintaxe/Compilação"
        
    # 3. Caso onde o código executa mas quebra em alguma asserção ou erro de runtime (ex: NameError, TypeError)
    else:
        return "Falha de Execução (Runtime/Assertion Error)"

def main():
    print("📊 Iniciando classificação da Taxa de Sucesso e Execução dos testes Python...")
    
    if not INPUT_EVAL.exists():
        print(f"❌ Erro: Arquivo base {INPUT_EVAL} não encontrado.")
        print("💡 Certifique-se de que o arquivo 'evaluation_results.csv' existe na pasta data/results/.")
        return

    df = pd.read_csv(INPUT_EVAL)
    
    # Descobre qual coluna identifica o arquivo de teste no seu CSV base
    coluna_id = 'file_name' if 'file_name' in df.columns else df.columns[0]
    
    # Aplica a regra de categorização linha por linha do experimento
    df['execution_category'] = df.apply(categorizar_sucesso, axis=1)
    
    # Isolamos apenas a coluna identificadora e a nova métrica para o CSV temporário
    df_resultado = df[[coluna_id, 'execution_category']].copy()
    
    # Salva os resultados das categorias
    df_resultado.to_csv(OUTPUT_DIR / "metric_execution_success.csv", index=False)
    print(f"✅ Métrica de Taxa de Sucesso salva em: {OUTPUT_DIR / 'metric_execution_success.csv'}")
    
    # Exibe um resumo percentual na tela para o seu TCC
    print("\n📈 Resumo Geral da Taxa de Sucesso da IA:")
    resumo = df['execution_category'].value_counts(normalize=True) * 100
    for cat, val in resumo.items():
        print(f" - {cat}: {val:.2f}%")

if __name__ == "__main__":
    main()