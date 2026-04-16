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
            ratio = min(1, progress_time / con.DASHING_COOLDOWN)

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
            ratio = min(1, progress_time / con.DASHING_COOLDOWN)

            progress_width = int(con.DASHING_BAR_WIDTH * ratio)
            pygame.draw.rect(display_surface, con.DASHING_BAR_COLOR, (con.DASHING_BAR_RIGHT_X + con.DASHING_BAR_WIDTH - progress_width, 
                                                                      con.DASHING_BAR_Y, 
                                                                      progress_width,
                                                                      con.DASHING_BAR_HEIGHT))

def draw_round_ui(fight_screen):
    font = con.FONT_VERY_BIG
    current_time = pygame.time.get_ticks()

    text_surface = None
    draw_flag = False
    if fight_screen.state == "countdown":
        remaining_time = con.ROUND_TEXT_DURATION - (current_time - fight_screen.state_timer)

        if remaining_time >= (con.ROUND_TEXT_DURATION // 2):
            text_surface = font.render(f"ROUND {fight_screen.current_round}", True, con.RED)
        else:
            text_surface = font.render("FIGHT!", True, con.RED)

    elif fight_screen.state == "round_end":
        text_surface = font.render(fight_screen.round_text, True, con.RED)
    
    elif fight_screen.state == "fight_end":
        if fight_screen.winner != "DRAW!":
            # print miltiple lines of text
            lines = fight_screen.winner.split("\n")
            font_height = font.get_height()
            for i, line in enumerate(lines):
                text_surface = font.render(line, True, con.RED)    
                text_rect = text_surface.get_rect()
                text_rect.centerx = con.SCREEN_WIDTH // 2
                text_rect.y = con.ROUND_TEXT_Y + i * font_height
                fight_screen.screen.blit(text_surface, text_rect)
        else:
            draw_flag = True
            text_surface = font.render(fight_screen.winner, True, con.RED)
    
    if fight_screen.state not in ["fight", "death_animation", "fade_out", "fade_in", "fight_end"] or draw_flag:
        text_rect = text_surface.get_rect()
        text_rect.centerx = con.SCREEN_WIDTH // 2
        text_rect.y = con.ROUND_TEXT_Y
        fight_screen.screen.blit(text_surface, text_rect)
        

def draw_screen(display_surface, background, floor_y, floor_height, screen_width, fighter1, fighter2, offset=(0, 0)):
    # RENDERING
    # Draw background
    x, y = offset
    display_surface.blit(background, (x, y))

    # Draw health bars
    draw_health_bar(display_surface, fighter1.health, con.HEALTH_BAR_LEFT_X, con.HEALTH_BAR_Y, False)
    draw_health_bar(display_surface, fighter2.health, con.HEALTH_BAR_RIGHT_X, con.HEALTH_BAR_Y, True)

    # Draw dashing bars
    draw_dashing_cooldown_bar(display_surface, fighter1, False)
    draw_dashing_cooldown_bar(display_surface, fighter2, True)

    # Draw floor
    pygame.draw.rect(display_surface, con.GREEN, (x, floor_y + y, screen_width, floor_height))