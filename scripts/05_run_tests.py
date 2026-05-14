import pandas as pd
import subprocess
import json
import os
from pathlib import Path

# Configurações de pastas usando caminhos absolutos do seu PC
BASE_DIR = Path(r"C:\Users\diogo\OneDrive\Área de Trabalho\Diogo\PUC\8 Periodo\TCC\TCC2_2026")
INPUT_SAMPLE = BASE_DIR / "data" / "selected_functions" / "pilot_sample_30.csv"
TESTS_DIR = BASE_DIR / "tests" / "generated_tests"
RESULTS_DIR = BASE_DIR / "data" / "results"
REPO_PATH = BASE_DIR / "repos" / "Python"

def main():
    if not INPUT_SAMPLE.exists():
        print(f"Arquivo não encontrado: {INPUT_SAMPLE}")
        return

    df = pd.read_csv(INPUT_SAMPLE)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    # Configura o PYTHONPATH explicitamente
    env = os.environ.copy()
    env["PYTHONPATH"] = str(REPO_PATH)

    print(" Iniciando medição final...")

    for i, row in df.iterrows():
        test_file = TESTS_DIR / f"test_{i:02d}_{row['function_name']}.py"
        
        # Comando focado apenas em rodar o teste e gerar o JSON
        # Removi o redirecionamento para DEVNULL para você ver o erro se acontecer
        cmd = [
            "pytest",
            f"--cov={REPO_PATH}",
            "--cov-report=json:coverage.json",
            str(test_file)
        ]

        print(f"[{i+1}/30] {row['function_name']}...", end=" ")
        
        # Executa e espera terminar
        subprocess.run(cmd, env=env, capture_output=True)
        
        cov_percent = 0.0
        cov_file = Path("coverage.json")
        
        if cov_file.exists():
            try:
                with open(cov_file, 'r') as f:
                    data = json.load(f)
                    cov_percent = data['totals']['percent_covered']
                cov_file.unlink() # Deleta para não interferir no próximo
                print(f" {cov_percent}%")
            except:
                print(" Erro no JSON")
        else:
            print(" Sem reporte")

        results.append({
            "function_name": row['function_name'],
            "complexity_level": row['complexity_level'],
            "coverage_percent": cov_percent
        })

    # Salva o resultado
    pd.DataFrame(results).to_csv(RESULTS_DIR / "coverage_results_gpt4.csv", index=False)
    print(f"\n✅ Processo finalizado!")

if __name__ == "__main__":
    main()