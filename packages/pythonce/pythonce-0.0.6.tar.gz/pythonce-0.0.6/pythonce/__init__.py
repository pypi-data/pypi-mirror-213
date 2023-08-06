import os
import subprocess

def executar_programa_c():
    module_path = os.path.dirname(__file__)
    executable_path = os.path.join(module_path, "ola")
    resultado = subprocess.run([executable_path], capture_output=True, text=True)
    saida = resultado.stdout.strip()  # Captura a saída e remove espaços em branco
    return saida

def soma(x, y):
    module_path = os.path.dirname(__file__)
    executable_path = os.path.join(module_path, "soma")
    resultado = subprocess.run([executable_path, str(x), str(y)], capture_output=True, text=True)
    return resultado.stdout.strip()

def subtracao(x, y):
    module_path = os.path.dirname(__file__)
    executable_path = os.path.join(module_path, "subtracao")
    resultado = subprocess.run([executable_path, str(x), str(y)], capture_output=True, text=True)
    return resultado.stdout.strip()




























def ola_milene():
    module_path = os.path.dirname(__file__)
    executable_path = os.path.join(module_path, "OlaMi")
    resultado = subprocess.check_output([executable_path])

    resultado_str = resultado.decode("utf-8")

    return resultado_str
