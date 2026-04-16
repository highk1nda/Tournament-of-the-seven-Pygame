import pygame
from pygame.locals import *

from src.modules.UI import constants as con
from src.modules.UI.Button import Button 


class MainMenuScreen:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.font = con.FONT_NORMAL
        
        self.background = con.background
        self.background_music = con.background_music.play(-1)

        # create the buttons, with play being in the center of the screen TODO add story, multiplayer, and singleplayer, buttons
        self.button_play = Button((con.SCREEN_WIDTH/2) - 100, con.SCREEN_HEIGHT/2, 200, 40, 'Play', self.font)
        self.button_help = Button((con.SCREEN_WIDTH/2) - 100, (con.SCREEN_HEIGHT/2) + 70, 200, 40, 'Help', self.font)
        self.button_options = Button((con.SCREEN_WIDTH/2) - 100, (con.SCREEN_HEIGHT/2) + 140, 200, 40, 'Options', self.font)
        self.button_quit = Button(con.SCREEN_WIDTH/2 - 100, (con.SCREEN_HEIGHT/2) + 210, 200, 40, 'Quit', self.font)
        self.buttons = [self.button_play, self.button_help, self.button_options, self.button_quit]

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
        mx, my = pygame.mouse.get_pos()

        if self.button_play.is_clicked((mx, my), self.click):
            self.click = False
            return 'play'
        if self.button_help.is_clicked((mx, my), self.click):
            self.click = False
            return 'help'
        if self.button_options.is_clicked((mx, my), self.click):
            self.click = False
            return 'options'
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
