# main.py
import sys
import pygame
import logic
import render
import settings


clock = pygame.time.Clock()
BOARD = logic.new_board(settings.SIZE_X, settings.SIZE_Y)
pygame.init()
gameboard_res = settings.SIZE_X*settings.CELL, settings.SIZE_Y*settings.CELL

app_screen = pygame.display.set_mode((gameboard_res[0], gameboard_res[1]+settings.PANEL_H))
game_screen = app_screen.subsurface(0, 0, gameboard_res[0], gameboard_res[1])
panel_name_screen = app_screen.subsurface(0, gameboard_res[1], gameboard_res[0], settings.PANEL_H)

render.draw_name_panel(panel_name_screen)
pygame.display.flip()


def switch_player(player):
    return "O" if player == "X" else "X"


def mouse_to_cell(pos):
    return pos[0]//settings.CELL, pos[1]//settings.CELL


def run():
    game_over = False
    player = "X"    

    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over == False:
                cell_x, cell_y = mouse_to_cell(event.pos)

                if logic.is_valid_move(BOARD, cell_x, cell_y):
                    logic.apply_move(BOARD, cell_x, cell_y, player)
                    render.draw_grid(game_screen)
                    render.draw_xo(BOARD, game_screen)
                    pygame.display.flip()

                    is_win = logic.is_win(BOARD, cell_x, cell_y, player, settings.WIN_LEN)
                    if is_win[0]:
                        render.draw_win_highland(BOARD, game_screen, is_win[1])
                        pygame.display.flip()
                        pygame.mouse.set_visible(True)
                        game_over = True
                        print(f"Vyhrál {player}")
                                            
                    player = switch_player(player)

        if not game_over:
            render.draw_grid(game_screen)
            render.draw_xo(BOARD, game_screen)

        # render X/O instead mouse
            mx, my = pygame.mouse.get_pos()
            if mx < gameboard_res[0] and my < gameboard_res[1]:
                pygame.mouse.set_visible(False)
            else: pygame.mouse.set_visible(True)

            if player == "X":
                render.draw_x(game_screen, mx//settings.CELL, my//settings.CELL, True)
            else:
                render.draw_o(game_screen, mx//settings.CELL, my//settings.CELL, True)
            pygame.display.flip()


        render.draw_name_panel(panel_name_screen)
        pygame.display.flip()

        clock.tick(30)



if __name__ == "__main__":
    run()