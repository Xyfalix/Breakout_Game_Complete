import pygame

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height, screen_width):
        super().__init__()
        # load player sprite
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill('blue')
        # shift player to the bottom middle of the screen.
        self.rect = self.image.get_rect(midbottom=(x_pos, y_pos))
        self.max_width = screen_width

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left >= 10:
            self.rect.x -= 10
        elif keys[pygame.K_RIGHT] and self.rect.right <= self.max_width - 10:
            self.rect.x += 10

    def update(self):
        self.movement()