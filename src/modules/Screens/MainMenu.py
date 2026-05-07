import pygame
from pygame.locals import *

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
        
        self.bg = load_menu_background(con.SCREEN_WIDTH, con.SCREEN_HEIGHT)
        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((5, 5, 5, 220))
        if con.background_music.get_num_channels() == 0:
            con.background_music.play(-1)

        self.button_story           = Button(con.button_x, con.button_y, con.buttonwidth, con.buttonheight, 'Story mode', con.font_Large, (200, 130, 40))
        self.button_singleplayer    = Button(con.button_x, con.button_y + con.buttonspacing, con.buttonwidth, con.buttonheight, 'Singleplayer', con.font_Large, (200, 130, 40))
        self.button_multiplayer     = Button(con.button_x, con.button_y + (con.buttonspacing*2), con.buttonwidth,con.buttonheight, 'Multiplayer', con.font_Large, (200, 130, 40))
        self.button_help            = Button(con.button_x, con.button_y + (con.buttonspacing*3), con.buttonwidth, con.buttonheight, 'Help', con.font_Large, (200, 130, 40))
        self.button_options         = Button(con.button_x, con.button_y + (con.buttonspacing*4), con.buttonwidth, con.buttonheight, 'Options', con.font_Large, (200, 130, 40))
        self.button_quit            = Button(con.button_x, con.button_y + (con.buttonspacing*5), con.buttonwidth, con.buttonheight, 'Quit', con.font_Large, (200, 130, 40))
        self.buttons                = [self.button_story, self.button_singleplayer, self.button_multiplayer, self.button_help, self.button_options, self.button_quit]

        self.click = False


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
        #check button interactions
        mx, my = scale_mouse()

        if self.button_story.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
            return 'Story'
        if self.button_singleplayer.is_clicked((mx, my), self.click):
            self.click = False
            con.select_sound.play()
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
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.overlay, (0, 0))

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
