import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems import res
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems.scalemouse import scale_mouse
from src.modules.UI.Button import Button
from src.modules.Screens.SelectCharScreen import CharPreview, CHAR_DATA
from src.modules.fighter.render import load_magic_projectiles, draw_magic_effect

# placeholder names and descriptions for now
boons = [
    {"name": "Active Boon 1",  "type": "ACTIVE",  "desc": ["Placeholder description", "for active boon 1."]},
    {"name": "Active Boon 2",  "type": "ACTIVE",  "desc": ["Placeholder description", "for active boon 2."]},
    {"name": "Passive Boon 1", "type": "PASSIVE", "desc": ["Placeholder description", "for passive boon 1."]},
    {"name": "Passive Boon 2", "type": "PASSIVE", "desc": ["Placeholder description", "for passive boon 2."]},
]

heal_boon_idx = 0     # boon index that triggers the heal effect (Active Boon 1)


def make_boon_rects(grid_x):
    # 2x2 grid layout: [0] active1 | [1] active2 then [2] passive1 | [3] passive2
    return [
        pygame.Rect(grid_x,                                        con.select_butt_row1_y,                                          con.boon_cell_width, con.boon_cell_height),
        pygame.Rect(grid_x + con.boon_cell_width+con.select_butt_gap, con.select_butt_row1_y,                                       con.boon_cell_width, con.boon_cell_height),
        pygame.Rect(grid_x,                                        con.select_butt_row1_y + con.boon_cell_height+con.select_butt_gap, con.boon_cell_width, con.boon_cell_height),
        pygame.Rect(grid_x + con.boon_cell_width+con.select_butt_gap, con.select_butt_row1_y + con.boon_cell_height+con.select_butt_gap, con.boon_cell_width, con.boon_cell_height),
    ]


p1_boon_rects = make_boon_rects(con.boon_p1_grid_x)
p2_boon_rects = make_boon_rects(con.boon_p2_grid_x)


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

        btn_y = con.select_butt_row1_y + con.boon_grid_height + 8
        self.p1_confirm = pygame.Rect(con.boon_p1_grid_x,                                        btn_y, con.boon_cell_width, 35)
        self.p1_back    = pygame.Rect(con.boon_p1_grid_x + con.boon_cell_width+con.select_butt_gap, btn_y, con.boon_cell_width, 35)
        self.p2_confirm = pygame.Rect(con.boon_p2_grid_x,                                        btn_y, con.boon_cell_width, 35)
        self.p2_back    = pygame.Rect(con.boon_p2_grid_x + con.boon_cell_width+con.select_butt_gap, btn_y, con.boon_cell_width, 35)

        self.continue_btn = Button(
            con.SCREEN_WIDTH // 2 - 100, btn_y + 43, 200, 40,
            "CONTINUE", self.font, button_color=con.butt_disabled_color,
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
                                 con.select_preview_y + (con.select_preview_size - frame.get_height()) // 2))

    def draw_player_boons(self, rects, grid_x, viewing, selected):
        if viewing is None:
            # 2x2 grid
            for i, boon in enumerate(boons):
                color = con.boon_active_color if boon["type"] == "ACTIVE" else con.select_p2_butt_color
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
            pygame.draw.rect(self.screen, con.boon_panel_color,
                             pygame.Rect(grid_x, con.select_butt_row1_y, con.boon_grid_width, con.boon_grid_height), border_radius=6)

            boon = boons[viewing]
            pcx  = grid_x + con.boon_grid_width // 2                    # panel horizontal centre
            pcy  = con.select_butt_row1_y + con.boon_grid_height // 2   # panel vertical centre

            # ACTIVE / PASSIVE label on top left corner of the panel
            type_s = self.small.render(boon["type"], True, (170, 200, 170))
            self.screen.blit(type_s, (grid_x + 6, con.select_butt_row1_y + 5))

            # boon name and description centred inside the panel
            name_s = self.big.render(boon["name"], True, con.WHITE)
            self.screen.blit(name_s, name_s.get_rect(center=(pcx, pcy - 15)))
            for i, line in enumerate(boon["desc"]):
                s = self.font.render(line, True, (200, 200, 200))
                self.screen.blit(s, s.get_rect(center=(pcx, pcy + 12 + i * 20)))

    #text and button drawing is all done in this function below
    def draw(self):
        self.screen.fill(con.select_bg_color)

        self.draw_centered(self.big.render("PLAYER 1", True, con.select_p1_label_color), con.select_p1_cx, con.select_label_y)
        self.draw_centered(self.big.render("PLAYER 2", True, con.select_p2_label_color), con.select_p2_cx, con.select_label_y)

        self.draw_preview(self.p1_idx, con.select_p1_cx)
        self.draw_preview(self.p2_idx, con.select_p2_cx, flip=True)

        heal_y_offset = int(con.select_preview_size * 0.30)  # 30% of select_preview_size — tied to preview height, scales with it
        if self.p1_viewing == heal_boon_idx:
            draw_magic_effect(self.screen, self.heal_frames, self.p1_heal,
                              con.select_p1_cx, con.select_preview_y + con.select_preview_size // 2, y_offset=heal_y_offset)
        if self.p2_viewing == heal_boon_idx:
            draw_magic_effect(self.screen, self.heal_frames, self.p2_heal,
                              con.select_p2_cx, con.select_preview_y + con.select_preview_size // 2, y_offset=heal_y_offset)

        self.draw_player_boons(p1_boon_rects, con.boon_p1_grid_x, self.p1_viewing, self.p1_selected)
        self.draw_player_boons(p2_boon_rects, con.boon_p2_grid_x, self.p2_viewing, self.p2_selected)

        # player confirm/back only visible when pressed
        if self.p1_viewing is not None:
            self.draw_button(self.p1_confirm, "Confirm", con.select_fight_butt_color)
            self.draw_button(self.p1_back,    "Back",    con.boon_back_color)
        if self.p2_viewing is not None:
            self.draw_button(self.p2_confirm, "Confirm", con.select_fight_butt_color)
            self.draw_button(self.p2_back,    "Back",    con.boon_back_color)

        both_ready = self.p1_selected is not None and self.p2_selected is not None
        self.continue_btn.button_color = con.select_fight_butt_color if both_ready else con.butt_disabled_color
        self.continue_btn.draw(self.screen)
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
                    mx, my = scale_mouse()

                    if self.p1_viewing is None:
                        for i in range(4):
                            if p1_boon_rects[i].collidepoint(mx, my):
                                con.select_sound.play()
                                self.p1_viewing = i
                                if i == heal_boon_idx:
                                    self.p1_heal = {"frame": 0, "time": pygame.time.get_ticks(), "waiting": False, "wait_start": 0}
                    else:
                        if self.p1_confirm.collidepoint(mx, my):
                            con.select_sound.play()
                            self.p1_selected = self.p1_viewing
                            self.p1_viewing  = None
                        elif self.p1_back.collidepoint(mx, my):
                            con.exit_sound.play()
                            self.p1_viewing = None

                    if self.p2_viewing is None:
                        for i in range(4):
                            if p2_boon_rects[i].collidepoint(mx, my):
                                con.select_sound.play()
                                self.p2_viewing = i
                                if i == heal_boon_idx:
                                    self.p2_heal = {"frame": 0, "time": pygame.time.get_ticks(), "waiting": False, "wait_start": 0}
                    else:
                        if self.p2_confirm.collidepoint(mx, my):
                            con.select_sound.play()
                            self.p2_selected = self.p2_viewing
                            self.p2_viewing  = None
                        elif self.p2_back.collidepoint(mx, my):
                            con.exit_sound.play()
                            self.p2_viewing = None

                    both_ready = self.p1_selected is not None and self.p2_selected is not None
                    if both_ready and self.continue_btn.is_clicked((mx, my), True):
                        con.select_sound.play()
                        con.p1_boon = boons[self.p1_selected]
                        con.p2_boon = boons[self.p2_selected]
                        return "Map"

            self.draw()
            res.render_to_surface()
            self.clock.tick(60)
