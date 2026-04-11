import pygame
from src.modules.UI import constants as con

"""
WE MAY HAVE TO MOVE THIS INTO FIGHTERSCREEN, i think this looks better though because fighterscreen class will look cleaner.
TODO we definetely have to check best practices on this dilemma
"""

def draw_health_bar(display_surface, health, x, y, right_side):
    ratio = health / 100
    max_width = con.HEALTH_BAR_WIDTH
    current_width = max_width * ratio
    
    pygame.draw.rect(display_surface, con.WHITE, (x - con.HEALTH_BAR_BORDER_THICKNESS, 
                                                  y - con.HEALTH_BAR_BORDER_THICKNESS, 
                                                  con.HEALTH_BAR_WIDTH + (con.HEALTH_BAR_BORDER_THICKNESS * 2), 
                                                  con.HEALTH_BAR_HEIGHT + (con.HEALTH_BAR_BORDER_THICKNESS * 2)), 
                                                  con.HEALTH_BAR_BORDER_THICKNESS)

    # make health bars axially symmetric
    if not right_side:
        pygame.draw.rect(display_surface, con.RED, (x, y, current_width, con.HEALTH_BAR_HEIGHT))
    else:
        pygame.draw.rect(display_surface, con.RED, (x + max_width - current_width, y, current_width, con.HEALTH_BAR_HEIGHT))

def draw_dashing_cooldown_bar(display_surface, fighter, right_side):
    current_time = pygame.time.get_ticks()

    if not right_side:
        if not fighter.dashing_in_cooldown:
            pygame.draw.rect(display_surface, con.DASHING_BAR_COLOR, (con.DASHING_BAR_LEFT_X, 
                                                                      con.DASHING_BAR_Y, 
                                                                     (con.DASHING_BAR_WIDTH // 2) - con.CHARGES_DISTANCE_IN_HALF,
                                                                      con.DASHING_BAR_HEIGHT))
            if fighter.dashing_count == 0:
                pygame.draw.rect(display_surface, con.DASHING_BAR_COLOR, (con.DASHING_BAR_LEFT_X + (con.DASHING_BAR_WIDTH // 2) + con.CHARGES_DISTANCE_IN_HALF,
                                                                          con.DASHING_BAR_Y, 
                                                                         (con.DASHING_BAR_WIDTH // 2) - con.CHARGES_DISTANCE_IN_HALF,
                                                                          con.DASHING_BAR_HEIGHT))
        else:
            # in cooldown
            progress_time = current_time - fighter.dashing_cooldown_start_time
            ratio = progress_time / con.DASHING_COOLDOWN

            progress_width = int(con.DASHING_BAR_WIDTH * ratio)
            pygame.draw.rect(display_surface, con.DASHING_BAR_COLOR, (con.DASHING_BAR_LEFT_X, 
                                                                      con.DASHING_BAR_Y, 
                                                                      progress_width,
                                                                      con.DASHING_BAR_HEIGHT))
    else:
        if not fighter.dashing_in_cooldown:
            pygame.draw.rect(display_surface, con.DASHING_BAR_COLOR, (con.DASHING_BAR_RIGHT_X + (con.DASHING_BAR_WIDTH // 2) + con.CHARGES_DISTANCE_IN_HALF, 
                                                                      con.DASHING_BAR_Y, 
                                                                     (con.DASHING_BAR_WIDTH // 2) - con.CHARGES_DISTANCE_IN_HALF,
                                                                      con.DASHING_BAR_HEIGHT))
            if fighter.dashing_count == 0:
                pygame.draw.rect(display_surface, con.DASHING_BAR_COLOR, (con.DASHING_BAR_RIGHT_X,
                                                                          con.DASHING_BAR_Y, 
                                                                         (con.DASHING_BAR_WIDTH // 2) - con.CHARGES_DISTANCE_IN_HALF,
                                                                          con.DASHING_BAR_HEIGHT))
        else:
            # in cooldown
            progress_time = current_time - fighter.dashing_cooldown_start_time
            ratio = progress_time / con.DASHING_COOLDOWN

            progress_width = int(con.DASHING_BAR_WIDTH * ratio)
            pygame.draw.rect(display_surface, con.DASHING_BAR_COLOR, (con.DASHING_BAR_RIGHT_X + con.DASHING_BAR_WIDTH - progress_width, 
                                                                      con.DASHING_BAR_Y, 
                                                                      progress_width,
                                                                      con.DASHING_BAR_HEIGHT))

def draw_screen(display_surface, background, floor_y, floor_height, screen_width, fighter1, fighter2):
    # RENDERING
    # Draw background
    display_surface.blit(background, (0, 0))

    # Draw health bars
    draw_health_bar(display_surface, fighter1.health, con.HEALTH_BAR_LEFT_X, con.HEALTH_BAR_Y, False)
    draw_health_bar(display_surface, fighter2.health, con.HEALTH_BAR_RIGHT_X, con.HEALTH_BAR_Y, True)

    # Draw dashing bars
    draw_dashing_cooldown_bar(display_surface, fighter1, False)
    draw_dashing_cooldown_bar(display_surface, fighter2, True)

    # Draw floor
    pygame.draw.rect(display_surface, con.GREEN, (0, floor_y, screen_width, floor_height))