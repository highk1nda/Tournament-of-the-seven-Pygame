import pygame

from src.modules.UI import constants as con
from src.modules.UI import CharDictionary as chardict
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems.scalemouse import scale_mouse
from src.modules.systems import res
from src.modules.UI.Button import Button
from src.modules.fighter.render import load_animation_frames, crop_and_scale_frames
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr

LABELS = ["Ser Edward", "Tyland", "Luna", "Rem", "Arland", "Venator"]

CHAR_DATA = chardict.CHARACTER_DATA


def make_button_rects(center_x):
    start_x = center_x - con.select_grid_width // 2
    return [
        pygame.Rect(
            start_x + (i % 3) * (con.select_butt_width + con.select_butt_gap),
            con.select_butt_row1_y if i < 3 else con.select_butt_row2_y,
            con.select_butt_width, con.select_butt_height,
        )
        for i in range(6)
    ]


# handles the idle render in the character preview box
class CharPreview:
    def __init__(self, char_data):
        idle_dict = {"IDLE": char_data["animations"]["IDLE"]}
        idle_frames  = load_animation_frames(idle_dict, char_data["size"], con.select_load_scale)["IDLE"]["ground"]
        self.frames  = crop_and_scale_frames(idle_frames, con.select_preview_size)

        self.frame_index = 0
        self.last_time = pygame.time.get_ticks()

        self.cooldown = char_data["animations"]["IDLE"]["cooldown"]
    def get_frame(self):
        now = pygame.time.get_ticks()
        if now - self.last_time > self.cooldown:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_time = now
        return self.frames[self.frame_index]


class SelectCharScreen():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font_medium = pygame.font.SysFont(None, 28)
        self.font_large = pygame.font.SysFont(None, 46)

        self.p1_btns = make_button_rects(con.select_p1_cx)
        self.p2_btns = make_button_rects(con.select_p2_cx)
        self.fight_btn = Button(con.select_fight_butt_x, con.select_fight_y, 200, 45, "CONTINUE",
                                self.font_medium, button_color=con.select_fight_butt_color)

        self.p1_idx = 0  # default: Knight
        self.p2_idx = 1  # default: Werebear

        self.previews = []
        for data in CHAR_DATA:
            if data is not None:
                self.previews.append(CharPreview(data))
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
        btn_color = con.butt_disabled_color if disabled else color
        pygame.draw.rect(self.screen, btn_color, rect, border_radius=5)
        if selected:
            pygame.draw.rect(self.screen, con.WHITE, rect, 3, border_radius=5)
        label_surf = self.font_medium.render(label, True, con.WHITE)
        self.screen.blit(label_surf, label_surf.get_rect(center=rect.center))

    def draw_preview(self, char_idx, center_x, flip=False):
        preview = self.previews[char_idx]
        if preview is not None:
            frame = preview.get_frame()
            if flip:
                frame = pygame.transform.flip(frame, True, False)
            self.screen.blit(frame, (center_x - frame.get_width() // 2,
                                     con.select_preview_y + (con.select_preview_size - frame.get_height()) // 2))

    def draw(self):
        #draw background
        self.screen.fill(con.select_bg_color)

        #draw player labels
        self.draw_centered(self.font_large.render("PLAYER 1", True, con.select_p1_label_color), con.select_p1_cx, con.select_label_y)
        self.draw_centered(self.font_large.render("PLAYER 2", True, con.select_p2_label_color), con.select_p2_cx, con.select_label_y)

        #draw character previews
        self.draw_preview(self.p1_idx, con.select_p1_cx)
        self.draw_preview(self.p2_idx, con.select_p2_cx, flip=True)

        #draw character select buttons for both players
        for i in range(6):
            disabled = CHAR_DATA[i] is None
            self.draw_button(self.p1_btns[i], LABELS[i], con.select_p1_butt_color,
                             selected=(i == self.p1_idx), disabled=disabled)
            self.draw_button(self.p2_btns[i], LABELS[i], con.select_p2_butt_color,
                             selected=(i == self.p2_idx), disabled=disabled)

        self.fight_btn.draw(self.screen)
        appBright(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = confscr(self.screen, self.clock, "Char").run()
                    return result

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        con.exit_sound.play()
                        return "Menu"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = scale_mouse()

                    # check character select buttons for both players
                    for i in range(6):
                        if self.p1_btns[i].collidepoint(mx, my):
                            if CHAR_DATA[i] is None:
                                con.ui_error_sound.play()
                            else:
                                con.select_sound.play()
                            self.select_char(1, i)
                        if self.p2_btns[i].collidepoint(mx, my):
                            if CHAR_DATA[i] is None:
                                con.ui_error_sound.play()
                            else:
                                con.select_sound.play()
                            self.select_char(2, i)

                    if self.fight_btn.is_clicked((mx, my), True):
                        con.select_sound.play()
                        con.p1_selected = CHAR_DATA[self.p1_idx]
                        con.p2_selected = CHAR_DATA[self.p2_idx]
                        con.p1_char_idx = self.p1_idx
                        con.p2_char_idx = self.p2_idx
                        return "Boon"

            self.draw()
            con.clock.tick(con.FPS)
            res.render_to_surface()
