import pygame 

class Ship:
    
    """A class to manage the ship."""

    def __init__(self, ai_game):

        """Initialize the ship and set its starting position."""
        
        self.screen = ai_game.screen

        self.screenRect = ai_game.screen.get_rect()

        # Load the ship's image and get its rect.

        self.image = pygame.image.load('images/fighter.bmp')

        self.rect = self.image.get_rect()

        # Start each new ship at the bottom of the screen.

        self.rect.midbottom = self.screenRect.midbottom

        # Movement flag; start with a ship that's not moving.

        self.movingRight = False

        self.movingLeft = False


    def update(self):

        """Update ships position based on the movement flag."""

        if self.movingRight == True:

            self.rect.x += 1

        if self.movingLeft == True:

            self.rect.x -= 1


    def blitme(self):

        """Draw the ship at its current location."""

        self.screen.blit(self.image, self.rect)

