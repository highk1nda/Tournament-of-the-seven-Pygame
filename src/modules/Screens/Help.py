import pygame
from pygame.locals import *
from src.modules.UI import constants as con

#The help screen
class Help():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        #we use 2 sizes of text here, so we define font and small.
        self.font  = pygame.font.SysFont("arial", 32)
        self.small = pygame.font.SysFont("arial", 16)

        #text
        self.txt = ["player 1 - Movement: A/D left and right respectively   Jump: W      Attacks: R, F, V",
                    "player 2 - Movement: Larrow and Rarrow respectively    Jump: UParrow      Attacks: .  /  Lshift",
                    "",
                    "press any key to return to main menu"]

        #overlay to make it smooth
        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((100, 100, 100, 100))
    
    def draw(self):
        #draw overlay, display title
        self.screen.blit(con.background, (0,0))
        self.screen.blit(self.overlay, (0,0))
        title = self.font.render("Controls", True, (212, 175, 55))
        self.screen.blit(title, title.get_rect(center=(con.SCREEN_WIDTH // 2, 200)))
        

        #display text
        count = 0
        for line in self.txt:
            rendered_l = self.small.render(line, True, (220, 220, 220))
            con.display_surface.blit(rendered_l, rendered_l.get_rect(center=(con.SCREEN_WIDTH // 2, 320 + count + 55)))
            count += 25

    def run(self):
        #help screen loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    return "menu"
            self.draw()
            pygame.display.update()