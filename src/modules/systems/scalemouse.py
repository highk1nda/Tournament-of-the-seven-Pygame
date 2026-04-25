import pygame

from src.modules.UI import constants as con

# a helper function that corrects mouse positions based off of resolution, the output is given as coordinates
def scale_mouse():
    x , y = pygame.mouse.get_pos()
    win_w, win_h = con.window.get_size()
    scaled_x = int(x * (con.SCREEN_WIDTH / win_w))
    scaled_y = int(y * (con.SCREEN_HEIGHT / win_h))
    return scaled_x, scaled_y