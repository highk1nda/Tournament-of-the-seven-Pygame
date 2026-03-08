import pygame
from src.modules.UI import constants as con

"""
WE MAY HAVE TO MOVE THIS INTO FIGHTERSCREEN, i think this looks better though because fighterscreen class will look cleaner.
TODO we definetely have to check best practices on this dilemma
"""

def draw_health_bar(display_surface, health, x, y, right_side):
    ratio = health / 100
    max_width = 400
    current_width = max_width * ratio
    
    pygame.draw.rect(display_surface, con.WHITE, (x - 2, y - 2, 404, 34), 2)

    # make health bars axially symmetric
    if not right_side:
        pygame.draw.rect(display_surface, con.RED, (x, y, current_width, 30))
    else:
        pygame.draw.rect(display_surface, con.RED, (x + max_width - current_width, y, current_width, 30))


def draw_screen(display_surface, background, floor_y, floor_height, screen_width, fighter1, fighter2):
    # RENDERING
    # Draw background
    display_surface.blit(background, (0, 0))

    # Draw health bars
    draw_health_bar(display_surface, fighter1.health, 20, 20, False)
    draw_health_bar(display_surface, fighter2.health, 580, 20, True)

    # Draw floor
    pygame.draw.rect(display_surface, con.GREEN, (0, floor_y, screen_width, floor_height))