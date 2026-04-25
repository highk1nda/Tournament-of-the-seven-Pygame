import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems import res 
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems.scalemouse import scale_mouse
from src.modules.UI.Button import Button
from src.modules.Screens.SelectCharScreen import CharPreview, CHAR_DATA
from src.modules.fighter.render import load_magic_projectiles, draw_magic_effect
#TODO: TO MOVE IT TO CONSTANTS LATER
BG           = con.SELECT_BG_COLOR
GREEN        = con.SELECT_FIGHT_BTN_COLOR
GREY         = con.BUTTON_DISABLED_COLOR
ACTIVE_COLOR = (70, 130, 80)
PASS_COLOR   = con.SELECT_P2_BTN_COLOR
PANEL_COLOR  = (40, 42, 58)
BACK_COLOR   = (120, 50, 50)

# placeholder names and descriptions for now
BOONS = [
    {"name": "Active Boon 1",  "type": "ACTIVE",  "desc": ["Placeholder description", "for active boon 1."]},
    {"name": "Active Boon 2",  "type": "ACTIVE",  "desc": ["Placeholder description", "for active boon 2."]},
    {"name": "Passive Boon 1", "type": "PASSIVE", "desc": ["Placeholder description", "for passive boon 1."]},
    {"name": "Passive Boon 2", "type": "PASSIVE", "desc": ["Placeholder description", "for passive boon 2."]},
]

P1_CX      = con.SELECT_P1_CX
P2_CX      = con.SELECT_P2_CX
PREVIEW_Y  = con.SELECT_PREVIEW_Y
PREVIEW_SZ = con.SELECT_PREVIEW_SIZE
HEAL_BOON_IDX = 0     # boon index that triggers the heal effect (Active Boon 1)

#TODO: TO MOVE IT TO CONSTANTS LATER
# boon grid dimensions
CELL_W = 150
CELL_H = 55
GAP    = 10
GRID_W = 2 * CELL_W + GAP
GRID_H = 2 * CELL_H + GAP
GRID_Y = con.SELECT_BTN_ROW1_Y

P1_GRID_X = P1_CX - GRID_W // 2
P2_GRID_X = P2_CX - GRID_W // 2


def make_boon_rects(grid_x):
    # 2x2 grid layout: [0] active1 | [1] active2 then [2] passive1 | [3] passive2
    return [
        pygame.Rect(grid_x,              GRID_Y,              CELL_W, CELL_H),
        pygame.Rect(grid_x + CELL_W+GAP, GRID_Y,              CELL_W, CELL_H),
        pygame.Rect(grid_x,              GRID_Y + CELL_H+GAP, CELL_W, CELL_H),
        pygame.Rect(grid_x + CELL_W+GAP, GRID_Y + CELL_H+GAP, CELL_W, CELL_H),
    ]


P1_BOON_RECTS = make_boon_rects(P1_GRID_X)
P2_BOON_RECTS = make_boon_rects(P2_GRID_X)


def remaining_center(rects, selected_idx):
    # average center of the 3 cells that are not selected, used to place info text
    others = [i for i in range(4) if i != selected_idx]
    cx = sum(rects[i].centerx for i in others) // 3
    cy = sum(rects[i].centery for i in others) // 3
    return cx, cy


class BoonScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock
        self.font   = pygame.font.SysFont(None, 24)
        self.big    = pygame.font.SysFont(None, 40)
        self.small  = pygame.font.SysFont(None, 20)

        self.p1_idx = con.p1_char_idx
        self.p2_idx = con.p2_char_idx

        self.previews = []
        for data in CHAR_DATA:
            if data is not None:
                sheet, steps = data
                self.previews.append(CharPreview(sheet, steps))
            else:
                self.previews.append(None)

        # heal effect
        self.heal_frames = load_magic_projectiles()["priest_heal"]  # loaded raw (100by100) then scaled at draw time
        # per player animation state ->  which frame, last frame time, wait flag, wait start time
        self.p1_heal = {"frame": 0, "time": 0, "waiting": False, "wait_start": 0}
        self.p2_heal = {"frame": 0, "time": 0, "waiting": False, "wait_start": 0}

        # viewing-> which boon info panel is open (None = grid view)
        # selected-> which boon the player confirmed (None = not yet)
        self.p1_viewing  = None
        self.p2_viewing  = None
        self.p1_selected = None
        self.p2_selected = None

        btn_y = GRID_Y + GRID_H + 8
        self.p1_confirm = pygame.Rect(P1_GRID_X,              btn_y, CELL_W, 35)
        self.p1_back    = pygame.Rect(P1_GRID_X + CELL_W+GAP, btn_y, CELL_W, 35)
        self.p2_confirm = pygame.Rect(P2_GRID_X,              btn_y, CELL_W, 35)
        self.p2_back    = pygame.Rect(P2_GRID_X + CELL_W+GAP, btn_y, CELL_W, 35)

        self.continue_btn = Button(
            con.SCREEN_WIDTH // 2 - 100, btn_y + 43, 200, 40,
            "CONTINUE", self.font, button_color=GREY,
        )

    # draw helpers

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

    def draw_player_boons(self, rects, grid_x, viewing, selected):
        if viewing is None:
            # 2x2 grid
            for i, boon in enumerate(BOONS):
                color = ACTIVE_COLOR if boon["type"] == "ACTIVE" else PASS_COLOR
                self.draw_button(rects[i], boon["name"], color, selected=(i == selected))

            # row labels to the left of the grid
            for label, ref_rect, color in [
                ("ACTIVE",  rects[0], (140, 210, 140)),
                ("PASSIVE", rects[2], (140, 150, 220)),
            ]:
                surf = self.small.render(label, True, color)
                self.screen.blit(surf, (grid_x - surf.get_width() - 6,
                                        ref_rect.centery - surf.get_height() // 2))
        else:
            # info panel
            pygame.draw.rect(self.screen, PANEL_COLOR,
                             pygame.Rect(grid_x, GRID_Y, GRID_W, GRID_H), border_radius=6)

            boon  = BOONS[viewing]
            pcx   = grid_x + GRID_W // 2       # panel horizontal centre
            pcy   = GRID_Y  + GRID_H // 2       # panel vertical centre

            # ACTIVE / PASSIVE label on top left corner of the panel
            type_s = self.small.render(boon["type"], True, (170, 200, 170))
            self.screen.blit(type_s, (grid_x + 6, GRID_Y + 5))

            # boon name and description centred inside the panel
            name_s = self.big.render(boon["name"], True, con.WHITE)
            self.screen.blit(name_s, name_s.get_rect(center=(pcx, pcy - 15)))
            for i, line in enumerate(boon["desc"]):
                s = self.font.render(line, True, (200, 200, 200))
                self.screen.blit(s, s.get_rect(center=(pcx, pcy + 12 + i * 20)))

    #text and button drawing is all done in this function below
    def draw(self):
        self.screen.fill(BG)

        self.draw_centered(self.big.render("PLAYER 1", True, con.SELECT_P1_LABEL_COLOR), P1_CX, con.SELECT_LABEL_Y)
        self.draw_centered(self.big.render("PLAYER 2", True, con.SELECT_P2_LABEL_COLOR), P2_CX, con.SELECT_LABEL_Y)

        self.draw_preview(self.p1_idx, P1_CX)
        self.draw_preview(self.p2_idx, P2_CX, flip=True)

        heal_y_offset = int(PREVIEW_SZ * 0.30)  # 30% of PREVIEW_SZ — tied to preview height, scales with it
        if self.p1_viewing == HEAL_BOON_IDX:
            draw_magic_effect(self.screen, self.heal_frames, self.p1_heal,
                              P1_CX, PREVIEW_Y + PREVIEW_SZ // 2, y_offset=heal_y_offset)
        if self.p2_viewing == HEAL_BOON_IDX:
            draw_magic_effect(self.screen, self.heal_frames, self.p2_heal,
                              P2_CX, PREVIEW_Y + PREVIEW_SZ // 2, y_offset=heal_y_offset)

        self.draw_player_boons(P1_BOON_RECTS, P1_GRID_X, self.p1_viewing, self.p1_selected)
        self.draw_player_boons(P2_BOON_RECTS, P2_GRID_X, self.p2_viewing, self.p2_selected)

        # player confirm/back only visible when pressed
        if self.p1_viewing is not None:
            self.draw_button(self.p1_confirm, "Confirm", GREEN)
            self.draw_button(self.p1_back,    "Back",    BACK_COLOR)
        if self.p2_viewing is not None:
            self.draw_button(self.p2_confirm, "Confirm", GREEN)
            self.draw_button(self.p2_back,    "Back",    BACK_COLOR)

        both_ready = self.p1_selected is not None and self.p2_selected is not None
        self.confirm_btn.button_color = GREEN if both_ready else GREY
        self.confirm_btn.draw(self.screen)
        appBright(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    if self.p1_viewing is not None or self.p2_viewing is not None:
                        self.p1_viewing = None
                        self.p2_viewing = None
                    else:
                        con.exit_sound.play()
                        return "play"
                if event.type == MOUSEBUTTONDOWN:
                    pos = event.pos

                    if self.p1_viewing is None:
                        for i in range(4):
                            if P1_BOON_RECTS[i].collidepoint(pos):
                                con.select_sound.play()
                                self.p1_viewing = i
                                if i == HEAL_BOON_IDX:
                                    self.p1_heal = {"frame": 0, "time": pygame.time.get_ticks(), "waiting": False, "wait_start": 0}
                    else:
                        if self.p1_confirm.collidepoint(pos):
                            con.select_sound.play()
                            self.p1_selected = self.p1_viewing
                            self.p1_viewing  = None
                        elif self.p1_back.collidepoint(pos):
                            con.exit_sound.play()
                            self.p1_viewing = None

                    if self.p2_viewing is None:
                        for i in range(4):
                            if P2_BOON_RECTS[i].collidepoint(pos):
                                con.select_sound.play()
                                self.p2_viewing = i
                                if i == HEAL_BOON_IDX:
                                    self.p2_heal = {"frame": 0, "time": pygame.time.get_ticks(), "waiting": False, "wait_start": 0}
                    else:
                        if self.p2_confirm.collidepoint(pos):
                            con.select_sound.play()
                            self.p2_selected = self.p2_viewing
                            self.p2_viewing  = None
                        elif self.p2_back.collidepoint(pos):
                            con.exit_sound.play()
                            self.p2_viewing = None

                    both_ready = self.p1_selected is not None and self.p2_selected is not None
                    if both_ready and self.confirm_btn.is_clicked((mx, my), True):
                        con.select_sound.play()
                        con.p1_boon = BOONS[self.p1_selected]
                        con.p2_boon = BOONS[self.p2_selected]
                        return "Map"

            self.draw()
            res.render_to_surface()
            self.clock.tick(60)
