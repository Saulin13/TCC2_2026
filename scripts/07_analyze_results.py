import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats

# Configuração de caminhos - Usando caminhos relativos para evitar problemas no Windows
BASE_DIR = Path(__file__).parent.parent.absolute()
INPUT_EVAL = BASE_DIR / "data" / "results" / "evaluation_results.csv"
OUTPUT_DIR = BASE_DIR / "data" / "results" / "plots"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    if not INPUT_EVAL.exists():
        print(f" Erro: Arquivo não encontrado em {INPUT_EVAL}")
        return

    # 1. Carregar Dados
    df = pd.read_csv(INPUT_EVAL)
    
    # Tratamento robusto das colunas de nota e cobertura
    if "overall_score" in df.columns:
        df["nota"] = pd.to_numeric(df["overall_score"], errors="coerce").fillna(0.0)
    elif "evaluation" in df.columns:
        def extract_nota(eval_str):
            try:
                data = json.loads(eval_str)
                return float(data.get('nota', 0))
            except:
                return 0.0
        df["nota"] = df["evaluation"].apply(extract_nota)
    else:
        df["nota"] = 0.0

    cov_col = "coverage_percent" if "coverage_percent" in df.columns else "coverage"
    df["coverage"] = pd.to_numeric(df[cov_col], errors="coerce").fillna(0.0)
    
    # Filtra apenas registros válidos para a análise acadêmica
    df_plot = df[df['nota'] > 0].copy()
    n_samples = len(df_plot)

    if n_samples == 0:
        print(" Nenhum dado válido encontrado para gerar os gráficos.")
        return

    # Limpa configurações anteriores da memória do matplotlib
    plt.close('all')
    
    # Configuração Visual Acadêmica (Corrigido sem o parâmetro global 'alpha')
    sns.set_theme(style="whitegrid", rc={"grid.linestyle": "--"})
    plt.rcParams.update({'font.size': 11, 'axes.labelsize': 12, 'axes.titlesize': 14})

    # --- GRÁFICO 1: Cobertura vs Nota (Dispersão com Regressão) ---
    fig1, ax1 = plt.subplots(figsize=(9, 5.5))
    
    # Plota a linha de tendência e os pontos (Ajustado para 'linewidths')
    sns.regplot(
        data=df_plot,
        x="coverage",
        y="nota", 
        ax=ax1,
        scatter_kws={'s': 80, 'alpha': 0.7, 'color': '#1f77b4', 'edgecolor': 'w', 'linewidths': 0.8},
        line_kws={'color': '#d62728', 'linewidth': 2}
    )
    
    # Calcula a correlação de Pearson de forma dinâmica para colocar no gráfico
    if n_samples > 1:
        r_val, _ = stats.pearsonr(df_plot["coverage"], df_plot["nota"])
        text_stats = f"Coef. Correlação (r): {r_val:.2f}\nAmostras (N): {n_samples}"
        ax1.text(0.05, 0.05, text_stats, transform=ax1.transAxes,
                 bbox=dict(facecolor='white', alpha=0.9, edgecolor='gainsboro', boxstyle='round,pad=0.5'))

    ax1.set_title('Análise de Correlação: Cobertura de Código vs. Qualidade do Teste (LLM)', pad=15, fontsize=13, weight='bold')
    ax1.set_xlabel('Cobertura de Código (Percentual)', fontsize=11)
    ax1.set_ylabel('Nota Avaliação IA (0 a 10)', fontsize=11)
    ax1.set_xlim(-5, 105)
    ax1.set_ylim(-0.5, 10.5)
    
    plt.savefig(OUTPUT_DIR / "01_dispersao_cobertura_nota.png", dpi=300, bbox_inches='tight')
    print(" Gráfico de dispersão gerado com sucesso.")

    # --- GRÁFICO 2: Boxplot de Notas (Distribuição Limpa e sem Duplicações) ---
    fig2, ax2 = plt.subplots(figsize=(6, 6))
    
    # showfliers=False desativa a plotagem de outliers nativa para evitar duplicar pontos confuso
    sns.boxplot(
        y=df_plot['nota'], 
        color='#8c564b', 
        width=0.35,
        showfliers=False,
        ax=ax2,
        boxprops=dict(alpha=0.25, edgecolor='#8c564b', linewidth=1.5),
        medianprops=dict(color='#d62728', linewidth=2.5) # Linha da mediana em destaque
    )
    
    # O stripplot desenha os pontos reais uma única vez por cima do esqueleto do Boxplot
    sns.stripplot(
        y=df_plot['nota'], 
        color='#1f77b4', 
        size=8, 
        alpha=0.75, 
        jitter=0.08, 
        edgecolor='w',
        ax=ax2
    )
    
    # Adiciona o texto descritivo com o valor exato da Mediana no gráfico
    mediana = df_plot['nota'].median()
    ax2.text(0.22, mediana, f' Mediana: {mediana:.1f}', 
             va='center', ha='left', color='#d62728', weight='bold', fontsize=11)

    ax2.set_title('Distribuição da Qualidade das Notas dos Testes', pad=15, fontsize=13, weight='bold')
    ax2.set_ylabel('Nota Final Avaliada (0 a 10)', fontsize=11)
    ax2.set_ylim(-0.5, 10.5)
    
    plt.savefig(OUTPUT_DIR / "02_boxplot_notas.png", dpi=300, bbox_inches='tight')
    print(" Boxplot de notas corrigido e gerado com sucesso.")

    print(f"\n Sucesso absoluto! Confira as imagens atualizadas em: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()