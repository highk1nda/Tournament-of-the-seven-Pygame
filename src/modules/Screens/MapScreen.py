import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems import res
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems.scalemouse import scale_mouse
from src.modules.Screens.SelectCharScreen import CharPreview, CHAR_DATA

MAPS = [
    {"name": "Forest",  "path": "assets/Colleseum.png",  "key": "map1"},
    {"name": "Fields",  "path": "assets/Heaven.png",  "key": "map2"},
]


class MapScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock  = clock
        self.font   = pygame.font.SysFont(None, 36)
        self.big    = pygame.font.SysFont(None, 52)
        self.small  = pygame.font.SysFont(None, 28)

        self.map_idx = 0

        self.map_images = [
            pygame.transform.scale(
                pygame.image.load(m["path"]).convert(),
                (con.map_preview_width, con.map_preview_height)
            )
            for m in MAPS
        ]

        self.p1_idx = con.p1_char_idx
        self.p2_idx = con.p2_char_idx

        self.previews = []
        for data in CHAR_DATA:
            if data is not None:
                sheet, steps = data
                self.previews.append(CharPreview(sheet, steps))
            else:
                self.previews.append(None)

        self.prev_rect  = pygame.Rect(con.map_cx - con.map_fight_butt_width // 2 - con.map_nav_butt_width - 20, con.map_nav_y, con.map_nav_butt_width,   con.map_nav_butt_height)
        self.fight_rect = pygame.Rect(con.map_cx - con.map_fight_butt_width // 2,                              con.map_nav_y, con.map_fight_butt_width, con.map_fight_butt_height)
        self.next_rect  = pygame.Rect(con.map_cx + con.map_fight_butt_width // 2 + 20,                         con.map_nav_y, con.map_nav_butt_width,   con.map_nav_butt_height)

    def draw_centered(self, surface, center_x, y):
        self.screen.blit(surface, (center_x - surface.get_width() // 2, y))

    def draw_button(self, rect, label, color):
        pygame.draw.rect(self.screen, color, rect, border_radius=6)
        s = self.font.render(label, True, con.WHITE)
        self.screen.blit(s, (rect.centerx - s.get_width() // 2,
                             rect.centery - s.get_height() // 2))

    def draw_char_on_preview(self, char_idx, rel_x, flip=False):
        preview = self.previews[char_idx]
        if preview is None:
            return
        frame = preview.get_frame()
        if flip:
            frame = pygame.transform.flip(frame, True, False)
        self.screen.blit(frame, (con.map_preview_x + rel_x - frame.get_width()  // 2,
                                 con.map_preview_y + con.map_preview_height - frame.get_height() - 10))

    def draw(self):
        self.screen.fill(con.select_bg_color)

        self.draw_centered(self.big.render("SELECT MAP", True, con.WHITE), con.map_cx, 22)

        self.screen.blit(self.map_images[self.map_idx], (con.map_preview_x, con.map_preview_y))

        self.draw_char_on_preview(self.p1_idx, rel_x=con.map_char_rel_x)
        self.draw_char_on_preview(self.p2_idx, rel_x=con.map_preview_width - con.map_char_rel_x, flip=True)

        self.draw_centered(self.small.render(MAPS[self.map_idx]["name"], True, con.WHITE), con.map_cx, con.map_preview_y + con.map_preview_height + 6)

        self.draw_button(self.prev_rect,  "< Previous", con.butt_disabled_color)
        self.draw_button(self.fight_rect, "FIGHT",      con.select_fight_butt_color)
        self.draw_button(self.next_rect,  "Next >",     con.butt_disabled_color)
        appBright(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "quit"
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    return "Boon"
                if event.type == MOUSEBUTTONDOWN:
                    mx, my = scale_mouse()
                    if self.prev_rect.collidepoint(mx, my):
                        con.select_sound.play()
                        self.map_idx = (self.map_idx - 1) % len(MAPS)
                    elif self.next_rect.collidepoint(mx, my):
                        con.select_sound.play()
                        self.map_idx = (self.map_idx + 1) % len(MAPS)
                    elif self.fight_rect.collidepoint(mx, my):
                        con.select_sound.play()
                        con.selected_map = MAPS[self.map_idx]["key"]
                        return "Fight"

            self.draw()
            res.render_to_surface()
            self.clock.tick(60)
