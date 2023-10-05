from const import *
from square import Square
from piece import *
from move import Move
from sound import Sound
import os
import copy
class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def move(self, piece, move, testing = False):
        initial = move.initial
        final = move.final

        en_passant_empty = self.squares[final.row][final.col].isempty()

        #display on board
        self.squares[initial.row][initial.col].piece = None 
        #we want to display the board after we made a move
        #so the initial square is none
        self.squares[final.row][final.col].piece = piece
        #and the final square is that piece 
        
        if isinstance(piece, Pawn):
            #en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:          
                self.squares[initial.row][initial.col + diff].piece = None 
                self.squares[final.row][final.col].piece = piece
                if not testing:
                    sound = Sound(os.path.join(
                        'assets/Sounds/capture.wav'
                    ))
                    sound.play()

            else:
            #pawn promotion
                self.check_promotion(piece, final)

        #king castling
        #TODO: check the next 2 squares is check
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1]) #-1 index is the last element
                #this make me confused with the recursive
        #move
        piece.moved = True

        #clear old valid moves
        piece.clear_moves(move)

        #set last move
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves
    
    def check_promotion(self, piece, final):
        #since pawn can only move forward so we don't need to check color
        if final.row == 0 or final.row == 7:
            #TODO: choose the piece to promote
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    
    def set_true_en_passant(self, piece):
        #check if the pawn is the real en passant
        if not isinstance(piece, Pawn):
            return
        
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False
        piece.en_passant = True

    def in_check(self, piece, move):
        #idea: for each move, check if the final square of all pieces has the enemy King, make some moves invalid
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self) #copy the present board
        temp_board.move(temp_piece, move, testing = True)

        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        return False

    def calc_moves(self, piece, row, col, bool=True):

        #calculate all valid moves of a specific piece
        #add 1 more parameter bool to ensure that we calc_moves method and in_check method won't call each other infinite
        #and using the bool parameter to decide which move is valid      

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

                        #check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)  
                        else:
                            piece.add_move(move)            
                    #pawn is blocked
                    else:
                        break
                #not in range (invalid moves)
                else:
                    break 

            #diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if(self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color)):
                        #create initial and final move square
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        #create a new move
                        move = Move(initial, final)
                        #append new move
                        if bool:
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)  
                        else:
                            piece.add_move(move) 

            #en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            direct = -1 if piece.color == 'white' else 1
            #left en passant
            if Square.in_range(col-1) and row == r:
                
                if self.squares[row][col-1].has_enemy_piece(piece.color):
                    p = self.squares[row][col-1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col-1, p)
                            #create a new move
                            move = Move(initial, final)
                            #append new move
                            if bool:
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)  
                            else:
                                piece.add_move(move) 

            #right en passant
            if Square.in_range(col+1) and row == r:
                
                if self.squares[row][col+1].has_enemy_piece(piece.color):
                    p = self.squares[row][col+1].piece
                    if isinstance(p, Pawn):
                        if p.en_passant:
                            initial = Square(row, col)
                            final = Square(fr, col+1, p)
                            #create a new move
                            move = Move(initial, final)
                            #append new move
                            if bool:
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)  
                            else:
                                piece.add_move(move) 
                   

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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        #create new move
                        move = Move(initial, final)
                        
                        #append new valid move
                        if bool:
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)
                            
                        else:
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        #create a possible new move
                        move = Move(initial, final)
                        #empty case
                        if self.squares[possible_move_row][possible_move_col].isempty():
                            #create a new move
                            if bool: 
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)  
                            else:
                                piece.add_move(move) 

                        #has enemy piece then add move then break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            if bool: 
                                if not self.in_check(piece, move):
                                    #append new move
                                    piece.add_move(move)  
                            else:
                                piece.add_move(move) 
                            
                            break

                        #blocked by team piece then break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break

                    #not in range
                    else:
                        break
                    #increase incr
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
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
                        if bool: 
                            if not self.in_check(piece, move):
                                #append new move
                                piece.add_move(move)
                             
                        else:
                            piece.add_move(move)

            #casling
            if not piece.moved:
                #king side castle
                right_rook = self.squares[row][7].piece
                if isinstance(right_rook, Rook):
                    if not right_rook.moved:
                        for c in range(5, 7): #column 1,2,3
                            if self.squares[row][c].has_piece():
                                break
                            if c==6: 
                                #add right_rook to king
                                piece.right_rook = right_rook
                                #rook move
                                initial = Square(row, 7)
                                final = Square(row, 5)
                                moveR = Move(initial, final)
                                

                                #king move
                                initial = Square(row, col)
                                final = Square(row, 6)
                                moveK = Move(initial, final)
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                        #append new move
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    right_rook.add_move(moveR)
                                    piece.add_move(moveK)
                #queen side castle
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4): #column 1,2,3
                            if self.squares[row][c].has_piece():
                                break
                            if c==3: 
                                #add left_rook to king
                                piece.left_rook = left_rook
                                #rook move
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                

                                #king move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                

                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        #append new move
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)


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