import pygame
from pygame.locals import *

from src.modules.UI import constants as con
from src.modules.UI.Button import Button 
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res 
from src.modules.systems.scalemouse import scale_mouse

class MainMenuScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.SysFont(None, 40)
        
        self.background = con.background
        self.background_music = con.background_music.play(-1)

        self.button_story           = Button(con.button_x, con.button_y, con.buttonwidth, con.buttonheight, 'Story mode', self.font)
        self.button_singleplayer    = Button(con.button_x, con.button_y + con.buttonspacing, con.buttonwidth, con.buttonheight, 'Singleplayer', self.font)
        self.button_multiplayer     = Button(con.button_x, con.button_y + (con.buttonspacing*2), con.buttonwidth,con.buttonheight, 'Multiplayer', self.font)
        self.button_help            = Button(con.button_x, con.button_y + (con.buttonspacing*3), con.buttonwidth, con.buttonheight, 'Help', self.font)
        self.button_options         = Button(con.button_x, con.button_y + (con.buttonspacing*4), con.buttonwidth, con.buttonheight, 'Options', self.font)
        self.button_quit            = Button(con.button_x, con.button_y + (con.buttonspacing*5), con.buttonwidth, con.buttonheight, 'Quit', self.font)
        self.buttons                = [self.button_story, self.button_singleplayer, self.button_multiplayer, self.button_help, self.button_options, self.button_quit]

        self.click = False

    def handle_event(self, event):
        #seperate method for handling events in menu, as it will contain a lot
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return 'quit'
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
            return 'Story mode'
        if self.button_singleplayer.is_clicked((mx, my), self.click):
            self.click = False
            return 'Singleplayer'
        if self.button_multiplayer.is_clicked((mx, my), self.click):
            self.click = False
            return 'Multiplayer'
        if self.button_help.is_clicked((mx, my), self.click):
            self.click = False
            return 'Help'
        if self.button_options.is_clicked((mx, my), self.click):
            self.click = False
            return 'Options'
        if self.button_quit.is_clicked((mx, my), self.click):
            self.click = False
            return 'quit'

        return None

    def draw(self):
        #draw main menu we are using the forest background as placeholder
        self.screen.blit(self.background, (0, 0))

        # draw buttons
        for button in self.buttons:
            button.draw(self.screen)
        appBright(self.screen)

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
