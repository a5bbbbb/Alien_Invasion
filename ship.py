import pygame 

class Ship:
    
    """A class to manage the ship."""

    def __init__(self, ai_game):

        """Initialize the ship and set its starting position."""
        
        self.screen = ai_game.screen

        self.settings = ai_game.settings

        self.screen_rect = ai_game.screen.get_rect()

        # Load the ship's image and get its rect.

        self.image = pygame.image.load('images/fighter.bmp')

        self.rect = self.image.get_rect()

        # Start each new ship at the bottom of the screen.

        self.rect.midleft = self.screen_rect.midleft

        # Store a float for the ship's exact horizontal position.

        self.y = float(self.rect.x)

        # Movement flag; start with a ship that's not moving.

        self.moving_up = False

        self.moving_down = False


    def update(self):

        """Update ships position based on the movement flag."""

        # Update the ship's x value, not the rect.

        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:

            self.y += self.settings.ship_speed

        if self.moving_up and self.rect.top > 0:

            self.y -= self.settings.ship_speed

        # Update rect object from self.x
        
        self.rect.y = self.y


    def blitme(self):

        """Draw the ship at its current location."""

        self.screen.blit(self.image, self.rect)

