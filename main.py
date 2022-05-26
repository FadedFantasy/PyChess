import pygame as p
from board import Board

width = height = 850
max_fps = 30  # if needed later for animations
p.init()

screen = p.display.set_mode((width, height))
clock = p.time.Clock()
screen.fill(p.Color('white'))
player_color = 'w'
multiplayer = True
board = Board(width, height, player_color)
start_pos = []
legal_moves = []
piece = None
eval = 0.0

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                # player moves against computer or in multiplayer
                if (not start_pos and player_color == board.color_to_move) or (not start_pos and multiplayer):
                    start_pos, piece, legal_moves = board.firstClickSelect()
                elif (start_pos and player_color == board.color_to_move) or (start_pos and multiplayer):
                    end_pos, is_move = board.secondClickSelect(legal_moves)
                    if is_move:
                        board.performMove(piece, start_pos, end_pos)
                        board.updatePiecesList()
                        board.changeMovingColor()
                        # eval = board.evaluatePosition()
                        board.checkCheckmate()
                    start_pos = []
                    piece = None
                    legal_moves = []
                # computer moves
                if not multiplayer and board.color_to_move != player_color:
                    # piece, start_pos, end_pos = board.getComputerMove()
                    board.performMove(piece, start_pos, end_pos)
                    board.updatePiecesList()
                    board.changeMovingColor()
                    # eval = board.evaluatePosition()
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

