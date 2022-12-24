import pygame
import os


class Weapons(pygame.sprite.Sprite):
    """Base class for all weapons"""

    def __init__(self, name):

        self.name = name
        self.dir = "right"
        self.image = self.image_right
        self.rect = self.image.get_rect()

        self.dx, self.dy = 0, 0
        self.attacking = False
        self.reversed = False

        self.lock = False

        path = os.path.join('data', 'attack.wav')
        self.attack = pygame.mixer.Sound(path)

        super().__init__()

    def attack(self, direction):
        self.dir = direction
        self.attacking = True
        self.time_atk = pygame.time.get_ticks()

        if self.dir == "up":
            self.image = self.image_up
            self.dy = -2
        elif self.dir == "down":
            self.image = self.image_down
            self.dy = 2
        elif self.dir == "left":
            self.image = self.image_left
            self.dx = -2
        elif self.dir == "right":
            self.image = self.image_right
            self.dx = 2

        self.rect = self.image.get_rect()
        self.attack.play()

    def load_image(name):
        path = os.path.join('data', name)
        image = pygame.image.load(path)

        return image, image.get_rect()

    def update(self):

        if self.attacking:

            self.rect.x += self.dx
            self.rect.y += self.dy

            self.time_since_atk = pygame.time.get_ticks() - self.time_atk

            if self.time_since_atk >= 500:
                self.attacking = False
                self.reversed = False
                self.dx, self.dy = 0, 0

            elif self.time_since_atk >= 250 and not self.reversed:
                self.reversed = True
                self.dx *= -1
                self.dy *= -1


class Sword(Weapons):
    """Class for sword type weapon"""

    def __init__(self, name, img, dmg):

        self.image_up, self.rect_up = self.load_image(
            os.path.join(img, "0.png"))
        self.image_down, self.rect_down = self.load_image(
            os.path.join(img, "180.png"))
        self.image_left, self.rect_left = self.load_image(
            os.path.join(img, "270.png"))
        self.image_right, self.rect_right = self.load_image(
            os.path.join(img, "90.png"))

        self.desc = "Sword type"
        self.dmg = dmg
        self.durability = 100

        super().__init__(name)


class Hammer(Weapons):
    """Class for sword type weapon"""

    def __init__(self, name, img, dmg):

        self.image_up, self.rect_up = self.load_image(
            os.path.join(img, "0.png"))
        self.image_down, self.rect_down = self.load_image(
            os.path.join(img, "180.png"))
        self.image_left, self.rect_left = self.load_image(
            os.path.join(img, "270.png"))
        self.image_right, self.rect_right = self.load_image(
            os.path.join(img, "90.png"))

        self.desc = "Hammer type"
        self.dmg = dmg
        self.durability = 100

        super().__init__(name)


class Projectile(pygame.sprite.Sprite):

    def __init__(self, pos, dir_vect, speed):
        super().__init__()

        path = os.path.join('data', "mage_projectile")
        self.image = pygame.image.load(path)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        self.dmg = 30
        self.speed = speed
        self.dx, self.dy = dir_vect
        self.time_created = pygame.time.get_ticks()

    def update(self, player, projectiles):

        if pygame.time.get_ticks() - self.time_created > 1500:
            self.kill()

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        for sprite in pygame.sprite.spritecollide(player, projectiles, False):
            player.take_dmg(self.dmg)
            projectiles.remove(sprite)
