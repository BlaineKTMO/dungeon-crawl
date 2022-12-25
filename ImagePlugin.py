import pygame
import os


class Image():
    def load_image(self, name):
        path = os.path.join('data', name)
        image = pygame.image.load(path)

        return image, image.get_rect()
