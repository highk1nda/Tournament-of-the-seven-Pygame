import pygame

pygame.mixer.init()


#constant variables to stop accumalating technical debt
SCREEN_WIDTH  = 1000
SCREEN_HEIGHT = 600

FPS = 60

RED = (255, 0 , 0)
WHITE = (255, 255, 255)
GREEN = (26, 66, 28)


FLOOR_Y      = 510
FLOOR_HEIGHT = SCREEN_HEIGHT - FLOOR_Y

CHARACTER_DATA           = [100, 7, [40, 37]]  # 0 - size, 1 - scale, 2 - offset
PLAYER_WIDTH             = 140
PLAYER_HEIGHT            = 140
KNIGHT_ANIMATION_STEPS   = [6, 8, 7, 10, 11, 4, 4, 4]
WEREBEAR_ANIMATION_STEPS = [6, 8, 9, 13, 9, 4, 4]

PLAYER_1_INIT_X = 160
PLAYER_2_INIT_X = 700

PLAYER_SPEED = 8
JUMPING_SPEED = -30
GRAVITY = 2
GROUND_FRICTION = 0.7
AIR_FRICTION = 0.93

P1_CONTROLS = {
    "left": pygame.K_a,
    "right": pygame.K_d,
    "up": pygame.K_w,
    "attack1": pygame.K_r,
    "attack2": pygame.K_f,
    "attack3": pygame.K_v
}

P2_CONTROLS = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "attack1": pygame.K_PERIOD,
    "attack2": pygame.K_SLASH,
    "attack3": pygame.K_RSHIFT
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

Knight = "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters" "/Characters(100x100)/Knight/Knight/Knight.png"
Werebear = "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters" "/Characters(100x100)/Werebear/Werebear/Werebear.png"

display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

background = pygame.transform.scale(pygame.image.load(menuscreenimage).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

knight_sheet = pygame.image.load(Knight).convert_alpha()

werebear_sheet = pygame.image.load(Werebear).convert_alpha()

background_music = pygame.mixer.Sound(menumusic)
