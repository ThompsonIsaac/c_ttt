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

    # Get best move. Assumes minimax was already called
    def get_best_move(self):
        best_child = None
        if self.player == X:
            best_score = 100
            for child in self.children:
                if child.score < best_score:
                    best_child = child
                    best_score = child.score
        else:
            best_score = -100
            for child in self.children:
                if child.score > best_score:
                    best_child = child
                    best_score = child.score
        if best_child == None:
            return -1
        return best_child.square

    # Add a level of nodes below this node
    def minimax(self, board, depth=0, alpha=-100, beta=100):

        # Update board according to this parent node
        self.update_board(board)

        # Set our score to the best possible case - minimax will override later
        if self.player == X:
            self.score = 100
            next_player = O
        else:
            self.score = -100
            next_player = X

        # If terminal node, just score this node (the higher the depth, the better)
        if board.is_terminal() or depth == 0:
            self.score = board.get_score()

        # Otherwise create new children and evaluate
        else:
            for i in range(9):
                if board.is_square_open(i):
                    
                    # Create new node and branches
                    new_node = Node(i, next_player, False)
                    self.children.append(new_node)
                    score = new_node.minimax(board, depth - 1, alpha, beta)

                    # Update this node's score according to child score
                    if self.player == X and score < self.score:
                        self.score = score
                    elif self.player == O and score > self.score:
                        self.score = score

                    # Apply alpha-beta pruning
                    if self.player == O:
                        alpha = max(alpha, score)
                        if (alpha >= beta):
                            pass
                    else:
                        beta = min(beta, score)
                        if (beta <= alpha):
                            pass

        # Revert board to before this parent node
        self.revert_board(board)

        return self.score

    # Update the board according to this node's move data
    def update_board(self, board):
        if self.square != -1:
            board.move(self.player, self.square)

    # Revert the board to before this node
    def revert_board(self, board):
        if self.square != -1:
            board.undo_move(self.square)

    # Print a traversal of the entire game tree
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
        self.squares_left = 9 # Number of empty squares

    # Print the board in a user-friendly way
    def print(self):
        print()
        print("    A   B   C\n")
        for i in range(3):
            print(str(i + 1) + " " * 3 + self.board[i*3] + " | " + self.board[(i*3)+1] + " | " + self.board[(i*3)+2])
            if i < 2:
                print(" "*3 + "-"*9)
        print()

    # Add move data to the board
    def move(self, player, square):
        assert self.is_square_open(square), "Cannot move on occupied tile"
        self.board[square] = player
        self.squares_left -= 1
        self.update_winner()

    # Remove move data from the board
    def undo_move(self, square):
        assert not self.is_square_open(square), "Cannot undo a move that hasn't been taken"
        self.board[square] = EMPTY
        self.squares_left += 1
        #self.update_winner()

    # See if a square is available
    def is_square_open(self, square):
        if square == -1:
            return False
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
    def is_full(self):
        for i in range(9):
            if self.board[i] == EMPTY:
                return False
        return True

    # Return true if the board is terminal
    def is_terminal(self):
        return self.is_full() or self.get_winner() != None

    # Get the score of this board pos. -1 if O wins, 1 if X wins.
    def get_score(self):
        winner = self.get_winner()
        if winner == X:
            return self.squares_left + 1
        elif winner == O:
            return -self.squares_left - 1
        return 0

    # Convert a user-input coordinate (A3, 2b, etc.) to a number, or -1 if failure
    def get_square_from_string(self, coord):
        if not isinstance(coord, str):
            return -1
        if len(coord) != 2:
            return -1
        coord = coord.lower()
        alpha = None
        numb = None
        if coord[0].isalpha() and coord[1].isnumeric():
            alpha = coord[0]
            numb = int(coord[1]) - 1
        elif coord[0].isnumeric() and coord[1].isalpha():
            alpha = coord[1]
            numb = int(coord[0]) - 1
        else:
            return -1
        if not alpha in ['a', 'b', 'c']:
            return -1
        if numb < 0 or numb > 2:
            return -1
        return {'a': 0, 'b': 1, 'c': 2}[alpha] + (int(numb) * 3)

def main():
    board = Board()
    start = 'a'
    while start != 'y' and start != 'n':
        start = input("You go first? (y/n) ")
        start = start.lower()
    skip = (start == 'n')

    while True:
        # Player's turn
        if skip:
            skip = False
        else:
            board.print()
            square = -1
            while not board.is_square_open(square):
                move = input("Input move: (a2, 3c, etc.) ")
                square = board.get_square_from_string(move)
            board.move(X, square)
            if board.is_full():
                print("Board is full. Draw game!")
                break
            elif board.is_terminal():
                print("You win!")
                break

        # CPU's turn
        start = perf_counter()
        root = Node(player=X)
        root.minimax(board, depth=6)
        #root.traverse()
        best_move = root.get_best_move()
        if best_move == -1:
            print("Error: Could not find a move.")
            break
        print("Took " + str(perf_counter() - start) + " to find the best move")
        board.move(O, best_move)
        
        if board.is_full():
            board.print()
            print("Board is full. Draw game!")
            break
        elif board.is_terminal():
            print("I win!")
            break

if __name__ == "__main__":
    main()
