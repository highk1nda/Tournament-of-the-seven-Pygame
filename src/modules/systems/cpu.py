import random
import pygame
from src.modules.UI import constants as con

EDGE_MARGIN = 80  # 80px from screen edge before treating the wall as blocking, so the char wont get stuck trying to retreat to the wall

LEVELS = {
    1: {
        "attack_range":    90, # how close the CPU needs to be, to start attacking
        "min_attack_dist": 10,  # if the CPU is closer than this, it will try to step back to get in range 
        "retreat_health":  50, # CPU starts retreating when health drops to 50 or below
        "attack_cooldown": 1100,  # ms between attacks
        "jump_chance":     0.008,
        "dash_chance":     0.003,
        "retreat_jump":    0.02,
        "attack_weights":  (33, 34, 33),
    },
    2: {
        "attack_range":    120,
        "min_attack_dist": 10,
        "retreat_health":  30, # CPU starts retreating when health drops to 30 or below
        "attack_cooldown": 600,
        "jump_chance":     0.02,
        "dash_chance":     0.01,
        "retreat_jump":    0.05,
        "attack_weights":  (33, 34, 33),
    },
    3: {
        "attack_range":    150,
        "min_attack_dist": 10,  # enemy gets stuck trying to retreat if min_attack_dist is too high, needs to be balanced with retreat_health too
        "retreat_health":  0,   # never retreats
        "attack_cooldown": 0,   # always tries to hit whenever in range
        "jump_chance":     0.04,
        "dash_chance":     0.02,
        "retreat_jump":    0.0,
        "attack_weights":  (2.5, 95, 2.5),
    },
}


class CPUController:
    def __init__(self, level=1):
        self.last_attack_time = 0
        cfg = LEVELS[level]
        self.attack_range    = cfg["attack_range"]
        self.min_attack_dist = cfg["min_attack_dist"]
        self.retreat_health  = cfg["retreat_health"]
        self.attack_cooldown = cfg["attack_cooldown"]
        self.jump_chance     = cfg["jump_chance"]
        self.dash_chance     = cfg["dash_chance"]
        self.retreat_jump    = cfg["retreat_jump"]
        self.attack_weights  = cfg["attack_weights"]
        
    # takes the fighter's controls dict, returns one attack key picked randomly based on attack_weights
    def pick_attack(self, controls):
        attack_options = [controls["attack1"], controls["attack2"], controls["attack3"]]
        chosen = random.choices(attack_options, weights=self.attack_weights) # gives a thing from attack_options with the specified probabilities in attack_weights
        return chosen[0]

    def can_attack(self, now, fighter):
        cooldown_ready = now - self.last_attack_time >= self.attack_cooldown
        not_busy = not fighter.attacking
        return not_busy and cooldown_ready

    def decide(self, fighter, target):
        controls = fighter.controls
        keys = dict.fromkeys(
            [controls["left"], controls["right"], controls["up"], controls["attack1"], controls["attack2"], controls["attack3"], controls["dash"]],
            False
        )

        incapacitated = fighter.stun or fighter.death
        if incapacitated:
            return keys

        now      = pygame.time.get_ticks()
        to_right = target.rect.centerx > fighter.rect.centerx

        # gap between the facing edges of the two rects (negative is overlapping)
        if to_right:
            gap = target.rect.left - fighter.rect.right
        else:
            gap = fighter.rect.left - target.rect.right

        # true when the wall blocks the natural retreat direction
        against_left_wall  = to_right and fighter.rect.left < EDGE_MARGIN
        against_right_wall = not to_right and fighter.rect.right > con.SCREEN_WIDTH - EDGE_MARGIN
        cornered = against_left_wall or against_right_wall

        low_health   = fighter.health <= self.retreat_health
        in_range     = gap < self.attack_range
        too_close    = gap < self.min_attack_dist
        sweet_spot   = gap <= self.attack_range

        if low_health and in_range:
            if cornered:
                keys[controls["right"] if to_right else controls["left"]] = True
                if not fighter.jumping:
                    keys[controls["up"]] = True
            else:
                keys[controls["left"] if to_right else controls["right"]] = True
                can_jump = not fighter.jumping and random.random() < self.retreat_jump
                if can_jump:
                    keys[controls["up"]] = True
            # counter attack while retreating if in range
            far_enough = gap >= self.min_attack_dist
            if far_enough and self.can_attack(now, fighter):
                keys[self.pick_attack(controls)] = True
                self.last_attack_time = now

        elif too_close:
            if cornered:
                keys[controls["right"] if to_right else controls["left"]] = True
                if not fighter.jumping:
                    keys[controls["up"]] = True
            else:
                # step back so the hitbox can reach
                keys[controls["left"] if to_right else controls["right"]] = True
            # swing while stepping back if cooldown is ready
            if self.can_attack(now, fighter):
                keys[self.pick_attack(controls)] = True
                self.last_attack_time = now

        elif sweet_spot:
            # if sweet spot -> attack
            if self.can_attack(now, fighter):
                keys[self.pick_attack(controls)] = True
                self.last_attack_time = now

        else:
            # if too far -> close the gap and go to the player
            keys[controls["right"] if to_right else controls["left"]] = True
            can_jump = not fighter.jumping and random.random() < self.jump_chance
            can_dash = not fighter.dashing and random.random() < self.dash_chance
            if can_jump:
                keys[controls["up"]] = True
            if can_dash:
                keys[controls["dash"]] = True

        return keys
