import pygame
import math
import os
import Weapons


class Character(pygame.sprite.Sprite):
    """Base class for all character objects"""

    def __init__(self, name, group,  pos, health, image):
        """Base class constructor"""

        # Retrieve sprite
        self.image, self.rect = image
        self.rect.x, self.rect.y = pos

        self.health = health

        self.invincible = False
        self.dmg_time = 0

        # Group in which the character is contained in
        self.group = group

        # Add to group
        super().__init__(group)

    def take_dmg(self, dmg):
        """Reduces health by dmg (int)"""

        if not self.invincible:

            self.health -= dmg
            self.invincible = True
            self.dmg_time = pygame.time.get_ticks()

    def heal(self, heal):
        """Increases health by heal (int)"""

        self.health += heal

    def move(self, delta_x=0, delta_y=0):
        """Adjusts position of character"""
        self.delta_x, self.delta_y = delta_x, delta_y

        self.rect.x += delta_x * self.speed
        self.rect.y += delta_y * self.speed

        if self.rect.top < 50:
            self.rect.top = 50
        elif self.rect.bottom > 325:
            self.rect.bottom = 325

        if self.rect.left < 50:
            self.rect.left = 50
        elif self.rect.right > 650:
            if self.rect.center[1] < 190 or self.rect.center[1] > 225:
                self.rect.right = 650

    def update(self, delta_x=0, delta_y=0):
        """pygame update function called by groups"""

        if self.health <= 0:
            print("dead")
            self.group.remove(self)

        self.move(delta_x, delta_y)

        self.time_since = pygame.time.get_ticks() - self.dmg_time

        # 1/2 second
        if self.time_since > 500:
            self.invincible = False

    # Does't work
    def drawOnScreen(self, surface):
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)

        self.draw(surface)

        # Draw Health
        health_percent = self.health/self.max_hp

        pygame.draw.rect(surface, BLACK,
                         (self.rect.left, self.rect.top - 7, 15, 3))
        pygame.draw.rect(surface, RED,
                         (self.rect.left, self.rect.top - 7, 15 * health_percent, 3))


class Player(Character):
    """Player controlled character"""

    UP = pygame.K_w
    DOWN = pygame.K_s
    LEFT = pygame.K_a
    RIGHT = pygame.K_d

    arr_up = pygame.K_UP
    arr_down = pygame.K_DOWN
    arr_left = pygame.K_LEFT
    arr_right = pygame.K_RIGHT

    def __init__(self, speed, **kwargs):

        super().__init__(**kwargs)

        self.dir = "RIGHT"
        self.speed = speed

        self.max_hp = 250
        self.mana = 50
        self.item = None
        self.weapon = None

        path = os.path.join('data', 'walk.wav')
        self.walk = pygame.mixer.Sound(path)

    def use_key(self):
        pass

    def pick_up_item(self, _item):
        pass

    def pick_up_weapon(self, weapon):
        self.weapon = weapon
        self.weapon.rect.x, self.weapon.rect.y = self.rect.x + 8, self.rect.y

    def health_pot(self):
        pass

    def update(self, keys):
        delta_x, delta_y = 0, 0

        # Player movement
        if not self.weapon.attacking:
            if keys[self.UP]:
                delta_y = -1
                self.walk.play()
            elif keys[self.DOWN]:
                delta_y = 1
                self.walk.play()
            elif keys[self.LEFT]:
                delta_x = -1
                self.walk.play()
            elif keys[self.RIGHT]:
                delta_x = 1
                self.walk.play()
        else:
            delta_x, delta_y = 0, 0

        if keys[self.arr_up]:
            self.weapon.attack("up")
            self.weapon.rect.x, self.weapon.rect.y = self.rect.x + \
                (self.rect.width/2), self.rect.y - 25

        elif keys[self.arr_down]:
            self.weapon.attack("down")
            self.weapon.rect.x, self.weapon.rect.y = self.rect.x + \
                (self.rect.width/2), self.rect.y + 20

        elif keys[self.arr_left]:
            self.weapon.attack("left")
            self.weapon.rect.x, self.weapon.rect.y = self.rect.x - \
                25, self.rect.y + (self.rect.height/2)

        elif keys[self.arr_right]:
            self.weapon.attack("right")
            self.weapon.rect.x, self.weapon.rect.y = self.rect.x + \
                16, self.rect.y + (self.rect.height/2)

        super().update(delta_x, delta_y)
        self.weapon.update()

        # Keeps weapon a fixed distance from player
        if not self.weapon.attacking:
            if self.weapon != None:
                if self.weapon.dir == "up":
                    self.weapon.rect.x, self.weapon.rect.y = self.rect.x + \
                        (self.rect.width/2), self.rect.y - 25

                elif self.weapon.dir == "down":
                    self.weapon.rect.x, self.weapon.rect.y = self.rect.x + \
                        (self.rect.width/2), self.rect.y + 20

                elif self.weapon.dir == "left":
                    self.weapon.rect.x, self.weapon.rect.y = self.rect.x - \
                        25, self.rect.y + (self.rect.height/2)

                elif self.weapon.dir == "right":
                    self.weapon.rect.x, self.weapon.rect.y = self.rect.x + \
                        16, self.rect.y + (self.rect.height/2)


# Create soft state switching
class Enemy(Character):
    """Base class for AI enemy characters"""

    def __init__(self, player, **kwargs):
        super().__init__(**kwargs)

        # self.dir = "left"
        self.delta_x, self.delta_y = 0, 0
        self.player = player
        self.move_away = False
        self.last_move_away_timer = 0

    def auto_move(self, player):
        """Pathfinding for enemies"""
        if self.move_away == True:

            if pygame.time.get_ticks() - self.last_move_away_timer > 250:
                x = self.delta_x * -1
                y = self.delta_y * -1

                strength = 2
                self.move(x * strength, y * strength)

            self.move_away = False
            self.last_move_away_timer = pygame.time.get_ticks()

        else:
            # Unity style movement
            # First finds direction vector, then normalizes it to create unit vector.
            goal_x, goal_y = player.rect.x, player.rect.y

            dx = goal_x - self.rect.x
            dy = goal_y - self.rect.y

            distance = math.hypot(dx, dy)

            if distance > 3:
                dx, dy = dx/distance, dy/distance

                # Final vector created by scaling unit vector by speed in the base class move method
                self.delta_x = dx
                self.delta_y = dy
            else:
                self.delta_x, self.delta_y = 0, 0

    def update(self):

        self.auto_move(self.player)
        super().update(self.delta_x, self.delta_y)


class Zombie(Enemy):
    """Zombie Enemies:
    name (str) : File name of sprite;
    group (RenderPlain) : Pygame group of enemy objects;
    pos (int, int) : (x, y) Coordinates of enemy;
    health (int) : Enemy health value
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.speed = 1.5
        self.dmg = 10
        self.max_hp = 150


class Slime(Enemy):
    """Slime Enemies"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.speed = 2
        self.dmg = 20
        self.max_hp = 50

        self.time_since_dash = 0
        self.last_dash = 0

    def update(self):

        p_x, p_y = self.player.rect.center
        dx = self.rect.center[0] - p_x
        dy = self.rect.center[1] - p_y
        dist = math.hypot(dx, dy)

        self.time_since_dash = pygame.time.get_ticks() - self.last_dash

        if self.time_since_dash > 500 or dist < 20:
            self.speed = 2

        if dist < 50 and self.time_since_dash > 1000:
            try:
                dx /= dist
                dy /= dist
                self.speed = 6
                self.move(-dx, -dy)

                self.last_dash = pygame.time.get_ticks()

            except ZeroDivisionError:
                pass

        else:
            super().update()


class Mage(Enemy):
    """Mage Enemies"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.speed = 2
        self.dmg = 20

        self.projectiles = pygame.sprite.RenderPlain()
        self.max_hp = 100

        self.time_since_atk = 0
        self.last_atk = 0

    def attack(self):

        top = Weapons.Projectile("mage_projectile.png",
                                 (self.rect.center[0], self.rect.center[1] - 30), (0, -1), 3)
        bottom = Weapons.Projectile(
            "mage_projectile.png", (self.rect.center[0], self.rect.center[1] + 30), (0, 1), 3)
        left = Weapons.Projectile(
            "mage_projectile.png", (self.rect.center[0] - 30, self.rect.center[1]), (-1, 0), 3)
        right = Weapons.Projectile(
            "mage_projectile.png", (self.rect.center[0] + 30, self.rect.center[1]), (1, 0), 3)

        self.projectiles.add(top)
        self.projectiles.add(bottom)
        self.projectiles.add(left)
        self.projectiles.add(right)

        self.last_atk = pygame.time.get_ticks()

    def update(self):

        self.time_since_atk = pygame.time.get_ticks() - self.last_atk

        if self.time_since_atk > 2000:
            self.delta_x, self.delta_y = 0, 0
            self.attack()

        elif self.time_since_atk < 1500:
            super().update()

        self.projectiles.update(self.player, self.projectiles)
        self.projectiles.draw(screen)
