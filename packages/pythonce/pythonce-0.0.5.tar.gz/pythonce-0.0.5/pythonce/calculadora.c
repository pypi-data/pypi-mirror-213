#include <stdio.h>

// Função de soma
float soma(float a, float b) {
    return a + b;
}

// Função de subtração
float subtracao(float a, float b) {
    return a - b;
}

// Função de multiplicação
float multiplicacao(float a, float b) {
    return a * b;
}

// Função de divisão
float divisao(float a, float b) {
    return a / b;
}

int main() {
    float x, y;

    // Exemplo de uso da função de soma
    x = 5;
    y = 3;
    printf("%.2f + %.2f = %.2f\n", x, y, soma(x, y));

    // Exemplo de uso da função de subtração
    x = 5;
    y = 3;
    printf("%.2f - %.2f = %.2f\n", x, y, subtracao(x, y));

    // Exemplo de uso da função de multiplicação
    x = 5;
    y = 3;
    printf("%.2f * %.2f = %.2f\n", x, y, multiplicacao(x, y));

    // Exemplo de uso da função de divisão
    x = 5;
    y = 3;
    printf("%.2f / %.2f = %.2f\n", x, y, divisao(x, y));

    return 0;
}
