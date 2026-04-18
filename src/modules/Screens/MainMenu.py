import pygame
from pygame.locals import *

from src.modules.UI import constants as con
from src.modules.UI.Button import Button
from src.modules.fighter.render import load_menu_background


class MainMenuScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.SysFont(None, 40)
        
        self.bg_frames = load_menu_background(con.SCREEN_WIDTH, con.SCREEN_HEIGHT)
        self.bg_frame_index = 0
        self.bg_update_time = pygame.time.get_ticks()
        if con.background_music.get_num_channels() == 0:
            con.background_music.play(-1)

        # create the buttons, with play being in the center of the screen TODO add story, multiplayer, and singleplayer, buttons
        self.button_play = Button((con.SCREEN_WIDTH/2) - 100, con.SCREEN_HEIGHT/2, 200, 40, 'Play', self.font)
        self.button_help = Button((con.SCREEN_WIDTH/2) - 100, (con.SCREEN_HEIGHT/2) + 70, 200, 40, 'Help', self.font)
        self.button_options = Button((con.SCREEN_WIDTH/2) - 100, (con.SCREEN_HEIGHT/2) + 140, 200, 40, 'Options', self.font)
        self.button_quit = Button(con.SCREEN_WIDTH/2 - 100, (con.SCREEN_HEIGHT/2) + 210, 200, 40, 'Quit', self.font)
        self.buttons = [self.button_play, self.button_help, self.button_options, self.button_quit]

        self.click = False
        self.confirm_quit = False
        self.small_font = pygame.font.SysFont(None, 30)

        center_x = con.SCREEN_WIDTH // 2
        center_y = con.SCREEN_HEIGHT // 2
        self.yes_rect = pygame.Rect(center_x - 130, center_y + 20, 100, 38)
        self.no_rect  = pygame.Rect(center_x +  30, center_y + 20, 100, 38)

    def handle_event(self, event):
        #seperate method for handling events in menu, as it will contain a lot
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if self.confirm_quit:
                    self.confirm_quit = False
                else:
                    self.confirm_quit = True
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.confirm_quit:
                    if self.yes_rect.collidepoint(event.pos):
                        con.exit_sound.play()
                        return 'quit'
                    if self.no_rect.collidepoint(event.pos):
                        self.confirm_quit = False
                else:
                    self.click = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.click = False
        return None

    def update(self):
        if self.confirm_quit:
            return None

        #check button interactions
        mx, my = pygame.mouse.get_pos()

        if self.button_play.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            return 'play'
        if self.button_help.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            return 'help'
        if self.button_options.is_clicked((mx, my), self.click):
            self.click = False
            con.ui_error_sound.play()
            return 'options'
        if self.button_quit.is_clicked((mx, my), self.click):
            self.click = False
            con.exit_sound.play()
            return 'quit'

        return None

    def draw_confirm_dialog(self):
        center_x = con.SCREEN_WIDTH // 2
        center_y = con.SCREEN_HEIGHT // 2

        msg = self.font.render("Are you sure you want to exit?", True, con.WHITE)
        self.screen.blit(msg, (center_x - msg.get_width() // 2, center_y - 30))

        for rect, label, color in (
            (self.yes_rect, "Yes", (140, 40, 40)),
            (self.no_rect,  "No",  (40, 40, 140)),
        ):
            pygame.draw.rect(self.screen, color, rect)
            s = self.small_font.render(label, True, con.WHITE)
            self.screen.blit(s, (rect.centerx - s.get_width() // 2,
                                 rect.centery - s.get_height() // 2))

    def draw(self):
        # every 100ms move to the next frame
        if pygame.time.get_ticks() - self.bg_update_time > 100:
            self.bg_frame_index = (self.bg_frame_index + 1) % len(self.bg_frames)  # loop back to 0 at the end
            self.bg_update_time = pygame.time.get_ticks()  # reset timer
        self.screen.blit(self.bg_frames[self.bg_frame_index], (0, 0))  # draw current frame

        # draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        if self.confirm_quit:
            self.draw_confirm_dialog()

    def run(self):
        #loop for main menu
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return 'quit'

                result = self.handle_event(event)
                if result:
                    return result

            action = self.update()
            if action:
                return action

            self.draw()
            pygame.display.update()
            self.clock.tick(60)

# DRACULA
#                   __,-----,,,,  ,,,--------,__ 
#                 _-/|\\/|\\/|\\\|\//\\\//|/|//|\\_ 
#                /|\/\//\\\\\\\\\\//////////////\\\\ 
#              //|//           \\\///            |\\|\ 
#             ///|\/             \/               \|\|\ 
#            |/|//                                 |\\|\  
#           |/|/                                    \|\|\
#           ///;    ,,=====,,,  ~~-~~  ,,,=====,,    ;|\|\
#          |/|/   '"          `'     '"          "'   ;|\|
#          ||/`;   _--~~~~--__         __--~~~~--_   ;/|\|
#          /|||;  :  /       \~~-___-~~/       \  :  ;|\| 
#          /\|;    -_\  (o)  / ,'; ;', \  (o)  /_-    ;|| 
#          |\|;      ~-____--~'  ; ;  '~--____-~      ;\| 
#           ||;            ,`   ;   ;   ',            ;||
#         __|\ ;        ,'`    (  _  )    `',        ;/|__ 
#     _,-~   \|/;    ,'`        ~~ ~~        `',    ;|\   ~-,_ 
#   ,'         ||;  '                           '  ;\|/       `, 
#  , _          ; ,         _--~~-~~--_           ;            _',
# ,-' `;-,        ;        ,; |_| | |_| ;,       ;;        ,-;' `-,
#       ; `,      ;       ;_| : `~'~' : |_;       ;      ,' ;
#        ;  `,     ;     :  `\/       \/   :     ;     ,'  ;
#         ;   `,    ;     :               ;     ;    ,'   ;
#          ;    `,_  ;     ;./\_     _/\.;     ;   _,    ;
#       _-'        ;  ;     ~~--|~|~|--~~     ;   ;       '-_
#   _,-'            ;  ;        ~~~~~        ;   ;           `-,_
# ,~                 ;  \`~--__         __--~/  ;                ~,
#                     ;   \   ~~-----~~    /   ;                   
#                      ~-_  \  /  |  \   /  _-~                    
#                         ~~-\/   |   \/ -~~                       
#                        (=)=;==========;=(=)
