import copy
from StartSquare import StartSquare

# SHOULD I CALCULATE A LIST OF VIABLE WORD POSITIONS UPON BOARD GENERATION?
# DICTIONARY WITH INDEX WORD LENGTH, returns list of points (one dictionary for rows and columns)
# WAYYY more efficient than going through every single square and testing whether word is possible there

class Board:
    # ATTRIBUTES
    # size: nxn size of the board
    # board: 2D array representing the board
    # rows: list of rows, each of which has a string representation
    # columns: list of columns, each of which has a string representation
    # constriction: number of diagonal constrictions made in tope left and bottom right corners respectively
    # next_row: next row to be created
    # start_squares: dictionary indexed by length of starting squares for unfilled words

    # METHODS
    # UTILS
    # print: prints board
    # clone: returns deep copy of board
    # transpose: returns transposed deep copy of board

    # MANIPuLATIONS
    # insert_word("word"): yields all copies of board with "word" where it can be placed

    def __init__(self, size, board=None, rows=None, columns=None, constriction=None, start_squares=None):
        self.constriction = constriction if constriction is not None else [0, 0]
        self.size = size
        if board: # why do i have this??
            self.board = board
            self.rows = rows
            self.columns = columns
            self.start_squares = start_squares
        else:     
            # building board and rows with constrictions
            self.board = [["0" for _ in range(self.size)] for _ in range(self.size)]
            first_constriction, second_constriction = self.constriction[0], self.constriction[1]
            self.rows = []
            self.start_squares = {}
            for row in range(self.size):
                # entries in start_squares
                c = max(0, first_constriction - row)
                word_len = self.size - c - max(0, row - self.size + second_constriction + 1)
                self.start_squares.setdefault(word_len, []).append(StartSquare(row, c, 1)) # 1 is row
                self.start_squares[word_len].append(StartSquare(c, row, 0)) # include associated col word
                
                # entries in self.board, self.rows, and self.columns
                word = ""
                for col in range(self.size):
                    if row + col < first_constriction:
                        self.board[row][col] = "#"
                        word += "#"
                    elif (2 * self.size - 1) - (row + col) <= second_constriction:
                        self.board[row][col] = "#"
                        word += "#"
                    else:
                        word += "0"
                
                self.rows.append(word)
            self.columns = self.rows[:]
            
    # returns clone of this board with word generated down at (row, col)
    # or None if not feasible
    def generate_word_at_start_square(self, start_square, word):
            # still need to check that perpendicular words are potentially valid
            if not start_square.orientation: # if column and not row
                inv_start_square = start_square.invert()
                result = self.transpose().generate_word_at_start_square(inv_start_square, word)
                return result.transpose() if result else result # transpose if board, just return if none
            
            col, row = start_square.col, start_square.row
            board_copy = self.clone()
            for i in range(len(word)):
                if word[i] == self.board[row][col + i] or self.board[row][col + i] == "0": # checks if each letter COULD fit
                    board_copy.board[row][col + i] = word[i]
                else:
                    return None
            return board_copy
    
    # have to update rows and cols?
    def insert_word(self, word):
        # yields a clone of this board with word somewhere
        viable_starts = self.start_squares[len(word)]
        for chosen_start_square in viable_starts:
            copy_with_word = self.generate_word_at_start_square(chosen_start_square, word)
            if copy_with_word:
                yield copy_with_word

    
    def __repr__(self):
        return_string = ""
        for row in range(self.size):
            for col in range(self.size):
                return_string += self.board[row][col] + " "
            return_string += "\n"
        return return_string

    def clone(self):
        new_board = copy.deepcopy(self.board)
        new_rows = self.rows[:]
        new_columns = self.columns[:]
        new_constriction = self.constriction[:]
        # new start squares
        new_start_squares = {}
        for word_length in self.start_squares:
            new_start_squares[word_length] = []
            for start_square in self.start_squares[word_length]:
                new_start_squares[word_length].append(start_square.copy())

        return Board(self.size, new_board, new_rows, new_columns, new_constriction, new_start_squares)
    
    def transpose(self): # doesn't transpose StartSquares...
        copy = self.clone()
        for row in range(self.size):
            for col in range(self.size):
                copy.board[row][col] = self.board[col][row]
        copy.rows, copy.columns = copy.columns, copy.rows
        return copy