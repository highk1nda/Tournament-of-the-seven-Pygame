import pygame


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

    # 0: idle, 1: run, 2: attack1, 3: attack2, 4: attack3, -2: hit stun, -1: death
    # Determine what action is happening
    if fighter.stun:
        new_action = -2
    elif fighter.attacking:
        if fighter.attack_type == 1:
            new_action = 2 #attack type 1
        elif fighter.attack_type == 2:
            new_action = 3 #attack type 2
        elif fighter.attack_type == 3:
            new_action = 4 #attack type 3
        else:
            new_action = fighter.action
    elif fighter.running:
        new_action = 1  # walk
    else:
        new_action = 0  # idle

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

    # loop frames and reset actions
    if fighter.frame_index >= len(fighter.animation_list[fighter.action]):
        fighter.frame_index = 0
        if fighter.attacking:
            fighter.attacking = False
            fighter.attack_sound_played = False
        if fighter.stun:
            fighter.stun = False
