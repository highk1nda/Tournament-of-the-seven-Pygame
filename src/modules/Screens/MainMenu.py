import pygame
from pygame.locals import *
pygame.init()

from src.modules.UI import constants as con
from src.modules.UI.Button import Button 
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res 
from src.modules.systems.scalemouse import scale_mouse
from src.modules.fighter.render import load_menu_background
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr

class MainMenuScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        
        self.bg_frames = load_menu_background(con.SCREEN_WIDTH, con.SCREEN_HEIGHT)
        self.bg_frame_index = 0
        self.bg_update_time = pygame.time.get_ticks()
        if con.background_music.get_num_channels() == 0:
            con.background_music.play(-1)

        self.button_story           = Button(con.button_x, con.button_y, con.buttonwidth, con.buttonheight, 'Story mode', con.font_Large, con.DARK_RED)
        self.button_singleplayer    = Button(con.button_x, con.button_y + con.buttonspacing, con.buttonwidth, con.buttonheight, 'Singleplayer', con.font_Large, con.DARK_RED)
        self.button_multiplayer     = Button(con.button_x, con.button_y + (con.buttonspacing*2), con.buttonwidth,con.buttonheight, 'Multiplayer', con.font_Large, con.DARK_RED)
        self.button_help            = Button(con.button_x, con.button_y + (con.buttonspacing*3), con.buttonwidth, con.buttonheight, 'Help', con.font_Large, con.DARK_RED)
        self.button_options         = Button(con.button_x, con.button_y + (con.buttonspacing*4), con.buttonwidth, con.buttonheight, 'Options', con.font_Large, con.DARK_RED)
        self.button_quit            = Button(con.button_x, con.button_y + (con.buttonspacing*5), con.buttonwidth, con.buttonheight, 'Quit', con.font_Large, con.DARK_RED)
        self.buttons                = [self.button_story, self.button_singleplayer, self.button_multiplayer, self.button_help, self.button_options, self.button_quit]

        self.click = False
        self.confirm_quit = False


    def handle_event(self, event):
        #seperate method for handling events in menu, as it will contain a lot
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                result = confscr(self.screen, self.clock, "Menu").run()
                return result
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click = True
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1:
                self.click = False
        return None

    def update(self):
        if self.confirm_quit:
            return None

        #check button interactions
        mx, my = scale_mouse()

        if self.button_story.is_clicked((mx, my), self.click):
            self.click = False
            con.ui_error_sound.play()
            return 'Story mode'
        if self.button_singleplayer.is_clicked((mx, my), self.click):
            self.click = False
            con.ui_error_sound.play()
            return 'Singleplayer'
        if self.button_multiplayer.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            return 'Multiplayer'
        if self.button_help.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            return 'Help'
        if self.button_options.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            return 'Options'
        if self.button_quit.is_clicked((mx, my), self.click):
            self.click = False
            con.exit_sound.play()
            result = confscr(self.screen, self.clock, "Menu").run()  
            return result
        
        return None

    def draw(self):
        # every 100ms move to the next frame
        if pygame.time.get_ticks() - self.bg_update_time > 100:
            self.bg_frame_index = (self.bg_frame_index + 1) % len(self.bg_frames)  # loop back to 0 at the end
            self.bg_update_time = pygame.time.get_ticks()  # reset timer
        self.screen.blit(self.bg_frames[self.bg_frame_index], (0, 0))  # draw current frame

        # draw buttons
        for button in self.buttons:
            button.draw(self.screen)

        appBright(self.screen)

    def run(self):
        #loop for main menu
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    result = confscr(self.screen, self.clock, "Menu").run()
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
