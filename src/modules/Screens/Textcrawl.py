import pygame
from pygame.locals import *
from src.modules.UI import constants as con
from src.modules.systems import res
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr
from src.modules.systems.save import saveGame

class Textcrawl:
    def __init__(self, screen, clock, caller = "Story", ending = False):
        self.screen = screen
        self.clock  = clock
        self.caller = caller
        self.ending = ending

        if con.p1_char_idx == 0:
            location = con.edwardIntroPath
            endLocation = con.edwardEndingPath
        elif con.p1_char_idx == 1:
            location = con.tylandIntroPath
            endLocation = con.tylandEndingPath
        elif con.p1_char_idx == 2:
            location = con.lunaIntroPath
            endLocation = con.lunaEndingPath
        elif con.p1_char_idx == 3:
            location = con.remIntroPath
            endLocation = con.remEndingPath
        elif con.p1_char_idx == 4:
            location = con.arlandIntroPath
            endLocation = con.arlandEndingPath
        elif con.p1_char_idx == 5:
            location = con.venatorIntroPath

        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((5, 5, 5, 220))

        self.txt = []
        if self.ending == True:
            with open(endLocation, "r") as text:
                for line in text:
                    self.txt.append(line.rstrip("\n"))
        else:
            with open(location, "r") as text:
                for line in text:
                    self.txt.append(line.rstrip("\n"))
        
        self.y = con.SCREEN_HEIGHT
        
        #how fast scrolling happens, endings contain less text so go faster
        if self.ending == True:
            self.scroll_speed = 0.6
        else:
            self.scroll_speed = 0.3 

        self.lineSpacing = 50

        self.lines = []
        for line in self.txt:
            rendered_line = con.font_Big.render(line, True, con.WHITE)
            self.lines.append(rendered_line)

    def draw(self):
        self.screen.blit(con.background, (0,0))
        self.screen.blit(self.overlay, (0,0))

        # count accumalates line spacing so lines are drawn 50 pixels apart
        count = 0
        for line in self.lines:
            y = self.y + count

            self.screen.blit(line, line.get_rect(center=(con.SCREEN_WIDTH // 2, y)))
            count += self.lineSpacing
            
        appBright(self.screen)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.ending == True:
                        result = confscr(self.screen, self.clock, "Crawlend").run()
                        return result
                    else:
                        result = confscr(self.screen, self.clock, "Textcrawl").run()
                        return result
                
                if event.type == pygame.KEYDOWN:
                    if (event.key == K_RETURN or event.key == K_ESCAPE) and self.caller != "Story":
                        if self.caller in ("Edward", "Tyland", "Luna", "Rem", "Arland", "Venator"):
                            con.exit_sound.play()
                            con.p1_char_idx = 0
                            return self.caller 
                          
                    if event.key == K_ESCAPE and self.caller == "Story":
                        con.exit_sound.play()
                        if self.ending:
                            if con.p1_char_idx == 0:
                                con.storyEdwardComplete = True
                            elif con.p1_char_idx == 1:
                                con.storyTylandComplete = True
                            elif con.p1_char_idx == 2:
                                con.storyLunaComplete = True
                            elif con.p1_char_idx == 3:
                                con.storyRemComplete = True
                            elif con.p1_char_idx == 4:
                                con.storyArlandComplete = True
                            con.p1_char_idx = 0
                            saveGame()
                            return "Menu"
                        else:
                            return "CPU"   
                     
                    if event.key == K_RETURN:
                        con.exit_sound.play()
                        if self.caller == "Story" and self.ending == False:
                            return "Levels"
                        if self.caller == "Story" and self.ending == True: 
                            if con.p1_char_idx == 0:
                                con.storyEdwardComplete = True
                            elif con.p1_char_idx == 1:
                                con.storyTylandComplete = True
                            elif con.p1_char_idx == 2:
                                con.storyLunaComplete = True
                            elif con.p1_char_idx == 3:
                                con.storyRemComplete = True
                            elif con.p1_char_idx == 4:
                                con.storyArlandComplete = True
                            con.p1_char_idx = 0
                            saveGame()
                            return "Menu"
                
            self.y -= self.scroll_speed # each line is moved upward based on scroll speed

            self.draw()
            res.render_to_surface()
            self.clock.tick(con.FPS)