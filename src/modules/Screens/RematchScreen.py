import pygame

from src.modules.UI import constants as con
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems.scalemouse import scale_mouse
from src.modules.systems import res
from src.modules.UI.Button import Button
from src.modules.Screens.SelectCharScreen import CharPreview
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr

class RematchScreen:


    def __init__(self, screen, winner_text, winner_data, winner_flip=False):
        self.screen      = screen
        self.winner_text = winner_text
        self.winner_data = winner_data
        self.winner_flip = winner_flip

        self.window_rect = pygame.Rect(con.WINDOW_X, con.WINDOW_Y, con.WINDOW_WIDTH, con.WINDOW_HEIGHT)

        self.font_title   = pygame.font.SysFont(None, int(con.SCREEN_HEIGHT * 0.072))
        self.font_rematch = pygame.font.SysFont(None, int(con.SCREEN_HEIGHT * 0.052))
        self.font_button     = pygame.font.SysFont(None, int(con.SCREEN_HEIGHT * 0.036))

        # CharPreview
        if winner_data:
            self.preview = CharPreview(winner_data)
        else:
            self.preview = None

        self.yes = Button(con.WINDOW_YES_X, con.WINDOW_BUTTON_Y, con.WINDOW_BUTTON_WIDTH, con.WINDOW_BUTTON_HEIGHT,
                              "YES", self.font_button,
                              button_color=con.DARK_RED)
        self.no  = Button(con.WINDOW_NO_X,  con.WINDOW_BUTTON_Y, con.WINDOW_BUTTON_WIDTH, con.WINDOW_BUTTON_HEIGHT,
                              "NO",  self.font_button,
                              button_color=con.DARK_BLUE)
        
        self.background_snapshot = self.screen.copy()
        overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(con.BLACK)
        self.background_snapshot.blit(overlay, (0, 0))

    def draw(self):
        self.screen.blit(self.background_snapshot, (0, 0))

        pygame.draw.rect(self.screen, con.GRAY_BLUE, self.window_rect, border_radius=con.WINDOW_BORDER_RADIUS)
        pygame.draw.rect(self.screen, con.WHITE, self.window_rect, con.WINDOW_BORDER_WIDTH, border_radius=con.WINDOW_BORDER_RADIUS)

        lines     = self.winner_text.split("\n")
        line_h    = self.font_title.get_height()
        title_top = self.window_rect.y + con.TITLE_GAP
        for i, line in enumerate(lines):
            text_surface = self.font_title.render(line.strip(), True, con.RED)
            self.screen.blit(text_surface, text_surface.get_rect(centerx=self.window_rect.centerx, y=title_top + i * line_h))

        title_block_bottom = title_top + len(lines) * line_h

        if self.preview:
            frame = self.preview.get_frame()
            if self.winner_flip:
                frame = pygame.transform.flip(frame, True, False)

            preview_y = title_block_bottom + con.TITLE_PREVIEW_GAP
            self.screen.blit(frame, frame.get_rect(centerx=self.window_rect.centerx, y=preview_y))

            rematch_y = preview_y + frame.get_height() + con.PREVIEW_REMATCH_GAP
        else:
            rematch_y = title_block_bottom + con.TITLE_REMATCH_GAP

        text_surface = self.font_rematch.render("Rematch?", True, con.WHITE)
        self.screen.blit(text_surface, text_surface.get_rect(centerx=self.window_rect.centerx, y=rematch_y))

        self.yes.draw(self.screen)
        self.no.draw(self.screen)

        appBright(self.screen)

    def run(self):
        while True:
            con.clock.tick(con.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = confscr(self.screen, con.clock, "pause").run()
                    return result
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "Menu"
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = scale_mouse()
                    if self.yes.is_clicked((mx, my), True):
                        con.select_sound.play()
                        return "Rematch"
                    if self.no.is_clicked((mx, my), True):
                        con.exit_sound.play()
                        return "Menu"

            self.draw()
            res.render_to_surface()