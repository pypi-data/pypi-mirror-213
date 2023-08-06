#include <Python.h>

int main(int argc, char *argv[]) {
    Py_SetProgramName(argv[0]);  // Define o nome do programa (opcional)

    // Inicializa o interpretador Python
    Py_Initialize();

    // Seu código em C usando funções do Python
    PyRun_SimpleString("print('Olá, mundo!')");
    // Finaliza o interpretador Python
    Py_Finalize();

    return 0;
}

