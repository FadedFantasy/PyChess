import pygame as p
from board import Board
from pieces import Piece


width = height = 850
max_fps = 30  # if needed later for animations
p.init()

screen = p.display.set_mode((width, height))
clock = p.time.Clock()
screen.fill(p.Color('white'))
player_color = 'w'
board = Board(width, height, player_color)
start_pos = []
legal_moves = []
piece = None


running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                if not start_pos:
                    start_pos, piece, legal_moves = board.firstClickSelect()
                else:
                    end_pos, is_move = board.secondClickSelect(legal_moves)
                    if is_move:
                        board.performMove(piece, start_pos, end_pos)
                        board.updatePiecesList()
                        if board.color_to_move == 'w':
                            board.color_to_move = 'b'
                        else:
                            board.color_to_move = 'w'
                        board.checkCheckmate()
                    start_pos = []
                    piece = None
                    legal_moves = []
            elif event.button == 3:  # right click
                start_pos = []
                piece = None
                legal_moves = []

    board.drawGameState(screen, start_pos, legal_moves)
    clock.tick(max_fps)
    p.display.flip()
p.quit()

