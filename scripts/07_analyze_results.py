import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Configuração de caminhos - Usando caminhos relativos para evitar erro de espaço no Windows
BASE_DIR = Path(__file__).parent.parent.absolute()
INPUT_EVAL = BASE_DIR / "data" / "results" / "evaluation_results.csv"
OUTPUT_DIR = BASE_DIR / "data" / "results" / "plots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_nota(eval_str):
    try:
        # Tenta carregar o JSON. Se falhar, procura o número da nota via texto
        data = json.loads(eval_str)
        return float(data.get('nota', 0))
    except:
        return 0.0

def main():
    if not INPUT_EVAL.exists():
        print(f" Erro: Arquivo não encontrado em {INPUT_EVAL}")
        return

    # 1. Carregar Dados
    df = pd.read_csv(INPUT_EVAL)
    if "overall_score" in df.columns:
        df["nota"] = pd.to_numeric(df["overall_score"], errors="coerce").fillna(0.0)
    elif "evaluation" in df.columns:
        df["nota"] = df["evaluation"].apply(extract_nota)
    else:
        df["nota"] = 0.0

    if "coverage_percent" in df.columns:
        df["coverage"] = pd.to_numeric(df["coverage_percent"], errors="coerce").fillna(0.0)
    elif "coverage" not in df.columns:
        df["coverage"] = 0.0
    
    # Filtra apenas quem tem nota maior que 0 para o gráfico não ficar poluído
    df_plot = df[df['nota'] > 0].copy()

    # Configuração Visual
    sns.set_theme(style="whitegrid")
    
    # --- GRÁFICO 1: Cobertura vs Nota ---
    plt.figure(figsize=(10, 6))
    cov_col = "coverage_percent" if "coverage_percent" in df_plot.columns else "coverage"
    sns.regplot(
        data=df_plot,
        x=cov_col,
        y='nota', 
        scatter_kws={'s': 100, 'alpha': 0.6, 'color': '#2c3e50'},
        line_kws={'color': '#e74c3c'}
    )
    
    plt.title('Correlação: Cobertura de Código vs. Qualidade do Teste', fontsize=14)
    plt.xlabel('Cobertura (Percentual)', fontsize=12)
    plt.ylabel('Nota IA (0-10)', fontsize=12)
    plt.ylim(-0.5, 10.5)

    plt.savefig(OUTPUT_DIR / "01_dispersao_cobertura_nota.png", dpi=300, bbox_inches='tight')
    print(" Gráfico de dispersão gerado com linha de tendência.")

    # --- GRÁFICO 2: Boxplot de Notas ---
    plt.figure(figsize=(8, 6))
    sns.boxplot(y=df_plot['nota'], color='#1abc9c')
    sns.stripplot(y=df_plot['nota'], color='#2c3e50', size=4, jitter=True)
    
    plt.title('Distribuição de Qualidade dos Testes Gerados', fontsize=14)
    plt.ylabel('Nota Final', fontsize=12)
    
    plt.savefig(OUTPUT_DIR / "02_boxplot_notas.png", dpi=300, bbox_inches='tight')
    print(" Boxplot de notas gerado.")

    print(f"\n Sucesso! Confira as imagens em: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()