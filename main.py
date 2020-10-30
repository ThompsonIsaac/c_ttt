# Tic tac toe program in Python by Isaac Thompson
# Focuses on Object Oriented Programming

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
        self.score = 0 # Positive favors X, Negative favors O
        self.best_move = -1 # Best move for the next node

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
                    #self.children.append(new_node)
                    score = new_node.minimax(board, depth - 1, alpha, beta)

                    # Update this node's score according to child score
                    if (self.player == X and score < self.score) or (self.player == O and score > self.score):
                        self.score = score
                        self.best_move = new_node.square

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

    # Return true if the board is full
    def is_full(self):
        for i in range(9):
            if self.board[i] == EMPTY:
                return False
        return True

    # Return true if the board is terminal
    def is_terminal(self):
        return self.is_full() or self.winner != None

    # Get the score of this board pos. -1 if O wins, 1 if X wins.
    def get_score(self):
        if self.winner == X:
            return self.squares_left + 1
        elif self.winner == O:
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


# Game controller class
class Game():

    def __init__(self):
        self.reset()

    # Reset the game state.
    def reset(self):
        self.player = X
        self.board = Board()

    # Flip turn from X to O or O to X.
    def flip_turn(self):
        if (self.player == X):
            self.player = O
        else:
            self.player = X

    # Make CPU take a turn.
    def cpu_move(self):
        # Set the root node to the player opposite of the CPU.
        if self.player == X:
            root = Node(player=O)
        else:
            root = Node(player=X)

        # Determine the best move.
        root.minimax(self.board, depth=6)
        best_move = root.best_move

        # Apply the move to the board and flip player.
        self.board.move(self.player, best_move)
        self.flip_turn()

    # Get player to input move.
    def player_move(self):
        square = -1
        while not self.board.is_square_open(square):
            move = input("Input move: (a2, 3c, etc.) ")
            square = self.board.get_square_from_string(move)

        # Apply the move to the board and flip player.
        self.board.move(self.player, square)
        self.flip_turn()

    # Main game loop
    def play(self):

        play_again = True
        while play_again:
            self.reset()

            # Determine who goes first.
            start = None
            while start != 'y' and start != 'n':
                start = input("You go first? (y/n) ")
                start = start.lower()

            # Loop until the game is done.
            continue_game = True
            while continue_game:
                self.board.print()

                # Player turn
                if start == 'n':
                    start = 'y'
                else:
                    self.player_move()
                    self.board.print()
                    if self.board.is_full():
                        print("Board is full. Draw game!")
                        continue_game = False
                    elif self.board.is_terminal():
                        print("You win!")
                        continue_game = False

                # CPU Turn
                if continue_game:
                    self.cpu_move()
                    if self.board.is_full():
                        self.board.print()
                        print("Board is full. Draw game!")
                        continue_game = False
                    elif self.board.is_terminal():
                        self.board.print()
                        print("I win!")
                        continue_game = False

            play_again = None
            while play_again != 'y' and play_again != 'n':
                play_again = input("Play again? (y/n) ")
                play_again = play_again.lower()
            play_again = (play_again == 'y')


if __name__ == "__main__":
    Game().play()
