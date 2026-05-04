import pygame
# from PIL import Image as PILImage  # used by GIF loader (main_menu_sky.gif) — not active

from src.modules.UI import constants as con
from src.modules.UI import CharDictionary as chardict

# GIF_PATH = "assets/main_menu_sky.gif"  # night sky GIF — swap load_menu_background below to use it

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

def load_animation_frames(animation_dict, size, scale):
    new_animation_dict = {}
    
    for action, data in animation_dict.items():
        new_animation_dict[action] = {"ground": [], "air": []}
        file_air = data.get("file_air")
        if file_air:
            air_sheet = pygame.image.load(data["file_air"]).convert_alpha()
        ground_sheet = pygame.image.load(data["file_ground"]).convert_alpha()
        
        frame_number = data["frame_number"]
 
        for x in range(frame_number):
            ground_frame = ground_sheet.subsurface(
                x * size,
                0,
                size,
                size
            )
            ground_frame = pygame.transform.scale(
                ground_frame,
                (size * scale, size * scale)
            )
            new_animation_dict[action]["ground"].append(ground_frame)

            if file_air:
                air_frame = air_sheet.subsurface(
                    x * size,
                    0,
                    size,
                    size
                )
                air_frame = pygame.transform.scale(
                    air_frame,
                    (size * scale, size * scale)
                )
                new_animation_dict[action]["air"].append(air_frame)

    return new_animation_dict


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

def draw_magic_effect(surface, frames, state, cx, cy, scale=6, frame_ms=120, wait_ms=1000, x_offset=0, y_offset=0):
    # draws one frame of a looping magic effect centered at (cx + x_offset, cy + y_offset),
    # scale multiplies the raw frame size before drawing
    # waits wait_ms ms after each full cycle before replaying
    now = pygame.time.get_ticks()
    if state["waiting"]:
        if now - state["wait_start"] >= wait_ms:
            state["frame"]   = 0
            state["waiting"] = False
        return
    frame_surf = frames[state["frame"]]
    if scale != 1:
        new_size = int(frame_surf.get_width() * scale)
        frame_surf = pygame.transform.scale(frame_surf, (new_size, new_size))
    surface.blit(frame_surf, (cx + x_offset - frame_surf.get_width()  // 2,
                               cy + y_offset - frame_surf.get_height() // 2))
    if now - state["time"] >= frame_ms:
        state["frame"] += 1
        state["time"]   = now
        if state["frame"] >= len(frames):
            state["frame"]      = 0
            state["waiting"]    = True
            state["wait_start"] = now


def load_magic_projectiles(scale=1):
    # loads all 4 magic projectile sprite sheets, each is a 100 by 100
    base = "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Magic(Projectile)/"
    size = 100
    sheets = {
        "priest_attack":   (base + "Priest-Attack_effect.png",    5),
        "priest_heal":     (base + "Priest-Heal_Effect.png",      4),
        "wizard_attack01": (base + "Wizard-Attack01_Effect.png", 10),
        "wizard_attack02": (base + "Wizard-Attack02_Effect.png",  7),
    }
    result = {}
    for key, (path, frame_count) in sheets.items():
        sheet  = pygame.image.load(path).convert_alpha()
        frames = []
        for x in range(frame_count):
            frame = sheet.subsurface(x * size, 0, size, size)
            if scale != 1:
                frame = pygame.transform.scale(frame, (size * scale, size * scale))
            frames.append(frame)
        result[key] = frames
    return result


# Update fighter animation n attack states
def update_fighter_animation(fighter):
    animation_cooldown = fighter.attack_cooldown_mult(fighter.action)

    # Determine what action is happening
    if fighter.health <= 0:
        fighter.health = 0
        if not fighter.death:
            fighter.sounds["death"].play()
        fighter.death = True
        new_action = "DEATH"
    elif fighter.stun:
        new_action = "HIT"
    elif fighter.attacking:
        if fighter.attack_type == 1:
            new_action = "ATTACK1"
        elif fighter.attack_type == 2:
            new_action = "ATTACK2"
        elif fighter.attack_type == 3:
            new_action = "ATTACK3"
        else:
            new_action = fighter.action
    elif fighter.dashing:
        new_action = "WALK"
    elif fighter.running:
        new_action = "WALK"
    else:
        new_action = "IDLE"

    # update action if changed
    if new_action != fighter.action:
        fighter.action = new_action
        fighter.frame_index = 0
        fighter.update_time = pygame.time.get_ticks()

    # check if on ground or in air
    if fighter.rect.bottom < con.FLOOR_Y:
        ground_state_key = "air"
    else:
        ground_state_key = "ground"

    # update image frame
    fighter.image = fighter.animation_list[fighter.action][ground_state_key][fighter.frame_index]

    # handle frame timing
    if pygame.time.get_ticks() - fighter.update_time > animation_cooldown:
        fighter.frame_index += 1
        fighter.update_time = pygame.time.get_ticks()

    # check if animation finished, loop frames and reset actions
    if fighter.frame_index >= len(fighter.animation_list[fighter.action][ground_state_key]):
        if fighter.death:
            fighter.frame_index = len(fighter.animation_list["DEATH"][ground_state_key]) - 1
        else:
            fighter.frame_index = 0
            if fighter.attacking:
                fighter.attacking = False
                fighter.attack_type = 0
                fighter.attack_sound_played = False
            if fighter.stun:
                fighter.stun = False

def update_wind_animation(fighter, surface):
    
    animation_cooldown = chardict.WIND_DATA["animation"]["WIND"]["cooldown"]
    wind_scaled_size = chardict.WIND_DATA["size"] * chardict.WIND_DATA["scale"]
    time = pygame.time.get_ticks()
    flip = False

    if fighter.dashing_direction == 1:  
        wind_x_offset = -(con.PLAYER_WIDTH // 2 + wind_scaled_size)   # dash right
    else:
        flip = True                               
        wind_x_offset = con.PLAYER_WIDTH // 2   # dash left

    wind_x = fighter.rect.centerx + wind_x_offset
    wind_y = fighter.rect.centery - (wind_scaled_size // 2)

    frame = fighter.wind_animation_list[fighter.wind_frame_index]
    frame = pygame.transform.flip(frame, flip, False)
    surface.blit(frame, (wind_x, wind_y))

 

    if time - fighter.wind_update_time > animation_cooldown:
        fighter.wind_frame_index += 1
        fighter.wind_update_time = time

    if fighter.wind_frame_index >= len(fighter.wind_animation_list):
        fighter.wind_frame_index = 0
        fighter.dashing = False
    