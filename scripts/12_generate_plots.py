import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuração de caminhos do ecossistema do seu TCC
BASE_DIR = Path(__file__).parent.parent.absolute()
INPUT_FINAL = BASE_DIR / "data" / "results" / "final_experiment_results.csv"
OUTPUT_DIR = BASE_DIR / "data" / "results"

def main():
    print("📊 Iniciando o pipeline automatizado de geração de gráficos estatísticos...")
    
    # 1. Validação de segurança dos dados de entrada
    if not INPUT_FINAL.exists():
        print(f"❌ Erro: O arquivo consolidado não foi encontrado em: {INPUT_FINAL}")
        print("💡 Dica: Rode primeiro o script '11_consolidate_results.py' para unificar a base.")
        return

    # 2. Carregamento dos dados
    df = pd.read_csv(INPUT_FINAL)
    
    # 3. Configurações visuais acadêmicas (Seaborn/Matplotlib)
    sns.set_theme(style="whitegrid")
    plt.rcParams.update({
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'figure.titlesize': 16,
        'xtick.labelsize': 10,
        'ytick.labelsize': 10
    })
    
    # -------------------------------------------------------------------------
    # GRÁFICO 1: Taxa de Sucesso de Execução (Pass Rate)
    # -------------------------------------------------------------------------
    print("📸 Plotando Gráfico 1: Taxa de Sucesso (Pass Rate)...")
    plt.figure(figsize=(7, 5))
    
    # Define paleta dinâmica (Vermelhos/Laranjas para falhas, Verde para sucesso)
    categorias_unicas = df['execution_category'].dropna().unique()
    cores_mapeadas = []
    for cat in categorias_unicas:
        if "Sucesso" in str(cat):
            cores_mapeadas.append('#2ecc71')  # Verde Esmeralda
        else:
            cores_mapeadas.append('#e74c3c')  # Vermelho Alerta
            
    ax1 = sns.countplot(x='execution_category', data=df, palette=cores_mapeadas, hue='execution_category')
    plt.title('Taxa de Sucesso e Execução dos Testes Python (TCC)', pad=15, fontweight='bold')
    plt.xlabel('Categoria de Execução de Runtime')
    plt.ylabel('Quantidade de Casos (Arquivos)')
    
    if plt.gca().legend_:
        plt.gca().legend_.remove()
        
    # Insere as labels de contagem e porcentagem no topo de cada coluna de dados
    total_testes = len(df)
    for p in ax1.patches:
        height = p.get_height()
        if height > 0:
            ax1.annotate(f'{int(height)} ({height/total_testes*100:.1f}%)', 
                         (p.get_x() + p.get_width() / 2., height + 0.2), 
                         ha='center', va='center', xytext=(0, 5), textcoords='offset points', fontweight='bold')
            
    plt.tight_layout()
    path_grafico1 = OUTPUT_DIR / 'grafico_status_execucao.png'
    plt.savefig(path_grafico1, dpi=300)
    plt.close()
    print(f"✅ Salvo com sucesso em: {path_grafico1}")

    # -------------------------------------------------------------------------
    # GRÁFICO 2: Paradoxo da Cobertura vs Mutation Score
    # -------------------------------------------------------------------------
    print("📸 Plotando Gráfico 2: Paradoxo da Cobertura de Código...")
    plt.figure(figsize=(8, 5))
    
    # Cria dispersão mapeando cores pelo status
    sns.scatterplot(
        x='coverage_percent', 
        y='mutation_score', 
        hue='execution_category', 
        style='execution_category', 
        s=130, 
        palette={'Sucesso Direto (Pass Rate)': '#2ecc71', 'Falha de Execução (Runtime/Assertion Error)': '#e74c3c'}, 
        data=df,
        alpha=0.85
    )
    
    plt.title('Paradoxo da Cobertura: Cobertura de Código vs. Mutation Score', pad=15, fontweight='bold')
    plt.xlabel('Cobertura de Código Estrutural (%)')
    plt.ylabel('Mutation Score Real (%)')
    plt.xlim(-5, 105)
    plt.ylim(-5, 105)
    plt.legend(title='Status do Caso de Teste', loc='upper left', frameon=True)
    plt.tight_layout()
    
    path_grafico2 = OUTPUT_DIR / 'grafico_paradoxo_cobertura.png'
    plt.savefig(path_grafico2, dpi=300)
    plt.close()
    print(f"✅ Salvo com sucesso em: {path_grafico2}")

    print("\n🏁 [CONCLUÍDO] Todos os gráficos foram atualizados na pasta data/results/!")

if __name__ == "__main__":
    main()