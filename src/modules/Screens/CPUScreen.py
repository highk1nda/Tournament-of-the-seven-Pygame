import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems import res
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems.scalemouse import scale_mouse
from src.modules.UI.Button import Button
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr


levels = [
    (1, "LEVEL 1"),
    (2, "LEVEL 2"),
    (3, "ANNIHILATION"),
]


class CPUScreen:
    def __init__(self, screen, clock, story=False):
        self.screen = screen
        self.clock  = clock
        self.story = story

        self.selected = con.cpu_level if con.cpu_enabled else 1
        self.click = False

        btn_w   = 160
        btn_h   = 48
        btn_gap = 16
        total_w = len(levels) * btn_w + (len(levels) - 1) * btn_gap
        btn_y   = 260

        cx = con.SCREEN_WIDTH // 2
        start_x = cx - total_w // 2
        self.level_btns = [
            Button(start_x + i * (btn_w + btn_gap), btn_y, btn_w, btn_h,
                   label, con.font_Small, con.butt_disabled_color, SelectScreen=True)
            for i, (lvl, label) in enumerate(levels)
        ]

        fight_w, fight_h = 200, 44
        self.fight_btn = Button(cx - fight_w // 2, btn_y + btn_h + 40, fight_w, fight_h,
                                "FIGHT", con.font_Small, con.select_fight_butt_color, SelectScreen=True)

    def handle_event(self, event):
        if event.type == QUIT:
            result = confscr(self.screen, self.clock, "CPU").run()
            return result
        if event.type == KEYDOWN and event.key == K_ESCAPE:
            if self.story == True:
                return "Boon"
            else:
                return "Map"
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            self.click = True
        return None

    def update(self):
        if not self.click:
            return None

        self.click = False
        mx, my = scale_mouse()

        for i, (lvl, _) in enumerate(levels):
            if self.level_btns[i].is_clicked((mx, my), True):
                con.select_sound.play()
                self.selected = lvl
                return None

        if self.fight_btn.is_clicked((mx, my), True):
            con.select_sound.play()
            con.cpu_enabled = True
            con.cpu_level   = self.selected
            if self.story == True:
                return "Textcrawl"
            else:
                return "Fight"

        return None

    def draw(self):
        self.screen.fill(con.select_bg_color)

        cx = con.SCREEN_WIDTH // 2
        title = con.font_Large.render("CPU MODE", True, con.WHITE)
        self.screen.blit(title, title.get_rect(centerx=cx, y=22))
        sub = con.font_Small.render("Select enemy difficulty", True, (180, 180, 180))
        self.screen.blit(sub, sub.get_rect(centerx=cx, y=80))

        for i, (lvl, _) in enumerate(levels):
            active = self.selected == lvl
            self.level_btns[i].button_color = con.select_fight_butt_color if active else con.butt_disabled_color
            self.level_btns[i].selected = active
            self.level_btns[i].draw(self.screen)

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
            self.clock.tick(con.FPS)
