import pygame

from src.modules.UI import constants as con

def load_fighter_sounds():
    sounds = {
        "walk": pygame.mixer.Sound(
            "assets/sfx/knight-right-footstep-on-gravel-4-with-chainmail-101937.mp3"
        ),
        "dash":     pygame.mixer.Sound("assets/sfx/woosh.mp3"),
        "death":    pygame.mixer.Sound("assets/sfx/death.mp3"),
        "hit":      pygame.mixer.Sound("assets/sfx/hit.mp3"),
        "cheering": pygame.mixer.Sound("assets/sfx/cheering.mp3") #TODO: use it randomly every 10to20 seconds
    }

    sounds["walk"].set_volume(con.sfxVolume)
    sounds["dash"].set_volume(con.sfxVolume) 
    sounds["death"].set_volume(con.sfxVolume)
    sounds["hit"].set_volume(con.sfxVolume)   
    return sounds

def load_attack_sounds(char_data):
    sounds = {}
    for action, path in char_data["attack_sounds"].items():
        s = pygame.mixer.Sound(path)
        s.set_volume(con.sfxVolume)
        sounds[action] = s
    return sounds

def load_boon_sounds():
    paths = {
        "devils_die_rolling":  "assets/sfx/boons/dice_rolling.mp3",
        "devils_die_curse":    "assets/sfx/boons/dice_curse.mp3",
        "devils_die_revive":   "assets/sfx/boons/dice_revive.mp3",
        "sub_zero_freeze":     "assets/sfx/boons/sub_zero_freeze.mp3",
        "sub_zero_break":      "assets/sfx/boons/sub_zero_break.mp3",
        "scorching_ray":       "assets/sfx/boons/scorching_ray_fireball.mp3",
        "burn":                "assets/sfx/boons/burn.mp3",
        "warding_loop":        "assets/sfx/boons/warding_loop.mp3",
        "last_stand_activate": "assets/sfx/boons/last_stand_activate.mp3"
    }
    sounds = {}
    for key, path in paths.items():
        s = pygame.mixer.Sound(path)
        s.set_volume(con.sfxVolume)
        sounds[key] = s
    return sounds

"""
                                             ,--,  ,.-.
               ,                   \,       '-,-`,'-.' | ._
              /|           \    ,   |\         }  )/  / `-,',
              [ ,          |\  /|   | |        /  \|  |/`  ,`
              | |       ,.`  `,` `, | |  _,...(   (      .',
              \  \  __ ,-` `  ,  , `/ |,'      Y     (   /_L\
               \  \_\,``,   ` , ,  /  |         )         _,/
                \  '  `  ,_ _`_,-,<._.<        /         /
                 ', `>.,`  `  `   ,., |_      |         /
                   \/`  `,   `   ,`  | /__,.-`    _,   `\
               -,-..\  _  \  `  /  ,  / `._) _,-\`       \
                \_,,.) /\    ` /  / ) (-,, ``    ,        |
               ,` )  | \_\       '-`  |  `(               \
              /  /```(   , --, ,' \   |`<`    ,            |
             /  /_,--`\   <\  V /> ,` )<_/)  | \      _____)
       ,-, ,`   `   (_,\ \    |   /) / __/  /   `----`
      (-, \           ) \ ('_.-._)/ /,`    /
      | /  `          `/ \\ V   V, /`     /
   ,--\(        ,     <_/`\\     ||      /
  (   ,``-     \/|         \-A.A-`|     /
 ,>,_ )_,..(    )\          -,,_-`  _--`
(_ \|`   _,/_  /  \_            ,--`
 \( `   <.,../`     `-.._   _,-`
    `                 \_      `--`
                         `---`
                                              -hmm...  
                                              
                                              IN THE NAME OF THE FATHER, THE SON, AND THE HOLY SPIRIT I REBUKE THIS! 
"""