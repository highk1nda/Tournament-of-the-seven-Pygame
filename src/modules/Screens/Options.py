import pygame


from src.modules.UI import constants as con
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res 
from src.modules.systems.scalemouse import scale_mouse
from src.modules.Screens.ConfirmScreen import confirm_dialog as confscr
from src.modules.UI.Slider import Slider
from src.modules.UI.Button import Button

class Options():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.window_sizes = [
            (1000, 600,  "1000 x 600"),
            (1280, 720,  "1280 x 720"),
            (1600, 900,  "1600 x 900"),
            (1920, 1080, "1920 x 1080"),
        ]

        self.window_size_index = con.window_size_index

        # same thing in help screen, allows text to be readable no matter what we choose as our final image
        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((5, 5, 5, 220)) # R, G, B, ALPHA (transparency)

        #slider customization
        self.slider_width = int(con.SCREEN_WIDTH / 2.5)
        self.slider_height = int(con.SCREEN_HEIGHT / 60)
        slider_x = con.center_x - self.slider_width // 2

        self.musicSlider        = Slider(slider_x, int(con.SCREEN_HEIGHT * 0.30), self.slider_width, self.slider_height, initial=con.musicVolume, name="Music Volume")
        self.sfxSlider          = Slider(slider_x, int(con.SCREEN_HEIGHT * 0.42), self.slider_width, self.slider_height, initial=con.sfxVolume, name="SFX Volume")
        self.brightnessSlider   = Slider(slider_x, int(con.SCREEN_HEIGHT * 0.54), self.slider_width, self.slider_height, initial=con.brightness/100, name="Brightness")
        self.wintxt = con.font_Large.render("window size: ", True, con.YELLOW)

        self.butt_y = int(con.SCREEN_HEIGHT / 1.44)
        self.butt_width = int(con.SCREEN_WIDTH / 9.6)
        self.butt_height = int(con.SCREEN_HEIGHT / 21.6)
        self.butt_gap = int(con.SCREEN_WIDTH / 38.4)
        self.total_width = len(self.window_sizes) * self.butt_width + (len(self.window_sizes) - 1) * self.butt_gap
        self.start_x = con.center_x - self.total_width // 2

        self.firstres   = Button(self.start_x, self.butt_y, self.butt_width, self.butt_height, '1000 x 600', con.font_Large, 
                                 con.GREY, con.WHITE, con.YELLOW)
        self.secondres  = Button(self.start_x + self.butt_gap + self.butt_width, self.butt_y, self.butt_width, self.butt_height, 
                                 '1280 x 720', con.font_Large, con.GREY, con.WHITE, con.YELLOW)
        self.thirdres   = Button(self.start_x + self.butt_gap*2 + self.butt_width*2, self.butt_y, self.butt_width, self.butt_height, 
                                 '1600 x 900', con.font_Large, con.GREY, con.WHITE, con.YELLOW)
        self.fourthres  = Button(self.start_x + self.butt_gap*3 + self.butt_width*3, self.butt_y, self.butt_width, self.butt_height, 
                                 '1920 x 1080', con.font_Large, con.GREY, con.WHITE, con.YELLOW)
        self.buttons    = [self.firstres, self.secondres, self.thirdres, self.fourthres]


    # change the volumes for all possible sounds, in constants
    def apply_volume(self):
        con.musicVolume = self.musicSlider.value / 100
        con.sfxVolume = self.sfxSlider.value / 100
        con.select_sound.set_volume(con.sfxVolume)
        con.ui_error_sound.set_volume(con.sfxVolume)
        con.exit_sound.set_volume(con.sfxVolume)
        con.background_music.set_volume(con.musicVolume)
        con.fight_music.set_volume(con.musicVolume)

    #change the brightness
    def changeBrightness(self):
        con.brightness = self.brightnessSlider.value

    def change_Win_Size(self):
        #look up the chosen resolution from self.window_sizes and unpack it.
        width, height, setting_string = self.window_sizes[self.window_size_index]
        #change the constants to match selected resolution
        con.window = pygame.display.set_mode((width, height))
        con.window_size_index = self.window_size_index

    def draw(self):
        #draw background and the overlay
        self.screen.blit(con.background, (0, 0))
        self.screen.blit(self.overlay, (0, 0))

        #draw title
        title = con.font_Large.render("Options", True, con.YELLOW)
        self.screen.blit(title, title.get_rect(center=(con.center_x, int(con.SCREEN_HEIGHT/6.75))))

        self.musicSlider.draw(self.screen)
        self.sfxSlider.draw(self.screen)
        self.brightnessSlider.draw(self.screen)

        self.screen.blit(self.wintxt, self.wintxt.get_rect(center=(con.center_x, self.butt_y - 60)))

        for i, button in enumerate(self.buttons):
            if i == self.window_size_index:
                button.button_color = con.YELLOW
            else:
                button.button_color = con.GREY
            button.draw(self.screen)

        exit_txt = con.font_Medium.render("Press ESC to return to main menu", True, con.YELLOW)
        self.screen.blit(exit_txt, exit_txt.get_rect(center=(con.center_x, con.SCREEN_HEIGHT - 50)))
        # apply the brightness to everything
        appBright(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    result = confscr(self.screen, self.clock, "Options").run()
                    return result

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        con.exit_sound.play()
                        return "Menu"

                if self.musicSlider.handle_event(event) or self.sfxSlider.handle_event(event):
                    self.apply_volume()
                if self.brightnessSlider.handle_event(event):
                    self.changeBrightness()

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = scale_mouse()
                    for i, button in enumerate(self.buttons):
                        if button.is_clicked((mx, my), True):
                            self.window_size_index = i
                            self.change_Win_Size()


            self.draw()
            res.render_to_surface()
            con.clock.tick(con.FPS)