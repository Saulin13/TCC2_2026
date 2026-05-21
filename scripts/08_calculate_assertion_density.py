import os
import re
import pandas as pd
from pathlib import Path

# Configuração de caminhos
BASE_DIR = Path(__file__).parent.parent.absolute()
TESTS_DIR = BASE_DIR / "tests" / "generated" 
OUTPUT_DIR = BASE_DIR / "data" / "results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def calcular_metricas_codigo(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Remove linhas vazias e comentários simples (#) para ter as Linhas de Código Reais (LOC)
    linhas_codigo = [l.strip() for l in linhas if l.strip() and not l.strip().startswith("#")]
    total_loc = len(linhas_codigo)
    
    if total_loc == 0:
        return 0, 0
    
    # Conta quantas vezes a palavra 'assert' aparece no código de teste Python
    conteudo_completo = "".join(linhas_codigo)
    assercoes = re.findall(r'\bassert\b', conteudo_completo)
    total_assercoes = len(assercoes)
    
    return total_loc, total_assercoes

def main():
    print("🔍 Iniciando cálculo de Densidade de Asserções nos testes Python...")
    
    if not TESTS_DIR.exists():
        print(f"❌ Erro: Diretório de testes não encontrado em {TESTS_DIR}")
        return

    resultados = []
    
    # Varre a pasta tests/generated procurando arquivos .py
    for root, _, files in os.walk(TESTS_DIR):
        for file in files:
            if file.endswith(".py") and file.startswith("test_"):
                caminho_completo = Path(root) / file
                loc, asserts = calcular_metricas_codigo(caminho_completo)
                
                # Densidade = Asserções / Linhas de Código
                densidade = round(asserts / loc, 4) if loc > 0 else 0.0
                
                resultados.append({
                    "file_name": file,
                    "test_loc": loc,
                    "assertion_count": asserts,
                    "assertion_density": densidade
                })

    if not resultados:
        print("⚠️ Nenhum arquivo test_*.py encontrado para análise.")
        return

    df = pd.DataFrame(resultados)
    df.to_csv(OUTPUT_DIR / "metric_assertion_density.csv", index=False)
    print(f"✅ Métrica de Densidade de Asserções salva em: {OUTPUT_DIR / 'metric_assertion_density.csv'}")

if __name__ == "__main__":
    main()