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

PLAYER_1 = 0
PLAYER_2 = 1

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
