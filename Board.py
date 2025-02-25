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
    # common_words: potential words for board filling

    # METHODS
    # UTILS
    # print: prints board
    # clone: returns deep copy of board
    # transpose: returns transposed deep copy of board

    # MANIPuLATIONS
    # insert_word("word"): yields all copies of board with "word" where it can be placed

    def __init__(self, size, common_words, board=None, constriction=None, start_squares=None):
        self.constriction = constriction if constriction is not None else [0, 0]
        self.size = size
        self.common_words = common_words
        if board:
            self.board = board
            self.start_squares = start_squares
        else:     
            # building board and rows with constrictions
            self.board = [["0" for _ in range(self.size)] for _ in range(self.size)]
            first_constriction, second_constriction = self.constriction[0], self.constriction[1]
            self.start_squares = {}
            for row in range(self.size):
                # entries in start_squares
                c = max(0, first_constriction - row)
                word_len = self.size - c - max(0, row - self.size + second_constriction + 1)
                self.start_squares.setdefault(word_len, []).append(StartSquare(row, c, 1)) # 1 is row
                self.start_squares[word_len].append(StartSquare(c, row, 0)) # include associated col word
                
                # entries in self.board, self.rows, and self.columns
                for col in range(self.size):
                    if row + col < first_constriction:
                        self.board[row][col] = "#"
                    elif (2 * self.size - 1) - (row + col) <= second_constriction:
                        self.board[row][col] = "#"
    
    # could keep a cache of words alerady tested? to make things faster
    def is_valid(self, row, orientation):
        # returns clone of this board with word generated down at (row, col)
        # or None if not feasible

        if not orientation:
            return self.transpose().is_valid(row, True)
        
        # to calculate where word is, taken from constructor
        first_constriction, second_constriction = self.constriction[0], self.constriction[1]
        start_col = max(0, first_constriction - row)
        word_len = self.size - start_col - max(0, row - self.size + second_constriction + 1)
        word = ""
        for i in range(word_len):
            word += self.board[row][start_col + i]
        
        # filtering self.common_words for match
        potential_words = self.common_words[word_len][:]
        for i in range(len(word)):
            if word[i] == '0':
                continue
            potential_words = [potential_word for potential_word in potential_words if potential_word[i] == word[i]]
        if potential_words:
            if len(potential_words) == 1 and potential_words[0] == word:
                self.common_words[word_len].remove(word) # to not repeat words
            return True
        else:
            return False

    def generate_word_at_start_square(self, start_square, word):
        if not start_square.orientation: # if column rather than row
            inv_start_square = start_square.invert()
            result = self.transpose().generate_word_at_start_square(inv_start_square, word)
            return result.transpose() if result else result # transpose if board, just return if none

        col, row = start_square.col, start_square.row
        board_copy = self.clone_without_start_square(start_square) # this doesn't work with the inv_start_square business..
        for i in range(len(word)):
            # checks if each letter COULD fit
            curr_char = board_copy.board[row][col + i]
            if (word[i] == curr_char or curr_char == "0"):
                    board_copy.board[row][col + i] = word[i]
                    if not board_copy.is_valid(col + i, 0): # checks whether perpendiculars could work
                        return None
            else:
                return None
        # board_copy.common_words[len(word)].remove(word) # to not repeat words
        return board_copy
    
    # yields a clone of this board with word somewhere
    def insert_word(self, word):
        # if first word inserted, avoid transposes?
        viable_starts = list(self.start_squares[len(word)])
        for chosen_start_square in viable_starts:
            copy_with_word = self.generate_word_at_start_square(chosen_start_square, word)
            if copy_with_word:
                copy_with_word.common_words[len(word)].remove(word) # to not repeat wordss
                yield copy_with_word
    
    def yield_key_words(self, key_words): # generator for each board containing the key words
        word = key_words[0]
        if len(key_words) == 1:
            yield from self.insert_word(word)
        else:
            first_word_boards = self.insert_word(word) # generator with first word
            for first_word_board in first_word_boards:
                yield from first_word_board.yield_key_words(key_words[1:])

    
    def __repr__(self):
        return_string = ""
        for row in range(self.size):
            for col in range(self.size):
                return_string += self.board[row][col] + " "
            return_string += "\n"
        return return_string

    def clone(self):
        new_common_words = copy.deepcopy(self.common_words)
        new_board = copy.deepcopy(self.board)
        new_constriction = self.constriction[:]

        # new start squares
        new_start_squares = {}
        for word_length in self.start_squares:
            new_start_squares[word_length] = []
            for start_square in self.start_squares[word_length]:
                new_start_squares[word_length].append(start_square.copy())

        return Board(self.size, common_words=new_common_words, board=new_board, constriction=new_constriction, start_squares=new_start_squares)
    
    def clone_without_start_square(self, start_square):
        copy = self.clone()
        
        # new start squares, without start_square
        new_start_squares = {}
        for word_length in self.start_squares:
            new_start_squares[word_length] = []
            for old_start_square in self.start_squares[word_length]:
                if old_start_square == start_square:
                    continue
                new_start_squares[word_length].append(old_start_square.copy())
        copy.start_squares = new_start_squares

        return copy
    
    def transpose(self): # doesn't transpose StartSquares... but fine as long as it's just for insert_word, which seems to be the case?
        copy = self.clone()
        for row in range(self.size):
            for col in range(self.size):
                copy.board[row][col] = self.board[col][row]
        return copy