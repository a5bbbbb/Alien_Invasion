import sys

import pygame

from settings import Settings

from ship import Ship

from bullet import Bullet

from alien import Alien

# Try it yourself 13-4 Raindrops.

from raindrop import Raindrop

class Alien_invasion:

    """Overall class to manage game assets and behavior."""

    def __init__(self):

        """Intialize the game, and create game resources."""

        pygame.init()

        # Make sure that game runs at consistent frame rate across all platforms.

        self.clock = pygame.time.Clock()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

        self.settings.screen_height = self.screen.get_rect().height

        self.settings.screen_width = self.screen.get_rect().width

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Try it yourself 13-4 Raindrops.

        self.rain_grid = pygame.sprite.Group()

        self._create_rain_grid()


    def run_game(self):

        """Start the main loop for the game."""

        while True:

            self._check_events()
            
            self.ship.update()

            self._update_bullets()

            self._update_aliens()

            self._update_rain()

            self._update_screen()

            # Setting the frame rate

            self.clock.tick(60)
    

    def _check_events(self):

        """Respond to keypresses and mouse events"""

         # Watch for keyboard and mouse events

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                sys.exit()

            elif event.type == pygame.KEYDOWN:
                
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:

                self._check_keyup_events(event)


    def _check_keydown_events(self, event):
        
        """Respond to keypresses."""

        if event.key == pygame.K_RIGHT:
                    
            self.ship.moving_right = True
        
        if event.key == pygame.K_LEFT:

            self.ship.moving_left = True

        if event.key == pygame.K_q:

            sys.exit()

        if event.key == pygame.K_SPACE:
            self._fire_bullet()
            

    def _check_keyup_events(self, event):

        """Respond to key releases."""

        if event.key == pygame.K_RIGHT:

            self.ship.moving_right = False
        
        if event.key == pygame.K_LEFT:

            self.ship.moving_left = False  


    def _fire_bullet(self):

        """Create a new bullet and add it to the bullet group."""

        if len(self.bullets) < self.settings.bullets_allowed:

            new_bullet = Bullet(self)

            self.bullets.add(new_bullet)


    def _update_bullets(self):

        """Update position of bullets and get rid of old bullets."""

        # Update bullets positions.

        self.bullets.update()
        
        # Get rid of bullets that have disappeared.

        for bullet in self.bullets.copy():

            if bullet.rect.bottom <= 0:
                
                self.bullets.remove(bullet)

    
    def _update_aliens(self):

        """Check if the fleet is at an edge, then update positions."""

        self._check_fleet_edges()

        self.aliens.update()

    def _check_fleet_edges(self):

        """Respond appropiately if any aliens have reached an edge."""

        for alien in self.aliens.sprites():
            
            if alien.check_edges():
                
                self._change_fleet_direction()

                break
    

    def _change_fleet_direction(self):

        """Drop the entire fleet and change the fleet's direction."""

        for alien in self.aliens.sprites():

            alien.rect.y += self.settings.fleet_drop_speed
        
        self.settings.fleet_direction *= -1

    
    def _create_fleet(self):

        """Create the fleet of aliens."""

        # Create an alien and keep adding aliens until there's no room left.

        # Spacing between aliens is one alien width and one alien height.

        alien = Alien(self)

        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height

        while current_y < (self.settings.screen_height - 3 * alien_height):

            while current_x < (self.settings.screen_width - 2 * alien_width):

                self._create_alien(current_x, current_y)

                current_x += 2 * alien_width
            
            # Finished a row; reset x value, and increment y value.
            
            current_x = alien_width

            current_y += 2 * alien_height


    
    def _create_alien(self, x_position, y_position):

        """Create new alien and place it in the row."""

        new_alien = Alien(self)

        new_alien.x = x_position

        new_alien.rect.x = x_position
        
        new_alien.rect.y = y_position

        self.aliens.add(new_alien)


    # Try it yourself 13-4 Raindrops.

    def _update_rain(self):

        """Delete raindrops that have disappeared; add new row of raindrops when one at the bottom disappears; update position of the raindrops."""

        self._delete_disappeared_raindrops()

        self._check_top_row()

        self.rain_grid.update()


    def _delete_disappeared_raindrops(self):

        """Delete disappeared raindrops."""

        for raindrop in self.rain_grid.copy():

            if raindrop.has_disappeared():

                self.rain_grid.remove(raindrop)

    
    def _check_top_row(self):

        """Add a new row of raindrops if there is enough room."""

        good = True

        for raindrop in self.rain_grid:

            if raindrop.rect.y < 2 * raindrop.rect.height:

                good = False

                break
        
        if good:

            self._add_new_raindrop_row(0)

    
    def _add_new_raindrop_row(self, y_position):

        """Add a new row of raindrops."""

        raindrop = Raindrop(self)

        raindrop_width = raindrop.rect.width

        current_x = raindrop_width

        while current_x < (self.settings.screen_width - 2 * raindrop_width):

            self._create_raindrop(current_x, y_position)

            current_x += 2 * raindrop_width


    def _create_raindrop(self, x_position, y_position):

        """Create new raindrop and place it in the row."""

        new_raindrop = Raindrop(self)

        new_raindrop.rect.x = x_position

        new_raindrop.rect.y = y_position

        self.rain_grid.add(new_raindrop)


    def _create_rain_grid(self):

        raindrop = Raindrop(self)

        raindrop_height = raindrop.rect.height

        current_y = 0

        while current_y < (self.settings.screen_height - raindrop_height):

            self._add_new_raindrop_row(current_y)

            current_y += 2 * raindrop_height


    def _update_screen(self):

        """Update images on the screen, and flip to the new screen."""

        # Redraw the screen during each call.
                    
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            
            bullet.draw_bullet()

        self.ship.blitme()

        # self.aliens.draw(self.screen)

        # Try it yourself 13-4 Raindrops.

        for raindrop in self.rain_grid.sprites():
            
            raindrop.draw_raindrop()

        # Make the most recently drawn screen visible.
                
        pygame.display.flip()





if __name__ == '__main__':
    
    # Make a game instance, and run the game.

    ai = Alien_invasion()
    
    ai.run_game()
                    
            

        