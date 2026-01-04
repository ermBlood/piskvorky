# main.py
import sys
import pygame
import logic

# board size
SIZE_X = 10
SIZE_Y = 7
WIN_LEN = 5
BOARD = logic.new_board(SIZE_X, SIZE_Y)

# visual
CELL = 25
LINE_W = 2
MARK_W = 8
PANEL_H = 90
PAD = 18

# colors
CELL_COLOR = (65, 112, 129)
GRID_COLOR = (90, 157, 182)
X_COLOR = (200, 60, 60)
O_COLOR = (240, 240, 240)


pygame.init()
screen = pygame.display.set_mode((SIZE_X*CELL+LINE_W, SIZE_Y*CELL+LINE_W))


def draw_grid():
    screen.fill(CELL_COLOR)

    for y in range(SIZE_Y+1):
        pygame.draw.line(screen, GRID_COLOR,(0, y*CELL), (SIZE_X*CELL, y*CELL), LINE_W)    
    for x in range(SIZE_X+1):
        pygame.draw.line(screen, GRID_COLOR,(x*CELL, 0), (x*CELL, SIZE_Y*CELL), LINE_W)


def draw_x(x, y):
    pygame.draw.line(screen, X_COLOR, (x*CELL, y*CELL), (x*CELL+CELL, y*CELL+CELL), width=MARK_W)
    pygame.draw.line(screen, X_COLOR, (x*CELL+CELL, y*CELL), (x*CELL, y*CELL+CELL), width=MARK_W)


def draw_o(x, y):
    pygame.draw.circle(screen, O_COLOR, (x*CELL+CELL/2, y*CELL+CELL/2), CELL/2, width=MARK_W//2)
       

def draw_xo():
    cell_y = -1

    for row in BOARD:
        cell_y += 1
        for col in range(len(row)):
            if row[col] == "X":
                draw_x(col, cell_y)
            elif row[col] == "O":
                draw_o(col, cell_y)


def switch_player(player):
    return "O" if player == "X" else "X"


def mouse_to_cell(pos):
    return pos[0]//CELL, pos[1]//CELL


def run():
    player = "X"
    draw_grid()
    pygame.display.flip()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                cell_x, cell_y = mouse_to_cell(event.pos)
                if logic.is_valid_move(BOARD, cell_x, cell_y):

                    logic.apply_move(BOARD, cell_x, cell_y, player)

                    draw_grid()
                    draw_xo()
                    pygame.display.flip()

                    if logic.is_win(BOARD, cell_x, cell_y, player, WIN_LEN):
                        print(f"Vyhrál {player}")
                        break
                    
                    player = switch_player(player)




if __name__ == "__main__":
    run()