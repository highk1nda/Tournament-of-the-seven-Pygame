
BONUS_MULT       = 1.30  # +30 % damage and speed

def check_activation(fighter):
    health_threshold = 30   # HP at which Last Stand activates
    return fighter.health <= health_threshold