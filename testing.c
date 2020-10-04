// Just some testing
// Written by Isaac Thompson

#include <stdio.h> // Input/Output
#include <stdlib.h> // Memory Management, String Conversions, etc

int main(int argc, char** argv) {
    int a, b;
    printf("Enter a number: ");
    scanf("%d", &a);
    printf("Enter another number: ");
    scanf("%d", &b);
    printf("The product is %d\n", a*b);
    printf("Address of a is &x\n", &a);
    printf("Address of b is &x\n", &b);
}
