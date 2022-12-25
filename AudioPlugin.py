import os
import pygame


class Audio():
    def __init__(self):
        pass

    def load_sound(self, name):
        pass

    def load_music(self, name):
        path = os.path.join('data', name)
        pygame.mixer.music.load(path)
