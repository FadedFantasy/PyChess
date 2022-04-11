import pygame as p
from board import Board
from piece import Piece


width = height = 850
max_fps = 30  # if needed later for animations

p.init()
screen = p.display.set_mode((width, height))
clock = p.time.Clock()
screen.fill(p.Color("white"))
player_color = "b"
board = Board(width, height, player_color)
running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

    board.drawGameState(screen)
    clock.tick(max_fps)
    p.display.flip()
p.quit()

