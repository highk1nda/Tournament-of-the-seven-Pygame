import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr

#The help screen
class Help():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        #text
        self.txt = ["player 1 - Movement: A/D left and right respectively   Jump: W      Attacks: R, F, V",
                    "",
                    "",
                    "",
                    "player 2 - Movement: Larrow and Rarrow respectively    Jump: UParrow      Attacks: .  /  Lshift",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "Press ESC to return to main menu"]

        #overlay to make it smooth
        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((100, 100, 100, 200))
    
    def draw(self):
        #draw overlay, display title
        self.screen.blit(con.background, (0,0))
        self.screen.blit(self.overlay, (0,0))
        title = con.font_XLarge.render("Controls", True, con.YELLOW)
        self.screen.blit(title, title.get_rect(center=(con.SCREEN_WIDTH // 2, 170)))

        #display text
        count = 0
        for line in self.txt:
            rendered_l = con.font_Medium.render(line, True, con.WHITE)
            con.display_surface.blit(rendered_l, rendered_l.get_rect(center=(con.SCREEN_WIDTH // 2, count + 400)))
            count += 25
        appBright(self.screen)

    def run(self):
        #help screen loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = confscr(self.screen, self.clock, "Help").run()
                    return result
                if event.type == pygame.KEYDOWN:
                    con.exit_sound.play()
                    return "Menu"
            self.draw()
            res.render_to_surface()
            self.clock.tick(con.FPS)