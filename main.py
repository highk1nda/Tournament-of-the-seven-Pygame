import pygame
from src.modules.Screens.MainMenu import MainMenuScreen as mainmenu
from src.modules.Screens.FightScreen import FightScreen as fightscr
from src.modules.Screens.Help import Help as helpscr
from src.modules.Screens.SelectCharScreen import SelectCharScreen as charselect
from src.modules.Screens.BoonScreen import BoonScreen as boonscr
from src.modules.Screens.MapScreen import MapScreen as mapscr
from src.modules.Screens.Options import Options as opt
from src.modules.UI import constants as con
from src.modules.Screens.Controlscreens.Edward import Edward as Edscr
from src.modules.Screens.Controlscreens.Tyland import Tyland as Tyscr
from src.modules.Screens.Controlscreens.Luna import Luna as Lunscr
from src.modules.Screens.Controlscreens.Rem import Rem as Remscr
from src.modules.Screens.Controlscreens.Arland import Arland as Arlscr
from src.modules.Screens.Controlscreens.Venator import Venator as Venscr


pygame.init()
pygame.display.set_caption("Liberty") #VIVA LA LIBERTAS


# three functions that run all screens that can be called from main menu.

def run_menu():
    menu = mainmenu(con.display_surface, con.clock)
    return menu.run()

def run_story():
    return "Menu"

def run_singleplayer():
    return "Menu"

def run_fight():
    fight = fightscr(con.display_surface, con.clock)
    return fight.run()

def run_help():
    help = helpscr(con.display_surface, con.clock)
    return help.run()

def run_edward():
    Edward = Edscr(con.display_surface, con.clock)
    return Edward.run()

def run_tyland():
    Tyland = Tyscr(con.display_surface, con.clock)
    return Tyland.run()

def run_luna():
    Luna = Lunscr(con.display_surface, con.clock)
    return Luna.run()

def run_rem():  
    Rem = Remscr(con.display_surface, con.clock)
    return Rem.run()

def run_arland():
    Arland = Arlscr(con.display_surface, con.clock)
    return Arland.run()

def run_venator():      
    Venator = Venscr(con.display_surface, con.clock)
    return Venator.run()

def run_options():
    options = opt(con.display_surface, con.clock)
    return options.run()

#start in the menu state
state = "Menu"

#main game loop
while state != "quit":
    if state == "Menu":
        state = run_menu()      
    
    elif state == "Story mode":
        con.background_music.stop()
        state = run_story()

    elif state == "Singleplayer":
        con.background_music.stop()
        state = run_singleplayer()

    elif state == "Fight":
        con.background_music.stop()
        state = run_fight() 

    elif state == "Multiplayer":
        sub_state = 'Char'
        while sub_state != "Fight":
            if sub_state == 'Char':
                sub_state = charselect(con.display_surface, con.clock).run()
                if sub_state == "Menu":
                    state = sub_state
                    break
            elif sub_state == "Boon":
                sub_state = boonscr(con.display_surface, con.clock).run()
            elif sub_state == "Map":
                sub_state = mapscr(con.display_surface, con.clock).run()
            elif sub_state == 'quit':
                break
            state = sub_state

    elif state == "Help":
        state = run_help()
    
    elif state == "Edward":
        state = run_edward()

    elif state == "Tyland":
        state = run_tyland()
    
    elif state == "Luna":
        state = run_luna()

    elif state == "Rem":
        state = run_rem()
    
    elif state == "Arland":
        state = run_arland()

    elif state == "Venator":
        state = run_venator()
        
    elif state == "Options":
        state = run_options()

pygame.quit()