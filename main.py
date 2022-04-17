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
player_clicks = []
start_pos_piece = []
legal_moves = []
move_log = []

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                start_pos_piece, legal_moves, player_clicks = board.click(legal_moves, player_clicks)
                if len(player_clicks) == 2:
                    move_success = board.performMove(player_clicks, legal_moves)
                    player_clicks = []
                    legal_moves = []
                    if move_success:
                        if board.color_to_move == 'w':
                            board.color_to_move = 'b'
                        else:
                            board.color_to_move = 'w'
            elif event.button == 3:  # right click
                player_clicks = []
                legal_moves = []
                start_pos_piece = []

    board.drawGameState(screen, start_pos_piece, legal_moves)
    clock.tick(max_fps)
    p.display.flip()
p.quit()

