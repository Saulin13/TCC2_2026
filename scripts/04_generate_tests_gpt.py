import pandas as pd
from pathlib import Path
from openai import OpenAI

# Configurações de Caminho
INPUT_SAMPLE = Path("data/selected_functions/pilot_sample_30.csv")
OUTPUT_TESTS_DIR = Path("tests/generated_tests")

# COLOQUE A CHAVE QUE VOCÊ ACABOU DE COPIAR AQUI
client = OpenAI(api_key="CHAVE_FICA_AQUI")

def generate_test_with_gpt(function_code, complexity):
    prompt = f"Gere um teste unitário em pytest para esta função (Complexidade {complexity}):\n\n{function_code}\n\nRetorne apenas o código."
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.replace("```python", "").replace("```", "")

def main():
    if not INPUT_SAMPLE.exists():
        print("Erro: Arquivo pilot_sample_30.csv não encontrado!")
        return

    df = pd.read_csv(INPUT_SAMPLE)
    OUTPUT_TESTS_DIR.mkdir(parents=True, exist_ok=True)

    for i, row in df.iterrows():
        file_name = f"test_{i:02d}_{row['function_name']}.py"
        print(f"Gerando teste {i+1}/30: {row['function_name']}...")
        
        test_code = generate_test_with_gpt(row['source_code'], row['complexity_level'])
        (OUTPUT_TESTS_DIR / file_name).write_text(test_code, encoding="utf-8")

    print(f"\n Sucesso! Testes salvos em: {OUTPUT_TESTS_DIR.resolve()}")

if __name__ == "__main__":
    main()