import pygame
import random
from pygame.locals import *

from src.modules.fighter.Fighter import Fighter
from src.modules.UI import constants as con
from src.modules.systems.Draw import draw_screen
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res
from tests.test import DebugPopup

# the fight screen class
class FightScreen():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.knight = None
        self.werebear = None

        # screen shake
        self.shake_end_time = 0
        self.screen_shake_offset = (0, 0)

    def loadfighters(self):
        p1 = getattr(con, "p1_selected", (con.knight_sheet,   con.KNIGHT_ANIMATION_STEPS)) # default to knight if not set
        p2 = getattr(con, "p2_selected", (con.werebear_sheet, con.WEREBEAR_ANIMATION_STEPS)) # default to werebear if not set
        self.knight   = Fighter(con.con.PLAYER_1_X, con.FLOOR_Y - con.PLAYER_HEIGHT, con.PLAYER_WIDTH, con.PLAYER_HEIGHT, False, con.CHARACTER_DATA, p1[0], p1[1], con.P1_CONTROLS)
        self.werebear = Fighter(con.con.PLAYER_2_X, con.FLOOR_Y - con.PLAYER_HEIGHT, con.PLAYER_WIDTH, con.PLAYER_HEIGHT, True,  con.CHARACTER_DATA, p2[0], p2[1], con.P2_CONTROLS)
        self.background = con.fight_backgrounds[con.selected_map]

    def update(self):
        self.knight.move(con.SCREEN_WIDTH, con.SCREEN_HEIGHT, con.FLOOR_HEIGHT, self.werebear)
        self.werebear.move(con.SCREEN_WIDTH, con.SCREEN_HEIGHT, con.FLOOR_HEIGHT, self.knight)
        self.knight.update()
        self.werebear.update()

        # check if any damage maded
        current_time = pygame.time.get_ticks()
        for fighter in (self.knight, self.werebear):
            if fighter.screen_shake:
                self.shake_end_time = current_time + con.SCREEN_SHAKE_DURATION
                fighter.screen_shake = False
        
        if current_time < self.shake_end_time:
            remain_time = self.shake_end_time - current_time
            ratio = remain_time / con.SCREEN_SHAKE_DURATION
            shake_intensity = int(ratio * con.SCREEN_SHAKE_INTENSITY)
            self.screen_shake_offset = (random.randint(-shake_intensity, shake_intensity),
                                        random.randint(-shake_intensity, shake_intensity))
        else:
            self.screen_shake_offset = (0, 0)

        if self.knight.death or self.werebear.death:
            return "menu"
        return None
    
    def draw(self):
        x, y = self.screen_shake_offset
        draw_screen(self.screen, self.background, con.FLOOR_Y, con.FLOOR_HEIGHT, con.SCREEN_WIDTH, self.knight, self.werebear, offset=(x, y))
        self.knight.draw(self.screen)
        self.werebear.draw(self.screen)
        appBright(self.screen)

    def run(self):
        self.loadfighters()
        forest_sfx = pygame.mixer.Sound(con.forestsound)

        con.background_music.stop()
        forest_sfx.play(-1)
        con.fight_music.play(-1)

        debug = DebugPopup(self)

        def stop_fight_sounds():
            forest_sfx.stop()
            con.fight_music.stop()

        #loop for fightscreen
        while True:
            con.clock.tick(con.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    stop_fight_sounds()
                    return "quit"
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    stop_fight_sounds()
                    con.exit_sound.play()
                    return "menu"
                debug.handle_event(event)

            self.update()
            self.draw()
            debug.draw(self.screen)
            res.render_to_surface()
            