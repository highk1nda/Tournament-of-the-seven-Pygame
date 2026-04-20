import pygame

pygame.font.init()
pygame.mixer.init()


#constant variables to stop accumalating technical debt
SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 600

SCREEN_SHAKE_DURATION = 300 # ms
SCREEN_SHAKE_INTENSITY = 3  # maximum offset

FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 , 0)
GREEN = (26, 66, 28)
LIGHT_GREEN = (0, 255, 0)
ORANGE = (222, 110, 0)
BLUE = (80, 180, 255)

FONT_NORMAL = pygame.font.SysFont(None, 40)
FONT_BIG = pygame.font.SysFont(None, 44)
FONT_SMALL = pygame.font.SysFont(None, 30)
FONT_VERY_BIG = pygame.font.SysFont(None, 70)

FLOOR_Y      = 510
FLOOR_HEIGHT = SCREEN_HEIGHT - FLOOR_Y

CHARACTER_DATA           = [100, 7, [40, 37]]  # 0 - size, 1 - scale, 2 - offset
PLAYER_WIDTH             = 140
PLAYER_HEIGHT            = 140
KNIGHT_ANIMATION_STEPS         = [6, 8, 7, 10, 11, 4, 4, 4]
WEREBEAR_ANIMATION_STEPS       = [6, 8, 9, 13, 9, 4, 4]
KNIGHT_TEMPLAR_ANIMATION_STEPS = [6, 8, 8, 7, 8, 11, 4, 4, 4]
WIZARD_ANIMATION_STEPS         = [6, 8, 15, 6, 10, 12, 6, 7, 4, 4]

ATTACK_ACTIVE_FRAMES = {
    0: None,
    1: [(3, 5)],        # (Start, End) index of animation
    2: [(3, 5), (7, 9)],
    3: [(7, 9)]
}                       # for knight, test

ATTACK_WIDTH_SCALE = {      # attacking hitbox width scale
    0: None,
    1: 0.6,
    2: 1,
    3: 1.5
}                       # for knight, test

KNOCKBACK_DISTANCE = 35

ANIMATION_COOLDOWNS = {
    0: 110,        # 110 ms between frames
    1: 110,
    2: 65,
    3: 75,
    4: 85,
    -2: 100,
    -1: 100
}

WIND_SIZE = 512
WIND_SCALE = 0.5
WIND_FRAMES = 16
WIND_SCALE_SIZE = WIND_SCALE * WIND_SIZE

HEALTH_BAR_WIDTH = 400
HEALTH_BAR_HEIGHT = 30
HEALTH_BAR_LEFT_X = 20
HEALTH_BAR_RIGHT_X = SCREEN_WIDTH - HEALTH_BAR_LEFT_X - HEALTH_BAR_WIDTH
HEALTH_BAR_Y = 20

HEALTH_BAR_BORDER_THICKNESS = 2

DASHING_BAR_WIDTH = HEALTH_BAR_WIDTH + (HEALTH_BAR_BORDER_THICKNESS * 2)
DASHING_BAR_HEIGHT = 5
DASHING_BAR_HEALTH_BAR_DISTANCE = 4
DASHING_BAR_LEFT_X = HEALTH_BAR_LEFT_X - HEALTH_BAR_BORDER_THICKNESS
DASHING_BAR_RIGHT_X = HEALTH_BAR_RIGHT_X - HEALTH_BAR_BORDER_THICKNESS
DASHING_BAR_Y = HEALTH_BAR_Y + HEALTH_BAR_HEIGHT + HEALTH_BAR_BORDER_THICKNESS + DASHING_BAR_HEALTH_BAR_DISTANCE
CHARGES_DISTANCE_IN_HALF = 4
DASHING_BAR_COLOR = LIGHT_GREEN

ROUND_DOT_RADIUS = 12
ROUND_DOT_GAP = 4
ROUND_DOT_Y = DASHING_BAR_Y + DASHING_BAR_HEIGHT + ROUND_DOT_RADIUS + 10
ROUND_DOT_BORDER_THICKNESS = 1

PLAYER_1_INIT_X = 160
PLAYER_2_INIT_X = 700

PLAYER_SPEED = 8
JUMPING_SPEED = -30

DASHING_SPEED = 80
DASHING_BRAKE = 0.5
DASHING_COOLDOWN = 2000   # ms -- 1000ms = 1s
DASHING_CHARGE = 2     # Dashing charge system:
                       # Player has 2 dash charges in every Shift press window
                       # Cooldown is triggered when:
                       #    1) 2 dash charges are both used, or
                       #    2) Shift is released after dash (at least 1 dash)

GROUND_FRICTION = 0.7
AIR_FRICTION = 0.93
GRAVITY = 2


ROUND_DURATION = 68 * 1000  # 68 seconds
MAX_WINS = 2
ROUND_TEXT_DURATION = 1700  # ms
ROUND_TEXT_Y = 80
DEATH_DURATION = 1500  # ms
FADE_OUT_DURATION = 500  # ms
MAX_ALPHA = 255  # full black

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
    "attack1": pygame.K_COMMA,
    "attack2": pygame.K_PERIOD,
    "attack3": pygame.K_SLASH,
    "dash": pygame.K_RSHIFT
}

ACTIONS = {
    "IDLE": 0,
    "WALK": 1,
    "ATTACK1": 2,
    "ATTACK2": 3,
    "ATTACK3": 4,
    "HIT": -2,
    "DEATH": -1
}

menumusic: str = "assets/sfx/menmusica.mp3"
forestsound: str = "assets/sfx/forest-ambience-296528.mp3"
menuscreenimage: str = "assets/forest.jpg"
fightscreenimage: str = "assets/forest.jpg"

wind = "assets/wind.png"
Knight       = "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight/Knight/Knight.png"
Werebear     = "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Werebear/Werebear/Werebear.png"
KnightTemplar = "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Knight Templar/Knight Templar/Knight Templar.png"
Wizard       = "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/Characters(100x100)/Wizard/Wizard/Wizard.png"

display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load(menuscreenimage).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

knight_sheet        = pygame.image.load(Knight).convert_alpha()
werebear_sheet      = pygame.image.load(Werebear).convert_alpha()
knight_templar_sheet = pygame.image.load(KnightTemplar).convert_alpha()
wizard_sheet        = pygame.image.load(Wizard).convert_alpha()

wind_sheet = pygame.image.load(wind).convert_alpha()

background_music = pygame.mixer.Sound(menumusic)
