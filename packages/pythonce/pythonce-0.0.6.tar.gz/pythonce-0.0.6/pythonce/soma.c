#include <stdio.h>
#include <stdlib.h>

int soma(int a, int b) {
    return a + b;
}

int main(int argc, char *argv[]) {
    int x, y, resultado;

    if (argc != 3) {
        printf("Uso: %s num1 num2\n", argv[0]);
        return 1;
    }

    x = atoi(argv[1]);
    y = atoi(argv[2]);

    resultado = soma(x, y);

    printf("%d\n", (int)resultado);

    return 0;
}
