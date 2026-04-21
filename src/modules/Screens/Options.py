import pygame


from src.modules.UI import constants as con
from src.modules.systems.applybright import apply_brightness as appBright
from src.modules.systems import res 
from src.modules.systems.scalemouse import scale_mouse

class Options():
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.font_large = pygame.font.SysFont("arial", 64)
        self.font_medium = pygame.font.SysFont("arial", 32)
        self.font_small = pygame.font.SysFont("arial", 16)

        # pygame uses 0-1  for volume, but we want to use 0-100, so we multiply
        self.volume = int(con.background_music.get_volume() * 100)
        self.brightness = con.brightness

        self.window_sizes = [
            (800,  480,  "800 x 480"),
            (1000, 600,  "1000 x 600"),
            (1280, 720,  "1280 x 720"),
            (1920, 1080,  "1920 x 1080"),
        ]
        self.window_size_index = con.window_size_index

        # same thing in help screen, allows text to be readable no matter what we choose as our final image
        self.overlay = pygame.Surface((con.SCREEN_WIDTH, con.SCREEN_HEIGHT), pygame.SRCALPHA)
        self.overlay.fill((100, 100, 100, 200)) # R, G, B, ALPHA (transparency)

        #slider customization
        self.slider_width = int(con.SCREEN_WIDTH / 2.5)
        self.slider_height = int(con.SCREEN_HEIGHT / 60)
        self.handle_radius = self.slider_height
        slider_x = con.center_x - self.slider_width // 2

        self.sliders = [
            {"name": "Volume", "setting": "volume", "x": slider_x, "y": int(con.SCREEN_HEIGHT / 2.91)},
            {"name": "Brightness", "setting": "brightness", "x": slider_x, "y": (con.SCREEN_HEIGHT / 2.07)},
        ]

        self.dragwhich = None # variable that stores which slider is being dragged,
        self.size_buttons = []

    def get_handle_x(self, slider):
        #gets value of the setting in question (volume or brightness)
        val = getattr(self, slider["setting"])
        # position in the slider
        precentage = val /100
        #multiply by width to get the position
        offset = precentage * self.slider_width
        #return the position where the handle should be drawn at
        return int(slider["x"] + offset)

    def get_val_from_mouse(self, slider, mouse_x):
        # how many pixels from the start of the slider
        offset = mouse_x - slider["x"]
        precentage = offset / self.slider_width
        # min is 0 max in 100
        if precentage < 0:
            precentage = 0
        if precentage > 1:
            precentage = 1
        # turn % back into 0-100 value and return it
        return int(precentage * 100)

    # change the volumes for all possible sounds, in constants
    def apply_volume(self):
        con.background_music.set_volume(self.volume / 100)
        con.forest_sfx.set_volume(self.volume / 100)
        con.volume = self.volume / 100
        con.select_sound.set_volume(self.volume / 100)
        con.exit_sound.set_volume(self.volume / 100)
        con.fight_music.set_volume(self.volume / 100)
 
    #change the brightness
    def changeBrightness(self):
        con.brightness = self.brightness

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
        title = self.font_large.render("Options", True, con.YELLOW)
        self.screen.blit(title, title.get_rect(center=(con.center_x, int(con.SCREEN_HEIGHT/6.75))))

        # draw sliders
        for slider in self.sliders:
            # get current value of slider
            val = getattr(self, slider["setting"])
            name_text = f"{slider['name']}: {val}%"
            name_surf = self.font_medium.render(name_text, True, con.WHITE)
            self.screen.blit(name_surf, name_surf.get_rect(center=(con.center_x, slider["y"] - int(con.SCREEN_HEIGHT / 36))))

            # grey background for slider 
            track = pygame.Rect(slider["x"], slider["y"] - self.slider_height // 2, self.slider_width, self.slider_height)
            pygame.draw.rect(self.screen, con.GREY, track, border_radius=6)

            # color indicator for slider.
            handle_x = self.get_handle_x(slider)
            fill = pygame.Rect(slider["x"], slider["y"] - self.slider_height // 2, handle_x - slider["x"], self.slider_height)
            pygame.draw.rect(self.screen, con.YELLOW, fill, border_radius=6)

            # draw a handle (white circle), at current position.
            pygame.draw.circle(self.screen, con.WHITE, (handle_x, slider["y"]), self.handle_radius)

        # window size txt
        butt_y = int(con.SCREEN_HEIGHT / 1.44)
        butt_name = self.font_medium.render("Window size:", True, con.WHITE)
        self.screen.blit(butt_name, butt_name.get_rect(center=(con.center_x, butt_y - 90)))

        # button info
        butt_width = int(con.SCREEN_WIDTH / 9.6)
        butt_height = int(con.SCREEN_HEIGHT / 21.6)
        butt_gap = int(con.SCREEN_WIDTH / 38.4)
        #total width of all buttons to center them on screen
        total_width = len(self.window_sizes) * butt_width + (len(self.window_sizes) - 1) * butt_gap
        start_x = con.center_x - total_width // 2

        self.size_buttons = []
        for i, (width, height, setting_string) in enumerate(self.window_sizes):
            # where each button should be placed
            butt_x = start_x + i * (butt_width + butt_gap)
            rect = pygame.Rect(butt_x, butt_y - butt_height // 2, butt_width, butt_height)
            self.size_buttons.append(rect)

            # yellow highlight means selected everything else is grey, the text color is always black
            if i == self.window_size_index:
                butt_color = con.YELLOW
                txt_color = con.BLACK
            else:
                butt_color = con.GREY
                txt_color = con.BLACK

            pygame.draw.rect(self.screen, butt_color, rect, border_radius=5)
            butt_txt = self.font_small.render(setting_string, True, txt_color)
            self.screen.blit(butt_txt, butt_txt.get_rect(center=rect.center))

        exit_txt = self.font_medium.render("Press ESC to return to main menu", True, con.YELLOW)
        self.screen.blit(exit_txt, exit_txt.get_rect(center=(con.center_x, con.SCREEN_HEIGHT - 50)))
        # apply the brightness to everything
        appBright(self.screen)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "Menu"

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    #get mouse positions
                    mx, my = scale_mouse()

                    # check if clicked on slider if yes then update the slider it was clicked on and change its respective setting
                    for i, slider in enumerate(self.sliders):
                        track = pygame.Rect(slider["x"], slider["y"] - self.slider_height // 2, self.slider_width, self.slider_height)

                        if track.collidepoint(mx, my):
                            self.dragwhich = i
                            setattr(self, slider["setting"], self.get_val_from_mouse(slider, mx))
                            if slider["setting"] == "volume":
                                self.apply_volume()
                            if slider["setting"] == "brightness":
                                self.changeBrightness()

                    # check if user clicked on any window size buttons if yes then change resolution
                    for i, rect in enumerate(self.size_buttons):
                        if rect.collidepoint(mx, my):
                            self.window_size_index = i
                            self.change_Win_Size()
                
                #if mouse is moving and slider is being dragged we update itsvalue
                if event.type == pygame.MOUSEMOTION and self.dragwhich is not None:
                    mx, my = scale_mouse()
                    slider = self.sliders[self.dragwhich]
                    setattr(self, slider["setting"], self.get_val_from_mouse(slider, mx))
                    if slider["setting"] == "volume":
                        self.apply_volume()
                    if slider["setting"] == "brightness":
                        self.changeBrightness()

                #stop dragging upon mouse button release
                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.dragwhich = None

            self.draw()
            con.clock.tick(con.FPS)
            res.render_to_surface()