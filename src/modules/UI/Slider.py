import pygame
from src.modules.UI import constants as con
from src.modules.systems.scalemouse import scale_mouse


class Slider:
    def __init__(self, x, y, width, height, initial=1.0, name="",
                 font=con.font_Medium, track_color=con.GREY, fill_color=con.YELLOW,
                 handle_color=con.WHITE, txt_color=con.WHITE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.font = font
        self.track_color = track_color
        self.fill_color = fill_color
        self.handle_color = handle_color
        self.txt_color = txt_color
        self.handle_radius = height
        # pygame uses 0-1 for volume, but we want to use 0-100, so we multiply
        self.value = int(initial * 100)
        self.dragging = False

    def get_handle_x(self):
        percentage = self.value / 100
        offset = percentage * self.width
        # return the position where the handle should be drawn at
        return int(self.x + offset)

    def get_val_from_mouse(self, mouse_x):
        # how many pixels from the start of the slider
        offset = mouse_x - self.x
        percentage = offset / self.width
        if percentage < 0:
            percentage = 0
        if percentage > 1:
            percentage = 1
        # turn % back into 0-100 value and return it
        return int(percentage * 100)

    def draw(self, screen):
        track = pygame.Rect(self.x, self.y - self.height // 2, self.width, self.height)
        pygame.draw.rect(screen, self.track_color, track, border_radius=self.height // 2)

        handle_x = self.get_handle_x()
        fill_width = handle_x - self.x
        if fill_width > 0:
            fill = pygame.Rect(self.x, self.y - self.height // 2, fill_width, self.height)
            pygame.draw.rect(screen, self.fill_color, fill, border_radius=self.height // 2)

        # draw a handle (white circle), at current position
        pygame.draw.circle(screen, self.handle_color, (handle_x, self.y), self.handle_radius)

        name_text = f"{self.name}: {self.value}%"
        name_surf = self.font.render(name_text, True, self.txt_color)
        screen.blit(name_surf, name_surf.get_rect(center=(self.x + self.width // 2, self.y - int(con.SCREEN_HEIGHT / 36))))

    def handle_event(self, event):
        pos = scale_mouse()
        # check if clicked on slider, if yes then update the value
        track = pygame.Rect(self.x, self.y - self.height // 2, self.width, self.height)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if track.collidepoint(pos):
                self.dragging = True
                new_val = self.get_val_from_mouse(pos[0])
                if new_val != self.value:
                    self.value = new_val
                    return True

        # if mouse is moving and slider is being dragged, update its value
        if event.type == pygame.MOUSEMOTION and self.dragging:
            new_val = self.get_val_from_mouse(pos[0])
            if new_val != self.value:
                self.value = new_val
                return True

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

        return False
