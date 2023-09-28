from const import *
from square import Square
from piece import *
from move import Move
class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        #display on board
        self.squares[initial.row][initial.col].piece = None 
        #we want to display the board after we made a move
        #so the initial square is none
        self.squares[final.row][final.col].piece = piece
        #and the final square is that piece 

        #move
        piece.moved = True

        #clear old valid moves
        piece.clear_moves(move)

        #set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def calc_moves(self, piece, row, col):
        #calculate all valid moves of a specific piece

        def pawn_moves(): #TODO: en-passant and promotion
            steps = 1 if piece.moved else 2

            #vertical moves
            start = row + piece.dir #???? no idea but it's true
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].isempty():
                        #create initial and final move square
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        #create a new move
                        move = Move(initial, final)
                        #append new move
                        piece.add_move(move)
                    #pawn is blocked
                    else:
                        break
                #not in range (invalid moves)
                else:
                    break  
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if(self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color)):
                        #create initial and final move square
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        #create a new move
                        move = Move(initial, final)
                        #append new move
                        piece.add_move(move)
            #diagonal moves

        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-2, col-1),
                (row-1, col+2),
                (row-1, col-2),
                (row+1, col+2),
                (row+1, col-2),
                (row+2, col+1),
                (row+2, col-1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        #create new move
                        move = Move(initial, final)
                        #append new valid move
                        piece.add_move(move)

        def straightline_moves(incrs): #for Queen, Bishop and Rook
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        #create squares of possible moves
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        #create a possible new move
                        move = Move(initial, final)
                        #empty case
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            #create a new move
                            piece.add_move(move)

                        #has enemy piece then add move then break
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break

                        #blocked by team piece then break
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    #not in range
                    else:
                        break
                    #increase incr
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves(): #TODO: O-O and O-O-O
            adjs = [
                (row-1, col+0), 
                (row+1, col+0), 
                (row+0, col-1), 
                (row+0, col+1), 
                (row-1, col+1), 
                (row-1, col-1), 
                (row+1, col-1), 
                (row+1, col+1),
            ]

            #standard moves
            for possible_move in adjs:
                possible_move_row, possible_move_col = possible_move
                
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_enemy(piece.color):
                        
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        #create new move
                        move = Move(initial, final)
                        #append new valid move
                        piece.add_move(move)
            #king side castle

            #queen side castle

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straightline_moves([
                (-1, 1), 
                (-1, -1), 
                (1, -1), 
                (1, 1),
            ])

        elif isinstance(piece, Rook):
            straightline_moves([
                (-1, 0), 
                (1, 0), 
                (0, -1), 
                (0, 1),
            ])

        elif isinstance(piece, Queen):
            straightline_moves([
                (-1, 0), 
                (1, 0), 
                (0, -1), 
                (0, 1), 
                (-1, 1), 
                (-1, -1), 
                (1, -1), 
                (1, 1),
            ])

        elif isinstance(piece, King):
            king_moves()   

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)
        #row count from 0 (top of the board) so white pawns stand at 6th rank, other pieces stand at 7th rank
        #pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        #self.squares[5][2] = Square(5, 2, Pawn('black'))
        
        #knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        #self.squares[3][3] = Square(3,3, Knight('black'))

        #bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        #self.squares[5][7] = Square(5, 7, Bishop('black'))

        #rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        #self.squares[3][4] = Square(3,4,Rook('black'))

        #Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        #self.squares[5][6] = Square(5,6,Queen('white'))

        #King
        self.squares[row_other][4] = Square(row_other, 4, King(color))
        #self.squares[4][5] = Square(4,5,King('white'))