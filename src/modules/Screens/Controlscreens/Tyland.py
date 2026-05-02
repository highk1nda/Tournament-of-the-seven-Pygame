import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr

#The help screen
class Tyland():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((100, 100, 100, 200))
        
        #text
        self.txt = ["Attack1: Tyland performs a single slash with his claw | P1: r | P2: Slash (/)",
                    "",
                    "",
                    "Attack2: A double slash with both claws | P1: f | P2: Period (.)",
                    "",
                    "",
                    "Attack3: smashes the ground with his paws, creating a shockwave, that damages the enemy | P1: v | P2: Comma (,)",
                    "",
                    "",
                    "A slow but lethal fighter, Tyland combines his beast side with his human, but like any wild animal, instinct takes over when backed into a corner."
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "Press ESC to return to main menu"]

    def draw(self):
        #draw overlay, display title
        self.screen.blit(con.background, (0,0))
        self.screen.blit(self.overlay, (0,0))
        title = con.font_XLarge.render("Controls for Tyland", True, con.YELLOW)
        self.screen.blit(title, title.get_rect(center=(con.SCREEN_WIDTH // 2, 170)))


        #display text
        count = 0
        for line in self.txt:
            rendered_l = con.font_Big.render(line, True, con.WHITE)
            con.display_surface.blit(rendered_l, rendered_l.get_rect(center=(con.SCREEN_WIDTH // 2, count + 400)))
            count += 25
        appBright(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = confscr(self.screen, self.clock, "Tyland").run()
                    return result
                if event.type == pygame.KEYDOWN:
                    con.exit_sound.play()
                    return "Help"
            self.draw()
            res.render_to_surface()
            self.clock.tick(con.FPS)
