import ImagePlugin
import pygame


class Interactables(pygame.sprite.Sprite, ImagePlugin.Image):
    """Base class for interactable objects"""

    def __init__(self, name, image, pos):
        super().__init__()
        self.image, self.rect = self.load_image(image)

        self.name = name
        self.rect.x, self.rect.y = pos


class Text(Interactables):
    """Text box interactables"""

    def __init__(self, name, image, pos):
        super().__init__(name, image, pos)
