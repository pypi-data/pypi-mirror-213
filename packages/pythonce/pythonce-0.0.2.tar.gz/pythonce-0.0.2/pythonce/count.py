import subprocess

def executar_programa_c():
    resultado = subprocess.run(["./ola"], capture_output=True, text=True)
    saida = resultado.stdout.strip()  # Captura a saída e remove espaços em branco
    return saida

saida_programa_c = executar_programa_c()
print(saida_programa_c)

