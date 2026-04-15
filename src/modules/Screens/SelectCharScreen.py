import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.UI.Button import Button
from src.modules.fighter.render import load_animation_frames, crop_and_scale_frames

BG    = con.SELECT_BG_COLOR
RED   = con.SELECT_P1_BTN_COLOR
BLUE  = con.SELECT_P2_BTN_COLOR
GREEN = con.SELECT_FIGHT_BTN_COLOR
GREY  = con.BUTTON_DISABLED_COLOR

LABELS = ["Ser Edward", "Tyland", "Luna", "Rem", "Arland", "Venator"]

# frame sheets and steps per row. #TODO: NONE means not yet implemented (for other characters)
CHAR_DATA = [
    (con.knight_sheet,          con.KNIGHT_ANIMATION_STEPS),
    (con.werebear_sheet,        con.WEREBEAR_ANIMATION_STEPS),
    (con.wizard_sheet,          con.WIZARD_ANIMATION_STEPS),
    None, # minotaur
    None, # archer
    (con.knight_templar_sheet,  con.KNIGHT_TEMPLAR_ANIMATION_STEPS),
]

LOAD_SCALE   = con.SELECT_LOAD_SCALE
PREVIEW_SIZE = con.SELECT_PREVIEW_SIZE
BTN_W        = con.SELECT_BTN_W
BTN_H        = con.SELECT_BTN_H
BTN_GAP      = con.SELECT_BTN_GAP
GRID_WIDTH   = con.SELECT_GRID_WIDTH
P1_CX        = con.SELECT_P1_CX
P2_CX        = con.SELECT_P2_CX
LABEL_Y      = con.SELECT_LABEL_Y
PREVIEW_Y    = con.SELECT_PREVIEW_Y
BTN_ROW1_Y   = con.SELECT_BTN_ROW1_Y
BTN_ROW2_Y   = con.SELECT_BTN_ROW2_Y
FIGHT_Y      = con.SELECT_FIGHT_Y


def make_button_rects(center_x):
    start_x = center_x - GRID_WIDTH // 2
    return [
        pygame.Rect(
            start_x + (i % 3) * (BTN_W + BTN_GAP),
            BTN_ROW1_Y if i < 3 else BTN_ROW2_Y,
            BTN_W, BTN_H,
        )
        for i in range(6)
    ]


# handles the idle render in the character preview box
class CharPreview:

    def __init__(self, sheet, steps):
        idle_frames  = load_animation_frames(sheet, 100, LOAD_SCALE, steps)[con.ACTIONS["IDLE"]]
        self.frames  = crop_and_scale_frames(idle_frames, PREVIEW_SIZE)

        self.frame_index = 0
        self.last_time   = pygame.time.get_ticks()

    def get_frame(self):
        now = pygame.time.get_ticks()
        if now - self.last_time > con.ANIMATION_COOLDOWNS[con.ACTIONS["IDLE"]]:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_time   = now
        return self.frames[self.frame_index]


class SelectCharScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock
        self.font   = pygame.font.SysFont(None, 28)
        self.big    = pygame.font.SysFont(None, 46)

        self.p1_btns   = make_button_rects(P1_CX)
        self.p2_btns   = make_button_rects(P2_CX)
        self.fight_btn = Button(con.SELECT_FIGHT_BTN_X, FIGHT_Y, 200, 45, "FIGHT",
                                self.font, button_color=GREEN)

        self.p1_idx = 0  # default: Knight
        self.p2_idx = 1  # default: Werebear

        self.previews = []
        for data in CHAR_DATA:
            if data is not None:
                sheet, steps = data
                self.previews.append(CharPreview(sheet, steps))
            else:
                self.previews.append(None)

    def select_char(self, player, idx):
        # only select if the character is implemented (has char data)
        if CHAR_DATA[idx] is not None:
            if player == 1:
                self.p1_idx = idx
            else:
                self.p2_idx = idx

    # draw helpers

    def draw_centered(self, surface, center_x, y):
        self.screen.blit(surface, (center_x - surface.get_width() // 2, y))

    def draw_button(self, rect, label, color, selected=False, disabled=False):
        btn_color = GREY if disabled else color
        pygame.draw.rect(self.screen, btn_color, rect, border_radius=5)
        if selected:
            pygame.draw.rect(self.screen, con.WHITE, rect, 3, border_radius=5)
        label_surf = self.font.render(label, True, con.WHITE)
        self.screen.blit(label_surf, (rect.centerx - label_surf.get_width()  // 2,
                                      rect.centery - label_surf.get_height() // 2))

    def draw_preview(self, char_idx, center_x, flip=False):
        preview = self.previews[char_idx]
        if preview is not None:
            frame = preview.get_frame()
            if flip:
                frame = pygame.transform.flip(frame, True, False)
            self.screen.blit(frame, (center_x - frame.get_width()  // 2,
                                     PREVIEW_Y + (PREVIEW_SIZE - frame.get_height()) // 2))
            
    #text and button drawing is all done in this function beloow
    def draw(self):
        self.screen.fill(BG)

        self.draw_centered(self.big.render("PLAYER 1", True, con.SELECT_P1_LABEL_COLOR), con.SELECT_P1_CX, con.SELECT_LABEL_Y)
        self.draw_centered(self.big.render("PLAYER 2", True, con.SELECT_P2_LABEL_COLOR), con.SELECT_P2_CX, con.SELECT_LABEL_Y)

        self.draw_preview(self.p1_idx, con.SELECT_P1_CX)
        self.draw_preview(self.p2_idx, con.SELECT_P2_CX, flip=True)

        for i in range(6):
            disabled = CHAR_DATA[i] is None
            self.draw_button(self.p1_btns[i], LABELS[i], RED,
                             selected=(i == self.p1_idx), disabled=disabled)
            self.draw_button(self.p2_btns[i], LABELS[i], BLUE,
                             selected=(i == self.p2_idx), disabled=disabled)

        self.fight_btn.draw(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    return "menu"
                if event.type == MOUSEBUTTONDOWN:
                    for i in range(6):
                        if self.p1_btns[i].collidepoint(event.pos):
                            self.select_char(1, i)
                        if self.p2_btns[i].collidepoint(event.pos):
                            self.select_char(2, i)
                    if self.fight_btn.is_clicked(event.pos, True):
                        con.p1_selected = CHAR_DATA[self.p1_idx]
                        con.p2_selected = CHAR_DATA[self.p2_idx]
                        return "fight"

            self.draw()
            pygame.display.update()
            self.clock.tick(60)
