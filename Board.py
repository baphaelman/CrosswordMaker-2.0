import copy

class Board:
    # ATTRIBUTES
    # size: nxn size of the board
    # board: 2D array representing the board
    # rows: list of rows, each of which has a string representation
    # columns: list of columns, each of which has a string representation
    # constriction: number of diagonal constrictions made in tope left and bottom right corners respectively
    # next_row: next row to be created

    # METHODS
    # print: prints board

    def __init__(self, size, board=None, rows=None, columns=None, constriction=None, next_row=0):
        self.size = size
        self.next_row = next_row
        self.constriction = constriction if constriction is not None else [0, 0]
        if board:
            self.board = board
            self.rows = rows
            self.columns = columns
        else:     
            # building board and rows with constrictions
            self.board = [["0" for _ in range(self.size)] for _ in range(self.size)]
            self.rows = []
            first_constriction, second_constriction = self.constriction[0], self.constriction[1]
            for row in range(size):
                word = ""
                for col in range(size):
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
    
    def generate_word_row(self, row, col, word):
            # returns clone of this board with word generated down at (row, col),
            # or None if not feasible

            if (col + len(word) - 1) > self.size - 1: # word too long for board
                return None
            if (self.board[row][col] == '#') or (self.board[row][col + len(word) - 1] == "#"): # if endpoint in "#"
                return None

            if (col != 0 and self.board[row][col - 1] != '#') or ((col + len(word) != self.size) and self.board[row][col + len(word)] != "#"): # not snug between "#"
                return None
            
            board_copy = self.clone()
            for i in range(len(word)):
                if word[i] == self.board[row][col + i] or self.board[row][col + i] == "0":
                    board_copy.board[row][col + i] = word[i]
                else:
                    return None
            return board_copy
    
    def generate_word_down(self, row, col, word):
            # returns clone of this board with word generated down at (row, col),
            # or None if not feasible
            copy = self.transpose()
            result = copy.generate_word_row(col, row, word)
            if result:
                return result.transpose()
    
    def insert_word(self, word):
        # yields a clone of this board with word somewhere
        for row in range(self.size):
            for col in range(self.size):
                copy_with_word_row = self.generate_word_row(row, col, word) # tries row,
                if copy_with_word_row:
                    copy_with_word_row.print()
                    yield copy_with_word_row
                
                trans = self.transpose()
                copy_with_word_col = trans.generate_word_row(col, row, word) # then col
                if copy_with_word_col:
                    col_board = copy_with_word_col.transpose()
                    col_board.print()
                    yield col_board
    
    def print(self):
        for row in range(self.size):
            line = ""
            for col in range(self.size):
                line += self.board[row][col] + " "
            print(line)

    def clone(self):
        new_board = copy.deepcopy(self.board)
        new_rows = self.rows[:]
        new_columns = self.columns[:]
        new_constriction = self.constriction[:]
        return Board(self.size, new_board, new_rows, new_columns, new_constriction, self.next_row)
    
    def transpose(self):
        copy = self.clone()
        for row in range(self.size):
            for col in range(self.size):
                copy.board[row][col] = self.board[col][row]
        copy.rows, copy.columns = copy.columns, copy.rows
        return copy