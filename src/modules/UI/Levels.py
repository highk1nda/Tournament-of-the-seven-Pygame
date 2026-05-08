import pygame
import random

from src.modules.UI import constants as con
from src.modules.UI.CharDictionary import CHARACTER_DATA
from src.modules.Screens.FightScreen import FightScreen as fightscr
from src.modules.Screens.BoonScreen import boons


class LoadLvls:
    def __init__(self):
        self.character_picked = con.p1_char_idx

    def run(self):
        Levels = [0, 1, 2, 3, 4, 5]
        if self.character_picked in Levels:
            Levels.remove(self.character_picked)
        
        con.cpu_enabled = True
        
        con.selected_map = "map1"

        active_boons  = [boon for boon in boons if boon["type"] == "ACTIVE"]
        passive_boons = [boon for boon in boons if boon["type"] == "PASSIVE"]

        for i in range(5):
            #change map for the final boss
            if i > 3:
                con.selected_map = "map2"

            con.p2_char_idx     = Levels[i]
            con.p2_selected     = CHARACTER_DATA[con.p2_char_idx]

            con.p2_boon         = random.choice(active_boons)
            con.p2_passive_boon = random.choice(passive_boons)["key"]

            fight = fightscr(con.display_surface, con.clock, story=True)
            result = fight.run()
            if result != "story_win":
                return result
        con.selected_map = "map1"
        return "Crawlend"
