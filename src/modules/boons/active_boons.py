import pygame
from src.modules.UI import constants as con

BOON_COOLDOWN = 12000  # 12 seconds between activations

BOON_ASSET_BASE = "assets/Tiny RPG Character Asset Pack v1.03 -Full 20 Characters/"

BOON_ASSET_KEY = {
    "Sub Zero":        "sub_zero_frames",
    "Scorching Ray":   "scorching_frames",
    "Area of Warding": "warding_frames",
}


def load_boon_assets():
    assets = {}

    # sub zero ice cocoon sheet 5x5 grid 32x32 per frame 25 total
    cocoon_sheet = pygame.image.load(
        BOON_ASSET_BASE + "boons/Sub_Zero/IceCocoon.png"
    ).convert_alpha()
    fw, fh = 32, 32
    assets["sub_zero_frames"] = [
        cocoon_sheet.subsurface((i % 5) * fw, (i // 5) * fh, fw, fh)
        for i in range(25)
    ]

    # scorching ray fireball sprite sheet 7 frames 100x100
    fireball_sheet = pygame.image.load(
        BOON_ASSET_BASE + "Characters(100x100)/Wizard/Magic(projectile)/Wizard-Attack02_Effect.png"
    ).convert_alpha()
    assets["scorching_frames"] = [
        fireball_sheet.subsurface(i * 100, 0, 100, 100) for i in range(7)
    ]

    # burn effect frames 8 frames 16x32
    fire_dir = BOON_ASSET_BASE + "boons/Group 4 - 3/"
    assets["burn_effect_frames"] = [
        pygame.image.load(f"{fire_dir}Group 4 - 3_{i}.png").convert_alpha()
        for i in range(1, 9)
    ]

    # area of warding frames 94 frames 24x24
    aqua_dir = BOON_ASSET_BASE + "boons/19-Aqua/"
    assets["warding_frames"] = [
        pygame.image.load(f"{aqua_dir}24_Pixels{i:03d}.png").convert_alpha()
        for i in range(94)
    ]

    return assets


class FreezeDebuff:
    duration = 3000

    def __init__(self, target):
        self.target = target
        self.start_time = pygame.time.get_ticks()
        self.active = True
        target.frozen = True

    def update(self):
        if not self.active:
            return False
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self._end()
        return self.active

    def notify_damage(self):
        self._end()

    def _end(self):
        self.active = False
        self.target.frozen = False

    @property
    def damage_multiplier(self):
        return 1.35 if self.active else 1.0


class BurnDebuff:
    duration = 3500
    damage_interval = 250
    burn_damage = 1
    hit_interval = 1000  # triggers hit animation every second

    def __init__(self, target):
        self.target = target
        self.start_time = pygame.time.get_ticks()
        self.active = True
        target.burning = True
        self.last_tick = pygame.time.get_ticks()
        self.last_hit = pygame.time.get_ticks()

    def update(self):
        if not self.active:
            return False
        now = pygame.time.get_ticks()
        if now - self.start_time > self.duration:
            self._end()
            return False
        if self.target.running and now - self.last_tick > self.damage_interval:
            self.target.receive_damage(self.burn_damage, attacker=None)
            self.last_tick = now
        if now - self.last_hit > self.hit_interval and not self.target.death:
            self.target.stun = True
            self.last_hit = now
        return True

    def _end(self):
        self.active = False
        self.target.burning = False


class SubZeroActiveBoon:
    warning_duration = 1200
    anim_cooldown = 80
    frame_scale = 10        # scales each frame up to fill the effect area
    freeze_frame = 14       # frame index when freeze is applied to target
    warning_seq = [24, 23, 22, 21]  # last 4 frames in reverse used as ground warning

    def __init__(self, caster, target, frames):
        self.caster = caster
        self.target = target
        self.frames = frames
        self.state = "warning"
        self.start_time = pygame.time.get_ticks()
        self.warn_index = 0
        self.frame_index = 0
        self.last_time = pygame.time.get_ticks()
        self.done = False
        self.freeze_applied = False
        self.freeze_pending = False
        self.locked_cx = None
        self.locked_bottom = None

    def update(self):
        if self.done:
            return
        now = pygame.time.get_ticks()

        if self.state == "warning":
            if now - self.last_time > self.anim_cooldown:
                self.warn_index = (self.warn_index + 1) % len(self.warning_seq)
                self.last_time = now
            if now - self.start_time > self.warning_duration:
                self.state = "hit"
                self.frame_index = 0
                self.last_time = now

        elif self.state == "hit":
            # release animation hold before freeze expires so the rest plays out
            ending_soon = (
                self.target.freeze_debuff is not None
                and self.target.freeze_debuff.active
                and now - self.target.freeze_debuff.start_time >= FreezeDebuff.duration - 1000
            )
            frozen_hold = self.frame_index >= self.freeze_frame and (self.target.frozen or self.freeze_pending) and not ending_soon
            if not frozen_hold and now - self.last_time > self.anim_cooldown:
                self.frame_index += 1
                self.last_time = now
            if self.frame_index >= self.freeze_frame and not self.freeze_applied and not self.target.death:
                self.freeze_pending = True
            if self.freeze_pending and not self.freeze_applied and not self.target.jumping and not self.target.death:
                self.target.freeze_debuff = FreezeDebuff(self.target)
                self.freeze_applied = True
                self.freeze_pending = False
                self.locked_cx     = self.target.rect.centerx
                self.locked_bottom = self.target.rect.bottom
            if self.frame_index >= len(self.frames):
                self.done = True

    def draw(self, surface):
        if self.done:
            return

        if self.state == "warning":
            raw = self.frames[self.warning_seq[self.warn_index]]
        elif self.frame_index < len(self.frames):
            raw = self.frames[self.frame_index]
        else:
            return

        w = raw.get_width() * self.frame_scale
        h = raw.get_height() * self.frame_scale
        scaled = pygame.transform.scale(raw, (w, h))
        cx     = self.locked_cx     if self.locked_cx     is not None else self.target.rect.centerx
        bottom = self.locked_bottom if self.locked_bottom is not None else self.target.rect.bottom
        surface.blit(scaled, (cx - w // 2, bottom - h + 40))


class ScorchingRayActiveBoon:
    anim_cooldown = 60
    scale = 16
    hitbox = 70     # smaller than the visual size
    fall_ms = 500
    initial_damage = 8

    def __init__(self, caster, target, frames):
        self.caster = caster
        self.target = target
        self.frames = frames

        start_y  = 0.0
        target_y = float(target.rect.centery)
        target_x = float(target.rect.centerx)

        # 45 degree angle so horizontal and vertical distance are equal
        dy_total = target_y - start_y
        self.x = target_x - dy_total
        self.y = start_y

        frames_count = self.fall_ms / (1000 / 60)
        self.vx = dy_total / frames_count
        self.vy = dy_total / frames_count

        self.frame_index = 0
        self.last_time = pygame.time.get_ticks()
        self.done = False
        self.hit  = False

    def update(self):
        if self.done:
            return
        now = pygame.time.get_ticks()

        self.x += self.vx
        self.y += self.vy

        if now - self.last_time > self.anim_cooldown:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_time = now

        h = self.hitbox
        ball_rect = pygame.Rect(int(self.x) - h // 2, int(self.y) - h // 2, h, h)

        if not self.hit and not self.target.death and not self.target.dashing:
            if ball_rect.colliderect(self.target.rect):
                self.hit  = True
                self.done = True
                if not self.target.burn_debuff or not self.target.burn_debuff.active:
                    self.target.burn_debuff = BurnDebuff(self.target)

                self.target.receive_damage(self.initial_damage, attacker=self.caster)
                self.target.stun = True
                self.target.sounds["hit"].play()
                self.caster.screen_shake = True

        if self.y > con.FLOOR_Y:
            self.done = True

    def draw(self, surface):
        if self.done:
            return
        raw  = self.frames[self.frame_index]
        size = raw.get_width() * self.scale
        scaled  = pygame.transform.scale(raw, (size, size))
        # rotate so the fireball points diagonally downward
        rotated = pygame.transform.rotate(scaled, -45)
        surface.blit(rotated, (int(self.x) - rotated.get_width()  // 2,
                               int(self.y) - rotated.get_height() // 2))


class AreaOfWardingActiveBoon:
    duration        = 8000
    anim_cooldown   = 35
    zone_radius     = 160
    damage_interval = 600
    zone_damage     = 3
    alpha           = 160

    def __init__(self, caster, target, frames):
        self.caster = caster
        self.target = target
        self.frames = frames
        self.start_time  = pygame.time.get_ticks()
        self.frame_index   = 0
        self.last_time   = pygame.time.get_ticks()
        self.last_damage = pygame.time.get_ticks()
        self.done = False

    def update(self):
        if self.done:
            return
        now = pygame.time.get_ticks()

        if now - self.start_time > self.duration:
            self.done = True
            return

        if now - self.last_time > self.anim_cooldown:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.last_time = now

        r = self.zone_radius
        zone_rect = pygame.Rect(
            self.caster.rect.centerx - r,
            self.caster.rect.bottom - r * 2 + 10,
            r * 2, r * 2,
        )
        if zone_rect.colliderect(self.target.rect) and not self.target.dashing:
            if now - self.last_damage > self.damage_interval and not self.target.death:
                self.target.receive_damage(self.zone_damage, attacker=self.caster)
                self.target.stun = True
                self.target.sounds["hit"].play()
                self.last_damage = now

    def draw(self, surface):
        if self.done:
            return
        r   = self.zone_radius
        raw = self.frames[self.frame_index]
        size   = r * 2
        scaled = pygame.transform.scale(raw, (size, size)).copy()
        scaled.set_alpha(self.alpha)
        cx = self.caster.rect.centerx
        cy = self.caster.rect.bottom - r + 10
        surface.blit(scaled, (cx - size // 2, cy - size // 2))


ACTIVE_BOON_CLASS_MAP = {
    "Sub Zero":        SubZeroActiveBoon,
    "Scorching Ray":   ScorchingRayActiveBoon,
    "Area of Warding": AreaOfWardingActiveBoon,
}
