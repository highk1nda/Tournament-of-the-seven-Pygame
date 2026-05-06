import pygame
from pygame.locals import *

import os
import json

from src.modules.UI import constants as con

def saveGame():
    os.makedirs("assets/save", exist_ok=True)
    data = {
        "storyEdwardComplete": con.storyEdwardComplete,
        "storyTylandComplete": con.storyTylandComplete,
        "storyLunaComplete": con.storyLunaComplete,
        "storyRemComplete": con.storyRemComplete,
        "storyArlandComplete": con.storyArlandComplete
    }

    with open("assets/save/save.json", "w") as file:
        json.dump(data, file, indent=2)

def loadSave():
    if not os.path.exists("assets/save/save.json"):
        saveGame()
    
    #in case its corrupted.
    try: 
        with open("assets/save/save.json", "r") as file:
            data = json.load(file)
        con.storyEdwardComplete = data.get("storyEdwardComplete", False)
        con.storyTylandComplete = data.get("storyTylandComplete", False)
        con.storyLunaComplete = data.get("storyLunaComplete", False)
        con.storyRemComplete = data.get("storyRemComplete", False)
        con.storyArlandComplete = data.get("storyArlandComplete", False)
    except (json.JSONDecodeError) as error:
        print(f"Error loading save file: {error}")
        saveGame()  
