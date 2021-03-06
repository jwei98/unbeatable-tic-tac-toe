# A tic-tac-toe game where user plays against unbeatable AI
''' TODO:
1. Refactor code
- make a turn loop which alternates turns
2. Let user choose symbol
3. Format board
4. Add GUI or web UI
'''
import copy
from termcolor import colored

def main():
    print("Welcome to Tic Tac Toe! You may enter 'Control-C' at any time to quit.")
    game = TicTacToeGame()
    did_quit = game.configure_settings()
    if not did_quit:
        winner = game.start()
    else:
        winner = "quit"
    end_game_message(winner)

def end_game_message(winner):
    if winner == "quit":
        print("\nUser has quit the game, which the AI would've won anyways")
    elif winner == "tie":
        print("\nThe game finished in a tie!")
    else:
        print(winner + " has won the game!")

class TicTacToeGame:

    def __init__(self):
        self.user_order = 1
        self.winner = None
        self.current_player = 'X'
        self.symbols = {'user': 'X', 'ai': 'O'}
        self.board = self.initialize_board()

    def initialize_board(self):
        return range(9)

    def configure_settings(self):
        user_order_valid= False
        while not user_order_valid:
            try:
                order = int(str(input("Would you like to go first or second? Enter a '1' or a '2':  ")))
                if order == 1 or order == 2:
                    user_order_valid = True
                    self.user_order = order
                else:
                    print("\n Please enter a 1 or a 2")
            except KeyboardInterrupt:
                return "quit"
            except:
                self.error_message()

    def draw_board(self, index, symbol):
        if index != -1: self.board[index] = symbol
        col_spacing = 3
        for i in range(9):
            ch = str(self.board[i])
            if ch == 'O': color = 'blue'
            elif ch == 'X': color = 'red'
            else: color = 'white'

            if (i+1) % 3 == 0:
                print(colored(ch,color) + "  ")
            else:
                print colored(ch,color) + "  ",
        print("\n")

    def get_score(self, winner):
        if winner == "tie": return 0
        elif winner == 'O': return 10
        elif winner == 'X': return -10

    def generate_state(self, player, move, game_state):
        new_game_state = copy.copy(game_state)
        new_game_state[move] = player
        return new_game_state

    def is_valid_move(self, move, game_state):
        if self.is_in_board(move) and self.has_not_been_taken(move, game_state):
            return True
        return False

    def is_in_board(self, move):
        if move >= 0 and move <= 8:
            return True
        return False

    def has_not_been_taken(self, move, game_state):
        if type(game_state[move]) == int:
            return True
        return False

    # Either returns 'X', 'O' or None (in case of tie)
    # or "quit" if user quit
    def start(self):
        user_has_quit = False
        print("\n")
        self.draw_board(-1, -1)

        # if user chose to go second, let AI make a move first
        if self.user_order == 2:
            print("AI is calculating its move...")
            ai_move = self.ai_turn()
            self.draw_board(ai_move,'O')
            end = self.check_end_game(self.board)
            if end: return end

        while not (self.winner or user_has_quit):
            # user move
            user_move = self.user_turn()
            if user_move == "quit": return "quit"
            self.draw_board(user_move,'X')
            end = self.check_end_game(self.board)
            if end: return end

            # ai turn
            print("AI is calculating its move...")
            ai_move = self.ai_turn()
            self.draw_board(ai_move, 'O')
            end = self.check_end_game(self.board)
            if end: return end

    # gets valid move from user
    def user_turn(self):
        self.current_player = 'X'
        user_move_valid = False
        while not user_move_valid:
            try:
                raw_move = str(input("It's your turn! Enter your move: "))
                int_move = int(raw_move)
                if self.is_valid_move(int_move, self.board):
                    user_move_valid = True
                    print("User went in space " + str(int_move))
                    return int_move
                else:
                    self.error_message()
            except KeyboardInterrupt:
                return "quit"
            except:
                self.error_message()

    def ai_turn(self):
        self.current_player = 'O'
        move = self.minimax('O', self.board)
        print("AI went in space " + str(move))
        return move

    # actual minimax algorithm to dictate AI move
    def minimax(self, player, game_state):
        moves = self.get_possible_moves(game_state)
        best_move = moves[0]
        best_score = float('-inf')
        for move in moves:
            clone = self.generate_state(player, move, game_state)
            score = self.min_play(self.get_other_player(player), clone)
            if score > best_score:
                best_move = move
                best_score = score
        return best_move

    def min_play(self, player, game_state):
        end = self.check_end_game(game_state)
        if end: return self.get_score(end)
        moves = self.get_possible_moves(game_state)
        best_score = float('inf')
        for move in moves:
            clone = self.generate_state(player, move, game_state)
            score = self.max_play(self.get_other_player(player), clone)
            if score < best_score:
                best_move = move
                best_score = score
        return best_score

    def max_play(self, player, game_state):
        end = self.check_end_game(game_state)
        if end: return self.get_score(end)
        moves = self.get_possible_moves(game_state)
        best_score = float('-inf')
        for move in moves:
            clone = self.generate_state(player, move, game_state)
            score = self.min_play(self.get_other_player(player), clone)
            if score > best_score:
                best_move = move
                best_score = score
        return best_score

    def get_other_player(self, user):
        if user == 'X': return 'O'
        else: return 'X'

    def get_possible_moves(self, game_state):
        possible_moves = []
        for space in game_state:
            if self.is_valid_move(space, game_state):
                possible_moves.append(space)
        return possible_moves

    # given a game state, checks if 'user' or 'ai' has won the game.
    # return their symbol if they won, otherwise returns None
    def check_end_game(self, game_state):
        # check winning combinations
        rows_inc = [[0,3,6],1,3]
        cols_inc = [[0,1,2],3,7]
        left_diag_inc = [[0],4,9]
        right_diag_inc = [[2],2,5]
        for incs in [rows_inc, cols_inc, left_diag_inc, right_diag_inc]:
            check = self.check(incs[0],incs[1],incs[2],game_state)
            if check != None:
                return check
        # if nobody won, check if board is filled
        if self.get_possible_moves(game_state) == []:
            return 'tie'

        return None

    # given a row/column/diagonal, checks if anyone has three in a row
    # if three in a row, returns the player's symbol, otherwise returns None
    def check(self,start_indices, inc, end_increment, game_state):
        for start in start_indices:
            player_count = 0
            ai_count = 0
            for i in range (start,start+end_increment,inc):
                if game_state[i] == 'X': player_count = player_count + 1
                elif game_state[i] == 'O': ai_count = ai_count + 1
            if player_count == 3:
                return 'X'
            elif ai_count == 3:
                return 'O'
        return None

    def error_message(self):
        print("\n*** Oops! Please enter a valid move!***")
        self.draw_board(-1,-1)


main()
