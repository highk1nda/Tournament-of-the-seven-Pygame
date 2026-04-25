import pygame
from src.modules.UI import constants as con

# used at the end of every draw function, applies the set brightness to the game
def apply_brightness(surface):
    if con.brightness < 100:
        alpha = int((1 - con.brightness / 100) * 200)
        dim = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        dim.fill((0, 0, 0, alpha))
        surface.blit(dim, (0, 0))