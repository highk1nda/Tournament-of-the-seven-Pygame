import pygame

from src.modules.UI import constants as con
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res
from src.modules.systems.scalemouse import scale_mouse
from src.modules.UI.Button import Button 

class confirm_dialog():
    def __init__(self, screen, clock, state):
        self.screen = screen
        self.clock = clock

        self.yes = Button(con.center_x - int(con.SCREEN_WIDTH/14.14), con.center_y + int(con.SCREEN_HEIGHT/54), 
                          int(con.SCREEN_WIDTH/14.14), int(con.SCREEN_HEIGHT/28.42), "Yes", con.font_Medium, con.DARK_RED)
        self.no = Button(con.center_x + int(con.SCREEN_WIDTH/64), con.center_y + int(con.SCREEN_HEIGHT/54), 
                         int(con.SCREEN_WIDTH/14.14), int(con.SCREEN_HEIGHT/28.42), "No", con.font_Medium, con.DARK_BLUE)

        self.state = state

    def draw_confirm_dialog(self):
        overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # draw message
        msg = con.font_Large.render("Are you sure you want to exit?", True, con.WHITE)
        self.screen.blit(msg, (con.center_x - msg.get_width() // 2, con.center_y - 30))

        self.yes.draw(self.screen)
        self.no.draw(self.screen)

        appBright(self.screen)

    def handle_event(self, event):
        mx, my = scale_mouse()
        if event.type == pygame.QUIT:
            return "quit"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return self.state
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.yes.is_clicked((mx, my), True):
                    con.exit_sound.play()
                    return "quit"
                if self.no.is_clicked((mx, my), True):
                    return self.state
        return None
    
    def run(self):
        while True:
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result:
                    return result
            self.draw_confirm_dialog()
            res.render_to_surface()
            self.clock.tick(con.FPS)