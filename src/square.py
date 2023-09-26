class Square:
    #a square can has 1 or 0 piece
    def __init__(self, row, col, piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def has_piece(self):
        return self.piece != None #true if that square has a piece
    
    def isempty(self):
        return not self.has_piece()
    
    def has_team_piece(self, color):
        return self.has_piece() and self.piece.color == color
    
    def has_enemy_piece(self, color):
        return self.has_piece() and self.piece.color != color
    
    def isempty_or_enemy(self, color):
        if self.isempty():
            return True
        elif self.has_enemy_piece(color):
            return True
        else:
            return False

    @staticmethod
    def in_range(*args): # * allows pass as many arguments as you want 
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True   


