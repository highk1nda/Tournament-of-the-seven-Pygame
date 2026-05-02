import pygame
from src.modules.fighter.render import load_animation_frames
from src.modules.UI import constants as con
from src.modules.systems.cpu import CPUController

RED   = (160, 45, 45)
BLUE  = (45, 70, 160)
WHITE = (255, 255, 255)
GREEN = (45, 160, 75)

font = None

def get_font():
    global font
    if font is None:
        font = pygame.font.SysFont(None, 22)
    return font

CHAR_SHEETS = [
    (con.knight_sheet,          con.KNIGHT_ANIMATION_STEPS),
    (con.werebear_sheet,        con.WEREBEAR_ANIMATION_STEPS),
    (con.wizard_sheet,          con.WIZARD_ANIMATION_STEPS),
    None,
    None,
    (con.knight_templar_sheet,  con.KNIGHT_TEMPLAR_ANIMATION_STEPS),
]

#debug thingy to quickly switch characters during development, gonna be removed later (or maybe not, who knows)
class DebugPopup:
    def __init__(self, fightscreen):
        self.fs = fightscreen
        self.visible = False
        W, H = 340, 330
        self.x = (1000 - W) // 2
        self.y = (600 - H) // 2
        self.bg = pygame.Surface((W, H))
        self.bg.fill((25, 25, 25))

        btn_w, btn_h, gap = 95, 36, 8
        start_x = (W - (3 * btn_w + 2 * gap)) // 2
        self.labels = ["Knight", "Werebear", "Wizard", "Minotaur", "Archer", "K.Templar"]

        self.p1 = [pygame.Rect(self.x + start_x + (i%3)*(btn_w+gap), self.y + 40  + (i//3)*(btn_h+gap), btn_w, btn_h) for i in range(6)]
        self.p2 = [pygame.Rect(self.x + start_x + (i%3)*(btn_w+gap), self.y + 170 + (i//3)*(btn_h+gap), btn_w, btn_h) for i in range(6)]
        self.btn_w, self.btn_h = btn_w, btn_h

        cpu_btn_w, cpu_btn_h, cpu_gap = 95, 30, 8
        cpu_total = 3 * cpu_btn_w + 2 * cpu_gap
        cpu_start = self.x + (W - cpu_total) // 2
        self.cpu1_btn = pygame.Rect(cpu_start,                           self.y + 288, cpu_btn_w, cpu_btn_h)
        self.cpu2_btn = pygame.Rect(cpu_start +   cpu_btn_w + cpu_gap,   self.y + 288, cpu_btn_w, cpu_btn_h)
        self.cpu3_btn = pygame.Rect(cpu_start + 2*(cpu_btn_w + cpu_gap), self.y + 288, cpu_btn_w, cpu_btn_h)

        self.key_step      = 0
        self.key_time      = 0
        self.sounds_swapped = False

    def reload(self, fighter, sheet, steps):
        fighter.animation_list = load_animation_frames(sheet, con.CHARACTER_DATA[0], con.CHARACTER_DATA[1], steps)
        fighter.action = 0
        fighter.frame_index = 0

    def swap_sounds(self):
        sound_paths = [("death", "assets/sfx/death2.mp3"),
                       ("hit",   "assets/sfx/hit2.mp3"),
                       ("dash",  "assets/sfx/jump.mp3")]
        self.sounds_swapped = not self.sounds_swapped
        for fighter in (self.fs.knight, self.fs.werebear):
            for key, path in sound_paths:
                if self.sounds_swapped:
                    fighter.sounds[key + "_"] = fighter.sounds[key]
                    fighter.sounds[key] = pygame.mixer.Sound(path)
                else:
                    fighter.sounds[key] = fighter.sounds.pop(key + "_", fighter.sounds[key])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.visible = not self.visible
        if event.type == pygame.KEYDOWN:
            now = pygame.time.get_ticks()
            if event.key == pygame.K_6:
                self.key_step = 1
                self.key_time = now
            elif event.key == pygame.K_7 and self.key_step == 1 and now - self.key_time <= 1000:
                self.key_step = 0
                self.swap_sounds()
            else:
                self.key_step = 0
        if event.type == pygame.MOUSEBUTTONDOWN and self.visible:
            for i in range(6):
                if CHAR_SHEETS[i]:
                    if self.p1[i].collidepoint(event.pos):
                        self.reload(self.fs.knight, *CHAR_SHEETS[i])
                    if self.p2[i].collidepoint(event.pos):
                        self.reload(self.fs.werebear, *CHAR_SHEETS[i])
            for lvl, btn in ((1, self.cpu1_btn), (2, self.cpu2_btn), (3, self.cpu3_btn)):
                if btn.collidepoint(event.pos):
                    if self.fs.cpu_enabled and self.fs.cpu_level == lvl:
                        self.fs.cpu_enabled = False
                    else:
                        self.fs.cpu_level = lvl
                        self.fs.cpu = CPUController(level=lvl)
                        self.fs.cpu_enabled = True

    def draw(self, screen):
        if not self.visible:
            return
        font = get_font()
        screen.blit(self.bg, (self.x, self.y))
        screen.blit(font.render("PLAYER 1", True, RED),  (self.x + 10, self.y + 15))
        screen.blit(font.render("PLAYER 2", True, BLUE), (self.x + 10, self.y + 145))
        for i in range(6):
            pygame.draw.rect(screen, RED,  self.p1[i])
            pygame.draw.rect(screen, BLUE, self.p2[i])
            t = font.render(self.labels[i], True, WHITE)
            screen.blit(t, (self.p1[i].x + (self.btn_w - t.get_width())//2, self.p1[i].y + (self.btn_h - t.get_height())//2))
            screen.blit(t, (self.p2[i].x + (self.btn_w - t.get_width())//2, self.p2[i].y + (self.btn_h - t.get_height())//2))

        cpu_labels = {
            1: ("CPU1lvlON",      "CPU1lvlOFF"),
            2: ("CPU2lvlON",      "CPU2lvlOFF"),
            3: ("annihilationON", "annihilationOFF"),
        }
        for lvl, btn in ((1, self.cpu1_btn), (2, self.cpu2_btn), (3, self.cpu3_btn)):
            active = self.fs.cpu_enabled and self.fs.cpu_level == lvl
            label = cpu_labels[lvl][0 if active else 1]
            pygame.draw.rect(screen, GREEN if active else RED, btn, border_radius=4)
            ct = font.render(label, True, WHITE)
            screen.blit(ct, (btn.x + (btn.width - ct.get_width()) // 2,
                             btn.y + (btn.height - ct.get_height()) // 2))

            # # # # # # # # # # # # # # #
            #   ,    ,    /\   /\       #
            #  /( /\ )\  _\ \_/ /_      #
            #  |\_||_/| < \_   _/ >     #
            #  \______/  \|0   0|/      #
            #    _\/_   _(_  ^  _)_     #
            #   ( () ) /`\|V"""V|/`\    #
            #     {}   \  \_____/  /    #
            #     ()   /\   )=(   /\    #
            #     {}  /  \_/\=/\_/  \   #
            # # # # # # # # # # # # # # #
