import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import  Bullet
from alien import  Alien
from time import sleep
from game_stats import  GameStats
from button import Button
from scoreboard import Scoreboard




class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    def __init__(self):
        """Initialize the pygame and create the game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        # self.bg_color =(230,230,230)
        self.screen  = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height=self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")
        # Create an instance to store game statistics, and create a scoreboard
        self.stats = GameStats(self)
        self.sb= Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        #Start Alien Invasion in an active state
        self.game_active = False

        # make the play button
        self.play_button= Button(self,"Play")


    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this same as ship got hit
                self.ship_hit()
                break

    def ship_hit(self):
        """Respond to the ship being hit by the alien """
        if self.stats.ships_left>0:
            #Decrement ships_left , and update scoreboard
            self.stats.ships_left-=1
            self.sb.prep_ships()

            # Get rid of any remaining alien ar bullet
            self.aliens.empty()
            self.bullets.empty()

            # Create new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # pause
            sleep(0.5)
        else:
            self.game_active=False
            pygame.mouse.set_visible(True)


    def _update_aliens(self):
        """Check if the fleet is at the edge, then update the position  """
        self._check_fleet_edges()
        self.aliens.update()
        #Look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()

        # Look for alien hitting the bottom of the screen
        self._check_aliens_bottom()


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached the edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y+=self.settings.fleet_drop_speed
        self.settings.fleet_direction*=-1


    def _create_fleet(self):
        """Create the fleet of the aliens"""
        #Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height
        alien =Alien(self)
        alien_width ,alien_height = alien.rect.size


        current_x ,current_y= alien_width,alien_height
        while current_y < (self.settings.screen_height-3*alien_height):
            while current_x <(self.settings.screen_width - 2*alien_width):
                self._create_alien(current_x,current_y)
                current_x+=2*alien_width

            #Finished a row reset the x value and increment y value.
            current_x = alien_width
            current_y+=2*alien_height

    def _create_alien(self,x_position ,y_position):
        """Create an alien and place it in the fleet"""
        new_alien = Alien(self)
        new_alien.x= x_position
        new_alien.rect.x=x_position
        new_alien.rect.y=y_position
        self.aliens.add(new_alien)

    def _update_bullets(self):
        """Update the position of the bullets and get rid of the old bullets"""
        # Update the bullet position
        self.bullets.update()
        # Get rid of the bullet that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collision()


    def _check_bullet_alien_collision(self):
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #increase level
            self.stats.level+=1
            self.sb.prep_level()

        # Check for any bullets that have hit aliens
        #if so , then get rid of that bullet and alien
        collisions = pygame.sprite.groupcollide(self.bullets,self.aliens,True ,True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score+=self.settings.alien_points*len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        print(len(self.bullets))


    def _check_events(self):
        # Watch for keyboard and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event=event)
            elif event.type==pygame.KEYUP:
                self._check_keyup_events(event=event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self,mouse_pos):
        """Start new game whenever player clicks play """
        button_clicked= self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            #Reset the game settings
            self.settings.initialize_dynamic_settings()
            #Reset the game stats
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active=True

            # Get rid of any remaining bullets or aliens
            self.bullets.empty()
            self.aliens.empty()

            #Create new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event ):
        """Handles the key presses."""
        if event.key == pygame.K_RIGHT:
            # move the ship to right
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self,event):
        """Handles the key releases """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # Create a new bullet and add it to bullets group
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()

        self.aliens.draw(self.screen)

        #Draw the score information
        self.sb.show_score()

        # Draw the play button if the game is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # Make the most recently drawn screen visible.
        pygame.display.flip()


if __name__=='__main__':
    # Make a game instance , and run the game.
    ai = AlienInvasion()
    ai.run_game()