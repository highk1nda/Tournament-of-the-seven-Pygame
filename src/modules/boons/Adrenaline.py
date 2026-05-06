 
MAX_ADRENALINE = 8
 
 
def damage_multiply():
    base_damage_ratio = 0.9     # -10 % damage baseline
    return base_damage_ratio
 
 
def speed_multiply(count):
    mult_unit = 0.08    # +5 % speed per time
    num = min(count, MAX_ADRENALINE)
    return 1.0 + num * mult_unit

def attack_speed_multiply(count):
    mult_unit = 0.06    # +6 % speed per time
    min_cooldown_mult = 0.4
    num = min(count, MAX_ADRENALINE)
    mult = (1.0 - mult_unit) ** num
    return max(mult, min_cooldown_mult)