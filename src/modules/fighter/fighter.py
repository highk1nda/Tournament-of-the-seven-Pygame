import pygame
from src.modules.fighter.render import load_animation_frames, update_fighter_animation
from src.modules.sfx.sound_loader import load_fighter_sounds


class Fighter():
    def __init__(self, x, y, data, sprite_sheet, animation_steps):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = False
        self.animation_list = load_animation_frames(
            sprite_sheet,
            self.size,
            self.image_scale,
            animation_steps
        )  # Load in the sheet straight away. List of lists of animations
        self.action = 0  # 0 - IDLE, 1 - Walk
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 140, 140)
        self.vel_y = 0
        self.running = False
        self.jumping = False
        self.attacking = False
        self.attack_type = 0
        self.health = 100
        self.hit = False
        self.death = False
        self.sounds = load_fighter_sounds()

        self.walk_sound = self.sounds["walk"]
        self.sword_attack1_sound = self.sounds["attack1"]
        self.sword_attack2_sound = self.sounds["attack2"]
        self.sword_attack3_sound = self.sounds["attack3"]
        self.sword_attack4_sound = self.sounds["attack4"]
        self.orc_attack_sound = self.sounds["orc_attack"]

        self.walk_sound_playing = False
        self.attack_sound_played = False

    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER):
        SPEED = 6
        GRAVITY = 2
        dx = 0
        dy = 0
        FLOOR_HEIGHT = 100
        self.running = False
        self.flip = False

        # Key presses
        key = pygame.key.get_pressed()
        #
        # EDIT FOR EACH PLAYER
        # SPLIT IN TWO CLASS INSTANCES
        #
        # MOVEMENT BINDS WASD
        if PLAYER == 0:
            if key[pygame.K_d]:  # RIGHT
                dx += SPEED
                self.running = True
            if key[pygame.K_a]:  # LEFT
                dx -= SPEED
                self.running = True

        # jumping
        if PLAYER == 0:
            if key[pygame.K_w]:  # UP
                self.vel_y -= SPEED
        if PLAYER == 1:
            if key[pygame.K_SPACE]:  # UP
                self.vel_y -= SPEED

        if key[pygame.K_i]:  # FLIP TEST
            if self.flip == True:
                self.flip = False
        # MOVEMENT BINDS ARROWS
        if PLAYER == 1:
            if key[pygame.K_RIGHT]:  # RIGHT
                dx += SPEED
                self.running = True
            if key[pygame.K_LEFT]:  # LEFT
                dx -= SPEED
                self.running = True
            # jumping
            if key[pygame.K_UP]:  # UP
                self.vel_y -= SPEED

        # Attack binds
        if PLAYER == 0:
            if not self.attacking:
                if key[pygame.K_r]:
                    self.attacking = True
                    self.attack_type = 1
                    self.attack_sound_played = False
                elif key[pygame.K_f]:
                    self.attacking = True
                    self.attack_type = 2
                    self.attack_sound_played = False
                elif key[pygame.K_v]:
                    self.attacking = True
                    self.attack_type = 3
                    self.attack_sound_played = False

        # Attack binds
        if PLAYER == 1:
            if not self.attacking:
                if key[pygame.K_RCTRL]:
                    self.attacking = True
                    self.attack_type = 1
                    self.attack_sound_played = False
                elif key[pygame.K_PERIOD]:
                    self.attacking = True
                    self.attack_type = 2
                    self.attack_sound_played = False
                elif key[pygame.K_SLASH]:
                    self.attacking = True
                    self.attack_type = 3
                    self.attack_sound_played = False

        if PLAYER == 1:
            self.flip = True

        # SFX
        # walking sound
        if self.running:
            if not self.walk_sound_playing:
                self.walk_sound.play(-2)  # loop
                self.walk_sound_playing = True
        else:
            if self.walk_sound_playing:
                self.walk_sound.stop()
                self.walk_sound_playing = False
        # sword sound
        if self.attacking and not self.attack_sound_played:
            if self.attack_type == 1:
                self.sword_attack1_sound.play()
            elif self.attack_type == 2:
                self.sword_attack2_sound.play()
            elif self.attack_type == 3:
                self.sword_attack3_sound.play()
            elif self.attack_type == 4:
                self.orc_attack_sound.play()
            self.attack_sound_played = True

        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # is player on screen
        if self.rect.left + dx < 0:
            dx -= self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
        if self.rect.bottom + dy > SCREEN_HEIGHT - FLOOR_HEIGHT:
            self.vel_y = 0
            dy = SCREEN_HEIGHT - FLOOR_HEIGHT - self.rect.bottom
        if self.rect.top + dy > SCREEN_HEIGHT:
            self.vel_y = 0
        if self.rect.top + dy < 0:
            self.vel_y = 0

        # update position
        self.rect.x += dx
        self.rect.y += dy

    # animation loop
    def update(self):
        update_fighter_animation(self)  # Update fighter animation & attack states

    def draw(self, surface):
        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, (222, 110, 0), self.rect)
        surface.blit(img,
                     (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))

    def update_action(self, new_action):
        # check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            # update the current animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
# Legacy code, don't mind
#     # Player 1 crouch (S)
#     if keys[pygame.K_s]:
#         bottom = player1_rect.bottom
#         centerx = player1_rect.centerx
#         player1_rect.size = (CROUCH_WIDTH, CROUCH_HEIGHT)
#         player1_rect.centerx = centerx
#         player1_rect.bottom = bottom
#     else:
#         bottom = player1_rect.bottom
#         centerx = player1_rect.centerx
#         player1_rect.size = (PLAYER_WIDTH, PLAYER_HEIGHT)
#         player1_rect.centerx = centerx
#         player1_rect.bottom = bottom
