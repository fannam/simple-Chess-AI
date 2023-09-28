
class Move:

    def __init__(self, initial, final):
        #initial and final (square)
        self.initial = initial
        self.final = final

    def __str__(self): #transform into string 
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f'-> ({self.final.col}, {self.final.row})'
        return s
    
    def __eq__(self, other): #without this method and __eq__ in square.py, compiler couldn't compare the move in def valid_move on board.py
        return self.initial == other.initial and self.final == other.final