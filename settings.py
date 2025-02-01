class Settings:
    """A class to store all settings for Alien Invasion"""
    def __init__(self):
        """Initialize the game's static settings"""
         # Screen setting
        self.screen_width = 1000
        self.screen_height = 650
        self.bg_color = (230,230,230)
        # Ships settings
        self.ship_limit =3
        self.ship_speed = None

        #Bullets settings
        self.bullet_speed=2.5
        self.bullet_width = 3
        self.bullet_height=15.0
        self.bullet_color = (60,60,60)
        self.bullet_allowed = 5

        # Alien settings
        self.alien_speed=1.0
        self.fleet_drop_speed =10
        self.fleet_direction = None

        #How quickly game speedups
        self.speedup_scale=1.1
        self.initialize_dynamic_settings()
        # Score setting
        self.alien_points = None
        self.score_scale= 1.5

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game"""
        self.ship_speed= 1.5
        self.bullet_speed=2.5
        self.alien_speed=1.0
        # Fleet direction of 1 represent right , -1 represent left
        self.fleet_direction =1
        self.alien_points=50

    def increase_speed(self):
        """Increase speed settings and alien point values"""
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale
        self.alien_points= int(self.alien_points*self.score_scale)
        print(self.alien_points)


