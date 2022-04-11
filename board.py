import pygame as p

class Board:
    def __init__(self, window_width, window_height, player_color):
        self.width = window_width
        self.height = window_height
        self.dimension = 8
        self.sq_size = self.height // self.dimension
        self.images = self.loadImages()
        self.player_color = player_color
        self.game_state = self.initializeBoard()

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
            board = [
                ['wR', 'wN', 'wB', 'wK', 'wQ', 'wB', 'wN', 'wR'],
                ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                ['bR', 'bN', 'bB', 'bK', 'bQ', 'bB', 'bN', 'bR']
            ]
        else:  # white or multiplayer
            board = [
                ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['--', '--', '--', '--', '--', '--', '--', '--'],
                ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']
            ]
        return board

    def drawGameState(self, screen):
        """
        controls the drawing work flow
        """
        self.drawSquares(screen)
        self.drawPieces(screen)

    def drawSquares(self, screen):
        """
        draws the squares on board
        """
        colors = [p.Color('white'), p.Color('gray')]
        for row in range(self.dimension):
            for col in range(self.dimension):
                color = colors[(row + col) % 2]
                p.draw.rect(screen, color, p.Rect(col * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size))

    def drawPieces(self, screen):
        """
        draws the pieces on the board using current game_state
        """
        for row in range(self.dimension):
            for col in range(self.dimension):
                piece = self.game_state[row][col]
                if not piece == '--':  # not an empty square
                    screen.blit(self.images[piece], p.Rect(col * self.sq_size, row * self.sq_size, self.sq_size, self.sq_size))

