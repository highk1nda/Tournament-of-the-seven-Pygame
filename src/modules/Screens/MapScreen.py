import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems import res 
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems.scalemouse import scale_mouse
from src.modules.Screens.SelectCharScreen import CharPreview, CHAR_DATA
#TODO: improve constants calling
BG    = con.SELECT_BG_COLOR
GREEN = con.SELECT_FIGHT_BTN_COLOR
GREY  = con.BUTTON_DISABLED_COLOR

MAPS = [
    {"name": "Forest",  "path": "assets/Colleseum.png",  "key": "map1"},
    {"name": "Fields",  "path": "assets/Heaven.png",  "key": "map2"},
]

PREVIEW_W   = con.MAP_PREVIEW_W
PREVIEW_H   = con.MAP_PREVIEW_H
PREVIEW_X   = con.MAP_PREVIEW_X
PREVIEW_Y   = con.MAP_PREVIEW_Y
NAV_BTN_W   = con.MAP_NAV_BTN_W
NAV_BTN_H   = con.MAP_NAV_BTN_H
NAV_Y       = con.MAP_NAV_Y
FIGHT_BTN_W = con.MAP_FIGHT_BTN_W
FIGHT_BTN_H = con.MAP_FIGHT_BTN_H
CX          = con.MAP_CX


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
                (PREVIEW_W, PREVIEW_H)
            )
            for m in MAPS
        ]

        self.p1_idx = con.p1_char_idx
        self.p2_idx = con.p2_char_idx

        self.previews = []
        for data in CHAR_DATA:
            if data is not None:
                self.previews.append(CharPreview(data))
            else:
                self.previews.append(None)

        self.prev_rect  = pygame.Rect(CX - FIGHT_BTN_W // 2 - NAV_BTN_W - 20, NAV_Y, NAV_BTN_W,   NAV_BTN_H)
        self.fight_rect = pygame.Rect(CX - FIGHT_BTN_W // 2,                   NAV_Y, FIGHT_BTN_W, FIGHT_BTN_H)
        self.next_rect  = pygame.Rect(CX + FIGHT_BTN_W // 2 + 20,              NAV_Y, NAV_BTN_W,   NAV_BTN_H)

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
        self.screen.blit(frame, (PREVIEW_X + rel_x - frame.get_width()  // 2,
                                 PREVIEW_Y + PREVIEW_H - frame.get_height() - 10))

    def draw(self):
        self.screen.fill(BG)

        self.draw_centered(self.big.render("SELECT MAP", True, con.WHITE), CX, 22)

        self.screen.blit(self.map_images[self.map_idx], (PREVIEW_X, PREVIEW_Y))

        self.draw_char_on_preview(self.p1_idx, rel_x=120)
        self.draw_char_on_preview(self.p2_idx, rel_x=PREVIEW_W - 120, flip=True)

        self.draw_centered(self.small.render(MAPS[self.map_idx]["name"], True, con.WHITE), CX, PREVIEW_Y + PREVIEW_H + 6)

        self.draw_button(self.prev_rect,  "< Previous", GREY)
        self.draw_button(self.fight_rect, "FIGHT",      GREEN)
        self.draw_button(self.next_rect,  "Next >",     GREY)
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
