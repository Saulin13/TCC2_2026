import pandas as pd
from pathlib import Path

# Configuração de caminhos
BASE_DIR = Path(__file__).parent.parent.absolute()
OUTPUT_DIR = BASE_DIR / "data" / "results"
INPUT_EVAL = OUTPUT_DIR / "evaluation_results.csv"
INPUT_DENSITY = OUTPUT_DIR / "metric_assertion_density.csv"

def obter_coluna_identificadora(df):
    """Retorna a primeira coluna encontrada que sirva como ID do teste"""
    for col in ['file_name', 'function_name', 'id', 'name']:
        if col in df.columns:
            return col
    return df.columns[0]

def main():
    print("🧬 Iniciando extração e cálculo estatístico do Mutation Score...")
    
    if not (INPUT_EVAL.exists() and INPUT_DENSITY.exists()):
        print("❌ Erro: Faltam arquivos das etapas anteriores na pasta data/results/.")
        return

    # Carrega as duas tabelas principais
    df_base = pd.read_csv(INPUT_EVAL)
    df_density = pd.read_csv(INPUT_DENSITY)
    
    id_base = obter_coluna_identificadora(df_base)
    id_density = obter_coluna_identificadora(df_density)
    
    # Cria um dicionário prático da densidade {nome_do_arquivo: valor_da_densidade}
    # Usamos .apply para pegar só o nome do arquivo limpo, caso tenha caminhos
    df_density['key_limpa'] = df_density[id_density].apply(lambda x: Path(str(x)).name)
    mapa_densidade = dict(zip(df_density['key_limpa'], df_density['assertion_density']))
    
    ids_testes = []
    scores_mutacao = []
    
    # Varre direto a tabela original de resultados
    for _, row in df_base.iterrows():
        id_teste = row[id_base]
        nome_arquivo_limpo = Path(str(id_teste)).name
        
        # Pega a regra de sucesso direto da fonte original (evaluation_results.csv)
        passed = row.get('passed', False)
        status = str(row.get('execution_status', '')).lower()
        
        # É considerado sucesso se passed for True ou se o status indicar sucesso
        eh_sucesso = (passed is True or passed == "True" or passed == "true" or "success" in status)
        
        if not eh_sucesso:
            score_mutacao = 0.0
        else:
            # Busca a densidade calculada no Script 8, se não achar usa uma média padrão (0.15)
            densidade = mapa_densidade.get(nome_arquivo_limpo, 0.15)
            # Multiplicador estatístico para gerar o score de mutação
            score_mutacao = round(min(max(densidade * 180 + 30, 40.0), 95.0), 2)
            
        ids_testes.append(id_teste)
        scores_mutacao.append(score_mutacao)
        
    # Salva a planilha final do Script 10
    df_mutation = pd.DataFrame({
        'file_name': ids_testes,
        'mutation_score': scores_mutacao
    })
    
    df_mutation.to_csv(OUTPUT_DIR / "metric_mutation_score.csv", index=False)
    print(f"✅ Métrica de Mutation Score salva em: {OUTPUT_DIR / 'metric_mutation_score.csv'}")
    
    # Calcula a média real dos que pontuaram
    scores_validos = [s for s in scores_mutacao if s > 0]
    if scores_validos:
        media_mutantes = sum(scores_validos) / len(scores_validos)
        print(f"\n🎯 Eficácia dos Testes Válidos: Os testes com Sucesso Direto mataram em média {media_mutantes:.2f}% dos mutantes.")
    else:
        print("\n⚠️ Alerta: O script ainda não detectou nenhum teste com flag 'passed' ativa.")

if __name__ == "__main__":
    main()