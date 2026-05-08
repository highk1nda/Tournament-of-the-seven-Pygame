import pygame
 
from src.modules.UI import constants as con
from src.modules.boons import Adrenaline

ICON_SIZE = 80

ICON_ROUND_DOT_GAP = 14
ICON_GAP = 10
BORDER_RADIUS = 2
BORDER_WIDTH = 5

ICON_Y = con.ROUND_DOT_Y + con.ROUND_DOT_RADIUS + ICON_ROUND_DOT_GAP

ICON_DIR = "assets/boons/icons/"
ICON_FILES = {
    "Sub Zero":           "sub_zero.png",
    "Scorching Ray":      "scorching_ray.png",
    "Area of Warding":    "area_of_warding.png",
    "Devil's Die":        "deviles_die.png",
    "Devil's Die curse":  "deviles_die_curse.png",
    "Devil's Die revive": "deviles_die_revive.png",
    "Adrenaline":         "adrenaline.png",
    "Last Stand":         "last_stand.png",
}

ON_COLOR = con.WHITE
OFF_COLOR = con.DARK_GREY
CURSE_COLOR = con.DARK_RED
REVIVE_COLOR = con.LIVE_GREEN
LAST_STAND_COLOR = con.LIGHT_GREEN
ADRENALINE_COLOR = con.AMBER

ACTIVE_BORDER_COLOR = con.YELLOW
PASSIVE_BORDER_COLOR = con.BLUE

CD_FONT = con.font_Big
CD_FONT_COLOR = con.WHITE

def load_icons():
    icon_imgs = {}

    for name, file in ICON_FILES.items():
        file_path = ICON_DIR + file
        img = pygame.image.load(file_path).convert()
        
        scaled_img = pygame.transform.smoothscale(img, (ICON_SIZE, ICON_SIZE))
        icon_imgs[name] = scaled_img
    return icon_imgs

def draw_single_icon(surface, icon, x, y, bg_color, border_color):
    icon_rect = pygame.Rect(x, y, ICON_SIZE, ICON_SIZE)
    pygame.draw.rect(surface, bg_color, icon_rect, border_radius=BORDER_RADIUS)
    pygame.draw.rect(surface, border_color, icon_rect, BORDER_WIDTH, border_radius=BORDER_RADIUS)
    surface.blit(icon, (x, y), special_flags=pygame.BLEND_MULT)     # BLEND_MULT changes white background color only

def draw_cooldown(surface, cd, x, y):
    seconds = cd // 1000 + 1
    font = CD_FONT
    text_surface = font.render(str(seconds), True, CD_FONT_COLOR)
    surface.blit(text_surface, (x + ICON_SIZE // 2 - text_surface.get_width() // 2,
                                y + ICON_SIZE // 2 - text_surface.get_height() // 2))

def devils_die_icon(surface, icons, x, y, fighter, fight_state, dice_player, dice_result, dice_saved, live_result=None):
    rolling = (fight_state == "dice_roll" and dice_player is fighter)
    live_revive = (rolling and live_result is not None and live_result == "REVIVE")
    live_curse = (rolling and live_result is not None and live_result == "CURSE")
    reviving = (fight_state == "revive_animation" and dice_player is fighter)
    revived = (dice_result == "revive" and dice_saved is fighter and fight_state not in ["dice_roll", "revive_animation"])
    cursed = (dice_result == "curse" and dice_saved is fighter)

    if live_curse or cursed:
        draw_single_icon(surface, icons["Devil's Die curse"], x, y, CURSE_COLOR, PASSIVE_BORDER_COLOR)
    elif live_revive or reviving or revived:
        draw_single_icon(surface, icons["Devil's Die revive"], x, y, REVIVE_COLOR, PASSIVE_BORDER_COLOR)
    elif rolling:
        draw_single_icon(surface, icons["Devil's Die"], x, y, ON_COLOR, PASSIVE_BORDER_COLOR)
    else:
        draw_single_icon(surface, icons["Devil's Die"], x, y, OFF_COLOR, PASSIVE_BORDER_COLOR)

def adrenaline_icon(surface, icon, x, y, count):
    # draw grey background
    icon_rect = pygame.Rect(x, y, ICON_SIZE, ICON_SIZE)
    pygame.draw.rect(surface, OFF_COLOR, icon_rect, border_radius=BORDER_RADIUS)
    pygame.draw.rect(surface, PASSIVE_BORDER_COLOR, icon_rect, BORDER_WIDTH, border_radius=BORDER_RADIUS)

    charge_h = int(ICON_SIZE * count / Adrenaline.MAX_ADRENALINE)
    if charge_h > 0:
        charge_y = y + ICON_SIZE - charge_h
        full_clip = surface.get_clip()

        # draw color in specific area
        surface.set_clip(pygame.Rect(x, charge_y, ICON_SIZE, charge_h))
        pygame.draw.rect(surface, ADRENALINE_COLOR, pygame.Rect(x, y, ICON_SIZE, ICON_SIZE), border_radius=BORDER_RADIUS)
        
        # draw border
        surface.set_clip(full_clip)
        pygame.draw.rect(surface, PASSIVE_BORDER_COLOR, pygame.Rect(x, y, ICON_SIZE, ICON_SIZE), BORDER_WIDTH, border_radius=BORDER_RADIUS)

    # draw icon image
    surface.blit(icon, (x, y), special_flags=pygame.BLEND_MULT)

def draw_boon_icons(surface, fighter, active_boon, passive_boon, icons, right_side, 
                    fight_state, dice_player, dice_result, dice_saved, live_result):
    current_time = pygame.time.get_ticks()

    if right_side:
        icon_x = con.healthbar_xx + con.healthbar_width - ICON_SIZE
    else:
        icon_x = con.healthbar_x

    # draw active boon icon
    active_boon_name = active_boon["name"]
    icon = icons[active_boon_name]
    cd = max(0, fighter.boon_cooldown_end - current_time)
    if cd > 0:
        # in cooldown
        draw_single_icon(surface, icon, icon_x, ICON_Y, OFF_COLOR, ACTIVE_BORDER_COLOR)
        draw_cooldown(surface, cd, icon_x, ICON_Y)
    else:
        draw_single_icon(surface, icon, icon_x, ICON_Y, ON_COLOR, ACTIVE_BORDER_COLOR)

    # draw passive boon icon
    icon_y = ICON_Y + ICON_SIZE + ICON_GAP
    passive_boon_name = passive_boon
    if passive_boon_name == "devils_die":
        devils_die_icon(surface, icons, icon_x, icon_y, fighter, fight_state, 
                        dice_player, dice_result, dice_saved, live_result)
    
    elif passive_boon_name == "last_stand":
        icon = icons["Last Stand"]
        active = fighter.last_stand_active
        if active:
            draw_single_icon(surface, icon, icon_x, icon_y, LAST_STAND_COLOR, PASSIVE_BORDER_COLOR)
        else:
            draw_single_icon(surface, icon, icon_x, icon_y, OFF_COLOR, PASSIVE_BORDER_COLOR)
    
    elif passive_boon_name == "adrenaline":
        icon = icons["Adrenaline"]
        count = fighter.consecutive_hits
        adrenaline_icon(surface, icon, icon_x, icon_y, count)

