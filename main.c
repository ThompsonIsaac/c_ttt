// C Program to solve Tic Tac Toe problems
// Written by Isaac Thompson

#include <stdio.h> // Input/Output
#include <stdlib.h> // Memory Management, String Conversions, etc

struct node {
    signed char square; // 0 to 8, -1 if no square
    signed char winner; // 0 if no winner, 1 if X wins, 2 if O wins
    struct node *next[9];
    
    // Method add_layer()
    // for i in range(9):
    //     next[i] = new node()
    //     
}

int main(int argc, char** argv) {
    unsigned char board[9] = {0,0,0,0,0,0,0,0,0};
    printf("Elements %d %d %d\n", board[0], board[4], board[8]);
}
