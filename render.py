#render.py

import pygame
import settings

pygame.font.init()
font = pygame.font.SysFont("Great Vibes", 30)


def draw_grid(screen):
    screen.fill(settings.GRID_COLOR)

    for x in range(settings.SIZE_Y):
        for y in range(settings.SIZE_X):
            pygame.draw.rect(screen, settings.CELL_COLOR, (settings.CELL*y, settings.CELL*x, settings.CELL, settings.CELL), width=settings.LINE_W//2)


def draw_name_panel(panel_screen):
    panel_screen.fill((35,35,35))
    text_piskvorky = font.render("piškvorky", True, (225,225,225))
    text_piskvorky_rect = text_piskvorky.get_rect(center=(settings.SIZE_X*(settings.CELL+settings.LINE_W)//2, settings.PANEL_H//2))
    panel_screen.blit(text_piskvorky, text_piskvorky_rect)


def draw_text(surface, font, text, x, y, color):
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, (x, y))


def draw_x(screen, x, y, cursor=False):
    if cursor: color = settings.CURSOR_COLOR
    else: color = settings.X_COLOR

    temp_surface = pygame.Surface((settings.CELL, settings.CELL), pygame.SRCALPHA)    
    pygame.draw.rect(temp_surface, color, (settings.CELL//2-settings.MARK_W//2, 0, settings.MARK_W, settings.CELL))
    pygame.draw.rect(temp_surface, color, (0, settings.CELL//2-settings.MARK_W//2, settings.CELL, settings.MARK_W))
    temp_surface = pygame.transform.rotate(temp_surface, 45)

    offset = (temp_surface.get_width()-settings.CELL)//2
    screen.blit(temp_surface, (x*settings.CELL-offset, y*settings.CELL-offset))


def draw_o(screen, x, y, cursor=False):
    if cursor: color = settings.CURSOR_COLOR
    else: color = settings.O_COLOR

    pygame.draw.circle(screen, color, (x*settings.CELL+settings.CELL//2, y*settings.CELL+settings.CELL//2), settings.CELL//2*.75, width=settings.MARK_W)


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
    for y,x in coordinates:
        pygame.draw.rect(screen, settings.WIN_HIGHLAND_COLOR, (y*settings.CELL+settings.LINE_W//2, x*settings.CELL+settings.LINE_W//2, settings.CELL-settings.LINE_W, settings.CELL-settings.LINE_W))
    draw_xo(BOARD, screen)