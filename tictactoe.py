import time
import math
import random

class TicTacToe:
    def __init__(self):
        """
        Initializes the game board and sets the human and AI players.
        The board is a simple list of 9 elements, representing a 3x3 grid.
        """
        self.board = [' ' for _ in range(9)]  # A list to represent the 3x3 board
        self.human_player = 'O'
        self.ai_player = 'X'
        self.winner = None

    def print_board(self):
        """Prints the game board to the console."""
        print("")
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        """Prints the board layout with corresponding numbers for user input."""
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        print("")
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        """Returns a list of available (empty) spots on the board."""
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def has_empty_squares(self):
        """Checks if there are any empty squares left on the board."""
        return ' ' in self.board

    def num_empty_squares(self):
        """Returns the number of empty squares on the board."""
        return self.board.count(' ')

    def make_move(self, square, letter):
        """
        Makes a move on the board if the square is valid and available.
        Returns True if the move was successful, False otherwise.
        """
        if self.board[square] == ' ':
            self.board[square] = letter
            # Check for winner after making a move
            if self.check_winner(square, letter):
                self.winner = letter
            return True
        return False

    def check_winner(self, square, letter):
        """
        Checks if the recent move resulted in a win.
        This is more efficient than checking the entire board every time.
        """
        # Check the row
        row_ind = square // 3
        row = self.board[row_ind*3 : (row_ind + 1)*3]
        if all([spot == letter for spot in row]):
            return True

        # Check the column
        col_ind = square % 3
        column = [self.board[col_ind + i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True

        # Check diagonals (only if the move is on a diagonal)
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        
        return False

    def check_winner_any(self, letter):
        """
        Checks if a player has won by checking all possible winning combinations.
        Used for the minimax algorithm.
        """
        # Check rows
        for i in range(0, 9, 3):
            if all(self.board[i+j] == letter for j in range(3)):
                return True
        
        # Check columns
        for i in range(3):
            if all(self.board[i+j*3] == letter for j in range(3)):
                return True
        
        # Check diagonals
        if all(self.board[i] == letter for i in [0, 4, 8]):
            return True
        if all(self.board[i] == letter for i in [2, 4, 6]):
            return True
        
        return False

    def is_terminal(self):
        """
        Checks if the game is in a terminal state (someone won or it's a tie).
        """
        # Check if X won
        if self.check_winner_any('X'):
            return True
        # Check if O won
        if self.check_winner_any('O'):
            return True
        # Check if it's a tie
        if not self.has_empty_squares():
            return True
        return False

# --- Player Classes ---

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8): ')
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again.')
        return val

class AIPlayer(Player):
    def __init__(self, letter, algorithm='alpha-beta'):
        super().__init__(letter)
        self.algorithm = algorithm

    def get_move(self, game):
        print(f"\nAI ({self.letter}) is thinking with {self.algorithm}...")
        
        start_time = time.time()
        
        if self.algorithm == 'minimax':
            square = self.minimax(game, self.letter)['position']
        else: # Default to alpha-beta
            square = self.alpha_beta(game, self.letter)['position']

        end_time = time.time()
        print(f"AI decision took: {end_time - start_time:.6f} seconds")
        
        return square

    def minimax(self, state, player):
        """
        Minimax algorithm implementation.
        """
        max_player = self.letter  # The AI
        other_player = 'O' if player == 'X' else 'X'

        # Base cases: check for terminal states (win, lose, tie)
        if state.check_winner_any(other_player):
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.has_empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # Maximize score
        else:
            best = {'position': None, 'score': math.inf}  # Minimize score

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)  # Recurse

            # Undo the move
            state.board[possible_move] = ' '
            state.winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

    def alpha_beta(self, state, player, alpha=-math.inf, beta=math.inf):
        """
        Minimax algorithm with Alpha-Beta Pruning optimization.
        """
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.check_winner_any(other_player):
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.has_empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}
        else:
            best = {'position': None, 'score': math.inf}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.alpha_beta(state, other_player, alpha, beta)

            state.board[possible_move] = ' '
            state.winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
                alpha = max(alpha, best['score'])
                if beta <= alpha:
                    break # Prune
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
                beta = min(beta, best['score'])
                if beta <= alpha:
                    break # Prune
        return best


# --- Game Execution ---

def play(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'
    while game.has_empty_squares():
        if letter == 'O':
            move = o_player.get_move(game)
        else:
            move = x_player.get_move(game)

        if game.make_move(move, letter):
            if print_game:
                print(letter + f' makes a move to square {move}')
                game.print_board()
                print('')

            if hasattr(game, 'winner') and game.winner:
                if print_game:
                    print(letter + ' wins!')
                return letter

            letter = 'O' if letter == 'X' else 'X'
    
    if print_game:
        print('It\'s a tie!')
    return 'Tie'


if __name__ == '__main__':
    print("Welcome to Tic Tac Toe!")
    
    while True:
        print("\nChoose game mode:")
        print("1: Human (O) vs. AI (X)")
        print("2: AI (O) vs. AI (X)")
        print("3: Human (O) vs. Human (X)")
        
        mode = input("Select a mode (1, 2, 3): ")

        if mode == '1':
            algo = input("Choose AI algorithm for X (minimax/alpha-beta): ").lower()
            if algo not in ['minimax', 'alpha-beta']:
                algo = 'alpha-beta' # default
            x_player = AIPlayer('X', algorithm=algo)
            o_player = HumanPlayer('O')
        elif mode == '2':
            algo_x = input("Choose algorithm for AI X (minimax/alpha-beta): ").lower()
            if algo_x not in ['minimax', 'alpha-beta']:
                algo_x = 'alpha-beta'
            algo_o = input("Choose algorithm for AI O (minimax/alpha-beta): ").lower()
            if algo_o not in ['minimax', 'alpha-beta']:
                algo_o = 'alpha-beta'
            x_player = AIPlayer('X', algorithm=algo_x)
            o_player = AIPlayer('O', algorithm=algo_o)
        elif mode == '3':
            x_player = HumanPlayer('X')
            o_player = HumanPlayer('O')
        else:
            print("Invalid mode selected. Exiting.")
            break
            
        t = TicTacToe()
        play(t, x_player, o_player)

        if input("\nPlay again? (y/n): ").lower() != 'y':
            break