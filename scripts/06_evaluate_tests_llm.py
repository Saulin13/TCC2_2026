import pandas as pd
import openai
from pathlib import Path
import os

# Configurações de caminhos
BASE_DIR = Path(r"C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026")
INPUT_RESULTS = BASE_DIR / "data" / "results" / "coverage_results_gpt4.csv"
SAMPLE_FILE = BASE_DIR / "data" / "selected_functions" / "pilot_sample_30.csv"
TESTS_DIR = BASE_DIR / "tests" / "generated_tests"
OUTPUT_EVAL = BASE_DIR / "data" / "results" / "evaluation_results.csv"

# Sua chave API (mantenha a que você já está usando)
client = openai.OpenAI(api_key="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")

def evaluate_test(func_code, test_code, coverage):
    prompt = f"""
    Como um especialista em QA, avalie a qualidade deste teste unitário gerado para a função abaixo.
    
    Cobertura alcançada: {coverage}%
    
    Código da Função:
    {func_code}
    
    Código do Teste:
    {test_code}
    
    Responda em formato JSON com:
    1. "nota": (0 a 10)
    2. "analise": (Resumo da eficácia do teste)
    3. "falhas": (O que faltou testar?)
    """
    
    response = client.chat.completions.create(
        model="gpt-4o", # Ou o modelo que você preferir
        messages=[{"role": "user", "content": prompt}],
        response_format={ "type": "json_object" }
    )
    return response.choices[0].message.content

def main():
    df_results = pd.read_csv(INPUT_RESULTS)
    df_sample = pd.read_csv(SAMPLE_FILE)
    
    evaluations = []
    
    print(" Iniciando avaliação qualitativa dos testes...")

    # Vamos avaliar as primeiras funções para testar (você pode rodar em todas depois)
    for i, row in df_results.iterrows():
        func_name = row['function_name']
        coverage = row['coverage_percent']
        
        # Busca o código fonte original no pilot_sample
        source_code = df_sample[df_sample['function_name'] == func_name]['source_code'].values[0]
        
        # Busca o código do teste gerado
        test_file = TESTS_DIR / f"test_{i:02d}_{func_name}.py"
        test_code = test_file.read_text(encoding="utf-8") if test_file.exists() else "Teste não encontrado"

        print(f"[{i+1}/30] Avaliando: {func_name}...")
        
        try:
            eval_json = evaluate_test(source_code, test_code, coverage)
            evaluations.append({
                "function_name": func_name,
                "coverage": coverage,
                "evaluation": eval_json
            })
        except Exception as e:
            print(f"Erro na API: {e}")

    # Salva o resultado final do TCC
    pd.DataFrame(evaluations).to_csv(OUTPUT_EVAL, index=False)
    print(f" Avaliação concluída! Resultados salvos em: {OUTPUT_EVAL}")

if __name__ == "__main__":
    main()