#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

int* Fibonacci(int length) {
    int* fibonacci[length];
    fibonacci[0] = 0;
    fibonacci[1] = 1;
    for (int i = 2; i < length; i++) {
        fibonacci[i] = fibonacci[i - 1] + fibonacci[i - 2];
    }
    return fibonacci;
}

int main() {
    int length = 10;
    int* fibonacci = Fibonacci(length);
    for (int step = 0; step < length; step++) printf("Fibonacci #%d: %d", step, fibonacci[step]);
    printf("\n");
    return 0;
}