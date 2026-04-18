import pygame
from src.modules.UI import constants as con

#helper function is called instead of pygame.display.update(), the functions scales the game to fit the window size.
def render_to_surface():
    scaled = pygame.transform.smoothscale(con.display_surface, (con.window.get_width(), con.window.get_height()))
    con.window.blit(scaled, (0, 0))
    pygame.display.update()