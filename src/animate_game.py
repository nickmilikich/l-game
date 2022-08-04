# +
import numpy as np
import pygame as pg
import time
import pickle

from utils import *
# -

# Get full graph of game moves
with open('../data/graph.pkl', 'rb') as file:
    G = pickle.load(file)

cell_size = 200

black = (0, 0, 0)
white = (255, 255, 255)
player_colors = {
    '0': (255, 0, 0),
    '1': (0, 0, 255),
}


def show_board(screen, board):
    
    # Drop first piece and restructure board to 4x4
    board = board[1:]
    board = np.reshape(list(board), (4, 4))
    
    # Clear screen
    screen.fill(black)
    
    for x in range(4):
        for y in range(4):
                        
            # Draw borders between squares
            pg.draw.lines(
                screen,
                white,
                closed=False,
                points=[
                    (x * cell_size, y * cell_size),
                    ((x + 1) * cell_size, y * cell_size),
                    ((x + 1) * cell_size, (y + 1) * cell_size),
                    (x * cell_size, (y + 1) * cell_size),
                ]
            )
                
            # Color appropriately
            if board[y][x] in ['0', '1']: # Flip axes since numpy array accessing is in (y, x) order
                pg.draw.polygon(
                    screen,
                    player_colors[board[y][x]],
                    width=0,
                    points=[
                        (x * cell_size + 1, y * cell_size + 1),
                        ((x + 1) * cell_size - 1, y * cell_size + 1),
                        ((x + 1) * cell_size - 1, (y + 1) * cell_size - 1),
                        (x * cell_size + 1, (y + 1) * cell_size - 1),
                    ]
                )
            elif board[y][x] == 'n':
                pg.draw.circle(
                    screen,
                    white,
                    width=0,
                    center=((x + 0.5) * cell_size, (y + 0.5) * cell_size),
                    radius=0.5 * cell_size - 1,
                )
    
    pg.display.update()


def main():

    pg.init()
    screen = pg.display.set_mode((cell_size * 4 + 1, cell_size * 4 + 1))
    
    # Initial board setup
    board = '0n00  10  10  11n'
    show_board(screen, board)
    time.sleep(2)
    
    # Gameplay
    while len(board) == 17:
        board = get_best_move(G, board)
        show_board(screen, board)
        time.sleep(2)


main()
