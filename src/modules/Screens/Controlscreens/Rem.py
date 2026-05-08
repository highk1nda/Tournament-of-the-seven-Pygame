import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr
from src.modules.UI import CharDictionary as charDict
from src.modules.Screens.SelectCharScreen import CharPreview
from src.modules.UI.Button import Button 
from src.modules.Screens.Textcrawl import Textcrawl as textscr
from src.modules.systems.scalemouse import scale_mouse

#The help screen
class Rem():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.Intro = Button(1600, 700, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Introduction', con.font_Large, con.DARK_RED)
        if con.storyRemComplete:
            self.Ending = Button(1600, 900, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Ending', con.font_Large, con.DARK_RED)
        else:
            self.Ending = Button(1600, 900, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Ending', con.font_Large, con.BLACK, nonselect=True)

        self.click = False
        self.preview = CharPreview(charDict.CHARACTER_DATA[3])

        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((5, 5, 5, 220))
        

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
        

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.click = False
    
    def update(self):
        mx, my = scale_mouse()
        if self.Intro.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            con.p1_char_idx = 3
            return textscr(con.display_surface, con.clock, "Rem").run()
        if self.Ending.is_clicked((mx, my), self.click) and con.storyRemComplete:
            self.click = False
            con.select_sound.play()
            con.p1_char_idx = 3
            return textscr(con.display_surface, con.clock, "Rem", True).run()
        if self.Ending.is_clicked((mx, my), self.click) and not con.storyRemComplete:
            self.click = False
            con.ui_error_sound.play()
        return None

    def draw(self):
        #draw overlay, display title
        self.screen.blit(con.background, (0,0))
        self.screen.blit(self.overlay, (0,0))
        title = con.font_XLarge.render("Controls for Rem", True, con.YELLOW)
        self.screen.blit(title, title.get_rect(center=(con.SCREEN_WIDTH // 2, 170)))


        frame = self.preview.get_frame()
        self.screen.blit(frame, (int(con.SCREEN_WIDTH // 28.3), int(con.SCREEN_HEIGHT // 1.45)))

        #display text
        count = 0
        for line in self.txt:
            rendered_l = con.font_Big.render(line, True, con.WHITE)
            con.display_surface.blit(rendered_l, rendered_l.get_rect(center=(con.SCREEN_WIDTH // 2, count + 400)))
            count += 25
        
        self.Intro.draw(self.screen)
        self.Ending.draw(self.screen)

        appBright(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = confscr(self.screen, self.clock, "Rem").run()
                    return result
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    con.exit_sound.play()
                    return "Help"
                self.handle_event(event)
            action = self.update()
            if action:
                return action
            self.draw()
            res.render_to_surface()
            self.clock.tick(con.FPS)
