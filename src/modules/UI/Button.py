import pygame
from src.modules.UI import constants as con
from src.modules.systems.scalemouse import scale_mouse
#TODO: implement the feature of select detection, right now button class doesnt actually give any visual feedback, which is why the buttons in
# Options.py are different (placeholder) if we can figure out a way to get the buttonclass to fit both the main menu, the character, and options
# could use this


# button class, this will most likely be redone a bit, i just did this for the menu screen but i think we have to readjust it so it works in character select
class Button():
    def __init__(self, x, y, width, height, text, font, button_color, text_color= con.WHITE, hovering_color=con.GREY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hovering_color = hovering_color
        self.clicked = False

    def draw(self, screen):
        #draw red rectangles, (PLACEHOLDER UNTIL A BETTER BUTTON ASSET IS FOUND)
        pygame.draw.rect(screen, self.button_color, self.rect)

        pos = scale_mouse()

        # switch colour if the button is being hovered over.
        if self.rect.collidepoint(pos):
            current_color = self.hovering_color
        else:            
            current_color = self.button_color
        pygame.draw.rect(screen, current_color, self.rect)

        # draw the text centered
        text_obj = self.font.render(self.text, True, self.text_color)
        text_rect = text_obj.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text_obj, text_rect)

    # self explanatory, check if the user clicks the button
    def is_clicked(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            self.button_color = con.DARK_GREEN
            return True
        return False

