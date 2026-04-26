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
        # STATE -----------
        self.state = "menu"
        self.game_over = False
        self.player = "X"
        self.winners_coordinates = []
        # BOARD -----------
        self.board_layouts = data["board_layouts"]
        self.board_layouts_keys = list(self.board_layouts.keys())
        self.board_selected_layout = 1
        self.board_selected_layout_temp = self.board_selected_layout
        # SCREEN ----------
        self.app_screen = pygame.display.set_mode((self.res[0], self.res[1]+self.panel_h))
        self.game_screen = self.app_screen.subsurface(0, 0, self.res[0], self.res[1])
        self.panel_name_screen = pygame.Surface((self.res[0], self.panel_h))

        self.menu_screen = pygame.Surface((self.game_screen.get_size()), pygame.SRCALPHA)
        self.menu_bg_screen = pygame.Surface((self.res), pygame.SRCALPHA)
        # BOARD -----------
        self.board = logic.new_board(self.get_scale_size_value())


    def get_scale_size_key(self):
        layout_n = self.board_selected_layout
        if self.state == "settings":
            layout_n = self.board_selected_layout_temp
        key = self.board_layouts_keys[layout_n]
        return key  #example: small

    def get_scale_size_value(self):
        value = self.board_layouts[self.get_scale_size_key()]
        return value    #example: 10    (actual value)


config = Config()


class Button:
    def __init__(self, text):
        self.text = text
        self.rect = None

    def is_clicked(self, clicked_pos):
        if self.rect:
            return self.rect.collidepoint(clicked_pos)
        return False


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
    config.state = "game"
    config.game_over = False
    config.winners_coordinates = []


def draw():
    if config.state in ("menu", "settings"):
        pygame.mouse.set_visible(True)
        render.draw_grid(config, config.game_screen, config.res)
        render.draw_board_with_xo(config, config.board, config.game_screen)
        render.draw_win_highland(config, config.board, config.game_screen, config.winners_coordinates)
        if config.state == "menu":
            render.draw_menu(config, config.menu_screen, menu_buttons)
        elif config.state == "settings":
            render.draw_menu(config, config.menu_screen, settings_buttons)
        config.game_screen.blit(config.menu_screen, (0, 0))

    elif config.state == "game":
        render.draw_grid(config, config.game_screen, config.res)
        render.draw_board_with_xo(config, config.board, config.game_screen)

        if not config.game_over:
            # render X/O cursor instead of pointer
            mx, my = pygame.mouse.get_pos()
            if mx < config.res[0] and my < config.res[0]:
                pygame.mouse.set_visible(False)
            else: pygame.mouse.set_visible(True)

            if config.player == "X":
                render.draw_x(config, config.game_screen, mx, my, True)
            else:
                render.draw_o(config, config.game_screen, mx, my, True)
        
        else:
            render.draw_win_highland(config, config.board, config.game_screen, config.winners_coordinates)
            pygame.mouse.set_visible(True)
            

def run():
    pygame.init()
    render.draw_name_panel(config)
    clock = pygame.time.Clock()

    # EVENT HANDLER -------------------------------------------------------------------------------------
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # NEW event menu
            if config.state == "menu":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    config.state = "game"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in menu_buttons:
                        if button.is_clicked(event.pos):
                            if button.text == "Continue":
                                config.state = "game"
                            elif button.text == "New game":
                                new_game()
                            elif button.text == "Settings":
                                config.state = "settings"
                
            # NEW settings menu
            elif config.state == "settings":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    config.board_selected_layout_temp = config.board_selected_layout
                    config.state = "menu"

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in settings_buttons:
                        if button.is_clicked(event.pos):
                            if button.text == "Return":
                                config.board_selected_layout_temp = config.board_selected_layout
                                config.state = "menu"
                            elif button.text == "<< Layout size >>":
                                print(config.board_selected_layout_temp)
                                if event.pos[0] < button.rect.centerx:
                                    config.board_selected_layout_temp -= 1
                                else:
                                    config.board_selected_layout_temp += 1
                                
                            elif button.text == "Save & New game":
                                config.board_selected_layout = config.board_selected_layout_temp
                                new_game()


                                



            # EVENT MENU -------------------------------------------------------------------------------
            # if config.state == "menu":
            #     if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #         config.state = "game"

            #     elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #         mx, my = event.pos
            #         for button in menu_buttons:
            #             if button.rect != None and button.rect.collidepoint(mx, my):

            #                 if button.text == "Continue":
            #                     config.state = "game"

            #                 elif button.text == "New game":
            #                     config.board = logic.new_board(config.get_scale_size_value())
            #                     config.state = "game"
            #                     config.game_over = False
            #                     config.winners_coordinates = []

            #                 elif button.text == "Settings":
            #                     config.state = "settings"

            # elif config.state == "settings":
            #     if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            #         config.state = "menu"

            #     elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #         mx, my = event.pos
            #         for button in settings_buttons:
            #             if button.rect != None and button.rect.collidepoint(mx, my):

            #                 temp_board_selected_layout = config.board_selected_layout

            #                 if button.text == "Return":
            #                     config.board_selected_layout = 0
            #                     config.state = "menu"

            #                 elif button.text == "<< Layout size >>":
            #                     if mx < button.rect.centerx:
            #                         config.board_selected_layout -= 1

            #                     else:
            #                         config.board_selected_layout += 1

            #                 elif button.text == "Save & New game":
            #                     new_game()
            #                     config.state = "game"

                            
                            
            # EVENT GAME -------------------------------------------------------------------------------
            elif config.state == "game":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    config.state = "menu"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and config.game_over == False:
                    cell_x, cell_y = mouse_to_cell(event.pos)

                    if logic.is_valid_move(config.board, cell_x, cell_y):
                        logic.apply_move(config.board, cell_x, cell_y, config.player)
                        win, coordinates = logic.is_win(config.board, cell_x, cell_y, config.player, config.win_len)
                        if win:
                            config.game_over = True
                            config.winners_coordinates = coordinates
                            print(f"Vyhrál {config.player}")

                        if logic.is_tie(config.board):
                            config.game_over = True
                            print("Remíza")
                                                
                        config.player = switch_player(config.player)

        draw()

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    run()