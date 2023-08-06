import os


class TicTacToe:
    def __init__(self, size=3):
        # init board size of type square
        self.board = [' '] * size * size
        # init current player as X by default
        self.current_player = 'X'
        # init game_over as False
        self.game_over = False
        # init size
        self.size = size

    def clear_screen(self):
        # Clear the console screen based on the operating system
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_board(self):

        self.clear_screen()
        print('-' * self.size * 4 + '-')
        board_text = ''
        for i in range(0,self.size**2):
            if (i + 1) % self.size != 0:
                board_text += f"| {self.board[i]} "
            else:
                print(board_text + f"| {self.board[i]} | ")
                print('-' * self.size * 4 + '-')
                board_text = ''

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            return True
        else:
            print('Invalid move! Please try again.')
            return False

    def check_game_over(self):
        checker = []
        # Check rows
        for i in range(0, self.size**2, self.size):
            checker = []
            for j in range(i, i + self.size):
                checker.append(self.board[j])

            if all(item == checker[0] != ' ' for item in checker):
                self.game_over = True
                return checker[0]

        # end check rows

        # Check columns
        for i in range(self.size):
            checker = []
            for j in range(0, self.size ** 2, self.size):
                checker.append(self.board[j])
            if all(item == checker[0] != ' ' for item in checker):
                self.game_over = True
                return checker[0]

        # Check diagonals
        # diagonal1
        checker = [self.board[i * (self.size + 1)] for i in range(self.size)]
        if all(item == checker[0] != ' ' for item in checker):
            self.game_over = True
            return checker[0]

        # diagonal2
        checker =  [self.board[(i + 1) * (self.size - 1)] for i in range(self.size - 1, -1, -1)]
        if all(item == checker[0] != ' ' for item in checker):
            self.game_over = True
            return checker[0]


        # Check for a tie
        if ' ' not in self.board:
            self.game_over = True
            return 'tie'

        return None

    def switch_player(self):
        if self.current_player == 'X':
            self.current_player = 'O'
        else:
            self.current_player = 'X'

    def play_game(self):
        print("Welcome to Tic Tac Toe!")
        self.print_board()

        while not self.game_over:
            print("It's", self.current_player, "'s turn.")
            position = int(input(f"Enter a position (1-{self.size ** 2}): ")) - 1
            if position in range(self.size ** 2):
                if self.make_move(position):
                    self.print_board()
                    result = self.check_game_over()
                    if result == 'tie':
                        print("It's a tie!")
                    elif result:
                        print(result, "wins!")
                    else:
                        self.switch_player()
                else:
                    continue
            else:
                print("Invalid position! Please try again.")

        print("Game Over!")
