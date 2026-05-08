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
class Luna():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.Intro = Button(1600, 700, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Introduction', con.font_Large, con.DARK_RED)
        if con.storyLunaComplete:
            self.Ending = Button(1600, 900, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Ending', con.font_Large, con.DARK_RED)
        else:
            self.Ending = Button(1600, 900, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Ending', con.font_Large, con.BLACK, Nonselect=True)

        self.click = False
        self.preview = CharPreview(charDict.CHARACTER_DATA[2])

        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((5, 5, 5, 220))
        
        #text
        self.txt = ["Attack1: Summons crystals around the enemy's current position. After a short delay, the crystals converge and pierce the enemy | P1: r | P2: Slash (/)",
                    "",
                    "",
                    "Attack2: A simple yet effective fireball attack | P1: f | P2: Period (.)",
                    "",
                    "",
                    "Slow and weak, Luna's appearence is deceiving, as her attacks pack quite a punch, using her crystal magic and fireball attacks.",
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
            con.p1_char_idx = 2
            return textscr(con.display_surface, con.clock, "Luna").run()
        if self.Ending.is_clicked((mx, my), self.click) and con.storyLunaComplete:
            self.click = False
            con.select_sound.play()
            con.p1_char_idx = 2
            return textscr(con.display_surface, con.clock, "Luna", True).run()
        if self.Ending.is_clicked((mx, my), self.click) and not con.storyLunaComplete:
            self.click = False
            con.ui_error_sound.play()
        return None

    def draw(self):
        #draw overlay, display title
        self.screen.blit(con.background, (0,0))
        self.screen.blit(self.overlay, (0,0))
        title = con.font_XLarge.render("Controls for Luna", True, con.YELLOW)
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
                    result = confscr(self.screen, self.clock, "Luna").run()
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
