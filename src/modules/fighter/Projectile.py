import pygame

from src.modules.UI import constants as con

class Projectile:
    def __init__(self, x, y, direction, fighter, target, pj_data, frame_list, pj_size_dict):
        self.pj_data = pj_data
        self.type = pj_data["type"]     # arrow / explosive / lock
        if self.type == "arrow" or self.type == "explosive":
            self.rect = pygame.Rect(x, (y + fighter.rect.height / 5.3), pj_data["hitbox_width"], pj_data["hitbox_height"])
        elif self.type == "lock":
            self.rect = pygame.Rect(target.rect.centerx - (pj_data["hitbox_width"] // 2), 
                                    target.rect.centery - (pj_data["hitbox_height"] // 2),
                                    pj_data["hitbox_width"], pj_data["hitbox_height"])
        self.frame_index = 0
        self.frames = frame_list
        self.image = self.frames[self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.animation_cooldown = pj_data["cooldown"]

        self.gen_time = pygame.time.get_ticks()         # time when attact object was created, fixed
        self.lock_delay = pj_data.get("delay")

        self.direction = direction
        self.speed = pj_data["speed"] * direction
        self.damage = pj_data["damage"]

        self.fighter = fighter
        self.target = target
        self.attack_hit = False
    
        self.state = "flying"       # flying / rendering (animation)

        self.scale = pj_size_dict["scale"]
        self.offset = pj_size_dict["offset"]

    def fly_attack_update(self):
        # update animation, maybe should put in render.py
        current_time = pygame.time.get_ticks()
        if self.type == "explosive" and self.state == "flying":
            self.frame_index = 0

        elif self.type == "lock" and (current_time - self.gen_time < self.lock_delay):
            self.frame_index = 0
            self.update_time = current_time
        
        elif len(self.frames) > 1:
            if current_time - self.update_time > self.animation_cooldown:
                self.frame_index += 1
                self.update_time = current_time
        
        if self.frame_index >= len(self.frames):
            if self.state == "rendering" or self.type == "lock":
                return "effect_done"
            else:
                self.frame_index = 0

        self.image = self.frames[self.frame_index]

        # pj move logic
        # only make object fly if its an arrow or fire ball (before collision)
        if self.state == "flying" and self.type in ["arrow", "explosive"]:
            self.rect.x += self.speed

            # remove the object if out of screen
            if self.rect.right < 0 or self.rect.left > con.SCREEN_WIDTH:
                return "effect_done"
            
        # collision detect
        lock_flag = False
        if self.type == "lock":
            start_frame, end_frame = self.pj_data["active_frame"]
            if start_frame <= self.frame_index <= end_frame:
                lock_flag = True

        if self.state == "flying" and not self.attack_hit and not self.target.dashing:
            if self.rect.colliderect(self.target.rect):
                if self.type == "arrow":
                    self.make_damage()
                    return "effect_done"
                
                elif self.type == "explosive":
                    self.make_damage()
                    self.attack_hit = True
                    self.state = "rendering"
                    self.speed = 0
                    self.frame_index = 1
                    self.update_time = pygame.time.get_ticks()
                    return "keep_alive"
                
                elif self.type == "lock" and lock_flag:
                    self.make_damage()
                    self.attack_hit = True
                    self.state = "rendering"
                    return "keep_alive"
            
            return "keep_alive"


    def make_damage(self):
        self.target.health -= self.damage
        self.target.stun = True
        self.target.sounds["hit"].play()
        if not self.target.death:
            self.target.frame_index = 0
            self.fighter.screen_shake = True
            # knockback by the attack
            if self.target.flip:
                self.target.rect.x += con.KNOCKBACK_DISTANCE
            else: 
                self.target.rect.x -= con.KNOCKBACK_DISTANCE
    
    def draw(self, surface):
        if self.direction == -1:
            flip = True
        else: 
            flip = False
        image = pygame.transform.flip(self.image, flip, False)
        #pygame.draw.rect(surface, con.ORANGE, self.rect)
        surface.blit(image, ((self.rect.x - self.offset[0] * self.scale, self.rect.y - self.offset[1] * self.scale)))