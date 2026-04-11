import pygame
from pygame.locals import *

from src.modules.fighter.Fighter import Fighter
from src.modules.UI import constants as con
from src.modules.sfx.sound_loader import load_fighter_sounds
from src.modules.systems.Draw import draw_screen
from tests.test import DebugPopup

# the fight screen class
class FightScreen():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.knight = None
        self.werebear = None

    def loadfighters(self):
        self.knight = Fighter(con.PLAYER_1_INIT_X, con.FLOOR_Y - con.PLAYER_HEIGHT, con.PLAYER_WIDTH, con.PLAYER_HEIGHT, False, con.CHARACTER_DATA, con.knight_sheet, con.KNIGHT_ANIMATION_STEPS, con.P1_CONTROLS)
        self.werebear = Fighter(con.PLAYER_2_INIT_X, con.FLOOR_Y - con.PLAYER_HEIGHT, con.PLAYER_WIDTH, con.PLAYER_HEIGHT, True, con.CHARACTER_DATA, con.werebear_sheet, con.WEREBEAR_ANIMATION_STEPS, con.P2_CONTROLS)

    def update(self):
        self.knight.move(con.SCREEN_WIDTH, con.SCREEN_HEIGHT, con.FLOOR_HEIGHT, self.werebear, self.screen)
        self.werebear.move(con.SCREEN_WIDTH, con.SCREEN_HEIGHT, con.FLOOR_HEIGHT, self.knight, self.screen)
        self.knight.update()
        self.werebear.update()

        if self.knight.death or self.werebear.death:
            return "menu"
        return None
    
    def draw(self):
        draw_screen(self.screen, con.background, con.FLOOR_Y, con.FLOOR_HEIGHT, con.SCREEN_WIDTH, self.knight, self.werebear)
        self.knight.draw(self.screen)
        self.werebear.draw(self.screen)

    def run(self):
        self.loadfighters()
        forest_sfx = pygame.mixer.Sound(con.forestsound)
        forest_sfx.play(-1)
        debug = DebugPopup(self)

        #loop for fightscreen
        while True:
            con.clock.tick(con.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    forest_sfx.stop()
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    forest_sfx.stop()
                    return "menu"
                debug.handle_event(event)

            self.update()
            self.draw()
            debug.draw(self.screen)
            pygame.display.update()
            