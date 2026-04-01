import pygame

from src.modules.UI import constants as con

def load_animation_frames(sprite_sheet, size, scale, animation_steps):
    animation_list = []

    for y, animation in enumerate(animation_steps):
        row = []
        for x in range(animation):
            frame = sprite_sheet.subsurface(
                x * size,
                y * size,
                size,
                size
            )
            frame = pygame.transform.scale(
                frame,
                (size * scale, size * scale)
            )

            row.append(frame)
        animation_list.append(row)
    return animation_list


# Update fighter animation & attack states
def update_fighter_animation(fighter):
    animation_cooldown = 110  # 110 ms between frames

    # Determine what action is happening
    if fighter.health <= 0:
        fighter.health = 0
        fighter.death = True
        new_action = con.ACTIONS["DEATH"]
    elif fighter.stun:
        new_action = con.ACTIONS["HIT"]
    elif fighter.attacking:
        if fighter.attack_type == 1:
            new_action = con.ACTIONS["ATTACK1"]
        elif fighter.attack_type == 2:
            new_action = con.ACTIONS["ATTACK2"]
        elif fighter.attack_type == 3:
            new_action = con.ACTIONS["ATTACK3"]
        else:
            new_action = fighter.action
    elif fighter.running:
        new_action = con.ACTIONS["WALK"]
    else:
        new_action = con.ACTIONS["IDLE"]

    # update action if changed
    if new_action != fighter.action:
        fighter.action = new_action
        fighter.frame_index = 0
        fighter.update_time = pygame.time.get_ticks()

    # update image frame
    fighter.image = fighter.animation_list[fighter.action][fighter.frame_index]

    # handle frame timing
    if pygame.time.get_ticks() - fighter.update_time > animation_cooldown:
        fighter.frame_index += 1
        fighter.update_time = pygame.time.get_ticks()

    # check if animation finished, loop frames and reset actions
    if fighter.frame_index >= len(fighter.animation_list[fighter.action]):
        if fighter.death:
            fighter.frame_index = len(fighter.animation_list[-1]) - 1
        else:
            fighter.frame_index = 0
            if fighter.attacking:
                fighter.attacking = False
                fighter.attack_sound_played = False
            if fighter.stun:
                fighter.stun = False
