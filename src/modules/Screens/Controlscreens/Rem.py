import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr

#The help screen
class Rem():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((100, 100, 100, 200))

        #text
        self.txt = ["Attack1: A swift, powerful single punch | P1: r | P2: Slash (/)",
                    "",
                    "",
                    "Attack2: Stomps the ground, creating a shockwave attack | P1: f | P2: Period (.)",
                    "",
                    "",
                    "Attack3: Uses her horns to perform an upward strike, piercing through the enemy | P1: v | P2: Comma (,)",
                    "",
                    "",
                    "Despite peaceful nature, Rem is hunted down by many heroes as a trophy for their victory, she endures their weak attacks",
                    "",
                    "",
                    "until she gets fed up and has to quickly dispose of the ignorant threat."
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
        title = con.font_XLarge.render("Controls for Rem", True, con.YELLOW)
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
                    result = confscr(self.screen, self.clock, "Rem").run()
                    return result
                if event.type == pygame.KEYDOWN:
                    con.exit_sound.play()
                    return "Help"
            self.draw()
            res.render_to_surface()
            self.clock.tick(con.FPS)
