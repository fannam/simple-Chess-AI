
class Piece:

    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color

        if color == 'white':
            value_sign = 1
        else: 
            value_sign = -1
        self.value = value * value_sign
        self.set_texture()
        self.texture_rect = texture_rect
    
    def set_texture(self):
        pass

class Pawn(Piece): #inherit from Piece

    def __init__(self, color):
        if color == 'white':
            self.dir = -1 #dir = direction
        else: 
            self.dir = 1       
        super().__init__('pawn', color, 1.0)

class Knight(Piece):

    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):

    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

class Rook(Piece):

    def __init__(self, color):
        super().__init__('rook', color, 5.0)

class Queen(Piece):

    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):

    def __init__(self, color):
        super().__init__('king', color, 10000.0)

        