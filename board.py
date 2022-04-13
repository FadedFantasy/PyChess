import pygame as p
import numpy as np
from pieces import King, Queen, Pawn, Bishop, Knight, Rook


class Board:
    def __init__(self, window_width, window_height, player_color):
        self.width = window_width
        self.height = window_height
        self.sq_size = self.height // 8
        self.player_color = player_color
        self.game_state = self.initializeBoard()
        self.images = self.loadImages()
        self.pieces = self.initializePieces()
        self.white_to_move = True

    def loadImages(self):
        """
        Initialize a global dict of images. This will be called exactly once
        """
        pieces = ['wp', 'wR', 'wN', 'wK', 'wQ', 'wB', 'bp', 'bR', 'bN', 'bK', 'bQ', 'bB']
        images = {}
        for piece in pieces:
            # transform scale: scales the image to (width, height)
            images[piece] = p.transform.scale(p.image.load(r'images/' + piece + '.png'), (self.sq_size, self.sq_size))
        return images

    def initializeBoard(self):
        if self.player_color == 'b':
            board = np.array([
                ['wR1', 'wN1', 'wB1', 'wK1', 'wQ1', 'wB2', 'wN2', 'wR2'],
                ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],
                ['bR1', 'bN1', 'bB1', 'bK1', 'bQ1', 'bB2', 'bN2', 'bR2']
            ])
        else:  # white or multiplayer
            board = np.array([
                ['bR1', 'bN1', 'bB1', 'bQ1', 'bK1', 'bB2', 'bN2', 'bR2'],
                ['bp1', 'bp2', 'bp3', 'bp4', 'bp5', 'bp6', 'bp7', 'bp8'],
                [None, None, None, None, None, None, None, None],
                [None, None, None, 'wN3', None, None, None, None],
                [None, None, None, 'wN4', None, None, None, None],
                [None, None, None, 'wN5', None, None, None, None],
                ['wp1', 'wp2', 'wp3', 'wp4', 'wp5', 'wp6', 'wp7', 'wp8'],
                ['wR1', 'wN1', 'wB1', 'wQ1', 'wK1', 'wB2', 'wN2', 'wR2']
            ])
        return board

    def initializePieces(self):
        """
        pieces is a dict that contains all piece objects
        """
        pieces = {}
        for row in range(self.game_state.shape[0]):
            for col in range(self.game_state.shape[1]):
                # everything that is not None
                if self.game_state[row][col]:
                    # second letter
                    if self.game_state[row][col][1] == 'p':
                        pieces[self.game_state[row][col]] = Pawn(row, col, self.game_state[row][col][0], self.game_state[row][col])
                    elif self.game_state[row][col][1] == 'R':
                        pieces[self.game_state[row][col]] = Rook(row, col, self.game_state[row][col][0], self.game_state[row][col])
                    elif self.game_state[row][col][1] == 'N':
                        pieces[self.game_state[row][col]] = Knight(row, col, self.game_state[row][col][0], self.game_state[row][col])
                    elif self.game_state[row][col][1] == 'B':
                        pieces[self.game_state[row][col]] = Bishop(row, col, self.game_state[row][col][0], self.game_state[row][col])
                    elif self.game_state[row][col][1] == 'K':
                        pieces[self.game_state[row][col]] = King(row, col, self.game_state[row][col][0], self.game_state[row][col])
                    elif self.game_state[row][col][1] == 'Q':
                        pieces[self.game_state[row][col]] = Queen(row, col, self.game_state[row][col][0], self.game_state[row][col])
        self.replaceBoardWithPieceObjects(pieces)
        return pieces

    def replaceBoardWithPieceObjects(self, pieces):
        # iterate over pieces dict
        for key, value in pieces.items():
            self.game_state[pieces[key].row][pieces[key].col] = value

    def drawGameState(self, screen, start_pos, legal_moves):
        """
        controls the drawing work flow
        """
        self.drawSquares(screen)
        self.drawPieces(screen)
        if start_pos and legal_moves:
            self.drawLegalMoves(screen, start_pos, legal_moves)

    def drawSquares(self, screen):
        """
        draws the squares on board
        """
        colors = [p.Color('white'), p.Color('gray')]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                p.draw.rect(screen, color, p.Rect(col * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size))

    def drawPieces(self, screen):
        """
        draws the pieces on the board using current game_state
        """
        for row in range(8):
            for col in range(8):
                piece = self.game_state[row][col]
                if piece:  # not an empty square
                    screen.blit(self.images[piece.name[:2]], p.Rect(col * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size))

    def drawLegalMoves(self, screen, start_pos, legal_moves):
        p.draw.rect(screen, [189, 0, 0], p.Rect(start_pos[1] * self.sq_size, start_pos[0] * self.sq_size, self.sq_size, self.sq_size), 1)
        for legal_move in legal_moves:
            p.draw.circle(screen, [189, 0, 0], ((legal_move[1] * self.sq_size)+self.sq_size//2, (legal_move[0] * self.sq_size)+self.sq_size//2), self.sq_size//2, 1)


    def click(self):
        location = p.mouse.get_pos()  # (x,y) location of mouse
        col = location[0] // self.sq_size
        row = location[1] // self.sq_size
        square_name = self.getSquareName(row, col)
        if self.game_state[row][col]:
            piece = self.game_state[row][col]
            start_pos, legal_moves = piece.getLegalMoves(self.game_state, self.white_to_move)
            print(piece)
            print(piece.name, piece.row, piece.col)
            print(legal_moves)
            print(square_name)
        else:
            legal_moves = []
            start_pos = []
            print(square_name)
        return start_pos, legal_moves

    def getSquareName(self, row, col):
        if self.player_color == 'b':
            rows_to_ranks = {0: 1, 1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8}
            cols_to_files = {0: 'h', 1: 'g', 2: 'f', 3: 'e', 4: 'd', 5: 'c', 6: 'b', 7: 'a'}
        else:
            rows_to_ranks = {7: 1, 6: 2, 5: 3, 4: 4, 3: 5, 2: 6, 1: 7, 0: 8}
            cols_to_files = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}

        return cols_to_files[col] + str(rows_to_ranks[row])


