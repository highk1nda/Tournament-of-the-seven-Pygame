import pygame


def load_fighter_sounds():
    sounds = {
        "walk": pygame.mixer.Sound(
            "assets/sfx/knight-right-footstep-on-gravel-4-with-chainmail-101937.mp3"
        ),
        "attack1": pygame.mixer.Sound(
            "assets/sfx/sword_sfx/sword-slice-393847.mp3"
        ),
        "attack2": pygame.mixer.Sound(
            "assets/sfx/sword_sfx/sword-slashing-game-sound-effect-1-379228.mp3"
        ),
        "attack3": pygame.mixer.Sound(
            "assets/sfx/sword_sfx/short-fire-whoosh_1-317280.mp3"
        ),
        "attack4": pygame.mixer.Sound(
            "assets/sfx/sword_sfx/fire-breath-6922.mp3"
        ),
        "orc_attack": pygame.mixer.Sound(
            "assets/sfx/sword_sfx/character-falling-on-ground-250069.mp3"
        ),
        "jump": pygame.mixer.Sound("assets/sfx/jump.mp3"),
        "dash": pygame.mixer.Sound("assets/sfx/woosh.mp3"),
        "death": pygame.mixer.Sound("assets/sfx/death.mp3"),
        "hit": pygame.mixer.Sound("assets/sfx/hit.mp3")
    }

    sounds["walk"].set_volume(0.3)
    sounds["attack1"].set_volume(0.4)
    sounds["attack2"].set_volume(0.4)
    sounds["attack3"].set_volume(0.4)

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
"""