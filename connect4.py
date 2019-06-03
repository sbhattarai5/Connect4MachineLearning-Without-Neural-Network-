##Copyright Saurav Bhattarai

##Pieces and Notations###############################
##Blue = 'B'
##Red = 'R'
##Space = ' '
####################################################
##Constants#########################################
ROW = 6
COL = 7
SEQUENCE_REQUIRED = 4   #line needed to win
####################################################

in_training = False
##Game class for the connect4 game
class Game:

    def __init__(self, R=ROW, C=COL):   #initialize the board with spaces and turn to whatever is passed or Blue 'B' as Default
        self.r = R
        self.c = C
        self.board_array = self.board_init(R, C)
        self.turn = 'B'
        self.last_move = None  #stores the last colomn where the move was made -- is None if Invalid move is made
        self.empty_spots = R * C
        self.game_over = False
        self.winner = None
        self.draw = False

    def make_move(self, col):          #this function tries to make a find_move, returns row if move is made, returns -1 if invalid move
        row = self.find_move(col)
        if row == -1:
            if not in_training: print ("Invalid Move!!")
            self.last_move = None
            return
        self.board_array[row][col] = self.turn
        self.empty_spots -= 1
        if (self.turn == 'B'):
            self.turn = 'R'
        else:
            self.turn = 'B'
        self.last_move = col
        self.check_win()
        self.check_draw()
        return

    def board_init(self, R, C):       #initializes the whole board to just spaces
        board = []
        for r in range(R):
            each_row = []
            for c in range(C):
                each_row.append(' ')
            board.append(each_row)
        return board

    def find_move(self, col):  #returns the row number for the specified colomn, returns -1 if the colomn is full which also means invalid move
        if (col < 0 or col >= self.c):
            return -1
        for row in range(self.r - 1, -1, -1):
            if self.board_array[row][col] == ' ':
                return row
        return -1

    def check_win(self):
        row = 0
        col = self.last_move
        for i in range(self.r):
            if (self.board_array[i][col] != ' '):
                row = i
                break
        if (self.check_E(row) + self.check_W(row) + 1 >= SEQUENCE_REQUIRED) or (self.check_NE(row) + self.check_SW(row) + 1 >= SEQUENCE_REQUIRED) or (self.check_N(row) + self.check_S(row) + 1 >= SEQUENCE_REQUIRED) or (self.check_NW(row) + self.check_SE(row) + 1 >= SEQUENCE_REQUIRED):
            self.game_over = True
            self.winner = self.board_array[row][self.last_move]
        return

    def check_draw(self):
        if self.empty_spots == 0:
            self.check_win()
            if self.winner == None:
                self.game_over = True
                self.draw = True

    def check_E(self, row):
        col = self.last_move
        no_of_consequent_pieces = 0
        piece = self.board_array[row][col]
        col += 1
        while (col < self.c):
            if self.board_array[row][col] == piece:
                no_of_consequent_pieces += 1
            else:
                break
            col += 1
        return no_of_consequent_pieces

    def check_NE(self, row):
        col = self.last_move
        no_of_consequent_pieces = 0
        piece = self.board_array[row][col]
        col += 1
        row -= 1
        while (row >= 0 and col < self.c):
            if self.board_array[row][col] == piece:
                no_of_consequent_pieces += 1
            else:
                break
            col += 1
            row -= 1
        return no_of_consequent_pieces

    def check_N(self, row):
        col = self.last_move
        no_of_consequent_pieces = 0
        piece = self.board_array[row][col]
        row -= 1
        while (row >= 0):
            if self.board_array[row][col] == piece:
                no_of_consequent_pieces += 1
            else:
                break
            row -= 1
        return no_of_consequent_pieces

    def check_NW(self, row):
        col = self.last_move
        no_of_consequent_pieces = 0
        piece = self.board_array[row][col]
        col -= 1
        row -= 1
        while (row >= 0 and col >= 0):
            if self.board_array[row][col] == piece:
                no_of_consequent_pieces += 1
            else:
                break
            col -= 1
            row -= 1
        return no_of_consequent_pieces

    def check_W(self, row):
        col = self.last_move
        no_of_consequent_pieces = 0
        piece = self.board_array[row][col]
        col -= 1
        while (col >= 0):
            if self.board_array[row][col] == piece:
                no_of_consequent_pieces += 1
            else:
                break
            col -= 1
        return no_of_consequent_pieces

    def check_SW(self, row):
        col = self.last_move
        no_of_consequent_pieces = 0
        piece = self.board_array[row][col]
        col -= 1
        row += 1
        while (row < self.r and col >= 0):
            if self.board_array[row][col] == piece:
                no_of_consequent_pieces += 1
            else:
                break
            col -= 1
            row += 1
        return no_of_consequent_pieces

    def check_S(self, row):
        col = self.last_move
        no_of_consequent_pieces = 0
        piece = self.board_array[row][col]
        row += 1
        while (row < self.r):
            if self.board_array[row][col] == piece:
                no_of_consequent_pieces += 1
            else:
                break
            row += 1
        return no_of_consequent_pieces

    def check_SE(self, row):
        col = self.last_move
        no_of_consequent_pieces = 0
        piece = self.board_array[row][col]
        col += 1
        row += 1
        while (row < self.r and col < self.c):
            if self.board_array[row][col] == piece:
                no_of_consequent_pieces += 1
            else:
                break
            col += 1
            row += 1
        return no_of_consequent_pieces

    def board_string(self):     #returns a string representing the board
        pieces = []
        for r in range(self.r):
            for c in range(self.c):
                pieces.append(self.board_array[r][c])
        return ''.join(pieces)

    def __str__(self):
        str = ""
        if (self.r == 0 and self.c == 0):
            return str
        for row in range(self.r):
            str += '|'
            for i in range(self.c - 1):
                str += '-+'
            str += '-|\n'
            str += '|'
            for col in range(self.c):
                str += self.board_array[row][col]
                str += '|'
            str += '\n'  #newline
        str += '|'
        for i in range(self.c - 1):
            str += '-+'
        str += '-|'
        return str
