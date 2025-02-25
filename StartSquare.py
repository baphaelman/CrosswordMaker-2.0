# to track where words can start--row and column indeces, plus orientation (across or down word)
class StartSquare:
    def __init__(self, row, col, orientation):
        self.row = row
        self.col = col
        self.orientation = orientation # 1 for row, 0 for column
    
    def copy(self):
        return StartSquare(self.row, self.col, self.orientation)
    
    def __repr__(self):
        orientation = "across" if self.orientation else "down"
        return "(" + str(self.row) + " , " + str(self.col) + " , " + orientation + ")"
    
    # row <-> col and orientation flips
    def invert(self):
        return StartSquare(self.col, self.row, not self.orientation)