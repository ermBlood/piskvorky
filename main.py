# main.py
import sys
import pygame
import logic
import render
import json

class Config:
    def __init__(self):
        with open("config.json") as file:
            data = json.load(file)

        self.cell = data["cell"]
        self.panel_h = data["panel_h"]
        self.win_len = data["win_len"]
        self.line_w = data["line_w"]
        self.mark_w = data["mark_w"]
        self.grid_color = data["grid_color"]
        self.cell_color = data["cell_color"]
        self.button_color = data["button_color"]
        self.x_color = data["x_color"]
        self.o_color = data["o_color"]
        self.cursor_color = data["cursor_color"]
        self.win_highland_color = data["win_highland_color"]
        self.menu_bg_color = data["menu_bg_color"]
        self.res = data["res"]
        # BOARD -----------
        self.board_layouts = data["board_layouts"]
        self.board_layouts_keys = list(self.board_layouts.keys())
        self.board_selected_layout = 1
        # SCREEN ----------
        self.app_screen = pygame.display.set_mode((self.res[0], self.res[1]+self.panel_h))
        self.game_screen = self.app_screen.subsurface(0, 0, self.res[0], self.res[1])
        self.panel_name_screen = pygame.Surface((self.res[0], self.panel_h))

        self.menu_screen = pygame.Surface((self.game_screen.get_size()), pygame.SRCALPHA)
        self.menu_bg_screen = pygame.Surface((self.res), pygame.SRCALPHA)
        # BOARD -----------
        self.board = logic.new_board(self.get_scale_size_value())


    def get_scale_size_key(self):
        key = self.board_layouts_keys[self.board_selected_layout]
        return key

    def get_scale_size_value(self):
        value = self.board_layouts[self.get_scale_size_key()]
        return value


config = Config()


class Button:
    def __init__(self, text):
        self.text = text
        # self.rect = pygame.

menu_buttons = [
    Button("Continue"),
    Button("New game"),
    Button("Settings"),
]
settings_buttons = [
    Button("Return"),
    Button("<< Layout size >>"),
    Button("Save & New game")
]


def switch_player(player):
    return "O" if player == "X" else "X"


def mouse_to_cell(pos):
    cells_in_row = config.get_scale_size_value()
    size_of_cell = config.res[0]//cells_in_row
    return pos[0]//size_of_cell, pos[1]//size_of_cell


def new_game():
    config.board = logic.new_board(config.get_scale_size_value())


def run():
    pygame.init()
    render.draw_name_panel(config)
    clock = pygame.time.Clock()
    state = "menu"
    game_over = False
    player = "X"
    winners_coordinates = []

    # EVENT HANDLER -------------------------------------------------------------------------------------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            # EVENT MENU -------------------------------------------------------------------------------
            if state == "menu":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "game"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for button in menu_buttons:
                        if button.rect.collidepoint(mx, my):

                            if button.text == "Continue":
                                state = "game"

                            elif button.text == "New game":
                                config.board = logic.new_board(config.get_scale_size_value())
                                state = "game"
                                game_over = False
                                winners_coordinates = []

                            elif button.text == "Settings":
                                state = "settings"

            elif state == "settings":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "menu"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for button in settings_buttons:
                        if button.rect.collidepoint(mx, my):

                            temp_board_selected_layout = config.board_selected_layout

                            if button.text == "Return":
                                config.board_selected_layout = 0
                                state = "menu"

                            elif button.text == "<< Layout size >>":
                                if mx < button.rect.centerx:
                                    config.board_selected_layout -= 1

                                else:
                                    config.board_selected_layout += 1

                            elif button.text == "Save & New game":
                                new_game()
                                state = "game"

                            
                            
            # EVENT GAME -------------------------------------------------------------------------------
            elif state == "game":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    state = "menu"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and game_over == False:
                    cell_x, cell_y = mouse_to_cell(event.pos)

                    if logic.is_valid_move(config.board, cell_x, cell_y):
                        logic.apply_move(config.board, cell_x, cell_y, player)
                        win, coordinates = logic.is_win(config.board, cell_x, cell_y, player, config.win_len)
                        if win:
                            game_over = True
                            winners_coordinates = coordinates
                            print(f"Vyhrál {player}")

                        if logic.is_tie(config.board):
                            game_over = True
                            print("Remíza")
                                                
                        player = switch_player(player)
               
                
    # DRAW ---------------------------------------------------------------------------------------------
        if state == "menu":
            pygame.mouse.set_visible(True)
            render.draw_grid(config, config.game_screen, config.res)
            render.draw_board_with_xo(config, config.board, config.game_screen)
            render.draw_win_highland(config, config.board, config.game_screen, winners_coordinates)
            render.draw_menu(config, config.menu_screen, menu_buttons)
            config.game_screen.blit(config.menu_screen, (0, 0))

        if state == "settings":
            pygame.mouse.set_visible(True)
            render.draw_grid(config, config.game_screen, config.res)
            render.draw_board_with_xo(config, config.board, config.game_screen)
            render.draw_win_highland(config, config.board, config.game_screen, winners_coordinates)
            render.draw_menu(config, config.menu_screen, settings_buttons)
            config.game_screen.blit(config.menu_screen, (0, 0))

        elif state == "game":
            render.draw_grid(config, config.game_screen, config.res)
            render.draw_board_with_xo(config, config.board, config.game_screen)

            if not game_over:
                # render X/O cursor instead of pointer
                mx, my = pygame.mouse.get_pos()
                if mx < config.res[0] and my < config.res[0]:
                    pygame.mouse.set_visible(False)
                else: pygame.mouse.set_visible(True)

                if player == "X":
                    render.draw_x(config, config.game_screen, mx, my, True)
                else:
                    render.draw_o(config, config.game_screen, mx, my, True)
            
            else:
                render.draw_win_highland(config, config.board, config.game_screen, winners_coordinates)
                pygame.mouse.set_visible(True)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    run()