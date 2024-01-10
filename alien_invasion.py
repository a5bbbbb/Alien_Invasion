import sys

from time import sleep

import pygame

from settings import Settings

from ship import Ship

from bullet import Bullet

from alien import Alien

from game_stats import GameStats

from button import Button

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

        # Create an instance to store game statistics.

        self.stats = GameStats(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Start Alien Invasion in an inactive state.

        self.game_active = False
        
        # Make play button.

        self.play_button = Button(self, 'Play')

        # Try it yourself 14-4 Difficulty Levels.

        self.difficulty_buttons = {'Easy' : Button(self, 'Easy'), 
                                   'Middle' : Button(self, 'Middle'),
                                   'Hard' : Button(self, 'Hard')}
        
        self.difficulty_buttons['Easy'].move_from_center(0, 10 + self.play_button.height)
        
        self.difficulty_buttons['Middle'].move_from_center(0, 2 * ( 10 + self.play_button.height) )
        
        self.difficulty_buttons['Hard'].move_from_center(0, 3 * ( 10 + self.play_button.height) )


    def run_game(self):

        """Start the main loop for the game."""

        while True:

            self._check_events()

            if self.game_active:
            
                self.ship.update()

                self._update_bullets()

                self._update_aliens()

            self._update_screen()

            # Setting the frame rate

            self.clock.tick(60)
    

    def _check_events(self):

        """Respond to keypresses and mouse events"""

         # Watch for keyboard and mouse events

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = pygame.mouse.get_pos()

                self._check_play_button(mouse_pos)

                self._check_difficulty_buttons(mouse_pos)

            elif event.type == pygame.KEYDOWN:
                
                self._check_keydown_events(event)
                
            elif event.type == pygame.KEYUP:

                self._check_keyup_events(event)

    
    def _check_play_button(self, mouse_pos):

        """Start a new game when the player clicks Play."""

        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.game_active:

            # Reset the game settings.

            self.settings.initialize_dynamic_settings()

            self._set_difficulty()
            
            # Reset the game statistics.

            self.stats.reset_statistics()

            self.game_active = True

            # Get rid of any remaining bullets and aliens.

            self.bullets.empty()

            self.aliens.empty()

            # Create a new fleet and center the ship.

            self._create_fleet()

            self.ship.center_ship()
            
            # Hide the mouse cursor

            pygame.mouse.set_visible(False)

    # Try it yourself 14-4 Difficulty Levels.

    def _check_difficulty_buttons(self, mouse_pos):

        """Respond appropriately if any difficulty button was pressed."""

        for difficulty, button in self.difficulty_buttons.items():
            
            button_clicked = button.rect.collidepoint(mouse_pos)

            if button_clicked and not self.game_active:
                
                self.difficulty = difficulty

                break


    def _set_difficulty(self):

        """Set the game difficulty."""

        if self.difficulty == 'Easy':
            
            self.settings.ship_speed = 1.5

            self.settings.bullet_speed = 2.5

            self.settings.alien_speed = 1.0

            print('Easy difficulty was set')

        elif self.difficulty == 'Middle':
            
            self.settings.ship_speed = 2

            self.settings.bullet_speed = 4

            self.settings.alien_speed = 3

            print('Middle difficulty was set')

        elif self.difficulty == 'Hard':
            
            self.settings.ship_speed = 4

            self.settings.bullet_speed = 5

            self.settings.alien_speed = 4

            print('Hard difficulty was set')

        else:

            print("UNIDENTIFIED DIFFICULTY")


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

        self._check_bullet_alien_collisions()

    
    def _check_bullet_alien_collisions(self):

        """Respond to bullet-alien collisions."""

        # Remove any bullets and aliens that have collided.

        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if not self.aliens:

            # Destroy the existing bullets and create new fleet.

            self.bullets.empty()

            self._create_fleet()

            self.settings.increase_speed()

    
    def _update_aliens(self):

        """Check if the fleet is at an edge, then update positions."""

        self._check_fleet_edges()

        self.aliens.update()

        # Look for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):

            self._ship_hit()    

        # Look for aliens hitting the bottom of the screen.
        
        self._check_aliens_bottom()


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

    
    def _ship_hit(self):

        """Respond to a ship being hit by an alien."""

        if self.stats.ships_left > 0:

            # Decrement ships left.

            self.stats.ships_left -= 1

            # Get rid of any remaining bullets and aliens.

            self.bullets.empty()

            self.aliens.empty()

            # Create a new fleet and center the ship.

            self._create_fleet()

            self.ship.center_ship()

            # Pause

            sleep(0.5)

        else:

            self.game_active = False

            pygame.mouse.set_visible(True)


    
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

    
    def _check_aliens_bottom(self):

        """Check if any aliens have reached the bottom of the screen."""

        for alien in self.aliens.sprites():

            if alien.rect.bottom >= self.settings.screen_height:

                # Treat this the same as if the ship got hit.

                self._ship_hit()

                break


    def _update_screen(self):

        """Update images on the screen, and flip to the new screen."""

        # Redraw the screen during each call.
                    
        self.screen.fill(self.settings.bg_color)

        for bullet in self.bullets.sprites():
            
            bullet.draw_bullet()

        self.ship.blitme()

        self.aliens.draw(self.screen)

        # Draw the play button if the game is inactive.

        if not self.game_active:

            self.play_button.draw_button()

        # Try it yourself 14-4 Difficulty Levels.
            
        if not self.game_active:

            for key, button in self.difficulty_buttons.items():

                button.draw_button()

        # Make the most recently drawn screen visible.
                
        pygame.display.flip()





if __name__ == '__main__':
    
    # Make a game instance, and run the game.

    ai = Alien_invasion()
    
    ai.run_game()
                    
            

        