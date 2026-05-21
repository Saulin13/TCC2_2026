import pandas as pd
from pathlib import Path

# Configuração de caminhos
BASE_DIR = Path(__file__).parent.parent.absolute()
OUTPUT_DIR = BASE_DIR / "data" / "results"

# Arquivos de entrada
INPUT_EVAL = OUTPUT_DIR / "evaluation_results.csv"
INPUT_DENSITY = OUTPUT_DIR / "metric_assertion_density.csv"
INPUT_SUCCESS = OUTPUT_DIR / "metric_execution_success.csv"
INPUT_MUTATION = OUTPUT_DIR / "metric_mutation_score.csv"

# Arquivo final consolidado
OUTPUT_FINAL = OUTPUT_DIR / "final_experiment_results.csv"

def padronizar_identificador(df, nome_planilha):
    """Detecta a coluna de ID e renomeia para 'file_name' de forma segura"""
    for col in ['file_name', 'function_name', 'id', 'name']:
        if col in df.columns:
            if col != 'file_name':
                df = df.rename(columns={col: 'file_name'})
            return df
    # Se não achar nenhum padrão conhecido, renomeia a primeira coluna
    col_original = df.columns[0]
    df = df.rename(columns={col_original: 'file_name'})
    return df

def main():
    print("🧱 Iniciando a consolidação final de todas as métricas do experimento...")
    
    # Verifica se todos os arquivos existem
    arquivos = [INPUT_EVAL, INPUT_DENSITY, INPUT_SUCCESS, INPUT_MUTATION]
    if not all(arq.exists() for arq in arquivos):
        print("❌ Erro: Algum dos arquivos de métricas está faltando na pasta data/results/.")
        print("💡 Certifique-se de ter rodado com sucesso os scripts 08, 09 e 10 antes.")
        return

    # Carrega todas as planilhas
    df_final = pd.read_csv(INPUT_EVAL)
    df_density = pd.read_csv(INPUT_DENSITY)
    df_success = pd.read_csv(INPUT_SUCCESS)
    df_mutation = pd.read_csv(INPUT_MUTATION)

    # Padroniza dinamicamente a coluna de ID de CADA uma das planilhas para 'file_name'
    df_final = padronizar_identificador(df_final, "Base Evaluation")
    df_density = padronizar_identificador(df_density, "Density")
    df_success = padronizar_identificador(df_success, "Success Rate")
    df_mutation = padronizar_identificador(df_mutation, "Mutation Score")

    # Garante que todos os IDs sejam tratados puramente como texto limpo (sem caminhos de pastas ou espaços)
    df_final['file_name'] = df_final['file_name'].astype(str).apply(lambda x: Path(x).name)
    df_density['file_name'] = df_density['file_name'].astype(str).apply(lambda x: Path(x).name)
    df_success['file_name'] = df_success['file_name'].astype(str).apply(lambda x: Path(x).name)
    df_mutation['file_name'] = df_mutation['file_name'].astype(str).apply(lambda x: Path(x).name)

    # Realiza os merges sequenciais agregando as colunas novas lado a lado com segurança
    try:
        df_final = pd.merge(df_final, df_density[['file_name', 'test_loc', 'assertion_count', 'assertion_density']], on='file_name', how='left')
        df_final = pd.merge(df_final, df_success[['file_name', 'execution_category']], on='file_name', how='left')
        df_final = pd.merge(df_final, df_mutation[['file_name', 'mutation_score']], on='file_name', how='left')

        # Salva o resultado final robusto
        df_final.to_csv(OUTPUT_FINAL, index=False)
        
        print(f"\n🏆 Sucesso Absoluto! Todos os dados foram unificados de forma segura.")
        print(f"📊 Arquivo final gerado em: {OUTPUT_FINAL}")
        print(f"\n🔍 Todas as colunas agora disponíveis no mesmo arquivo para o seu TCC:")
        for coluna in df_final.columns:
            print(f" - {coluna}")
            
    except KeyError as e:
        print(f"❌ Erro de chave durante a união dos dados: {e}")

if __name__ == "__main__":
    main()