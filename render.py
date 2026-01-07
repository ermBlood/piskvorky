#render.py

import pygame
import settings

# board size
SIZE_X = settings.SIZE_X
SIZE_Y = settings.SIZE_Y
WIN_LEN = settings.WIN_LEN

# visual
CELL = settings.CELL
LINE_W = settings.LINE_W
MARK_W = settings.MARK_W
PANEL_H = settings.PANEL_H
PAD = settings.PAD

# colors
CELL_COLOR = settings.CELL_COLOR
GRID_COLOR = settings.GRID_COLOR
X_COLOR = settings.X_COLOR
O_COLOR = settings.O_COLOR


def draw_grid(screen):
    screen.fill(CELL_COLOR)

    for y in range(SIZE_Y+1):
        pygame.draw.line(screen, GRID_COLOR,(0, y*CELL), (SIZE_X*CELL, y*CELL), LINE_W)    
    for x in range(SIZE_X+1):
        pygame.draw.line(screen, GRID_COLOR,(x*CELL, 0), (x*CELL, SIZE_Y*CELL), LINE_W)


def draw_x(screen, x, y):
    pygame.draw.line(screen, X_COLOR, (x*CELL, y*CELL), (x*CELL+CELL, y*CELL+CELL), width=MARK_W)
    pygame.draw.line(screen, X_COLOR, (x*CELL+CELL, y*CELL), (x*CELL, y*CELL+CELL), width=MARK_W)


def draw_o(screen, x, y):
    pygame.draw.circle(screen, O_COLOR, (x*CELL+CELL/2, y*CELL+CELL/2), CELL/2, width=MARK_W//2)
       

def draw_xo(BOARD, screen):
    cell_y = -1

    for row in BOARD:
        cell_y += 1
        for col in range(len(row)):
            if row[col] == "X":
                draw_x(screen, col, cell_y)
            elif row[col] == "O":
                draw_o(screen, col, cell_y)


def draw_win_highland(BOARD, screen, coordinates):
    for x,y in coordinates:
        pygame.draw.rect(screen, "green", ((x*CELL+LINE_W, y*CELL+LINE_W), (CELL-LINE_W, CELL-LINE_W)))
    draw_xo(BOARD, screen)