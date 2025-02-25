from Board import Board
from parser import common_words

class Crossword:
    # ATTRIBUTES
    # size: integer, passed to Board
    # key_words: list of words required in Board
    # constriction: list of two integers, passed to Board
    # board: Board representation
    # commno_words: list of potential filler words

    # METHODS

    def __init__(self, size, key_words, constriction=None, board=None):
        self.size = size
        self.key_words = sorted(key_words, key=len, reverse=True) # sorted with longest first
        self.constriction = constriction if constriction else [0, 0]
        self.common_words = common_words # to omptimize, could only consider indexes that have viable lengths; see board's StartSquares
        # adding key words to accepted list
        for word in self.key_words:
            if word not in self.common_words[len(word)]:
                self.common_words[len(word)].append(word)
        self.board = board if board else Board(self.size, self.common_words, constriction=constriction)
    
    # put key words in board
    def yield_key_words_boards(self):
        yield from self.board.yield_key_words(self.key_words)

    # fill rest of board
    # def fill_board(self):

    
    # even necessary anymore??
    def copy(self):
        return Crossword(self.size, list(self.key_words), list(self.constriction), self.board.copy())
