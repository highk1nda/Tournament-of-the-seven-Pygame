import pygame
from src.modules.UI import constants as con
from src.modules.systems.scalemouse import scale_mouse

class Button():
    def __init__(self, x, y, width, height, text, font, button_color, text_color= con.WHITE, hovering_color=con.GREY, nonselect=False, SelectScreen=False, border_color=con.WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.text_color = text_color
        self.button_color = button_color
        self.hovering_color = hovering_color
        self.nonselect = nonselect
        self.select_screen = SelectScreen 
        self.selected = False    
        self.disabled = False    
        self.border_color = border_color

    def draw(self, screen):
        pos = scale_mouse()

        #if caller is select screen we raw a a line on the edge of the button, similar to the select screens
        if self.select_screen:
            draw_color = con.butt_disabled_color if self.disabled else self.button_color

            if not self.disabled and self.rect.collidepoint(pos):
                draw_color = self.hovering_color
            pygame.draw.rect(screen, draw_color, self.rect)
            if self.selected:
                pygame.draw.rect(screen, self.border_color, self.rect, 3, border_radius=7)

        else:
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
            if self.nonselect == False and self.select_screen == False:
                self.button_color = con.YELLOW
            return True
        return False

