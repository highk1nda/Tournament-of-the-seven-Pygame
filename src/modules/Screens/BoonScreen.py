import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.UI.Button import Button
from src.modules.Screens.SelectCharScreen import CharPreview, CHAR_DATA
#TODO: this is a very basic implementation of the boon screen, we can add more functionality later (like different boons, or maybe even a small animation when selecting)
BG    = con.SELECT_BG_COLOR
RED   = con.SELECT_P1_BTN_COLOR
BLUE  = con.SELECT_P2_BTN_COLOR
GREEN = con.SELECT_FIGHT_BTN_COLOR
GREY  = con.BUTTON_DISABLED_COLOR

BOONS = ["BOON 1", "BOON 2", "BOON 3"]

P1_CX      = con.SELECT_P1_CX
P2_CX      = con.SELECT_P2_CX
PREVIEW_Y  = con.SELECT_PREVIEW_Y
PREVIEW_SZ = con.SELECT_PREVIEW_SIZE

BTN_W    = con.BOON_BTN_W
BTN_H    = con.BOON_BTN_H
BTN_GAP  = con.BOON_BTN_GAP
BOON_Y   = con.SELECT_BTN_ROW1_Y
CONFIRM_Y = con.SELECT_FIGHT_Y


class BoonScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock
        self.font   = pygame.font.SysFont(None, 30)
        self.big    = pygame.font.SysFont(None, 46)

        self.p1_idx = con.p1_char_idx
        self.p2_idx = con.p2_char_idx

        self.previews = []
        for data in CHAR_DATA:
            if data is not None:
                sheet, steps = data
                self.previews.append(CharPreview(sheet, steps))
            else:
                self.previews.append(None)

        self.p1_selected = None
        self.p2_selected = None

        self.p1_rects = [
            pygame.Rect(P1_CX - BTN_W // 2, BOON_Y + i * (BTN_H + BTN_GAP), BTN_W, BTN_H)
            for i in range(3)
        ]
        self.p2_rects = [
            pygame.Rect(P2_CX - BTN_W // 2, BOON_Y + i * (BTN_H + BTN_GAP), BTN_W, BTN_H)
            for i in range(3)
        ]
        self.confirm_btn = Button(con.SCREEN_WIDTH // 2 - 100, CONFIRM_Y, 200, 45,
                                  "CONTINUE", self.font, button_color=GREY)

    def draw_centered(self, surface, center_x, y):
        self.screen.blit(surface, (center_x - surface.get_width() // 2, y))

    def draw_button(self, rect, label, color, selected=False):
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        if selected:
            pygame.draw.rect(self.screen, con.WHITE, rect, 3, border_radius=5)
        s = self.font.render(label, True, con.WHITE)
        self.screen.blit(s, (rect.centerx - s.get_width() // 2,
                             rect.centery - s.get_height() // 2))

    def draw_preview(self, char_idx, center_x, flip=False):
        preview = self.previews[char_idx]
        if preview is None:
            return
        frame = preview.get_frame()
        if flip:
            frame = pygame.transform.flip(frame, True, False)
        self.screen.blit(frame, (center_x - frame.get_width() // 2,
                                 PREVIEW_Y + (PREVIEW_SZ - frame.get_height()) // 2))

    def draw(self):
        self.screen.fill(BG)

        self.draw_centered(self.big.render("PLAYER 1", True, con.SELECT_P1_LABEL_COLOR), P1_CX, con.SELECT_LABEL_Y)
        self.draw_centered(self.big.render("PLAYER 2", True, con.SELECT_P2_LABEL_COLOR), P2_CX, con.SELECT_LABEL_Y)

        self.draw_preview(self.p1_idx, P1_CX)
        self.draw_preview(self.p2_idx, P2_CX, flip=True)

        for i in range(3):
            self.draw_button(self.p1_rects[i], BOONS[i], RED,  self.p1_selected == i)
            self.draw_button(self.p2_rects[i], BOONS[i], BLUE, self.p2_selected == i)

        both_ready = self.p1_selected is not None and self.p2_selected is not None
        self.confirm_btn.button_color = GREEN if both_ready else GREY
        self.confirm_btn.draw(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    con.exit_sound.play()
                    return "play"
                if event.type == MOUSEBUTTONDOWN:
                    for i in range(3):
                        if self.p1_rects[i].collidepoint(event.pos):
                            con.select_sound.play()
                            self.p1_selected = i
                        if self.p2_rects[i].collidepoint(event.pos):
                            con.select_sound.play()
                            self.p2_selected = i

                    both_ready = self.p1_selected is not None and self.p2_selected is not None
                    if both_ready and self.confirm_btn.is_clicked(event.pos, True):
                        con.select_sound.play()
                        con.p1_boon = BOONS[self.p1_selected]
                        con.p2_boon = BOONS[self.p2_selected]
                        return "map"

            self.draw()
            pygame.display.update()
            self.clock.tick(60)
