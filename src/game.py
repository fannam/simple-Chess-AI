import pygame

from const import *
from board import Board

class Game:

    def __init__(self):
        self.board = Board()
    
    #Show method
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)
                else: 
                    color = (119, 154, 88)

                rect = (col * SQSZIE, row * SQSZIE, SQSZIE, SQSZIE)

                pygame.draw.rect(surface, color, rect)
    
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if(self.board.squares[row][col].has_piece()):
                    piece = self.board.squares[row][col].piece

                    img = pygame.image.load(piece.texture)
                    img_center = col * SQSZIE + SQSZIE // 2, row * SQSZIE + SQSZIE // 2
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)