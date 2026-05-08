import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res
from src.modules.UI.Button import Button 
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr
from src.modules.systems.scalemouse import scale_mouse

#The help screen
class Help():
    def __init__(self, screen, clock):
        
        self.screen = screen
        self.clock = clock
        self.Button_Edward          = Button(100, 800, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Edward', con.font_Large, con.DARK_RED)
        self.Button_Tyland          = Button(400, 800, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Tyland', con.font_Large, con.DARK_RED)
        self.Button_Luna            = Button(700, 800, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Luna', con.font_Large, con.DARK_RED)
        self.Button_Rem             = Button(1000, 800, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Rem', con.font_Large, con.DARK_RED)
        self.Button_Arland          = Button(1300, 800, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Arland', con.font_Large, con.DARK_RED)
        if con.storyEdwardComplete or con.storyTylandComplete or con.storyLunaComplete or con.storyRemComplete or con.storyArlandComplete:
            self.Button_Venator     = Button(1600, 800, int(con.SCREEN_WIDTH/8), con.buttonheight, 'Venator', con.font_Large, con.DARK_RED)
        else:
            self.Button_Venator     = Button(1600, 800, int(con.SCREEN_WIDTH/8), con.buttonheight, '???', con.font_Large, con.BLACK, nonselect=True)
        self.buttons                = [self.Button_Edward, self.Button_Tyland, self.Button_Luna, self.Button_Rem, self.Button_Arland, self.Button_Venator]
        self.click = False

        #text
        self.txt = ["Player 1: Movement: A/D left and right respectively | Jump: W | LShift: Dash  | Attacks: R, F, V | Active boon: e",
                    "",
                    "",
                    "Player 2: Movement: <- /-> left and right respectively | Jump: ↑ | RShift: Dash  | Attacks: slash (/), period (.), comma (,) | Active boon:  (;)",
                    "",
                    "",
                    "Dash: Press Shift + direction(left or right) to dash in the respective direction. Player has 2 dash charges in every Shift press window(visualized under the health bar).",
                    "",
                    "",
                    "Dash Cooldown is triggered when: 1) 2 dash charges are both used, 2) Shift is released after 1 dash.",
                    "",
                    "",
                    "Hint: Dashing results in a brief moment of invincibility, use it to dodge attacks and reposition.",
                    "",
                    "",
                    "Character specific attacks and mechanics:",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "Boon descriptions can be found in the boon select screen, during the selection process",
                    "",
                    "",
                    "Press ESC to return to main menu"]

        #overlay to make it smooth
        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((5, 5, 5, 220))
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                con.exit_sound.play()
                return "Menu"
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click = True
        return None
    
    def update(self):
        #check button interactions
        mx, my = scale_mouse()

        if self.Button_Edward.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            con.p1_char_idx = 0
            return 'Edward'
        if self.Button_Tyland.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            con.p1_char_idx = 1
            return 'Tyland'
        if self.Button_Luna.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            con.p1_char_idx = 2
            return 'Luna'
        if self.Button_Rem.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            con.p1_char_idx = 3
            return 'Rem'
        if self.Button_Arland.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            con.p1_char_idx = 4
            return 'Arland'
        if self.Button_Venator.is_clicked((mx, my), self.click):
            if con.storyEdwardComplete or con.storyTylandComplete or con.storyLunaComplete or con.storyRemComplete or con.storyArlandComplete:
                self.click = False
                con.select_sound.play()
                con.p1_char_idx = 5
                return "Venator"
            else:
                self.click = False
                con.ui_error_sound.play()
                
        return None

    def draw(self):
        #draw overlay, display title
        self.screen.blit(con.background, (0,0))
        self.screen.blit(self.overlay, (0,0))
        title = con.font_XLarge.render("Controls", True, con.YELLOW)
        self.screen.blit(title, title.get_rect(center=(con.center_x, 170)))

        #display text
        count = 0
        for line in self.txt:
            rendered_l = con.font_Big.render(line, True, con.WHITE)
            self.screen.blit(rendered_l, rendered_l.get_rect(center=(con.center_x, count + 400)))
            count += 25
        
        for button in self.buttons:
            button.draw(self.screen)

        appBright(self.screen)

    def run(self):
        #help screen loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = confscr(self.screen, self.clock, "Help").run()
                    return result
                result = self.handle_event(event)
                if result:
                    return result
            action = self.update()
            if action:
                return action
            
            self.draw()
            res.render_to_surface()
            self.clock.tick(con.FPS)