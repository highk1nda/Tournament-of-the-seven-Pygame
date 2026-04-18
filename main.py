import pygame


from src.modules.Screens.MainMenu import MainMenuScreen as mainmenu
from src.modules.Screens.FightScreen import FightScreen as fightscr
from src.modules.Screens.Help import Help as helpscr
from src.modules.Screens.Options import Options as opt
from src.modules.UI import constants as con


pygame.init()
pygame.display.set_caption("Liberty") #VIVA LA LIBERTAS


# three functions that run all screens that can be called from main menu.
def run_menu():
    menu = mainmenu(con.display_surface, con.clock)
    return menu.run()  

def run_story():
    return "menu"

def run_singleplayer():
    return "menu"

def run_fight():
    fight = fightscr(con.display_surface, con.clock)
    return fight.run()
    
def run_help():
    help = helpscr(con.display_surface, con.clock)
    return help.run()

def run_options():
    options = opt(con.display_surface, con.clock)
    return options.run()

#start in the menu state
state = "menu"

#main game loop
while state != "quit":
    if state == "menu":
        state = run_menu()      
    
    elif state == "Story mode":
        con.background_music.stop()
        state = run_story()

    elif state == "Singleplayer":
        con.background_music.stop()
        state = run_singleplayer()

    elif state == "Multiplayer":
        con.background_music.stop()
        state = run_fight()  

    elif state == "Help":
        state = run_help()  

    elif state == "Options":
        state = run_options()

pygame.quit()