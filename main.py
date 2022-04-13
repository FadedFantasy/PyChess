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
player_clicks = []  # keep track of player clicks [(6,4), (4,4)]
start_pos_piece = []
legal_moves = []

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
        elif event.type == p.MOUSEBUTTONDOWN:
            if event.button == 1:  # left click
                start_pos_piece, legal_moves = board.click()
            elif event.button == 3:  # right click
                player_clicks = []
                legal_moves = []
                start_pos_piece = []

    board.drawGameState(screen, start_pos_piece, legal_moves)
    clock.tick(max_fps)
    p.display.flip()
p.quit()

