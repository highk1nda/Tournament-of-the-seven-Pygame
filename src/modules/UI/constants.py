import pygame

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

FLOOR_COLOR = (106, 80, 80)

# Character select screen colours
SELECT_BG_COLOR        = (30, 30, 30)
SELECT_P1_BTN_COLOR    = (160, 45, 45)
SELECT_P2_BTN_COLOR    = (45, 70, 160)
SELECT_FIGHT_BTN_COLOR = (60, 140, 60)
SELECT_P1_LABEL_COLOR  = (210, 65, 65)
SELECT_P2_LABEL_COLOR  = (65, 100, 210)
BUTTON_DISABLED_COLOR  = (70, 70, 70)

# =============== Buttons ===============

buttonwidth = SCREEN_WIDTH / 5
buttonheight = SCREEN_HEIGHT / 15
buttonspacing = SCREEN_HEIGHT / 10

button_y = (center_y) - (buttonspacing * 2)
button_x = (center_x) - (buttonwidth / 2)

# =============== Select Char,Boon,Map Screen ===============

# Select Char Screen layout and sizes
SELECT_LOAD_SCALE   = 4
SELECT_PREVIEW_SIZE = 260

SELECT_BTN_W       = 120
SELECT_BTN_H       = 42
SELECT_BTN_GAP     = 10
SELECT_GRID_WIDTH  = 3 * SELECT_BTN_W + 2 * SELECT_BTN_GAP

SELECT_P1_CX       = SCREEN_WIDTH // 4
SELECT_P2_CX       = SCREEN_WIDTH * 3 // 4

_sel_block_top     = (SCREEN_HEIGHT - 517) // 2
SELECT_LABEL_Y     = _sel_block_top
SELECT_PREVIEW_Y   = _sel_block_top + 46
SELECT_BTN_ROW1_Y  = SELECT_PREVIEW_Y + SELECT_PREVIEW_SIZE + 14
SELECT_BTN_ROW2_Y  = SELECT_BTN_ROW1_Y + SELECT_BTN_H + SELECT_BTN_GAP
SELECT_FIGHT_Y     = SELECT_BTN_ROW2_Y + SELECT_BTN_H + 18
SELECT_FIGHT_BTN_X = SCREEN_WIDTH // 2 - 100

BOON_BTN_W   = 200
BOON_BTN_H   = 40
BOON_BTN_GAP = 8

# Map screen layout
MAP_PREVIEW_W  = 700
MAP_PREVIEW_H  = 340
MAP_PREVIEW_X  = (SCREEN_WIDTH - MAP_PREVIEW_W) // 2
MAP_PREVIEW_Y  = 80
MAP_NAV_BTN_W  = 130
MAP_NAV_BTN_H  = 45
MAP_NAV_Y      = MAP_PREVIEW_Y + MAP_PREVIEW_H + 30
MAP_FIGHT_BTN_W = 160
MAP_FIGHT_BTN_H = 45
MAP_CX          = SCREEN_WIDTH // 2

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

# music
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
