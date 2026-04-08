import pygame

from src.modules.fighter.render import load_animation_frames, update_fighter_animation, update_wind_animation
from src.modules.sfx.sound_loader import load_fighter_sounds
from src.modules.UI import constants as con

class Fighter():
    def __init__(self, x, y, player_width, player_height, flip, data, sprite_sheet, animation_steps, controls):
        self.size = data[0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.animation_list = load_animation_frames(
            sprite_sheet,
            self.size,
            self.image_scale,
            animation_steps
        )  # Load in the sheet straight away. List of lists of animations
        self.action = 0  # 0: idle, 1: run, 2: attack1, 3: attack2, 4: attack3, -2: hit stun, -1: death
        self.frame_index = 0
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, player_width, player_height)
        self.vel_x = 0
        self.vel_y = 0
        self.running = False
        self.jumping = False

        self.attacking = False
        self.attack_type = 0
        self.hitbox_set = set()     # avoid duplicate collision detection

        self.stun = False
        self.death = False
        self.health = 100
        self.controls = controls

        self.dashing = False
        self.dashing_direction = 0
        self.wind_animation_list = load_animation_frames(
            con.wind_sheet,
            con.WIND_SIZE,
            con.WIND_SCALE,
            [con.WIND_FRAMES]
        )[0]
        self.wind_frame_index = 0
        self.wind_update_time = 0
        

        self.dashing_charge = con.DASHING_CHARGE
        self.dashing_count = 0
        self.dashing_in_cooldown = False
        self.shift_was_pressed = False
        self.dashing_cooldown_start_time = 0

        self.sounds = load_fighter_sounds()
        self.walk_sound = self.sounds["walk"]
        self.sword_attack1_sound = self.sounds["attack1"]
        self.sword_attack2_sound = self.sounds["attack2"]
        self.sword_attack3_sound = self.sounds["attack3"]
        self.sword_attack4_sound = self.sounds["attack4"]
        self.orc_attack_sound = self.sounds["orc_attack"]

        self.walk_sound_playing = False
        self.attack_sound_played = False

    def move(self, SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_HEIGHT, TARGET):
        SPEED = con.PLAYER_SPEED
        GRAVITY = con.GRAVITY
        if self.jumping:
            FRICTION = con.AIR_FRICTION
        else:
            FRICTION = con.GROUND_FRICTION
        dx = 0
        dy = 0

        self.running = False

        # Key presses
        key = pygame.key.get_pressed()

        # reset speed if stun or dead
        if self.stun or self.death:
            self.vel_x = 0
            self.dashing = False

        current_time = pygame.time.get_ticks()

        # check dashing cooldown
        if self.dashing_in_cooldown:
            if current_time - self.dashing_cooldown_start_time > con.DASHING_COOLDOWN:
                self.dashing_in_cooldown = False
                self.dashing_charge = con.DASHING_CHARGE
                self.dashing_count = 0

        # read input
        if self.death == False:

            shift_pressed = key[self.controls["dash"]]

            # start dashing cooldown if dashed and released shift
            if self.shift_was_pressed and not shift_pressed:
                if self.dashing_count > 0 and not self.dashing_in_cooldown:
                    self.dashing_in_cooldown = True
                    self.dashing_cooldown_start_time = current_time
                else:
                    self.dashing_count = 0      # reset

            self.shift_was_pressed = shift_pressed

            if shift_pressed and not self.dashing and not self.dashing_in_cooldown:
                if self.dashing_charge > 0:
                    if key[self.controls["right"]]:
                        self.dashing = True
                        self.dashing_direction = 1
                        self.wind_update_time = current_time
                        self.dashing_charge -= 1
                        self.dashing_count += 1
                    elif key[self.controls["left"]]:
                        self.dashing = True
                        self.dashing_direction = -1
                        self.dashing_charge -= 1
                        self.dashing_count += 1

                    if self.dashing_charge == 0:
                        self.dashing_in_cooldown = True
                        self.dashing_cooldown_start_time = current_time

                if self.dashing:
                    self.vel_x = con.DASHING_SPEED * self.dashing_direction * 2
            else: 
                if self.dashing:
                    self.vel_x *= con.DASHING_BRAKE
                    
                if key[self.controls["right"]]:  # RIGHT
                    self.vel_x = SPEED
                    self.running = True
                elif key[self.controls["left"]]:  # LEFT
                    self.vel_x = -SPEED
                    self.running = True
                else:
                    self.vel_x *= FRICTION  # apply friction
                    if abs(self.vel_x) < 0.2:
                        self.vel_x = 0      # avoid infinite issue
            
            # jumping
            if key[self.controls["up"]] and not self.jumping:  # UP
                self.vel_y = con.JUMPING_SPEED
                self.jumping = True

            # attacting
            if not self.attacking:
                if key[self.controls["attack1"]] or key[self.controls["attack2"]] or key[self.controls["attack3"]]:
                    self.attacking = True
                    self.hitbox_set.clear()
                    if key[self.controls["attack1"]]:
                        self.attack_type = 1
                        self.attack_sound_played = False
                    elif key[self.controls["attack2"]]:
                        self.attack_type = 2
                        self.attack_sound_played = False
                    elif key[self.controls["attack3"]]:
                        self.attack_type = 3
                        self.attack_sound_played = False
            
            if self.attacking:
                self.attack(TARGET)
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

        # apply gravity
        self.vel_y += GRAVITY

        dx = self.vel_x
        dy = self.vel_y

        # check if player is in screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
            self.vel_x = 0
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right
            self.vel_x = 0
        if self.rect.bottom + dy > SCREEN_HEIGHT - FLOOR_HEIGHT:
            self.vel_y = 0
            dy = SCREEN_HEIGHT - FLOOR_HEIGHT - self.rect.bottom
            self.jumping = False

        # ensure players face each other
        if not self.death:
            if TARGET.rect.centerx > self.rect.centerx:
                self.flip = False
            else:
                self.flip = True

        # update position
        self.rect.x += dx
        self.rect.y += dy

    def attack(self, TARGET):
        active_frame_list = con.ATTACK_ACTIVE_FRAMES[self.attack_type]
        if active_frame_list == None:
            return

        current_attack_index = -1
        attack_width_scale = con.ATTACK_WIDTH_SCALE[self.attack_type]
        for i, (start_frame, end_frame) in enumerate(active_frame_list):
            if start_frame <= self.frame_index <= end_frame:
                current_attack_index = i
                break
        
        if current_attack_index == -1:
            return
       
        if current_attack_index not in self.hitbox_set:
        # create attacking hitbox 
            attack_width = int(attack_width_scale * self.rect.width)
            if self.flip:   
                # facing left
                attacking_rect = pygame.Rect(self.rect.left - attack_width, 
                                        self.rect.y, 
                                        attack_width, 
                                        self.rect.height)
            else:     
                # facing right
                attacking_rect = pygame.Rect(self.rect.right, 
                                        self.rect.y, 
                                        attack_width, 
                                        self.rect.height)
            # collision detect
            if attacking_rect.colliderect(TARGET.rect):
                TARGET.health -= 10
                TARGET.stun = True
                if not TARGET.death:
                    TARGET.frame_index = 0
                self.hitbox_set.add(current_attack_index)

    # animation loop
    def update(self):
        update_fighter_animation(self)  # Update fighter animation & attack states

    def draw(self, surface):
        if self.dashing:
            update_wind_animation(self, surface)

        img = pygame.transform.flip(self.image, self.flip, False)
        pygame.draw.rect(surface, con.ORANGE, self.rect)
        surface.blit(img,
                     (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))

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
