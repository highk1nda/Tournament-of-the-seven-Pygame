import pygame

#TODO: implement the feature of select detection, right now button class doesnt actually give any visual feedback, which is why the buttons in
# Options.py are different (placeholder) if we can figure out a way to get the buttonclass to fit both the main menu, the character, and options
# could use this

# button class, this will most likely be redone a bit, i just did this for the menu screen but i think we have to readjust it so it works in character select
class Button():
    def __init__(self, x, y, width, height, text, font, text_color=(255, 255, 255), button_color=(255, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.clicked = False

    def draw(self, screen):
        #draw red rectangles, (PLACEHOLDER UNTIL A BETTER BUTTON ASSET IS FOUND)
        pygame.draw.rect(screen, self.button_color, self.rect)

        # draw the text centered
        text_obj = self.font.render(self.text, True, self.text_color)
        text_rect = text_obj.get_rect()
        text_rect.center = self.rect.center
        screen.blit(text_obj, text_rect)

    # self explanatory, check if the user clicks the button
    def is_clicked(self, mouse_pos, mouse_click):
        if self.rect.collidepoint(mouse_pos) and mouse_click:
            return True
        return False

