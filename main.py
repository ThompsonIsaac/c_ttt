# Tic tac toe program in Python
# Written as a template for the C program

from time import perf_counter

X = 'X'
O = 'O'
EMPTY = '-'

# Node in minimax tree
class Node():
    
    # Initialize node
    def __init__(self, square=-1, player=O, root=True):
        self.is_root = root
        self.square = square # 0 to 8
        self.player = player # Player who went (X or O)
        self.score = 0 # 1 if X wins, -1 if O wins
        self.children = []

    # Assign a score for this node
    def score_self(self, board):
        # Update board according to this node
        self.update_board(board)
        
        # Generate score
        winner = board.get_winner()
        if winner == X:
            self.score = 1
        elif winner == O:
            self.score = -1
        else:
            self.score = 0
        
        # Revert board to before this node
        self.revert_board(board)

        return self.score

    # Add a level of nodes below this node
    def add_level(self, board, alpha=-1, beta=1):
        # Update board according to this parent node
        self.update_board(board)

        # Set our score to the best possible case - minimax will override later
        if self.player == X:
            self.score = 1
            next_player = O
        else:
            self.score = -1
            next_player = X
        
        # Create new children
        if len(self.children) == 0 and board.get_winner() == None:
            for i in range(9):
                if board.is_square_open(i):
                    new_node = Node(i, next_player, False)
                    self.children.append(new_node)
                    score = new_node.score_self(board)
                    
                    self.update_score(score)
                    if self.player == O:
                        alpha = max(alpha, score)
                        if (alpha >= beta):
                            break
                    else:
                        beta = min(beta, score)
                        if (beta <= alpha):
                            break
                    
        # Tell children to add level of nodes below them
        else:
            for child in self.children:
                score = child.add_level(board, alpha, beta)

                self.update_score(score)
                if self.player == O:
                    alpha = max(alpha, score)
                    if (alpha >= beta):
                        break
                else:
                    beta = min(beta, score)
                    if (beta <= alpha):
                        break

        # Revert board to before this parent node
        self.revert_board(board)

        return self.score

    # Update current score according to minimax
    def update_score(self, score):
        if self.player == X and score < self.score:
            self.score = score
        elif self.player == O and score > self.score:
            self.score = score

    # Update the board according to this node's move data
    def update_board(self, board):
        if self.square != -1:
            board.move(self.player, self.square)

    # Revert the board to before this node
    def revert_board(self, board):
        if self.square != -1:
            board.undo_move(self.square)

    # Print a traversal of the entire tree
    def traverse(self, level=0):
        if self.is_root:
            print("Root Node - Score " + str(self.score))
        else:
            print("  " * level + "Player " + self.player + ", Square " + str(self.square) + ", Score " + str(self.score))
        for child in self.children:
            child.traverse(level + 1)

# Store data about the 3x3 grid
class Board():

    # Initialize a 3x3 grid as a 9-long array
    def __init__(self):
        self.board = [EMPTY] * 9 # 3x3 grid
        self.winner = None

    def print(self):
        for i in range(3):
            print(self.board[i*3] + " | " + self.board[(i*3)+1] + " | " + self.board[(i*3)+2])
            if i < 2:
                print("-"*9)

    # Add move data to the board
    def move(self, player, square):
        assert self.is_square_open(square), "Cannot move on occupied tile"
        self.board[square] = player
        self.update_winner()

    # Remove move data from the board
    def undo_move(self, square):
        assert not self.is_square_open(square), "Cannot undo a move that hasn't been taken"
        self.board[square] = EMPTY
        self.update_winner() # NOTE THAT WE COULD PROBABLY JUST SET THE WINNER TO NONE BECAUSE OF MINIMAX.

    # See if a square is available
    def is_square_open(self, square):
        return self.board[square] == EMPTY

    # Determine the current winner
    def update_winner(self):
        self.winner = None
        for i in range(3):
            start = self.board[i*3]
            if start != EMPTY and start == self.board[(i*3)+1] and start == self.board[(i*3)+2]:
                self.winner = start
                break
        for j in range(3):
            start = self.board[j]
            if start != EMPTY and start == self.board[j+3] and start == self.board[j+6]:
                self.winner = start
                break
        start = self.board[0]
        if start != EMPTY and start == self.board[4] and start == self.board[8]:
            self.winner = start
        start = self.board[2]
        if start != EMPTY and start == self.board[4] and start == self.board[6]:
            self.winner = start

    # Get the current winner
    def get_winner(self):
        return self.winner

    # Return true if the board is full
    def is_board_full(self):
        for i in range(9):
            if self.board[i] == EMPTY:
                return False
        return True

def main():
    start = perf_counter()
    print("Started.")
    board = Board()
    board.move(O, 0)
    board.move(O, 8)
    board.print()
    root = Node()
    for i in range(6):
        root.add_level(board)
    #root.traverse()
    print("Done.")
    print(perf_counter() - start)

if __name__ == "__main__":
    main()
