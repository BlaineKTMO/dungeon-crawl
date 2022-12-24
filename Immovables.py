import pygame
import os


class Immovable(pygame.sprite.Sprite):
    def __init__(self, image, pos, group):
        super().__init__(group)
        self.image, self.rect = self.load_image(image)
        self.rect.x, self.rect.y = pos

    def update(self):
        pass

    def load_image(self, name):
        path = os.path.join('data', name)
        image = pygame.image.load(path)

        return image, image.get_rect()
