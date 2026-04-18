import pygame

from src.modules.UI import constants as con

#TODO: We can use this base function to implement a real background gif later,
# but for now it just loads the main menu animation frames and darkens them to use as a background in the menu and character select screens.
def load_menu_background(width, height):
    dark = pygame.Surface((width, height))
    dark.set_alpha(80)
    dark.fill((0, 0, 0))

    frames = []
    i = 1
    while True:
        try:
            img = pygame.image.load(f"assets/mainmenu_frames/frame_{i:03d}.png").convert()
        except:
            break  # no more frames
        img = pygame.transform.scale(img, (width, height))
        img.blit(dark, (0, 0))
        frames.append(img)
        i += 1
    return frames

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


#TODO: rewrite my main render char function so the characters image will actually take the space that eye can see, instead of being scaled to the size of the sprite sheet, which includes a lot of empty space.
def crop_and_scale_frames(frames, target_height):
    #Used in preview!!!
    bounds = frames[0].get_bounding_rect()
    for frame in frames[1:]:
        bounds = bounds.union(frame.get_bounding_rect())
    #Used in preview!!!
    # crop each frame to box, then scale everything to the height needed (with aspect ratio kept and other dimensions)
    cropped = [frame.subsurface(bounds).copy() for frame in frames]
    scale = target_height / bounds.height
    w = int(bounds.width  * scale)
    h = int(bounds.height * scale)
    return [pygame.transform.scale(frame, (w, h)) for frame in cropped]

# Update fighter animation n attack states
def update_fighter_animation(fighter):
    animation_cooldown = con.ANIMATION_COOLDOWNS[fighter.action]

    # Determine what action is happening
    if fighter.health <= 0:
        fighter.health = 0
        if not fighter.death:
            fighter.sounds["death"].play()
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
    elif fighter.dashing:
        new_action = con.ACTIONS["WALK"]
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
                fighter.attack_type = 0
                fighter.attack_sound_played = False
            if fighter.stun:
                fighter.stun = False

def update_wind_animation(fighter, surface):
    
    animation_cooldown = 5
    time = pygame.time.get_ticks()
    flip = False

    if fighter.dashing_direction == 1:  
        wind_x_offset = -(con.PLAYER_WIDTH // 2 + con.WIND_SCALE_SIZE)   # dash right
    else:
        flip = True                               
        wind_x_offset = con.PLAYER_WIDTH // 2   # dash left

    wind_x = fighter.rect.centerx + wind_x_offset
    wind_y = fighter.rect.centery - (con.WIND_SCALE_SIZE // 2)

    frame = fighter.wind_animation_list[fighter.wind_frame_index]
    frame = pygame.transform.flip(frame, flip, False)
    surface.blit(frame, (wind_x, wind_y))

 

    if time - fighter.wind_update_time > animation_cooldown:
        fighter.wind_frame_index += 1
        fighter.wind_update_time = time

    if fighter.wind_frame_index >= len(fighter.wind_animation_list):
        fighter.wind_frame_index = 0
        fighter.dashing = False
    