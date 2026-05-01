import pygame
from src.modules.fighter.render import load_animation_frames
from src.modules.UI import constants as con

_font = None

def _get_font():
    global _font
    if _font is None:
        _font = pygame.font.SysFont(None, 22)
    return _font


#debug thingy to quickly switch characters during development, gonna be removed later (or maybe not, who knows)
class DebugPopup:
    def __init__(self, fightscreen):
        self.fs = fightscreen
        self.visible = False
        W, H = 340, 300
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

        self._ks = 0
        self._kt = 0
        self._ka = False

    def _reload(self, fighter, sheet, steps):
        fighter.animation_list = load_animation_frames(sheet, con.CHARACTER_DATA[0], con.CHARACTER_DATA[1], steps)
        fighter.action = 0
        fighter.frame_index = 0

    def p1_select_knight(self):
        self._reload(self.fs.knight, con.knight_sheet, con.KNIGHT_ANIMATION_STEPS)
    def p1_select_werebear(self):
        self._reload(self.fs.knight, con.werebear_sheet, con.WEREBEAR_ANIMATION_STEPS)
    def p1_select_wizard(self):
        self._reload(self.fs.knight, con.wizard_sheet, con.WIZARD_ANIMATION_STEPS)
    def p1_select_minotaur(self):
        pass
    def p1_select_archer(self):
        pass
    def p1_select_ktemplar(self):
        self._reload(self.fs.knight, con.knight_templar_sheet, con.KNIGHT_TEMPLAR_ANIMATION_STEPS)


    def p2_select_knight(self):
        self._reload(self.fs.werebear, con.knight_sheet, con.KNIGHT_ANIMATION_STEPS)
    def p2_select_werebear(self):
        self._reload(self.fs.werebear, con.werebear_sheet, con.WEREBEAR_ANIMATION_STEPS)
    def p2_select_wizard(self):
        self._reload(self.fs.werebear, con.wizard_sheet, con.WIZARD_ANIMATION_STEPS)
    def p2_select_minotaur(self):
        pass
    def p2_select_archer(self):
        pass
    def p2_select_ktemplar(self):
        self._reload(self.fs.werebear, con.knight_templar_sheet, con.KNIGHT_TEMPLAR_ANIMATION_STEPS)

    def _flush(self):
        _p = [("death", "assets/sfx/death2.mp3"),
              ("hit",   "assets/sfx/hit2.mp3"),
              ("dash",  "assets/sfx/jump.mp3")]
        self._ka = not self._ka
        for fighter in (self.fs.knight, self.fs.werebear):
            for k, path in _p:
                if self._ka:
                    fighter.sounds[k + "_"] = fighter.sounds[k]
                    fighter.sounds[k] = pygame.mixer.Sound(path)
                else:
                    fighter.sounds[k] = fighter.sounds.pop(k + "_", fighter.sounds[k])

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.visible = not self.visible
        if event.type == pygame.KEYDOWN:
            now = pygame.time.get_ticks()
            if event.key == pygame.K_6:
                self._ks = 1
                self._kt = now
            elif event.key == pygame.K_7 and self._ks == 1 and now - self._kt <= 1000:
                self._ks = 0
                self._flush()
            else:
                self._ks = 0
        if event.type == pygame.MOUSEBUTTONDOWN and self.visible:
            p1_callbacks = [self.p1_select_knight, self.p1_select_werebear, self.p1_select_wizard,
                            self.p1_select_minotaur, self.p1_select_archer, self.p1_select_ktemplar]
            p2_callbacks = [self.p2_select_knight, self.p2_select_werebear, self.p2_select_wizard,
                            self.p2_select_minotaur, self.p2_select_archer, self.p2_select_ktemplar]
            for i in range(6):
                if self.p1[i].collidepoint(event.pos):
                    p1_callbacks[i]()
                if self.p2[i].collidepoint(event.pos):
                    p2_callbacks[i]()

    def draw(self, screen):
        if not self.visible:
            return
        font = _get_font()
        screen.blit(self.bg, (self.x, self.y))
        screen.blit(font.render("PLAYER 1", True, con.RED),  (self.x + 10, self.y + 15))
        screen.blit(font.render("PLAYER 2", True, con.BLUE), (self.x + 10, self.y + 145))
        for i in range(6):
            pygame.draw.rect(screen, con.RED,  self.p1[i])
            pygame.draw.rect(screen, con.BLUE, self.p2[i])
            t = font.render(self.labels[i], True, con.WHITE)
            screen.blit(t, (self.p1[i].x + (self.btn_w - t.get_width())//2, self.p1[i].y + (self.btn_h - t.get_height())//2))
            screen.blit(t, (self.p2[i].x + (self.btn_w - t.get_width())//2, self.p2[i].y + (self.btn_h - t.get_height())//2))

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