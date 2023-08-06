import subprocess

def ola_milene():
    resultado = subprocess.check_output(["./ola_milene"])

    resultado_str = resultado.decode("utf-8")

    return resultado_str

mensagem = ola_milene()
print(mensagem)

