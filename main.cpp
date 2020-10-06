#include <iostream>
//using namespace std;

class Node
{
private:
    bool is_root;
    unsigned char square; // CANNOT BE -1. Square from 0 to 8.
    unsigned char player; // 0 for X, 1 for O
    signed char score; // Positive favors X, Negative favors O
    unsigned char best_move;
    
public:
    Node(bool root=false, unsigned char sq=0, unsigned char plr=1)
    {
        is_root = root;
        square = sq;
        player = plr;
    }
    int minimax();
    void update_board();
    void revert_board();
    void traverse(int level=0);
};

int main()
{
    
}
