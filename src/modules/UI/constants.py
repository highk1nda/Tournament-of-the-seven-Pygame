import pygame

pygame.mixer.init()


#constant variables to stop accumalating technical debt
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

FPS = 60

RED = (255, 0 , 0)
WHITE = (255, 255, 255)
GREEN = (26, 66, 28)
YELLOW = (212, 175, 55)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
CYAN = (0, 255, 00)
ORANGE = (222, 110, 0)

buttonwidth = SCREEN_WIDTH / 5
buttonheight = SCREEN_HEIGHT / 15
buttonspacing = SCREEN_HEIGHT / 10

button_y = (center_y) - (buttonspacing * 2)
button_x = (center_x) - (buttonwidth / 2)

FLOOR_Y      = SCREEN_HEIGHT / 1.1
FLOOR_HEIGHT = SCREEN_HEIGHT - FLOOR_Y

char_size = 100
char_scale =  SCREEN_WIDTH / 142.86
char_offset = [int(SCREEN_WIDTH / 48), int(SCREEN_HEIGHT / 27.8)]

CHARACTER_DATA           = [char_size, char_scale, char_offset]  
PLAYER_WIDTH             = int(SCREEN_WIDTH / 7.14)
PLAYER_HEIGHT            = int(SCREEN_HEIGHT / 4.28)
KNIGHT_ANIMATION_STEPS   = [6, 8, 7, 10, 11, 4, 4, 4]
WEREBEAR_ANIMATION_STEPS = [6, 8, 9, 13, 9, 4, 4]

PLAYER_1 = 0
PLAYER_2 = 1

PLAYER_1_X = int(SCREEN_WIDTH * 0.15)
PLAYER_2_X = int(SCREEN_WIDTH * 0.7)

healthbar_width = int(SCREEN_WIDTH * 0.4)
healthbar_height = int(SCREEN_WIDTH * 0.037)
healthbar_padding = 2
healthbar_x = int(SCREEN_WIDTH * 0.02)
healthbar_y = int(SCREEN_WIDTH * 0.02)
healtbar_xx = int(SCREEN_WIDTH * 0.58)

menumusic: str = "assets/sfx/menmusica.mp3"
forestsound: str = "assets/sfx/forest-ambience-296528.mp3"
menuscreenimage: str = "assets/forest.jpg"
fightscreenimage: str = "assets/forest.jpg"

Knight = "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters" "/Characters(100x100)/Knight/Knight/Knight.png"
Werebear = "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters" "/Characters(100x100)/Werebear/Werebear/Werebear.png"

background = pygame.transform.scale(pygame.image.load(menuscreenimage).convert(), (SCREEN_WIDTH, SCREEN_HEIGHT))

knight_sheet = pygame.image.load(Knight).convert_alpha()

werebear_sheet = pygame.image.load(Werebear).convert_alpha()

background_music = pygame.mixer.Sound(menumusic)
forest_sfx = pygame.mixer.Sound(forestsound)
