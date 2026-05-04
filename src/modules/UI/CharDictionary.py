import pygame
from src.modules.UI import constants as con

DEFAULT_SIZE = 100
DEFAULT_SCALE =  con.SCREEN_WIDTH / 142.86
DEFAULT_OFFSET = [int(con.SCREEN_WIDTH / 48), int(con.SCREEN_HEIGHT / 27.8)]

KNIGHT_DATA = {
    "name": "Ser Edward",
    "size": DEFAULT_SIZE,
    "scale": DEFAULT_SCALE,
    "offset": DEFAULT_OFFSET,
    "jumpable": True,
    "animations": {
        "IDLE":    {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight/Knight-Idle.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight with shadows/Knight-Idle.png",
                    "frame_number": 6,      # 6 frames for this action
                    "cooldown": 110},       # 110 ms between frames
        "WALK":    {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight/Knight-Walk.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight with shadows/Knight-Walk.png", 
                    "frame_number": 8,
                    "cooldown": 110},
        "ATTACK1": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight/Knight-Attack01.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight with shadows/Knight-Attack01.png", 
                    "frame_number": 7,
                    "cooldown": 65},
        "ATTACK2": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight/Knight-Attack02.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight with shadows/Knight-Attack02.png", 
                    "frame_number": 10,
                    "cooldown": 75},
        "ATTACK3": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight/Knight-Attack03.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight with shadows/Knight-Attack03.png", 
                    "frame_number": 11,
                    "cooldown": 85},
        "HIT":     {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight/Knight-Hurt.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight with shadows/Knight-Hurt.png",
                    "frame_number": 4, 
                    "cooldown": 100},
        "DEATH":   {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight/Knight-Death.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight with shadows/Knight-Death.png",
                    "frame_number": 4, 
                    "cooldown": 100},
    },
    "attack_active_frames": {
            "ATTACK1": [(3, 4)],        # (Start, End) index of animation
            "ATTACK2": [(3, 4), (7, 8)],
            "ATTACK3": [(7, 9)]
    },
    "attack_width_scale": {
            "ATTACK1": 0.6,             # attacking hitbox width scale
            "ATTACK2": 1,
            "ATTACK3": 1.5
    },
    "attack_damage": {
            "ATTACK1": 5,               # damage made by attacks
            "ATTACK2": 3,
            "ATTACK3": 10
    }
}

WEREBEAR_DATA = {
    "name": "Tyland",
    "size": DEFAULT_SIZE,
    "scale": DEFAULT_SCALE,
    "offset": DEFAULT_OFFSET,
    "jumpable": True,
    "animations": {
        "IDLE":    {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear/Werebear-Idle.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear with shadows/Werebear-Idle.png",
                    "frame_number": 6,      
                    "cooldown": 110},       
        "WALK":    {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear/Werebear-Walk.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear with shadows/Werebear-Walk.png",
                    "frame_number": 8,
                    "cooldown": 110},
        "ATTACK1": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear/Werebear-Attack01.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear with shadows/Werebear-Attack01.png", 
                    "frame_number": 9,
                    "cooldown": 65},
        "ATTACK2": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear/Werebear-Attack02.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear with shadows/Werebear-Attack02.png",
                    "frame_number": 13,
                    "cooldown": 75},
        "ATTACK3": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear/Werebear-Attack03.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear with shadows/Werebear-Attack03.png", 
                    "frame_number": 9,
                    "cooldown": 85},
        "HIT":     {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear/Werebear-Hurt.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear with shadows/Werebear-Hurt.png",
                    "frame_number": 4, 
                    "cooldown": 100},
        "DEATH":   {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear/Werebear-Death.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear with shadows/Werebear-Death.png",
                    "frame_number": 4, 
                    "cooldown": 100},
    },
    "attack_active_frames": {
            "ATTACK1": [(5, 6)],        
            "ATTACK2": [(4, 5), (9, 10)],
            "ATTACK3": [(5, 7)]
    },
    "attack_width_scale": {
            "ATTACK1": 1,            
            "ATTACK2": 1,
            "ATTACK3": 1.5
    },
    "attack_damage": {
            "ATTACK1": 5,
            "ATTACK2": 3,
            "ATTACK3": 10
    }
}

WIZARD_DATA = {
    "name": "Luna",
    "size": DEFAULT_SIZE,
    "scale": DEFAULT_SCALE,
    "offset": DEFAULT_OFFSET,
    "jumpable": True,
    "animations": {
        "IDLE":    {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard/Wizard-Idle.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard with shadows/Wizard-Idle.png",
                    "frame_number": 6,      
                    "cooldown": 110},       
        "WALK":    {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard/Wizard-Walk.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard with shadows/Wizard-Walk.png",
                    "frame_number": 8,
                    "cooldown": 110},
        "ATTACK1": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard/Wizard-Attack01.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard with shadows/Wizard-Attack01.png", 
                    "frame_number": 6,
                    "cooldown": 65},
        "ATTACK2": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard/Wizard-Attack02.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard with shadows/Wizard-Attack02.png",
                    "frame_number": 6,
                    "cooldown": 75},
        "HIT":     {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard/Wizard-Hurt.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard with shadows/Wizard-Hurt.png",
                    "frame_number": 4, 
                    "cooldown": 100},
        "DEATH":   {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard/Wizard-Death.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard with shadows/Wizard-Death.png",
                    "frame_number": 4, 
                    "cooldown": 100},
    },
    "attack_active_frames": {
            "ATTACK1": [(5, 6)],        
            "ATTACK2": [(4, 5)]
    },
    "attack_width_scale": {
            "ATTACK1": 0.1,            
            "ATTACK2": 0.2,
    },
    "attack_damage": {
            "ATTACK1": 0.1,
            "ATTACK2": 0.2,
    },
    "projectiles": {
        "ATTACK1": {
            "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Magic(projectile)/Wizard-Attack01_Effect.png",
            "frame_number": 10,
            "cooldown": 60,
            "type": "lock",             # attack will lock on the enemy('s current position)
            "delay": 800,              # delay for 800ms then attack
            "gen_frame": 2,             # at Wizard attack1 frame index 2: generate the projectile
            "active_frame": (1, 3),
            "speed": 0,
            "damage": 10,
            "hitbox_width": 80,
            "hitbox_height": 80
        },
        "ATTACK2": {
            "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Magic(projectile)/Wizard-Attack02_Effect.png",
            "frame_number": 7,
            "cooldown": 60,
            "type": "explosive",        # explosive fire ball
            "gen_frame": 4,             
            "speed": 15,
            "damage": 10,
            "hitbox_width": 20,
            "hitbox_height": 20
        }
    },
    "projectile_size": {
        "ATTACK1": {
            "size": DEFAULT_SIZE,
            "scale": con.SCREEN_WIDTH / 170,
            "offset": [int(con.SCREEN_WIDTH / 40), int(con.SCREEN_HEIGHT / 22)]
        },
        "ATTACK2": {
            "size": DEFAULT_SIZE,
            "scale": con.SCREEN_WIDTH / 190,
            "offset": [int(con.SCREEN_WIDTH / 40), int(con.SCREEN_HEIGHT / 20)]
        }
    }
}

MINOTAUR_DATA = {
    "name": "Rem",
    "size": 80,
    "scale": con.SCREEN_WIDTH / 250,
    "offset": [int(con.SCREEN_WIDTH / 90), int(con.SCREEN_HEIGHT / 40)],
    "jumpable": False,
    "animations": {
        "IDLE":    {"file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Minotaur/Minotaur-Idle.png",
                    "frame_number": 4,      
                    "cooldown": 200},       
        "WALK":    {"file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Minotaur/Minotaur-Walk.png", 
                    "frame_number": 8,
                    "cooldown": 110},
        "ATTACK1": {"file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Minotaur/Minotaur-Attack01.png", 
                    "frame_number": 6,
                    "cooldown": 65},
        "ATTACK2": {"file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Minotaur/Minotaur-Attack02.png", 
                    "frame_number": 6,
                    "cooldown": 75},
        "ATTACK3": {"file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Minotaur/Minotaur-Attack03.png", 
                    "frame_number": 6,
                    "cooldown": 85},
        "HIT":     {"file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Minotaur/Minotaur-Hurt.png",
                    "frame_number": 2, 
                    "cooldown": 100},
        "DEATH":   {"file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Minotaur/Minotaur-Death.png",
                    "frame_number": 6, 
                    "cooldown": 100},
    },
    "attack_active_frames": {
            "ATTACK1": [(3, 4)],        
            "ATTACK2": [(3, 5)],
            "ATTACK3": [(3, 4)]
    },
    "attack_width_scale": {
            "ATTACK1": 0.6,            
            "ATTACK2": 1,
            "ATTACK3": 0.6
    },
    "attack_damage": {
            "ATTACK1": 3,
            "ATTACK2": 5,
            "ATTACK3": 8
    }
}

ARCHER_DATA = {
    "name": "Arland",
    "size": DEFAULT_SIZE,
    "scale": DEFAULT_SCALE,
    "offset": DEFAULT_OFFSET,
    "jumpable": True,
    "animations": {
        "IDLE":    {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer/Archer-Idle.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer with shadows/Archer-Idle.png",
                    "frame_number": 6,      
                    "cooldown": 110},       
        "WALK":    {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer/Archer-Walk.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer with shadows/Archer-Walk.png", 
                    "frame_number": 8,
                    "cooldown": 110},
        "ATTACK1": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer/Archer-Attack01.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer with shadows/Archer-Attack01.png", 
                    "frame_number": 9,
                    "cooldown": 65},
        "ATTACK2": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer/Archer-Attack02.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer with shadows/Archer-Attack02.png", 
                    "frame_number": 12,
                    "cooldown": 75},
        "HIT":     {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer/Archer-Hurt.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer with shadows/Archer-Hurt.png",
                    "frame_number": 4, 
                    "cooldown": 100},
        "DEATH":   {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer/Archer-Death.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Archer with shadows/Archer-Death.png",
                    "frame_number": 4, 
                    "cooldown": 100},
    },
    "projectiles": {
        "ATTACK1": {
            "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Arrow(projectile)/Arrow02(100x100).png",
            "frame_number": 1,
            "cooldown": 100,
            "type": "arrow",             # fire arrow
            "gen_frame": 6,             
            "speed": 23,
            "damage": 10,
            "hitbox_width": 40,
            "hitbox_height": 10
        },
        "ATTACK2": {
            "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Archer/Arrow(projectile)/Arrow02(100x100).png",
            "frame_number": 1,
            "cooldown": 100,
            "type": "arrow",        
            "gen_frame": 9,             
            "speed": 30,
            "damage": 20,
            "hitbox_width": 40,
            "hitbox_height": 10
        }
    },
    "projectile_size": {
        "ATTACK1": {
            "size": DEFAULT_SIZE,
            "scale": con.SCREEN_WIDTH / 300,
            "offset": [int(con.SCREEN_WIDTH / 40), int(con.SCREEN_HEIGHT / 21.3)]
        },
        "ATTACK2": {
            "size": DEFAULT_SIZE,
            "scale": con.SCREEN_WIDTH / 300,
            "offset": [int(con.SCREEN_WIDTH / 40), int(con.SCREEN_HEIGHT / 21.3)]
        }
    }
}

KNIGHT_TEMPLAR_DATA = {
    "name": "Venator",
    "size": DEFAULT_SIZE,
    "scale": DEFAULT_SCALE,
    "offset": DEFAULT_OFFSET,
    "jumpable": True,
    "animations": {
        "IDLE":    {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar/Knight Templar-Idle.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar with shadows/Knight Templar-Idle.png",
                    "frame_number": 6,      
                    "cooldown": 110},       
        "WALK":    {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar/Knight Templar-Walk01.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar with shadows/Knight Templar-Walk01.png",
                    "frame_number": 8,                       # Fun fact: this guy has two types of walk (with shield at the side or in front), maybe implement later
                    "cooldown": 110},
        "ATTACK1": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar/Knight Templar-Attack01.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar with shadows/Knight Templar-Attack01.png", 
                    "frame_number": 7,
                    "cooldown": 65},
        "ATTACK2": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar/Knight Templar-Attack02.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar with shadows/Knight Templar-Attack02.png", 
                    "frame_number": 8,
                    "cooldown": 75},
        "ATTACK3": {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar/Knight Templar-Attack03.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar with shadows/Knight Templar-Attack03.png", 
                    "frame_number": 11,
                    "cooldown": 85},
        "HIT":     {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar/Knight Templar-Hurt.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar with shadows/Knight Templar-Hurt.png",
                    "frame_number": 4, 
                    "cooldown": 100},
        "DEATH":   {"file_air": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar/Knight Templar-Death.png",
                    "file_ground": "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar with shadows/Knight Templar-Death.png",
                    "frame_number": 4, 
                    "cooldown": 100},
    },
    "attack_active_frames": {
            "ATTACK1": [(4, 6)],       
            "ATTACK2": [(5, 6)],
            "ATTACK3": [(3, 4), (7, 8)]
    },
    "attack_width_scale": {
            "ATTACK1": 1.2,             
            "ATTACK2": 1,
            "ATTACK3": 1
    },
    "attack_damage": {
            "ATTACK1": 8,
            "ATTACK2": 8,
            "ATTACK3": 8
    }
}


CHARACTER_DATA = [KNIGHT_DATA, WEREBEAR_DATA, WIZARD_DATA, MINOTAUR_DATA, ARCHER_DATA, KNIGHT_TEMPLAR_DATA]  
LABELS = ["Ser Edward", "Tyland", "Luna", "Rem", "Arland", "Venator"]

ACTIONS = {
    "IDLE": 0,
    "WALK": 1,
    "ATTACK1": 2,
    "ATTACK2": 3,
    "ATTACK3": 4,
    "HIT": -2,
    "DEATH": -1
}


WIND_DATA = {
    "size": 512,
    "scale": 0.5,
    "animation": {"WIND": {"file_ground": "assets/wind.png", "frame_number": 16, "cooldown": 5}}
}

DICE_ROLLING_DATA = {
    "size": 96,
    "scale": con.SCREEN_WIDTH / 480,
    "rolling_duration": 2500,
    "animation": {"ROLLING": {"file_ground": "assets/dice_rolling.png", "frame_number": 11, "cooldown": 5}}
}

DICE_RESULT_DATA = {
    "size": 96,
    "scale": con.SCREEN_WIDTH / 290,
    "showing_duration": 2000,
    "animation": {"RESULT": {"file_ground": "assets/dice_results.png", "frame_number": 20}}
}
