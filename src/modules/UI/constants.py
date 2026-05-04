import pygame
from pathlib import Path

pygame.font.init()
pygame.mixer.init()

# constant variables to stop accumalating technical debt:

# =============== Initial Screen ===============

SCREEN_WIDTH  = 1920
SCREEN_HEIGHT = 1080

center_x = SCREEN_WIDTH / 2
center_y = SCREEN_HEIGHT / 2

window_size_index = 3

display_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

volume = 1
brightness = 100

SCREEN_SHAKE_DURATION = 300 # ms
SCREEN_SHAKE_INTENSITY = 3  # maximum offset

FPS = 60

FLOOR_Y      = SCREEN_HEIGHT / 1.1
FLOOR_HEIGHT = SCREEN_HEIGHT - FLOOR_Y

PLAYER_1_X = int(SCREEN_WIDTH * 0.15)
PLAYER_2_X = int(SCREEN_WIDTH * 0.7)
PLAYER_WIDTH = int(SCREEN_WIDTH / 7.14)
PLAYER_HEIGHT = int(SCREEN_HEIGHT / 4.28)

# =============== Colors ===============
BLACK = (0, 0, 0)
RED = (255, 0 , 0)
DARK_RED = (140, 40, 40)
DARK_BLUE = (40, 40, 140)
WHITE = (255, 255, 255)
RED = (255, 0 , 0)
GREEN = (26, 66, 28)
YELLOW = (212, 175, 55)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
CYAN = (0, 255, 0)
ORANGE = (222, 110, 0)
LIGHT_GREEN = (0, 255, 0)
BLUE = (80, 180, 255)
DARK_GREEN = (1,50,32)

FLOOR_COLOR = (106, 80, 80)

buttonwidth = SCREEN_WIDTH / 5
buttonheight = SCREEN_HEIGHT / 15
buttonspacing = SCREEN_HEIGHT / 10

button_y = (center_y) - (buttonspacing * 2)
button_x = (center_x) - (buttonwidth / 2)

# Character select screen colours
select_bg_color = (30, 30, 30)
select_p1_butt_color = (160, 45, 45)
select_p2_butt_color = (45, 70, 160)
select_fight_butt_color = (60, 140, 60)
select_p1_label_color = (210, 65, 65)
select_p2_label_color = (65, 100, 210)
butt_disabled_color = (70, 70, 70)

# =============== Buttons ===============

buttonwidth = SCREEN_WIDTH / 5
buttonheight = SCREEN_HEIGHT / 15
buttonspacing = SCREEN_HEIGHT / 10

button_y = (center_y) - (buttonspacing * 2)
button_x = (center_x) - (buttonwidth / 2)

# =============== Select Char,Boon,Map Screen ===============

# Select Char Screen layout and sizes
select_load_scale = 4
select_preview_size = 260

select_butt_width = 120
select_butt_height = 42
select_butt_gap = 10
select_grid_width = 3 * select_butt_width + 2 * select_butt_gap

select_p1_cx = SCREEN_WIDTH // 4
select_p2_cx = SCREEN_WIDTH * 3 // 4

_sel_block_top = (SCREEN_HEIGHT - 517) // 2
select_label_y = _sel_block_top
select_preview_y = _sel_block_top + 46
select_butt_row1_y = select_preview_y + select_preview_size + 14
select_butt_row2_y = select_butt_row1_y + select_butt_height + select_butt_gap
select_fight_y = select_butt_row2_y + select_butt_height + 18
select_fight_butt_x = int(center_x) - 100

# Boon screen colours
boon_active_color = (70, 130, 80)
boon_panel_color  = (40, 42, 58)
boon_back_color   = (120, 50, 50)

# Boon screen grid dimensions
boon_cell_width  = 150
boon_cell_height = 55
boon_grid_width  = 2 * boon_cell_width  + select_butt_gap
boon_grid_height = 2 * boon_cell_height + select_butt_gap

boon_p1_grid_x = select_p1_cx - boon_grid_width // 2
boon_p2_grid_x = select_p2_cx - boon_grid_width // 2

# Map screen layout
map_cx = int(center_x)
map_preview_width = int(SCREEN_WIDTH * 0.65)                        # 65% of screen width
map_preview_height = int(map_preview_width * 1120 / 1940)           # preserve 1940:1120 source ratio
map_preview_x = (SCREEN_WIDTH - map_preview_width) // 2
map_preview_y = 80
map_char_rel_x = int(map_preview_width * 0.10)                      # character x offset inside preview
map_nav_butt_width = 130
map_nav_butt_height = 45
map_nav_y = map_preview_y + map_preview_height + 50
map_fight_butt_width = 160
map_fight_butt_height = 45

# =============== Health Bar ===============

healthbar_width = int(SCREEN_WIDTH * 0.4)
healthbar_height = int(SCREEN_WIDTH * 0.037)
healthbar_padding = max(1, int(SCREEN_WIDTH * 0.001))
healthbar_x = int(SCREEN_WIDTH * 0.02)
healthbar_y = int(SCREEN_WIDTH * 0.02)
healthbar_xx = int(SCREEN_WIDTH * 0.58)

# =============== Dashing ===============

DASHING_BAR_WIDTH = int(SCREEN_WIDTH * 0.4)
DASHING_BAR_HEIGHT = int(SCREEN_HEIGHT / 150)
DASHING_BAR_HEALTH_BAR_DISTANCE = int(SCREEN_HEIGHT / 13)
DASHING_BAR_LEFT_X = healthbar_x
DASHING_BAR_RIGHT_X = healthbar_xx
DASHING_BAR_Y = int(healthbar_y * 3)
CHARGES_DISTANCE_IN_HALF = int(SCREEN_WIDTH * 0.0042)
DASHING_BAR_COLOR = LIGHT_GREEN

DASHING_SPEED = 80
DASHING_BRAKE = 0.5
DASHING_COOLDOWN = 2000   # ms -- 1000ms = 1s
DASHING_CHARGE = 2     # Dashing charge system:
                       # Player has 2 dash charges in every Shift press window
                       # Cooldown is triggered when:
                       #    1) 2 dash charges are both used, or
                       #    2) Shift is released after dash (at least 1 dash)

# =============== Round Logic ===============

ROUND_DOT_RADIUS = int(SCREEN_HEIGHT * 0.02)
ROUND_DOT_GAP = int(SCREEN_HEIGHT * 0.004)
ROUND_DOT_Y = DASHING_BAR_Y + DASHING_BAR_HEIGHT + ROUND_DOT_RADIUS + int(SCREEN_HEIGHT * 0.01)
ROUND_DOT_BORDER_THICKNESS = 1
ROUND_FONT = pygame.font.SysFont(None, int(SCREEN_HEIGHT * 0.1))

ROUND_DURATION = 68 * 1000  # 68 seconds
MAX_WINS = 2
ROUND_TEXT_DURATION = 1700  # ms
ROUND_TEXT_Y = int(SCREEN_HEIGHT * 0.15)
DEATH_DURATION = 1500  # ms
FADE_OUT_DURATION = 500  # ms
MAX_ALPHA = 255  # full black

# =============== Physical Variables ===============

PLAYER_SPEED = 8
JUMPING_SPEED = -30
KNOCKBACK_DISTANCE = 35

GROUND_FRICTION = 0.7
AIR_FRICTION = 0.93
GRAVITY = 2
DASHING_GRAVITY = 0.5

# =============== Player ===============

P1_CONTROLS = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "up": pygame.K_w,
    "attack1": pygame.K_r,
    "attack2": pygame.K_f,
    "attack3": pygame.K_v,
    "dash": pygame.K_LSHIFT
}

P2_CONTROLS = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "attack1": pygame.K_SLASH,
    "attack2": pygame.K_PERIOD,
    "attack3": pygame.K_COMMA,
    "dash": pygame.K_RSHIFT
}

# =============== Assets ===============
ACTIONS = {
    "IDLE": 0,
    "WALK": 1,
    "ATTACK1": 2,
    "ATTACK2": 3,
    "ATTACK3": 4,
    "HIT": -2,
    "DEATH": -1
}

PLAYER_1_X = int(SCREEN_WIDTH * 0.15)
PLAYER_2_X = int(SCREEN_WIDTH * 0.7)

# Music

# assetdir = Path(__file__).resolve().parent.parent
# assetdir = assetdir/"assets"
# menumusic: str = f"{assetdir}/sfx/menmusica.mp3"
# fightmusic: str = f"{assetdir}/sfx/fightmusica.mp3"
menumusic: str = "assets/sfx/menmusica.mp3"
fightmusic: str = "assets/sfx/fightmusica.mp3"
forestsound: str = "assets/sfx/forest-ambience-296528.mp3"
menuscreenimage: str = "assets/forest.jpg" # DEAFULTIMAGE, not changable from game
fightscreenimage: str = "assets/Colleseum.png" # DEAFULTIMAGE, changable in MapScreen.py

background_music = pygame.mixer.Sound(menumusic)
fight_music      = pygame.mixer.Sound(fightmusic)
select_sound     = pygame.mixer.Sound("assets/sfx/select2.mp3")
ui_error_sound   = pygame.mixer.Sound("assets/sfx/floraphonic-arcade-ui-4.mp3")
exit_sound       = pygame.mixer.Sound("assets/sfx/musicholder-woosh-260275.mp3")

forest_sfx = pygame.mixer.Sound(forestsound)

# backgrounds
background = pygame.transform.scale(pygame.image.load(fightscreenimage).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

fight_backgrounds = {
    "map1": background,
    "map2": pygame.transform.scale(pygame.image.load("assets/Heaven.png").convert(), (SCREEN_WIDTH, SCREEN_HEIGHT)),
}

# =============== Selections ===============

# Store selected character indices (in SelectCharScreen)
p1_selected = None
p2_selected = None
p1_char_idx = 0
p2_char_idx = 1

# Store selected boons (in Boon Screen)
p1_boon = None
p2_boon = None

# Store selected map (dynamicly changable btw, its set in MapScreen)
selected_map = "map1"

# fonts
font_XLarge = pygame.font.SysFont(None, 64)
font_Large = pygame.font.SysFont(None, 46)
font_Big = pygame.font.SysFont(None, 35)
font_Medium = pygame.font.SysFont(None, 32)
font_Small = pygame.font.SysFont(None, 29)
font_Tiny = pygame.font.SysFont(None, 16)