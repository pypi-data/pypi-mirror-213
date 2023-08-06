import subprocess

def executar_programa_c():
    resultado = subprocess.run(["./pythonce/ola"], capture_output=True, text=True)
    saida = resultado.stdout.strip()  # Captura a saída e remove espaços em branco
    return saida

def somar(x, y):
    resultado = subprocess.run(['./pythonce/soma', str(x), str(y)], capture_output=True, text=True)
    if resultado.returncode != 0:
        print("Erro ao executar o programa")
        return None
    else:
        return resultado.stdout.strip()
    
def olaMi():
    resultado = subprocess.run(['./pythonce/OlaMi'], capture_output=True, text=True)
    saida = resultado.stdout.strip()
    return saida
