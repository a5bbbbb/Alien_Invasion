import sys

import pygame

from settings import Settings

from ship import Ship

class AlienInvasion:

    """Overall class to manage game assets and behavior."""

    def __init__(self):

        """Intialize the game, and create game resources."""

        pygame.init()

        # Make sure that game runs at consistent frame rate across all platforms.

        self.clock = pygame.time.Clock()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screenWidth,self.settings.screenHeight))

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)


    def runGame(self):

        """Start the main loop for the game."""

        while True:

            self._check_events()
            
            self.ship.update()

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
                
                if event.key == pygame.K_RIGHT:
                    
                    self.ship.movingRight = True
                
                if event.key == pygame.K_LEFT:

                    self.ship.movingLeft = True
                
            elif event.type == pygame.KEYUP:

                if event.key == pygame.K_RIGHT:

                    self.ship.movingRight = False
                
                if event.key == pygame.K_LEFT:

                    self.ship.movingLeft = False        
                





    
    def _update_screen(self):

        """Update images on the screen, and flip to the new screen."""

        # Redraw the screen during each call.
                    
        self.screen.fill(self.settings.bgColor)

        self.ship.blitme()

        # Make the most recently drawn screen visible.
                
        pygame.display.flip()





if __name__ == '__main__':
    
    # Make a game instance, and run the game.

    ai = AlienInvasion()
    
    ai.runGame()
                    
            

        