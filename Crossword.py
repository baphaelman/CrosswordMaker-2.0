from Board import Board

class Crossword:
    # ATTRIBUTES
    # size: integer, passed to Board
    # key_words: list of words required in Board
    # constriction: list of two integers, passed to Board

    # METHODS

    def __init__(self, size, key_words, constriction=None):
        self.size = size
        self.key_words = sorted(key_words, key=len, reverse=True) # sorted with longest first
        self.constriction = constriction if constriction else [0, 0]
        self.board = Board(self.size, constriction=constriction)
    
    def yield_key_words_board(self): # turn this into a generator for each board containing the key words
        new_board = self.board
        for word in self.key_words:
            new_board_generator = new_board.insert_word(word)
            new_board = next(new_board_generator)
            new_board.print()
            print()
        yield new_board