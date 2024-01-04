import sys

import pygame

from settings import Settings

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


    def runGame(self):

        """Start the main loop for the game."""

        while True:

            # Watch for keyboard and mouse events

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    sys.exit()
            
            # Redraw the screen during each pass through the loop.
                    
            self.screen.fill(self.settings.bgColor)

            # Make the most recently drawn screen visible.
                    
            pygame.display.flip()

            # Setting the frame rate

            self.clock.tick(60)


if __name__ == '__main__':
    
    # Make a game instance, and run the game.

    ai = AlienInvasion()
    
    ai.runGame()
                    
            

        