import pygame
import random

from src.modules.fighter.render import load_animation_frames
from src.modules.UI import CharDictionary as chardict
from src.modules.UI import constants as con

class Dice:
    def __init__(self, display_surface):
        self.screen = display_surface
        self.dice_size = chardict.DICE_RESULT_DATA["size"] * chardict.DICE_RESULT_DATA["scale"]
        self.rolling_animation_list = load_animation_frames(
            chardict.DICE_ROLLING_DATA["animation"],
            chardict.DICE_ROLLING_DATA["size"],
            chardict.DICE_ROLLING_DATA["scale"]
        )["ROLLING"]["ground"]
        
        self.result_frame_list = load_animation_frames(
            chardict.DICE_RESULT_DATA["animation"],
            chardict.DICE_RESULT_DATA["size"],
            chardict.DICE_RESULT_DATA["scale"]
        )["RESULT"]["ground"]

        self.frame_index = 0
        self.animation_cooldown = chardict.DICE_ROLLING_DATA["animation"]["ROLLING"]["cooldown"]
        self.result = random.randint(1, 20)
        

        self.state = "rolling"  # rolling / showing / done
        self.state_timer = pygame.time.get_ticks()
        self.update_time = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()
        state_consumed_time = current_time - self.state_timer

        if self.state == "rolling":
            if current_time - self.update_time >= self.animation_cooldown:
                # loop rolling
                self.frame_index = (self.frame_index + 1) % len(self.rolling_animation_list)  
                self.update_time = current_time

            if state_consumed_time >= chardict.DICE_ROLLING_DATA["rolling_duration"]:
                self.state = "showing"
                self.state_timer = current_time

        elif self.state == "showing":
            if state_consumed_time >= chardict.DICE_RESULT_DATA["showing_duration"]:
                self.state = "done"
        
        return self.state

    def draw(self):
        rolling_image = self.rolling_animation_list[self.frame_index]
        result_image = self.result_frame_list[self.result - 1]

        
        #pygame.draw.rect(self.screen, con.ORANGE, dice_rect)
        if self.state == "rolling":
            dice_rect = rolling_image.get_rect()
            dice_rect.centerx = con.SCREEN_WIDTH // 2
            dice_rect.centery = con.ROUND_TEXT_Y + 300
            self.screen.blit(rolling_image, dice_rect)
        else:
            dice_rect = result_image.get_rect()
            dice_rect.centerx = con.SCREEN_WIDTH // 2
            dice_rect.centery = con.ROUND_TEXT_Y + 258
            self.screen.blit(result_image, dice_rect)

        if self.state == "showing":

            if self.result > 10:
                text = "REVIVE"
                text_color = con.RED
            elif self.result < 10:
                text = "CURSE"
                text_color = con.BLACK
            else:
                text = None

            if text:
                text_surface = con.ROUND_FONT.render(text, True, text_color)
                text_rect = text_surface.get_rect()
                text_rect.centerx = con.SCREEN_WIDTH // 2
                text_rect.y = dice_rect.centery + self.dice_size // 4 + 58
                self.screen.blit(text_surface, text_rect)


