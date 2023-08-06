#include <stdio.h>
#include <stdlib.h>
int main(int argc, char *argv[]){
	if (argc <3 ){
	printf("Digite os valores de a e b\n");
	return 1;
	}

	int a = atoi(argv[1]);
	int b = atoi(argv[2]);

	int resultado = a +b;

	printf("O resltado é %d\n", resultado);
	ncmreturn 0;
}
