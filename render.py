#render.py
import pygame

pygame.font.init()
font = pygame.font.SysFont("Noto Sans", 30)


def draw_grid(config, screen, board_size):
    screen.fill(config.cell_color)
    cells_in_row = config.get_scale_size_value()

    for x in range(cells_in_row):
        for y in range(cells_in_row):
            pygame.draw.rect(screen, config.grid_color, (config.res[0]//cells_in_row*y, config.res[0]//cells_in_row*x, config.res[0]//cells_in_row, config.res[0]//cells_in_row), width=config.line_w//2)


def draw_menu(config, screen, buttons):
    screen.fill(config.menu_bg_color)

    screen_height = config.res[1]
    button_height = screen_height//10
    gap = button_height//2
    
    # celková výška všech tlačítek dohromady
    total_height = len(buttons) * button_height + (len(buttons) - 1) * gap

    # kde začít (aby byl blok tlačítek vycentrovaný)
    start_y = screen_height // 2 

    for n, button in enumerate(buttons):
        button.rect = draw_button(config, screen, button.text, button.name, button_height, start_y, gap, n)

    
def draw_button(config, screen, text, name, button_height, start_y, gap, n):
    button_rect = pygame.Rect(0, 0, screen.get_width()*.5, button_height)   #----- create whole button
    button_rect.centerx = screen.get_rect().centerx                         
    button_rect.centery = start_y + n * (button_height + gap)
    pygame.draw.rect(screen, config.button_color, button_rect)              #-----
    
    text_surface = font.render(f"{text}", True, "white")                    # create surface for base text
    text_rect = text_surface.get_rect()                                     # create rect for surface base text
    text_rect.center = button_rect.center                                   # move base text rect to base rect pos

    # with values
    if name in ("layout_size", "win_len"):
        value = None

        if name == "layout_size": value = config.get_scale_size_key()
        elif name == "win_len" : value = config.win_len_temp
        
        text_rect.right = button_rect.centerx                               
        value_surface = font.render(f": {value}", True, "white")  # create surface for value
        value_rect = value_surface.get_rect()                                           # create rect for surface value
        value_rect.center = button_rect.center                                          # move value rect to button rect
        value_rect.left = button_rect.centerx
        screen.blit(value_surface, value_rect)      # draw value surface on screen in position of value rect - (picture, pos)

    # with arrows
    if name in ("layout_size", "win_len"):
        l_arrow_surface = font.render(" <", True, "white")   # create arrow text surface
        r_arrow_surface = font.render("> ", True, "white")

        l_arrow_rect = l_arrow_surface.get_rect()           # create rect from text surface
        r_arrow_rect = r_arrow_surface.get_rect()

        l_arrow_rect.midleft = button_rect.midleft          # move rect to button pos
        r_arrow_rect.midright = button_rect.midright

        screen.blit(l_arrow_surface, l_arrow_rect)
        screen.blit(r_arrow_surface, r_arrow_rect)
    
    screen.blit(text_surface, text_rect)
    return button_rect
    

def draw_name_panel(config):
    font = pygame.font.SysFont("Great Vibes", 30)
    config.panel_name_screen.fill((35,35,35))
    text_piskvorky = font.render("piškvorky", True, (225,225,225))
    text_piskvorky_rect = text_piskvorky.get_rect(center=(config.res[0]//2, config.panel_h//2))
    config.panel_name_screen.blit(text_piskvorky, text_piskvorky_rect)
    config.app_screen.blit(config.panel_name_screen, ((0, config.res[0])))


def draw_text(surface, text, x, y, color, size=30):
    font = pygame.font.SysFont("Noto Sans", size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x-text_surface.get_width()//2, y-text_surface.get_height()//2))


def draw_x(config, screen, x, y, is_like_cursor=False):
    if is_like_cursor: color = config.cursor_color
    else: color = config.x_color
    cells_in_row = config.get_scale_size_value()
    size_of_cell = config.res[0]//cells_in_row

    temp_surface = pygame.Surface((size_of_cell, size_of_cell), pygame.SRCALPHA)
    pygame.draw.rect(temp_surface, color, (size_of_cell//2-config.mark_w/2, 0, config.mark_w, size_of_cell))  
    pygame.draw.rect(temp_surface, color, (0, size_of_cell//2-config.mark_w/2, size_of_cell, config.mark_w))
    temp_surface = pygame.transform.rotate(temp_surface, 45)

    offset= (temp_surface.get_width()//2)
    screen.blit(temp_surface, (x-offset, y-offset))


def draw_o(config, screen, x, y, is_like_cursor=False):
    if is_like_cursor: color = config.cursor_color
    else: color = config.o_color
    cells_in_row = config.get_scale_size_value()

    pygame.draw.circle(screen, color, (x, y), config.res[0]//cells_in_row//2*.75, width=config.mark_w)
    # pygame.gfxdraw.aacircle(screen, int(x), int(y), int(config.res[0]//cells_in_row//2*.75), (200, 200, 200))

def draw_board_with_xo(config, board, screen):
    cells_in_row = config.get_scale_size_value()
    size_of_cell = config.res[0]//cells_in_row

    row_n = 0
    for row in board:
        cell_n = 0
        for cell in row:
            if cell == "X":
                draw_x(config, screen, cell_n*size_of_cell + size_of_cell*.5, row_n*size_of_cell + size_of_cell*.5)
            elif cell == "O":
                draw_o(config, screen, cell_n*size_of_cell + size_of_cell*.5, row_n*size_of_cell + size_of_cell*.5)
            cell_n += 1
        row_n += 1


def draw_win_highland(config, board, screen, winners_coordinates):
    cells_in_row = config.get_scale_size_value()
    size_of_cell = config.res[0]//cells_in_row

    for y,x in winners_coordinates:
        pygame.draw.rect(screen, config.win_highland_color, (y*size_of_cell+config.line_w//2, x*size_of_cell+config.line_w//2, size_of_cell-config.line_w, size_of_cell-config.line_w))
    draw_board_with_xo(config, board, screen)