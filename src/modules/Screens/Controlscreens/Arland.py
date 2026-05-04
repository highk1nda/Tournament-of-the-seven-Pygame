import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr
from src.modules.UI import CharDictionary as charDict
from src.modules.Screens.SelectCharScreen import CharPreview

#The help screen
class Arland():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.preview = CharPreview(charDict.CHARACTER_DATA[4])

        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((5, 5, 5, 220))
        
        #text
        self.txt = ["Attack1: Fires a straightforward single arrow shot | P1: r | P2: Slash (/)",
                    "",
                    "",
                    "Attack2: Charges briefly before firing a faster, more powerful arrow | P1: f | P2: Period (.)",
                    "",
                    "",
                    "An agile ranged fighter, Arland excels when keeping his distance and mowing down enemies slowly with his bow.",
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
                    "",
                    "",
                    "Press ESC to return to main menu"]

    def draw(self):
        #draw overlay, display title
        self.screen.blit(con.background, (0,0))
        self.screen.blit(self.overlay, (0,0))
        title = con.font_XLarge.render("Controls for Arland", True, con.YELLOW)
        self.screen.blit(title, title.get_rect(center=(con.SCREEN_WIDTH // 2, 170)))


        frame = self.preview.get_frame()
        self.screen.blit(frame, (int(con.SCREEN_WIDTH // 28.3), int(con.SCREEN_HEIGHT // 1.45)))

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
                    result = confscr(self.screen, self.clock, "Arland").run()
                    return result
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    con.exit_sound.play()
                    return "Help"
            self.draw()
            res.render_to_surface()
            self.clock.tick(con.FPS)
