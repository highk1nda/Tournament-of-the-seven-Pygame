import pygame
from src.modules.UI import constants as con


def draw_health_bar(display_surface, health, x, y, right_side):
    ratio = health / 100
    current_width = int(con.healthbar_width * ratio)
    
    border_rect = (
        x - con.healthbar_padding,
        y - con.healthbar_padding,
        con.healthbar_width + con.healthbar_padding * 2,
        con.healthbar_height + con.healthbar_padding * 2
    )
    
    pygame.draw.rect(display_surface, con.WHITE, border_rect, 2)

    # make health bars axially symmetric
    if not right_side:
        pygame.draw.rect(display_surface, con.RED, (x, y, current_width, con.healthbar_height))
    else:
        pygame.draw.rect(display_surface, con.RED, (x + con.healthbar_width - current_width, y, current_width, con.healthbar_height))

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
    font = con.ROUND_FONT
    current_time = pygame.time.get_ticks()

    text_surface = None
    draw_flag = False
    if fight_screen.state == "countdown":
        remaining_time = con.ROUND_TEXT_DURATION - (current_time - fight_screen.state_timer)

        if remaining_time >= (con.ROUND_TEXT_DURATION // 2):
            text_surface = font.render(f"ROUND {fight_screen.current_round}", True, con.RED)
        else:
            text_surface = font.render("FIGHT!", True, con.RED)

    elif fight_screen.state in ["round_end", "time_over"]:
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

def draw_round_indicator(display_surface, target_wins, on_right):
    r = con.ROUND_DOT_RADIUS
    gap = con.ROUND_DOT_GAP
    total_width = con.MAX_WINS * (r * 2) + (con.MAX_WINS - 1) * gap
    y = con.ROUND_DOT_Y

    lifes_remain = con.MAX_WINS - target_wins
    if not on_right:
        init_x = con.healthbar_x + r
    else:
        init_x = con.healthbar_xx + con.healthbar_width - total_width + r
    for i in range(con.MAX_WINS):
        x = init_x + i * (r * 2 + gap)
        if not on_right:
            if i < lifes_remain:
                pygame.draw.circle(display_surface, con.RED, (x, y), r)
        else:
            if (con.MAX_WINS - i) <= lifes_remain:
                pygame.draw.circle(display_surface, con.RED, (x, y), r)
        pygame.draw.circle(display_surface, con.WHITE, (x, y), r, con.ROUND_DOT_BORDER_THICKNESS)

def draw_timer(display_surface, second):
    font = con.ROUND_FONT
    text_surface = font.render(str(second), True, con.RED)
    text_rect = text_surface.get_rect()
    text_rect.centerx = con.SCREEN_WIDTH // 2
    text_rect.centery = con.healthbar_y + con.healthbar_height // 2
    display_surface.blit(text_surface, text_rect)


def draw_screen(display_surface, background, floor_y, floor_height, screen_width, fighter1, fighter2, offset=(0, 0)):
    # RENDERING
    # Draw background
    x, y = offset
    display_surface.blit(background, (x, y))

    # Draw health bars
    draw_health_bar(display_surface, fighter1.health, con.healthbar_x, con.healthbar_y, False)
    draw_health_bar(display_surface, fighter2.health, con.healthbar_xx, con.healthbar_y, True)

    # Draw dashing bars
    draw_dashing_cooldown_bar(display_surface, fighter1, False)
    draw_dashing_cooldown_bar(display_surface, fighter2, True)

    # Draw floor
    pygame.draw.rect(display_surface, con.FLOOR_COLOR, (x, floor_y + y, screen_width, floor_height))