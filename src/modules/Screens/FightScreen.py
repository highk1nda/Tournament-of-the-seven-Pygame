import pygame
import random
from pygame.locals import *

from src.modules.fighter.Fighter import Fighter
from src.modules.UI import constants as con
from src.modules.UI import CharDictionary as chardict
from src.modules.systems.Draw import draw_screen, draw_round_ui, draw_round_indicator, draw_timer
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res
from tests.test import DebugPopup
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr
from src.modules.boons.DevilsDie import Dice

# the fight screen class
class FightScreen():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.player1 = None
        self.player2 = None

        # screen shake
        self.shake_end_time = 0
        self.screen_shake_offset = (0, 0)

        # round logic
        self.p1_wins = 0
        self.p2_wins = 0
        self.max_wins = con.MAX_WINS
        self.current_round = 1
        self.round_text = ""    # Fighter 1 wins! / Fighter 2 wins! / Draw! / Time over
        self.round_second_text = ""
        self.round_death = None
        self.state = "countdown"    # countdown / fight / death animation / (dice roll / revive animation) /
                                    # time over / round end / fade out / fade in / fight end
        self.winner = "\n"

        self.state_timer = 0
        self.round_start_time = 0

        # screen fade between rounds
        self.fade_surface = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT))
        self.fade_surface.fill(con.BLACK)
        self.fade_alpha = 0  # 0 - 255, transparency of the surface

        self.dice = None
        self.dice_player = None

        self.revive_update_time = 0
        self.revive_frame_index = 0

    def loadfighters(self):
        p1_data = getattr(con, "p1_selected", chardict.KNIGHT_DATA) # default to knight if not set
        p2_data = getattr(con, "p2_selected", chardict.WEREBEAR_DATA) # default to werebear if not set
        p1_passive_boon = getattr(con, "p1_passive_boon", None)
        p2_passive_boon = getattr(con, "p2_passive_boon", None)
        self.player1 = Fighter(con.PLAYER_1_X, con.FLOOR_Y - con.PLAYER_HEIGHT, con.PLAYER_WIDTH, con.PLAYER_HEIGHT, False, p1_data, con.P1_CONTROLS, "devils_die")
        self.player2 = Fighter(con.PLAYER_2_X, con.FLOOR_Y - con.PLAYER_HEIGHT, con.PLAYER_WIDTH, con.PLAYER_HEIGHT, True, p2_data, con.P2_CONTROLS, "devils_die")
        self.background = con.fight_backgrounds[con.selected_map]
        
    def revive_fighter(self, fighter):
        fighter.death = False
        fighter.health = 100
        fighter.stun = False
        fighter.attacking = False
        fighter.attack_type  = 0
        fighter.frame_index  = 0
        fighter.action       = "IDLE"
        fighter.vel_x        = 0
        fighter.vel_y        = 0

    def update(self):
        current_time = pygame.time.get_ticks()

        if self.state == "countdown":
            if current_time - self.state_timer >= con.ROUND_TEXT_DURATION:
                self.state = "fight"
                self.round_death = None
                self.round_start_time = current_time
            return None
        
        if self.state == "fight":
            self.player1.move(con.SCREEN_WIDTH, con.SCREEN_HEIGHT, con.FLOOR_HEIGHT, self.player2)
            self.player2.move(con.SCREEN_WIDTH, con.SCREEN_HEIGHT, con.FLOOR_HEIGHT, self.player1)
            self.player1.update()
            self.player2.update()
            # check if any damage maded (for screen shake)
            for fighter in (self.player1, self.player2):
                if fighter.screen_shake:
                    self.shake_end_time = current_time + con.SCREEN_SHAKE_DURATION
                    fighter.screen_shake = False
            
            if current_time < self.shake_end_time:
                remain_time = self.shake_end_time - current_time
                ratio = remain_time / con.SCREEN_SHAKE_DURATION
                shake_intensity = int(ratio * con.SCREEN_SHAKE_INTENSITY)
                self.screen_shake_offset = (random.randint(-shake_intensity, shake_intensity),
                                            random.randint(-shake_intensity, shake_intensity))
            else:
                self.screen_shake_offset = (0, 0)

            # time over check
            round_time = current_time - self.round_start_time
            if round_time >= con.ROUND_DURATION:
                self.round_text = "TIME OVER"
                self.state = "time_over"
                self.state_timer = current_time
                if self.player1.health > self.player2.health:
                    self.round_second_text = "PLAYER 1 WINS!"
                    self.p1_wins += 1
                elif self.player2.health > self.player1.health:
                    self.round_second_text = "PLAYER 2 WINS!"
                    self.p2_wins += 1
                else:
                    self.round_second_text = "DRAW!"

                self.player1.clean_up()
                self.player2.clean_up()
                return None
            
            # player died in round time
            if self.player1.death or self.player2.death:
                if self.player1.death and self.player2.death:
                    self.round_text = "DRAW!"
                    self.round_death = "both"
                    self.p1_wins += 1
                    self.p2_wins += 1
                elif self.player1.death:
                    self.round_text = "PLAYER 2 WINS!"
                    self.round_death = self.player1
                    self.p2_wins += 1
                elif self.player2.death:
                    self.round_text = "PLAYER 1 WINS!"
                    self.round_death = self.player2
                    self.p1_wins += 1

                self.state = "death_animation"
                self.state_timer = current_time
            return None
        
        if self.state == "time_over":
            if current_time - self.state_timer > con.ROUND_TEXT_DURATION:
                self.round_text = self.round_second_text
                self.state = "round_end"
                self.state_timer = current_time
            return None
        
        if self.state == "death_animation":
            self.player1.move(con.SCREEN_WIDTH, con.SCREEN_HEIGHT, con.FLOOR_HEIGHT, self.player2)
            self.player2.move(con.SCREEN_WIDTH, con.SCREEN_HEIGHT, con.FLOOR_HEIGHT, self.player1)
            self.player1.update()
            self.player2.update()

            if current_time - self.state_timer > con.DEATH_DURATION:
                self.player1.clean_up()
                self.player2.clean_up()

                if self.round_death.passive_boon == "devils_die" and self.round_death != "both":
                    self.state = "dice_roll"
                    self.dice_player = self.round_death
                    self.dice = Dice(self.screen)
                else:
                    self.state = "round_end"
                self.state_timer = current_time
            return None
            
        if self.state == "dice_roll":
            dice_state = self.dice.update()

            if dice_state == "done":
                result = self.dice.result

                if result > 10:
                    # survived
                    if self.dice_player is self.player1:
                        self.p2_wins -= 1
                    else:
                        self.p1_wins -= 1

                    # prepare to load revive animation
                    death_frames = self.dice_player.animation_list["DEATH"]["ground"]
                    self.revive_frame_index = len(death_frames) - 1
                    self.revive_update_time = current_time

                    self.dice = None
                    self.state = "revive_animation"


                elif result == 10:
                    # re-roll
                    self.dice = Dice(self.screen)

                else: 
                    # cursed
                    if self.dice_player is self.player1:
                        self.p2_wins += 1
                    else:
                        self.p1_wins += 1
                    
                    self.dice = None
                    self.dice_player = None
                    self.state = "round_end"
                    self.state_timer = current_time

            return None
        
        if self.state == "revive_animation":
            death_frames = self.dice_player.animation_list["DEATH"]["ground"]
            animation_cooldown = self.dice_player.char_data["animations"]["DEATH"]["cooldown"]

            # reverse death animation frames
            if current_time - self.revive_update_time >= animation_cooldown:
                self.revive_frame_index -= 1
                self.revive_update_time = current_time

            index = max(0, self.revive_frame_index)
            self.dice_player.image = death_frames[index]

            # animation finished
            if self.revive_frame_index < 0:
                self.revive_fighter(self.dice_player)
                self.dice_player = None
                self.current_round += 1
                self.state = "countdown"
                self.state_timer = current_time
            
            return None

        if self.state == "round_end":
            if current_time - self.state_timer > con.ROUND_TEXT_DURATION:
                    self.state = "fade_out"
                    self.state_timer = current_time
            return None
        
        if self.state == "fade_out":
            passed_time = current_time - self.state_timer
            if passed_time <= con.FADE_OUT_DURATION:
                self.fade_alpha = int(con.MAX_ALPHA * passed_time / con.FADE_OUT_DURATION)
            else:
                self.loadfighters()
                self.fade_alpha = con.MAX_ALPHA
                self.state = "fade_in"
                self.state_timer = current_time
            return None

        if self.state == "fade_in":
            passed_time = current_time - self.state_timer
            if passed_time <= con.FADE_OUT_DURATION:
                self.fade_alpha = con.MAX_ALPHA - int(con.MAX_ALPHA * passed_time / con.FADE_OUT_DURATION)
            else:
                self.fade_alpha = 0
                self.current_round += 1
                if self.p1_wins >= self.max_wins or self.p2_wins >= self.max_wins:
                    self.state = "fight_end"
                else:
                    self.state = "countdown"
                self.state_timer = current_time
            return None
       
        if self.state == "fight_end":
            # Draw
            if self.p1_wins == self.p2_wins == self.max_wins: 
                self.winner = "DRAW!"
            elif self.p1_wins > self.p2_wins:
                self.winner = "WINNER:\nPLAYER 1"
            elif self.p2_wins > self.p1_wins:
                self.winner = "WINNER:\nPLAYER 2"
            return None

    
    def draw(self):
        x, y = self.screen_shake_offset
        draw_screen(self.screen, self.background, con.FLOOR_Y, con.FLOOR_HEIGHT, con.SCREEN_WIDTH, self.player1, self.player2, offset=(x, y))
        self.player1.draw(self.screen)
        self.player2.draw(self.screen)

        for pj in self.player1.projectiles:
            pj.draw(self.screen)
        for pj in self.player2.projectiles:
            pj.draw(self.screen)

        draw_round_ui(self)
        draw_round_indicator(self.screen, self.p2_wins, False)
        draw_round_indicator(self.screen, self.p1_wins, True)

        if self.state == "fight":
            round_time = pygame.time.get_ticks() - self.round_start_time
            display_seconds = max(0, (con.ROUND_DURATION - round_time) // 1000)
            draw_timer(self.screen, display_seconds)

        if self.fade_alpha > 0:
            self.fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(self.fade_surface, (0, 0))
        
        if self.state == "dice_roll" and self.dice:
            self.dice.draw()
        
        appBright(self.screen)
        
    def run(self):
        self.loadfighters()

        con.background_music.stop()
        con.forest_sfx.play(-1)
        con.fight_music.play(-1)

        debug = DebugPopup(self)

        self.state_timer = pygame.time.get_ticks()

        #loop for fightscreen
        while True:
            con.clock.tick(con.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = confscr(self.screen, self.clock, "Fight").run()
                    return result
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.player1.clean_up()
                    self.player2.clean_up()
                    con.forest_sfx.stop()
                    con.fight_music.stop()
                    con.exit_sound.play()
                    return "Menu"
                debug.handle_event(event)

            result = self.update()
            if result:
                return result

            self.draw()
            debug.draw(self.screen)
            res.render_to_surface()
            
