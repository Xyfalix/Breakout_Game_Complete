import pygame


class Ball(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, radius, color):
        super().__init__()
        # load player sprite
        self.radius = radius
        self.color = color
        self.image = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surface=self.image, color=color, center=(radius, radius), radius=radius)
        self.rect = self.image.get_rect(center=(x_pos, y_pos))

    def update(self, x_direction, y_direction):
        self.rect.x += x_direction
        self.rect.y += y_direction

