import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems import res
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems.scalemouse import scale_mouse
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr


levels = [
    (1, "LEVEL 1"),
    (2, "LEVEL 2"),
    (3, "ANNIHILATION"),
]


class CPUScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock

        self.selected = con.cpu_level if con.cpu_enabled else 1

        btn_w   = 160
        btn_h   = 48
        btn_gap = 16
        total_w = len(levels) * btn_w + (len(levels) - 1) * btn_gap
        btn_y   = 260

        cx = con.SCREEN_WIDTH // 2
        start_x = cx - total_w // 2
        self.level_btns = [
            pygame.Rect(start_x + i * (btn_w + btn_gap), btn_y, btn_w, btn_h)
            for i in range(len(levels))
        ]

        fight_w, fight_h = 200, 44
        self.fight_btn = pygame.Rect(cx - fight_w // 2, btn_y + btn_h + 40, fight_w, fight_h)

    def draw_button(self, rect, label, color, selected=False):
        pygame.draw.rect(self.screen, color, rect, border_radius=5)
        if selected:
            pygame.draw.rect(self.screen, con.WHITE, rect, 3, border_radius=5)
        label_surf = con.font_Small.render(label, True, con.WHITE)
        self.screen.blit(label_surf, label_surf.get_rect(center=rect.center))

    def draw(self):
        self.screen.fill(con.select_bg_color)

        cx = con.SCREEN_WIDTH // 2
        title = con.font_Large.render("CPU MODE", True, con.WHITE)
        self.screen.blit(title, title.get_rect(centerx=cx, y=22))
        sub = con.font_Small.render("Select enemy difficulty", True, (180, 180, 180))
        self.screen.blit(sub, sub.get_rect(centerx=cx, y=80))

        for i, (lvl, label) in enumerate(levels):
            active = self.selected == lvl
            color  = con.select_fight_butt_color if active else con.butt_disabled_color
            self.draw_button(self.level_btns[i], label, color, selected=active)

        self.draw_button(self.fight_btn, "FIGHT", con.select_fight_butt_color)

        appBright(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    result = confscr(self.screen, self.clock, "CPU").run()
                    return result
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    return "Map"
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = scale_mouse()

                    for i, (lvl, _) in enumerate(levels):
                        if self.level_btns[i].collidepoint(mx, my):
                            con.select_sound.play()
                            self.selected = lvl

                    if self.fight_btn.collidepoint(mx, my):
                        con.select_sound.play()
                        con.cpu_enabled = True
                        con.cpu_level   = self.selected
                        return "Fight"

            self.draw()
            res.render_to_surface()
            self.clock.tick(con.FPS)
