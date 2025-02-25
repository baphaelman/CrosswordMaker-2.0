from Board import Board

class Crossword:
    # ATTRIBUTES
    # size: integer, passed to Board
    # key_words: list of words required in Board
    # constriction: list of two integers, passed to Board
    # board: Board representation

    # METHODS

    def __init__(self, size, key_words, constriction=None, board=None):
        self.size = size
        self.key_words = sorted(key_words, key=len, reverse=True) # sorted with longest first
        self.constriction = constriction if constriction else [0, 0]
        self.board = board if board else Board(self.size, constriction=constriction)
    
    def yield_key_words_board(self): # turn this into a generator for each board containing the key words
        word = self.key_words[0]
        copy = self.copy()
        # eventually yield from copy.yield_key_words_board() with truncated key_words list?
        
    
    def copy(self):
        return Crossword(self.size, list(self.key_words), list(self.constriction), self.board.copy())
