import pygame
from pygame.locals import *
from src.modules.UI import constants as con

BG    = (30, 30, 30)
RED   = (160, 45, 45)
BLUE  = (45, 70, 160)
WHITE = (255, 255, 255)
GREEN = (60, 140, 60)

LABELS = ["Knight", "Werebear", "Wizard", "Minotaur", "Archer", "K.Templar"]

# frame sheets and steps per row. #TODO: NONE means not yet implemented (for other characters)
CHAR_DATA = [
    (con.knight_sheet,         con.KNIGHT_ANIMATION_STEPS),
    (con.werebear_sheet,       con.WEREBEAR_ANIMATION_STEPS),
    (con.wizard_sheet,         con.WIZARD_ANIMATION_STEPS),
    None,
    None,
    (con.knight_templar_sheet, con.KNIGHT_TEMPLAR_ANIMATION_STEPS),
]

W, H     = con.SCREEN_WIDTH, con.SCREEN_HEIGHT
BTN_W    = 140
BTN_H    = 55
BTN_GAP  = 16
START_X  = (W - (3 * BTN_W + 2 * BTN_GAP)) // 2


def _grid_rects(top_y):
    return [
        pygame.Rect(START_X + (i % 3) * (BTN_W + BTN_GAP),
                    top_y   + (i // 3) * (BTN_H + BTN_GAP),
                    BTN_W, BTN_H)
        for i in range(6)
    ]


class SelectCharScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock
        self.font   = con.FONT_SMALL
        self.big    = con.FONT_BIG

        self.p1_btns   = _grid_rects(top_y=130)
        self.p2_btns   = _grid_rects(top_y=360)
        self.fight_btn = pygame.Rect(W // 2 - 100, H - 60, 200, 45)

        self.p1_idx = 0  # default: Knight
        self.p2_idx = 1  # default: Werebear

        self.p1_callbacks = [
            self.p1_select_knight,
            self.p1_select_werebear,
            self.p1_select_wizard,
            self.p1_select_minotaur,
            self.p1_select_archer,
            self.p1_select_ktemplar,
        ]
        self.p2_callbacks = [
            self.p2_select_knight,
            self.p2_select_werebear,
            self.p2_select_wizard,
            self.p2_select_minotaur,
            self.p2_select_archer,
            self.p2_select_ktemplar,
        ]

    # p1 character select
    def p1_select_knight(self):    
        self.p1_idx = 0
    def p1_select_werebear(self):  
        self.p1_idx = 1
    def p1_select_wizard(self):
        self.p1_idx = 2
    def p1_select_minotaur(self):  
        pass
    def p1_select_archer(self):    
        pass
    def p1_select_ktemplar(self):
        self.p1_idx = 5

    # p2 character select
    def p2_select_knight(self):    
        self.p2_idx = 0
    def p2_select_werebear(self):  
        self.p2_idx = 1
    def p2_select_wizard(self):
        self.p2_idx = 2
    def p2_select_minotaur(self):  
        pass
    def p2_select_archer(self):    
        pass
    def p2_select_ktemplar(self):
        self.p2_idx = 5

    def _draw_centered(self, surface, rect):
        self.screen.blit(surface, (rect.x + (rect.w - surface.get_width())  // 2,
                                   rect.y + (rect.h - surface.get_height()) // 2))

    def _draw_btn(self, rect, label, color, selected=False):
        pygame.draw.rect(self.screen, color, rect)
        if selected:
            pygame.draw.rect(self.screen, WHITE, rect, 3)
        self._draw_centered(self.font.render(label, True, WHITE), rect)

    def _draw_label(self, text, color, y):
        surf = self.big.render(text, True, color)
        self.screen.blit(surf, (W // 2 - surf.get_width() // 2, y))

    def _draw(self):
        self.screen.fill(BG)

        self._draw_label("PLAYER 1", RED,  85)
        self._draw_label("PLAYER 2", BLUE, 315)

        for i in range(6):
            self._draw_btn(self.p1_btns[i], LABELS[i], RED,  selected=(i == self.p1_idx))
            self._draw_btn(self.p2_btns[i], LABELS[i], BLUE, selected=(i == self.p2_idx))

        self._draw_btn(self.fight_btn, "FIGHT", GREEN)

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
                            self.p1_callbacks[i]()
                        if self.p2_btns[i].collidepoint(event.pos):
                            self.p2_callbacks[i]()
                    if self.fight_btn.collidepoint(event.pos):
                        con.p1_selected = CHAR_DATA[self.p1_idx]
                        con.p2_selected = CHAR_DATA[self.p2_idx]
                        return "fight"

            self._draw()
            pygame.display.update()
            self.clock.tick(60)
