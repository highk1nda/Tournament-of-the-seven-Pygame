import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems import res
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems.scalemouse import scale_mouse
from src.modules.UI.Button import Button
from src.modules.Screens.SelectCharScreen import CharPreview, CHAR_DATA
from src.modules.fighter.render import load_magic_projectiles, draw_magic_effect
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr

boons = [
    {
        "name": "Sub Zero",
        "type": "ACTIVE",
        "desc": [
            "Illuminates the ground below the opponent,",
            "then freezes them solid.",
            "Freeze: can't move/attack/use boon for 3s,",
            "+35% damage taken. Breaks on hit.",
        ],
    },
    {
        "name": "Scorching Ray",
        "type": "ACTIVE",
        "desc": [
            "A fireball falls from the sky at a 45° angle.",
            "Deals damage and applies Burn.",
            "Burn: moving while burning causes health loss.",
            "Duration: 3.5 seconds.",
        ],
    },
    {
        "name": "Area of Warding",
        "type": "ACTIVE",
        "desc": [
            "Creates a magical zone around you.",
            "Any opponent who enters",
            "continuously takes damage.",
            "Duration: 8 seconds.",
        ],
    },
    {
        "name": "Devil's Die",
        "type": "PASSIVE",
        "key": "devils_die",
        "desc": [
            "After losing a round, roll a 20-sided die.",
            "Above 10: revive — no life lost.",
            "Below 10: lose an extra life.",
            "Exactly 10: roll again.",
        ],
    },
    {
        "name": "Adrenaline",
        "type": "PASSIVE",
        "key": "adrenaline",
        "desc": [
            "-10% damage dealt.",
            "Each consecutive hit increases attack",
            "and movement speed (up to a cap).",
            "Taking damage resets all stacks.",
        ],
    },
    {
        "name": "Last Stand",
        "type": "PASSIVE",
        "key": "last_stand",
        "desc": [
            "While below 30% health,",
            "attack damage and movement speed",
            "increase by 30%.",
        ],
    },
]

BOON_PREVIEW_KEYS = [
    "wizard_attack01",  # Sub Zero
    "wizard_attack02",  # Scorching Ray
    "priest_heal",      # Area of Warding
    "priest_heal",      # Passive 1
    "priest_heal",      # Passive 2
    "priest_heal",      # Passive 3
]

ACTIVE_INDICES  = [i for i, b in enumerate(boons) if b["type"] == "ACTIVE"]
PASSIVE_INDICES = [i for i, b in enumerate(boons) if b["type"] == "PASSIVE"]

def make_boon_rects(grid_x):
    return [
        pygame.Rect(
            grid_x + (i % 2) * (con.boon_cell_width + con.select_butt_gap),
            con.select_butt_row1_y + (i // 2) * (con.boon_cell_height + con.select_butt_gap),
            con.boon_cell_width, con.boon_cell_height,
        )
        for i in range(6)
    ]


p1_boon_rects = make_boon_rects(con.boon_p1_grid_x)
p2_boon_rects = make_boon_rects(con.boon_p2_grid_x)


def fresh_anim():
    return {"frame": 0, "time": pygame.time.get_ticks(), "waiting": False, "wait_start": 0}


class BoonScreen:
    def __init__(self, screen, clock, story=False):
        self.screen = screen
        self.clock  = clock
        self.font   = pygame.font.SysFont(None, 24)
        self.big    = pygame.font.SysFont(None, 40)
        self.small  = pygame.font.SysFont(None, 20)

        self.story = story

        self.p1_idx = con.p1_char_idx
        self.p2_idx = con.p2_char_idx

        self.previews = []
        for data in CHAR_DATA:
            if data is not None:
                self.previews.append(CharPreview(data))
            else:
                self.previews.append(None)

        magic = load_magic_projectiles()
        self.boon_preview_frames = [magic[k] for k in BOON_PREVIEW_KEYS]

        self.p1_anim = [fresh_anim() for _ in range(6)]
        self.p2_anim = [fresh_anim() for _ in range(6)]

        self.p1_viewing = None
        self.p2_viewing = None

        self.p1_active_sel  = None
        self.p1_passive_sel = None
        self.p2_active_sel  = None
        self.p2_passive_sel = None
 

        btn_y = con.select_butt_row1_y + con.boon_grid_height + 8
        self.p1_confirm = pygame.Rect(con.boon_p1_grid_x,
                                      btn_y, con.boon_cell_width, 35)
        self.p1_back    = pygame.Rect(con.boon_p1_grid_x + con.boon_cell_width + con.select_butt_gap,
                                      btn_y, con.boon_cell_width, 35)
        self.p2_confirm = pygame.Rect(con.boon_p2_grid_x,
                                        btn_y, con.boon_cell_width, 35)
        self.p2_back    = pygame.Rect(con.boon_p2_grid_x + con.boon_cell_width + con.select_butt_gap,
                                        btn_y, con.boon_cell_width, 35)

        self.continue_btn = Button(
            con.SCREEN_WIDTH // 2 - 100, btn_y + 43, 200, 40,
            "CONTINUE", self.font, button_color=con.butt_disabled_color,
        )

    def p1_ready(self):
        return self.p1_active_sel is not None and self.p1_passive_sel is not None
 
    def p2_ready(self):
        return self.p2_active_sel is not None and self.p2_passive_sel is not None
    
    def both_ready(self):
        if self.story:
            return self.p1_ready()
        return self.p1_ready() and self.p2_ready()
    
    def draw_centered(self, surface, center_x, y):
        self.screen.blit(surface, (center_x - surface.get_width() // 2, y))

    def draw_button(self, rect, label, color, border_color=None, border_width=3):
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        if border_color is not None:
            pygame.draw.rect(self.screen, border_color, rect, border_width, border_radius=5)
        s = con.font_Small.render(label, True, con.WHITE)
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

    def draw_player_boons(self, rects, grid_x, viewing, active_sel, passive_sel):
        if viewing is None:
            for i, boon in enumerate(boons):
                base_color = con.boon_active_color if boon["type"] == "ACTIVE" else con.select_p2_butt_color
                
                if i == active_sel:
                    border_color = con.YELLOW
                elif i == passive_sel:
                    border_color = con.BLUE
                else:
                    border_color = None
                
                self.draw_button(rects[i], boon["name"], base_color, border_color)

            # row labels on the left: ACTIVE for row 0, PASSIVE for row 2
            for label, ref_rect, color in [
                ("ACTIVE",  rects[0], (140, 210, 140)),
                ("PASSIVE", rects[4], (140, 150, 220)),
            ]:
                surf = self.small.render(label, True, color)
                self.screen.blit(surf, (grid_x - surf.get_width() - 6,
                                        ref_rect.centery - surf.get_height() // 2))
                
            # selection hints under the grid
            hints = []
            if active_sel is None:
                hints.append("choose an Active boon")
            if passive_sel is None:
                hints.append("choose a Passive boon")
            if hints:
                hint_surf = self.small.render("  ·  ".join(hints), True, (160, 160, 160))
                hint_y = rects[4].bottom + 6
                self.screen.blit(hint_surf, (grid_x + con.boon_grid_width // 2 - hint_surf.get_width() // 2,
                                             hint_y))
                
        else:
            pygame.draw.rect(self.screen, con.boon_panel_color,
                             pygame.Rect(grid_x, con.select_butt_row1_y,
                                         con.boon_grid_width, con.boon_grid_height),
                             border_radius=6)
            boon = boons[viewing]
            pcx = grid_x + con.boon_grid_width // 2
            pcy = con.select_butt_row1_y + con.boon_grid_height // 2

            if boon["type"] == "ACTIVE":
                type_color = (140, 210, 140)  
            else:
                type_color = (140, 150, 220)
            type_s = self.small.render(boon["type"], True, type_color)
            self.screen.blit(type_s, (grid_x + 6, con.select_butt_row1_y + 5))

            name_s = self.big.render(boon["name"], True, con.WHITE)
            self.screen.blit(name_s, name_s.get_rect(center=(pcx, pcy - 25)))
            for i, line in enumerate(boon["desc"]):
                s = self.font.render(line, True, (200, 200, 200))
                self.screen.blit(s, s.get_rect(center=(pcx, pcy + 5 + i * 20)))

    def draw(self):
        self.screen.fill(con.select_bg_color)

        self.draw_centered(self.big.render("PLAYER 1", True, con.select_p1_label_color),
                           con.select_p1_cx, con.select_label_y)
        if self.story != True:
            self.draw_centered(self.big.render("PLAYER 2", True, con.select_p2_label_color),
                               con.select_p2_cx, con.select_label_y)

        self.draw_preview(self.p1_idx, con.select_p1_cx)
        if self.story != True:
            self.draw_preview(self.p2_idx, con.select_p2_cx, flip=True)

        # boon preview animation over character portrait when viewing a boon
        heal_y_offset = int(con.select_preview_size * 0.30)
        preview_cy = con.select_preview_y + con.select_preview_size // 2
        if self.p1_viewing is not None:
            draw_magic_effect(self.screen,
                              self.boon_preview_frames[self.p1_viewing],
                              self.p1_anim[self.p1_viewing],
                              con.select_p1_cx, preview_cy,
                              y_offset=heal_y_offset)
        if self.story != True:
            if self.p2_viewing is not None:
                draw_magic_effect(self.screen,
                                  self.boon_preview_frames[self.p2_viewing],
                                  self.p2_anim[self.p2_viewing],
                                  con.select_p2_cx, preview_cy,
                                  y_offset=heal_y_offset)

        self.draw_player_boons(p1_boon_rects, con.boon_p1_grid_x,
                               self.p1_viewing, self.p1_active_sel, self.p1_passive_sel)
        if self.story != True:
            self.draw_player_boons(p2_boon_rects, con.boon_p2_grid_x,
                                   self.p2_viewing, self.p2_active_sel, self.p2_passive_sel)

        if self.p1_viewing is not None:
            self.draw_button(self.p1_confirm, "Confirm", con.select_fight_butt_color)
            self.draw_button(self.p1_back,    "Back",    con.boon_back_color)
        if self.story != True:
            if self.p2_viewing is not None:
                self.draw_button(self.p2_confirm, "Confirm", con.select_fight_butt_color)
                self.draw_button(self.p2_back,    "Back",    con.boon_back_color)

        self.continue_btn.button_color = (
            con.select_fight_butt_color if self.both_ready() else con.butt_disabled_color
        )
        self.continue_btn.draw(self.screen)
 
        # hint under continue button
        if not self.both_ready():
            hint = self.small.render(
                "Each player must select 1 Active  +  1 Passive boon",
                True, (120, 120, 120),
            )
            self.screen.blit(hint, (
                con.SCREEN_WIDTH // 2 - hint.get_width() // 2,
                self.continue_btn.rect.bottom + 6,
            ))
 
        appBright(self.screen)

    def run(self):
        while True:
            mx, my = scale_mouse()
            for event in pygame.event.get():
                if event.type == QUIT:
                    result = confscr(self.screen, self.clock, "Boon").run()
                    return result
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    if self.p1_viewing is not None or (not self.story and self.p2_viewing is not None):
                            self.p1_viewing = None
                            if self.story != True:
                                self.p2_viewing = None
                    else:
                        con.exit_sound.play()
                        return "Char"
                    
                if event.type == MOUSEBUTTONDOWN:
                    mx, my = scale_mouse()

                    self.handle_click_p1(mx, my)
                    if self.story != True:
                        self.handle_click_p2(mx, my)
 
                    # Continue
                    if self.both_ready() and self.continue_btn.is_clicked((mx, my), True):
                        con.select_sound.play()

                        con.p1_active_boon = boons[self.p1_active_sel]
                        con.p1_passive_boon = boons[self.p1_passive_sel]
                        if not self.story:
                            con.p2_active_boon = boons[self.p2_active_sel]
                            con.p2_passive_boon = boons[self.p2_passive_sel]
        
                        if self.story != True:
                            return "Map"
                        else:
                            return "Textcrawl"
 
            self.draw()
            res.render_to_surface()
            self.clock.tick(con.FPS)

    def handle_click_p1(self, mx, my):
        if self.p1_viewing is None:
            for i in range(6):
                if p1_boon_rects[i].collidepoint(mx, my):
                    con.select_sound.play()
                    self.p1_viewing = i
                    self.p1_anim[i] = fresh_anim()
                    return
        else:
            if self.p1_confirm.collidepoint(mx, my):
                con.select_sound.play()
                self.confirm_boon("p1", self.p1_viewing)
                self.p1_viewing = None
            elif self.p1_back.collidepoint(mx, my):
                con.exit_sound.play()
                self.p1_viewing = None
 
    def handle_click_p2(self, mx, my):
        if self.p2_viewing is None:
            for i in range(6):
                if p2_boon_rects[i].collidepoint(mx, my):
                    con.select_sound.play()
                    self.p2_viewing = i
                    self.p2_anim[i] = fresh_anim()
                    return
        else:
            if self.p2_confirm.collidepoint(mx, my):
                con.select_sound.play()
                self.confirm_boon("p2", self.p2_viewing)
                self.p2_viewing = None
            elif self.p2_back.collidepoint(mx, my):
                con.exit_sound.play()
                self.p2_viewing = None
 
    def confirm_boon(self, player, idx):

        boon = boons[idx]
        if boon["type"] == "ACTIVE":
            if player == "p1":
                self.p1_active_sel = idx
            else:
                self.p2_active_sel = idx
        else:  # PASSIVE
            if player == "p1":
                self.p1_passive_sel = idx
            else:
                self.p2_passive_sel = idx

        