import pygame

from src.modules.fighter.render import load_animation_frames, update_fighter_animation, update_wind_animation
from src.modules.sfx.sound_loader import load_fighter_sounds
from src.modules.UI import constants as con
from src.modules.UI import CharDictionary as chardict
from src.modules.fighter.Projectile import Projectile

class Fighter():
    def __init__(self, x, y, player_width, player_height, flip, char_data, controls):
        self.char_data = char_data
        self.size = char_data["size"]
        self.image_scale = char_data["scale"]
        self.offset = char_data["offset"]
        self.flip = flip

        self.animation_list = load_animation_frames(
            char_data["animations"],
            self.size,
            self.image_scale
        )

        self.action = "IDLE"
        self.frame_index = 0
        self.image = self.animation_list[self.action]["ground"][self.frame_index]  # on ground default
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, player_width, player_height)
        self.vel_x = 0
        self.vel_y = 0
        self.running = False
        self.jumping = False
        self.jumpable = char_data["jumpable"]

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
            chardict.WIND_DATA["animation"],
            chardict.WIND_DATA["size"],
            chardict.WIND_DATA["scale"]
        )["WIND"]["ground"]
        self.wind_frame_index = 0
        self.wind_update_time = 0
        

        self.dashing_charge = con.DASHING_CHARGE
        self.dashing_count = 0
        self.dashing_in_cooldown = False
        self.shift_was_pressed = False
        self.dashing_cooldown_start_time = 0

        self.projectiles = []

        self.screen_shake = False

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
                    self.sounds["dash"].play()
                else:
                    self.vel_x *= FRICTION  # apply friction
                    if abs(self.vel_x) < 0.2:
                        self.vel_x = 0      # avoid infinite issue
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
            if key[self.controls["up"]] and not self.jumping and self.jumpable:  # UP
                self.vel_y = con.JUMPING_SPEED
                self.jumping = True

            # attacting
            if not self.attacking:
                attack1 = key[self.controls["attack1"]] and ("ATTACK1" in self.char_data["animations"])
                attack2 = key[self.controls["attack2"]] and ("ATTACK2" in self.char_data["animations"])
                attack3 = key[self.controls["attack3"]] and ("ATTACK3" in self.char_data["animations"])
                if attack1 or attack2 or attack3:
                    self.attacking = True
                    self.hitbox_set.clear()
                    if attack1:
                        self.attack_type = 1
                        self.attack_sound_played = False
                    elif attack2:
                        self.attack_type = 2
                        self.attack_sound_played = False
                    elif attack3:
                        self.attack_type = 3
                        self.attack_sound_played = False
            
            if self.attacking:
                self.attack(TARGET)
        # SFX
        # walking sound
        if self.running:
            if not self.walk_sound_playing:
                self.walk_sound.play(-1)  # loop
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
        attack_key = f"ATTACK{self.attack_type}"

        # projectile attack
        if "projectiles" in self.char_data and attack_key in self.char_data["projectiles"]:
            pj_data = self.char_data["projectiles"][attack_key]
            gen_frame = pj_data["gen_frame"]

            if self.frame_index == gen_frame and attack_key not in self.hitbox_set:
                if self.flip:
                    direction = -1
                    pj_x = self.rect.left
                else:
                    direction = 1
                    pj_x = self.rect.right
                pj_y = self.rect.centery

                pj_animation_list = load_animation_frames(
                    self.char_data["projectiles"],
                    self.char_data["projectile_size"][attack_key]["size"],
                    self.char_data["projectile_size"][attack_key]["scale"]
                )[attack_key]["ground"]
                pj = Projectile(pj_x, pj_y, direction, self, TARGET, pj_data, 
                                pj_animation_list,
                                self.char_data["projectile_size"][attack_key])
                self.projectiles.append(pj)
                self.hitbox_set.add(attack_key)
            return

        # close attack
        active_frame_list = self.char_data["attack_active_frames"].get(attack_key)
        if active_frame_list == None:
            return

        current_attack_index = -1
        attack_width_scale = self.char_data["attack_width_scale"].get(attack_key)
        for i, (start_frame, end_frame) in enumerate(active_frame_list):
            if start_frame <= self.frame_index <= end_frame:
                current_attack_index = i                # store the "ID" of an attack to avoid duplicate collision detect of a single attack
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
            if attacking_rect.colliderect(TARGET.rect) and not TARGET.dashing:
                TARGET.health -= self.char_data["attack_damage"].get(attack_key)
                TARGET.stun = True
                TARGET.sounds["hit"].play()
                if not TARGET.death:
                    TARGET.frame_index = 0
                    self.screen_shake = True
                    # knockback by the attack
                    if TARGET.flip:
                        TARGET.rect.x += con.KNOCKBACK_DISTANCE
                    else: 
                        TARGET.rect.x -= con.KNOCKBACK_DISTANCE
                self.hitbox_set.add(current_attack_index)

    # animation loop
    def update(self):
        update_fighter_animation(self)  # Update fighter animation & attack states

        # update projectiles
        for pj in self.projectiles:
            pj_status = pj.fly_attack_update()
            if pj_status == "effect_done":
                self.projectiles.remove(pj)

    def draw(self, surface):
        if self.dashing:
            update_wind_animation(self, surface)

        img = pygame.transform.flip(self.image, self.flip, False)
        #pygame.draw.rect(surface, con.ORANGE, self.rect)
        surface.blit(img,
                     (self.rect.x - self.offset[0] * self.image_scale, self.rect.y - self.offset[1] * self.image_scale))

    def clean_up(self):
        self.walk_sound.stop()
        self.walk_sound_playing = False
