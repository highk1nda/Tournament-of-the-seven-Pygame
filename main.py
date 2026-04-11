import pygame


from src.modules.Screens.MainMenu import MainMenuScreen as mainmenu
from src.modules.Screens.FightScreen import FightScreen as fightscr
from src.modules.Screens.Help import Help as helpscr
from src.modules.Screens.SelectCharScreen import SelectCharScreen as charselect
from src.modules.UI import constants as con
pygame.init()
pygame.display.set_caption("Liberty") #VIVA LA LIBERTAS


# three functions that run all screens that can be called from main menu.
def run_menu():
    menu = mainmenu(con.display_surface, con.clock)
    return menu.run()

def run_fight():
    fight = fightscr(con.display_surface, con.clock)
    return fight.run()

def run_help():
    help = helpscr(con.display_surface, con.clock)
    return help.run()

def run_options():
    #TODO to be implemented
    pass

#start in the menu state
state = "menu"

#main game loop
while state != "quit":
    if state == "menu":
        state = run_menu()

    elif state == "play":
        con.background_music.stop()
        state = charselect(con.display_surface, con.clock).run()

    elif state == "fight":
        state = run_fight()

    elif state == "help":
        state = run_help()

    elif state == "options":
        # TODO: boys, we need to implement this when we get done with projects
        state = "menu"

pygame.quit()