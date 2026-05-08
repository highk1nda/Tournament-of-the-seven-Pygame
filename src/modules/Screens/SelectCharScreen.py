import pygame

from src.modules.UI import constants as con
from src.modules.UI import CharDictionary as chardict
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems.scalemouse import scale_mouse
from src.modules.systems import res
from src.modules.UI.Button import Button
from src.modules.fighter.render import load_animation_frames, crop_and_scale_frames
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr


CHAR_DATA = chardict.CHARACTER_DATA


def make_char_buttons(center_x, labels, color):
    # creates 6 character select Button objects in a 3x2 grid centered around center_x
    start_x = center_x - con.select_grid_width // 2
    return [
        Button(
            start_x + (i % 3) * (con.select_butt_width + con.select_butt_gap),
            con.select_butt_row1_y if i < 3 else con.select_butt_row2_y,
            con.select_butt_width, con.select_butt_height,
            labels[i], con.font_Small, color, SelectScreen=True
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
    def __init__(self, screen, clock, story=False):
        self.screen = screen
        self.clock = clock

        self.story = story

        self.p1_idx = 0  # default: Knight
        self.p2_idx = 1  # default: Werebear

        self.previews = []
        for data in CHAR_DATA:
            if data is not None:
                self.previews.append(CharPreview(data))
            else:
                self.previews.append(None)

        if con.storyEdwardComplete or con.storyTylandComplete or con.storyLunaComplete or con.storyRemComplete or con.storyArlandComplete:
            self.story_complete = True
        else:
            self.story_complete = False

        if self.story_complete == True:
            self.LABELS = ["Ser Edward", "Tyland", "Luna", "Rem", "Arland", "Venator"]
        else:
            self.LABELS = ["Ser Edward", "Tyland", "Luna", "Rem", "Arland", "???"]

        self.p1_btns = make_char_buttons(con.select_p1_cx, self.LABELS, con.select_p1_butt_color)
        if self.story != True:
            self.p2_btns = make_char_buttons(con.select_p2_cx, self.LABELS, con.select_p2_butt_color)
        self.fight_btn = Button(con.select_fight_butt_x, con.select_fight_y, 200, 45, "CONTINUE",
                                con.font_Small, button_color=con.select_fight_butt_color, SelectScreen=True)

        self.click = False

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

    def draw_preview(self, char_idx, center_x, flip=False):
        preview = self.previews[char_idx]
        if preview is not None:
            frame = preview.get_frame()
            if flip:
                frame = pygame.transform.flip(frame, True, False)
            self.screen.blit(frame, (center_x - frame.get_width() // 2,
                                     con.select_preview_y + (con.select_preview_size - frame.get_height()) // 2))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            result = confscr(self.screen, self.clock, "Char").run()
            return result
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                con.exit_sound.play()
                return "Menu"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click = True
        return None

    def update(self):
        if not self.click:
            return None

        self.click = False
        mx, my = scale_mouse()

        # check character select buttons for both players
        for i in range(6):
            if self.p1_btns[i].is_clicked((mx, my), True):
                if CHAR_DATA[i] is None or (i == 5 and not (con.storyEdwardComplete or con.storyTylandComplete
                                                            or con.storyLunaComplete or con.storyRemComplete
                                                            or con.storyArlandComplete)) or (self.story == True and i == 5):
                    con.ui_error_sound.play()
                else:
                    con.select_sound.play()
                    self.select_char(1, i)
            if self.story != True:
                if self.p2_btns[i].is_clicked((mx, my), True):
                    if CHAR_DATA[i] is None or (i == 5 and not (con.storyEdwardComplete or con.storyTylandComplete
                                                                or con.storyLunaComplete or con.storyRemComplete or con.storyArlandComplete)):
                        con.ui_error_sound.play()
                    else:
                        con.select_sound.play()
                        self.select_char(2, i)

        if self.fight_btn.is_clicked((mx, my), True):
            con.select_sound.play()
            con.p1_selected = CHAR_DATA[self.p1_idx]
            if self.story != True:
                con.p2_selected = CHAR_DATA[self.p2_idx]
            con.p1_char_idx = self.p1_idx
            con.p2_char_idx = self.p2_idx
            return "Boon"

        return None

    def draw(self):
        #draw background
        self.screen.fill(con.select_bg_color)

        #draw player labels
        self.draw_centered(con.font_Large.render("PLAYER 1", True, con.select_p1_label_color), con.select_p1_cx, con.select_label_y)
        if self.story != True:
            self.draw_centered(con.font_Large.render("PLAYER 2", True, con.select_p2_label_color), con.select_p2_cx, con.select_label_y)

        #draw character previews
        self.draw_preview(self.p1_idx, con.select_p1_cx)
        if self.story != True:
            self.draw_preview(self.p2_idx, con.select_p2_cx, flip=True)

        venatorDisabled = self.story or not self.story_complete

        #draw character select buttons for both players
        for i in range(6):
            disabled = venatorDisabled if i == 5 else (CHAR_DATA[i] is None)
            self.p1_btns[i].disabled = disabled
            self.p1_btns[i].selected = (i == self.p1_idx)
            self.p1_btns[i].draw(self.screen)
            if self.story != True:
                self.p2_btns[i].disabled = disabled
                self.p2_btns[i].selected = (i == self.p2_idx)
                self.p2_btns[i].draw(self.screen)

        self.fight_btn.draw(self.screen)
        appBright(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                result = self.handle_event(event)
                if result:
                    return result

            action = self.update()
            if action:
                return action

            self.draw()
            res.render_to_surface()
            con.clock.tick(con.FPS)
