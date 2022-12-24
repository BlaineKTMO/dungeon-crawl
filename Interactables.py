import pygame
import os


class Interactables(pygame.sprite.Sprite):
    """Base class for interactable objects"""

    def __init__(self, name, image, pos):
        super().__init__()

        self.name = name
        self.image, self.rect = self.load_image(image)
        self.rect.x, self.rect.y = pos

    def load_image(self, name):
        path = os.path.join('data', name)
        image = pygame.image.load(path)

        return image, image.get_rect()


class Text(Interactables):
    """Text box interactables"""

    def __init__(self, name, image, pos):
        super().__init__(name, image, pos)
