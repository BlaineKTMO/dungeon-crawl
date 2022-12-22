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
        attack.play()

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

        self.image_up, self.rect_up = load_image(os.path.join(img, "0.png"))
        self.image_down, self.rect_down = load_image(
            os.path.join(img, "180.png"))
        self.image_left, self.rect_left = load_image(
            os.path.join(img, "270.png"))
        self.image_right, self.rect_right = load_image(
            os.path.join(img, "90.png"))

        self.desc = "Sword type"
        self.dmg = dmg
        self.durability = 100

        super().__init__(name)


class Hammer(Weapons):
    """Class for sword type weapon"""

    def __init__(self, name, img, dmg):

        self.image_up, self.rect_up = load_image(os.path.join(img, "0.png"))
        self.image_down, self.rect_down = load_image(
            os.path.join(img, "180.png"))
        self.image_left, self.rect_left = load_image(
            os.path.join(img, "270.png"))
        self.image_right, self.rect_right = load_image(
            os.path.join(img, "90.png"))

        self.desc = "Hammer type"
        self.dmg = dmg
        self.durability = 100

        super().__init__(name)
