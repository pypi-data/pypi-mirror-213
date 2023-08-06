import subprocess

def executar_programa_c():
    resultado = subprocess.run(["./pythonce/ola"], capture_output=True, text=True)
    saida = resultado.stdout.strip()  # Captura a saída e remove espaços em branco
    return saida

def somar(x, y):
    resultado = subprocess.run(['./pythonce/soma', str(x), str(y)], capture_output=True, text=True)
    return resultado.stdout.strip()
    
def ola_milene():
    resultado = subprocess.check_output(["./pythonce/OlaMi"])

    resultado_str = resultado.decode("utf-8")

    return resultado_str