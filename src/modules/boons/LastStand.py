import pygame
from src.modules.UI import constants as con

BONUS_MULT       = 1.30  # +30 % damage and speed
THRESHOLD = 0.3     # 30%
def check_activation(fighter):
    health_threshold = int(THRESHOLD * 100)   # HP at which Last Stand activates
    return fighter.health <= health_threshold

def draw_threshold_line(display_surface, right_side):
    line_width = 2

    if not right_side:
        pygame.draw.rect(display_surface, con.WHITE, (con.healthbar_x + (THRESHOLD * con.healthbar_width), con.healthbar_y, 
                                                      line_width, con.healthbar_height))
    else:
        pygame.draw.rect(display_surface, con.WHITE, (con.healthbar_xx + (1 - THRESHOLD) * con.healthbar_width, con.healthbar_y, 
                                                      line_width, con.healthbar_height))
