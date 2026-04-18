import pygame
from src.modules.UI import constants as con


def draw_health_bar(display_surface, health, x, y, right_side):
    ratio = health / 100
    current_width = int(con.healthbar_width * ratio)
    
    border_rect = (
        x - con.healthbar_padding,
        y - con.healthbar_padding,
        con.healthbar_width + con.healthbar_padding * 2,
        con.healthbar_height + con.healthbar_padding * 2
    )
    
    pygame.draw.rect(display_surface, con.WHITE, border_rect, 2)

    # make health bars axially symmetric
    if not right_side:
        pygame.draw.rect(display_surface, con.RED, (x, y, current_width, con.healthbar_height))
    else:
        pygame.draw.rect(display_surface, con.RED, (x + con.healthbar_width - current_width, y, current_width, con.healthbar_height))


def draw_screen(display_surface, background, floor_y, floor_height, screen_width, fighter1, fighter2):
    # RENDERING
    # Draw background
    display_surface.blit(background, (0, 0))

    # Draw health bars
    draw_health_bar(display_surface, fighter1.health, con.healthbar_x, con.healthbar_y, False)
    draw_health_bar(display_surface, fighter2.health, con.healtbar_xx, con.healthbar_y, True)

    # Draw floor
    pygame.draw.rect(display_surface, con.GREEN, (0, floor_y, screen_width, floor_height))