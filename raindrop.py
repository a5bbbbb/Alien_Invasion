# Try it yourself 13-3 Raindrops.

import pygame

from pygame.sprite import Sprite

class Raindrop(Sprite):

    """A class to represent a raindrop in a rain."""

    def __init__(self, ai_game):

        """Initialize the raindrop and set its starting position."""

        super().__init__()

        self.screen = ai_game.screen

        self.settings = ai_game.settings

        self.color = self.settings.raindrop_color

        self.rect = pygame.Rect(0, 0, self.settings.raindrop_width, self.settings.raindrop_height)

        # Start each new raindrop near the top of the screen

        self.rect.x = self.rect.width

        self.rect.y = self.rect.height

    
    def update(self):

        """Move the raindrop down the screen."""

        self.rect.y += self.settings.rain_drop_speed
    

    def has_disappeared(self):

        """Returns True if raindrop has disappeared down the screen."""

        return (self.rect.y >= self.screen.get_rect().height)
    
    
    def draw_raindrop(self):

        """Draw the raindrop to the screen."""

        pygame.draw.rect(self.screen, self.color, self.rect)


