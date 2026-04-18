import pygame
from pygame.locals import *

from src.modules.fighter.Fighter import Fighter 
from src.modules.UI import constants as con
from src.modules.systems.Draw import draw_screen
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res

# the fight screen class
class FightScreen():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.knight = None
        self.werebear = None

    def loadfighters(self):
        self.knight = Fighter(con.PLAYER_1_X, con.FLOOR_Y - con.PLAYER_HEIGHT, con.PLAYER_WIDTH, con.PLAYER_HEIGHT, False, con.CHARACTER_DATA, con.knight_sheet, con.KNIGHT_ANIMATION_STEPS)
        self.werebear = Fighter(con.PLAYER_2_X, con.FLOOR_Y - con.PLAYER_HEIGHT, con.PLAYER_WIDTH, con.PLAYER_HEIGHT, True, con.CHARACTER_DATA, con.werebear_sheet, con.WEREBEAR_ANIMATION_STEPS)

    def update(self):
        self.knight.move(con.SCREEN_WIDTH, con.SCREEN_HEIGHT, con.FLOOR_HEIGHT, con.PLAYER_1, self.werebear, self.screen)
        self.werebear.move(con.SCREEN_WIDTH, con.SCREEN_HEIGHT, con.FLOOR_HEIGHT, con.PLAYER_2, self.knight, self.screen)
        self.knight.update()
        self.werebear.update()

        if self.knight.death or self.werebear.death:
            return "menu"
        return None
    
    def draw(self):
        draw_screen(self.screen, con.background, con.FLOOR_Y, con.FLOOR_HEIGHT, con.SCREEN_WIDTH, self.knight, self.werebear)
        self.knight.draw(self.screen)
        self.werebear.draw(self.screen)
        appBright(self.screen)

    def run(self):
        self.loadfighters()
        con.forest_sfx.play(-1)

        #loop for fightscreen
        while True:
            con.clock.tick(con.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    con.forest_sfx.stop()
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    con.forest_sfx.stop()
                    return "menu"

            self.update()
            self.draw()
            res.render_to_surface()
            