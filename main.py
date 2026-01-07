# main.py
import sys
import pygame
import logic
import render
import settings


BOARD = logic.new_board(settings.SIZE_X, settings.SIZE_Y)
pygame.init()
screen = pygame.display.set_mode((settings.SIZE_X*settings.CELL+settings.LINE_W, settings.SIZE_Y*settings.CELL+settings.LINE_W))




def switch_player(player):
    return "O" if player == "X" else "X"


def mouse_to_cell(pos):
    return pos[0]//settings.CELL, pos[1]//settings.CELL


def run():
    game_over = False
    player = "X"
    render.draw_grid(screen)
    pygame.display.flip()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over == False:
                cell_x, cell_y = mouse_to_cell(event.pos)
                if logic.is_valid_move(BOARD, cell_x, cell_y):

                    logic.apply_move(BOARD, cell_x, cell_y, player)

                    render.draw_grid(screen)
                    render.draw_xo(BOARD, screen)
                    pygame.display.flip()

                    is_win = logic.is_win(BOARD, cell_x, cell_y, player, settings.WIN_LEN)
                    if is_win[0]:
                        print(f"Vyhrál {player}")
                        render.draw_win_highland(BOARD, screen, is_win[1])
                        pygame.display.flip()
                        game_over = True
                                            
                    player = switch_player(player)




if __name__ == "__main__":
    run()