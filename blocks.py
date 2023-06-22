import pygame

class Blocks(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, width, height, color):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.image = pygame.Surface((width, height))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x_pos, y_pos))
        # assign score to block depending on color
        if self.color == 'red':
            self.value = 7
        elif self.color == 'orange':
            self.value = 5
        elif self.color == 'green':
            self.value = 3
        elif self.color == 'yellow':
            self.value = 1

