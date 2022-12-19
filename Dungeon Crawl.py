# Class : ITCS 1950 T/TH
# Student Name : Blaine Oania
# Last Edit Date : 28/4/2020
# File Name : Dungeon Crawl.py
# Description : Beta Release of Dungeon Crawl

import pygame
import os
import random
import math

SCRN_W, SCRN_H = 700, 400
pygame.init()
screen = pygame.display.set_mode((SCRN_W, SCRN_H))
arena = pygame.Surface((700, 400))

font_path = os.path.join('data', 'PressStart2P-vaV7.ttf')
font = pygame.font.Font(font_path, 20)
small_font = pygame.font.Font(font_path, 10)

clock = pygame.time.Clock()

player = None

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)


def load_image(name):
    path = os.path.join('data', name)
    image = pygame.image.load(path)

    return image, image.get_rect()

def load_music(name):
    path = os.path.join('music', name)
    music = pygame.mixer.music.load(path)

    return music


path = os.path.join('data', 'walk.wav')
walk = pygame.mixer.Sound(path)

path = os.path.join('data', 'attack.wav')
attack = pygame.mixer.Sound(path)


def tint(surf, tint_color):
    """ adds tint_color onto surf.
    """
    surf = surf.copy()
    surf.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    surf.fill(tint_color[0:3] + (0,), None, pygame.BLEND_RGBA_ADD)
    return surf

# # STATE SWITCHING - scrapped movement system
#
# class Character_States():
#     """Base class for all character states"""
#     def __init__(self):
#         self.done = False
#         self.next_state = None

# class Move_Right(Character_States):
#     """Character moving right state"""
#     def __init(self):
#         super().__init__()

#     def update(self, character):
#         """Moves character"""
#         character.rect.x += character.speed

#     def get_events(self, event):
#         """Retrieves current events"""
#         if event.type == pygame.KEYUP:
#             if event.key == pygame.K_d:
#                 self.next_state = "idle"

#             self.done = True

# class Idle(Character_States):
#     """Character Idle state"""
#     def __init__(self):
#         super().__init__()

#     def start_state(self):
#         """Begins current state"""

#     def update(self, character):
#         """Idle state does nothing"""
#         pass

#     def get_events(self, event):
#         if event.type == pygame.KEYDOWN:
#             # Switch to corresponding state for every direction
#             if event.key == pygame.K_d:
#                 self.next_state = "right"

#             self.done = True


# class Character_Controller():
#     """State controller for all characters"""

#     def setup_states(self, state_dictionary, initial_state):
#         """Creates state dictionary and sets initial state"""
#         self.state_dictionary = state_dictionary
#         self.state = self.state_dictionary[initial_state]

#     def change_state(self):
#         """Changes state"""
#         self.state = self.state_dictionary[self.state.next_state]

#     def state_update(self, character, event):
#         """Calls update of current state"""
#         if self.state.done == True:
#             self.change_state()
#         elif self.state.done == False:
#             self.state.get_events(event)
#             self.state.update(character)

# char_states = {
#     "idle" : Idle(),
#     "right" : Move_Right()
# }

class Character(pygame.sprite.Sprite):
    """Base class for all character objects"""

    def __init__(self, name, group,  pos, health):
        """Base class constructor"""

        # Retrieve sprite
        self.image, self.rect = load_image(name)
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

    def draw_health(self):
        health_percent = self.health/self.max_hp

        pygame.draw.rect(
            screen, BLACK, (self.rect.left, self.rect.top - 7, 15, 3))
        pygame.draw.rect(screen, RED, (self.rect.left,
                         self.rect.top - 7, 15 * health_percent, 3))


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
                walk.play()
            elif keys[self.DOWN]:
                delta_y = 1
                walk.play()
            elif keys[self.LEFT]:
                delta_x = -1
                walk.play()
            elif keys[self.RIGHT]:
                delta_x = 1
                walk.play()
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

        top = Projectile("mage_projectile.png",
                         (self.rect.center[0], self.rect.center[1] - 30), (0, -1), 3)
        bottom = Projectile(
            "mage_projectile.png", (self.rect.center[0], self.rect.center[1] + 30), (0, 1), 3)
        left = Projectile(
            "mage_projectile.png", (self.rect.center[0] - 30, self.rect.center[1]), (-1, 0), 3)
        right = Projectile(
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


class Projectile(pygame.sprite.Sprite):

    def __init__(self, image, pos, dir_vect, speed):
        super().__init__()

        self.image, self.rect = load_image(image)
        self.rect.x, self.rect.y = pos

        self.dmg = 30
        self.speed = speed
        self.dx, self.dy = dir_vect

        self.time_created = pygame.time.get_ticks()

    def update(self, player, projectiles):

        if pygame.time.get_ticks() - self.time_created > 1500:
            self.kill

        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed

        for sprite in pygame.sprite.spritecollide(player, projectiles, False):
            player.take_dmg(self.dmg)
            projectiles.remove(sprite)


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


class Interactables(pygame.sprite.Sprite):
    """Base class for interactable objects"""

    def __init__(self, name, image, pos):
        super().__init__()

        self.name = name
        self.image, self.rect = load_image(image)
        self.rect.x, self.rect.y = pos


class Text(Interactables):
    """Text box interactables"""

    def __init__(self, name, image, pos):
        super().__init__(name, image, pos)


class Immovable(pygame.sprite.Sprite):
    def __init__(self, image, pos, group):
        super().__init__(group)
        self.image, self.rect = load_image(image)
        self.rect.x, self.rect.y = pos

    def update(self):
        pass


class Game_Controller():
    """State controller for game"""

    def setup_states(self, state_dictionary, initial_state):
        """Creates state dictionary and sets initial state"""
        self.state_dictionary = state_dictionary
        self.state = self.state_dictionary[initial_state]
        self.state.start()

    def change_state(self):
        """Changes state"""
        self.state = self.state_dictionary[self.state.next_state]
        self.state.start()

    def state_update(self):
        """Calls update of current state"""
        if self.state.done == True:
            self.change_state()
        elif self.state.done == False:
            self.state.update()


class Game_States():
    """Base class for all game states"""

    def __init__(self):
        self.done = False
        self.next_state = None


class Main_Menu(Game_States):
    def __init__(self):
        super().__init__()

        self.player = None

        self.player_sprite = pygame.sprite.RenderPlain()
        self.weapon_sprites = pygame.sprite.RenderPlain()
        self.text_options = pygame.sprite.RenderPlain()

    def start(self):
        self.done = False
        # Loads Main Menu Room
        self.background, background_rect = load_image("arena.png")
        arena.blit(self.background, (0, 0))

        # Background Music
        bg_music = load_music("main_menu.ogg")
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)

        self.player = Player(speed=2, name="player_right.png",
                             group=self.player_sprite, pos=(200, SCRN_H/2), health=100)

        weapon = Sword("Base Sword", "base_sword", 20)
        self.weapon_sprites.add(weapon)

        self.player.pick_up_weapon(weapon)

        self.startText = Text("start", "start.png", (300, 150))
        self.credits = Text("credits", "credits.png", (300, 180))

        self.text_options.add(self.credits)
        self.text_options.add(self.startText)

    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

        keys = pygame.key.get_pressed()

        # Update calls
        self.player.update(keys)
        # Update calls #

        # Collision Detection
        # text is a Text Interactable object
        for text in pygame.sprite.spritecollide(self.player, self.text_options, False):
            if text.name == "start":
                self.next_state = "Game"
            # if text.name == "credits":
            #     self.next_state = "credits"

            self.end_state()
        # Collsion Detection #

        # Draw commands
        arena.blit(self.background, (0, 0))
        screen.blit(arena, (0, 0))
        self.player_sprite.draw(screen)
        for sprite in self.player_sprite:
            sprite.draw_health()
        self.weapon_sprites.draw(screen)
        self.text_options.draw(screen)
        pygame.display.flip()
        # Draw commands #

        clock.tick(60)

    def end_state(self):
        pygame.mixer.music.fadeout(500)

        self.done = True


class Main_Game(Game_States):
    """Gameplay state"""

    def __init__(self):
        super().__init__()

        self.player_sprite = pygame.sprite.RenderPlain()
        self.weapon_sprites = pygame.sprite.RenderPlain()
        self.enemy_sprites = pygame.sprite.RenderPlain()
        self.immovable_sprites = pygame.sprite.RenderPlain()
        self.exit = pygame.sprite.RenderPlain()

        self.room_num = 1

        self.menu = False
        self.hit_esc = 0

    def create_room(self):
        """Creates next room"""
        num_enemies = random.randint(3, 6)
        room_type = None
        room_layout = random.randint(0, 2)

        objects_in_room = []

        if room_layout == 0:
            # 12 torches spaced evenly in center of room

            x, y = 300, 75
            for j in range(4):
                for i in range(3):
                    new_object = Immovable(
                        "torch_1.png", (x, y), self.immovable_sprites)
                    objects_in_room.append(new_object)
                    x += new_object.rect.width * 5

                y += 75
                x = 300

        elif room_layout == 1:
            # Diamond torch pattern
            offset = 30
            x, y = 250, 175
            for i in range(3):
                x += offset
                y += offset
                new_object = Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)
            for i in range(3):
                x += offset
                y -= offset
                new_object = Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)

            x = 250
            for i in range(3):
                x += offset
                y -= offset
                new_object = Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)

            for i in range(3):
                x += offset
                y += offset
                new_object = Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)

        elif room_layout == 2:
            offset_x = 35
            offset_y = 20

            x, y = 200, 60
            for i in range(4):
                x -= offset_x
                y += offset_y
                new_object = Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)

            x, y = 475, 310
            for i in range(4):
                x += offset_x
                y -= offset_y
                new_object = Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)

            weapon = Hammer("hammer", "base_hammer", 30)
            weapon.rect.x, weapon.rect.y = 50, 50
            self.weapon_sprites.add(weapon)

        print(objects_in_room)

        # Creates enemies at random positions
        while len(self.enemy_sprites.sprites()) < num_enemies:
            pos = (random.randint(300, 500), random.randint(60, 300))
            spawn = True
            for sprite in objects_in_room:
                x, y = sprite.rect.center
                if abs(pos[0] - x) < 50:
                    spawn = False
            enemy = random.randint(0, 10)
            if enemy == 1:
                new_enemy = Mage(name="mage.png", player=self.player,
                                 group=self.enemy_sprites, pos=pos, health=100)
            elif enemy <= 5:
                new_enemy = Slime(name="slime.png", player=self.player,
                                  group=self.enemy_sprites, pos=pos, health=50)
            elif enemy <= 10:
                new_enemy = Zombie(name="Zombie.png", player=self.player,
                                   group=self.enemy_sprites, pos=pos, health=150)
            objects_in_room.append(new_enemy)

        print(len(self.enemy_sprites.sprites()))

        # Room exit
        self.exit.add(Interactables("exit", "right_exit.png", (670, 190)))

    def next_room(self):

        # Reposition Player
        self.player.rect.center = (150, SCRN_H/2)

        # Clear room contents
        self.enemy_sprites.empty()
        self.immovable_sprites.empty()
        self.exit.empty()

        # Small pause
        start_time = pygame.time.get_ticks()
        time_passed = 0
        while time_passed < 500:
            time_passed = pygame.time.get_ticks() - start_time

        self.room_num += 1
        self.create_room()

    def start(self):
        """Starts main game state"""
        self.done = False
        # Loads Starting Room
        self.room, room_rect = load_image("arena.png")
        arena.blit(self.room, (0, 0))

        self.room_num = 1

        # Background Music
        bg_music = load_music("main_game.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

        self.player = Player(speed=4, name="player_right.png",
                             group=self.player_sprite, pos=(150, SCRN_H/2), health=250)
        weapon = Sword("Base Sword", "base_sword", 20)
        self.weapon_sprites.add(weapon)

        self.player.pick_up_weapon(weapon)

        self.create_room()

    def restart(self):
        # Clear room contents
        self.player_sprite.empty()
        self.weapon_sprites.empty()
        self.enemy_sprites.empty()
        self.immovable_sprites.empty()
        self.exit.empty()

        # Small pause
        start_time = pygame.time.get_ticks()
        time_passed = 0
        while time_passed < 500:
            time_passed = pygame.time.get_ticks() - start_time

        self.start()

    def update(self):
        """Main game loop"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

        keys = pygame.key.get_pressed()

        # Room counter
        self.room_counter = font.render(
            "Room:" + str(self.room_num), True, WHITE)
        global screen
        arena.blit(self.room, (0, 0))
        screen.blit(arena, (0, 0))
        screen.blit(self.room_counter, (550, 10))

        darken = pygame.Surface((700, 400))

        if self.menu == False:
            if keys[pygame.K_ESCAPE] and pygame.time.get_ticks() - self.hit_esc > 200:
                self.menu = True
                self.hit_esc = pygame.time.get_ticks()

        if self.menu == False:
            # Update calls
            self.player.update(keys)
            self.enemy_sprites.update()
            # Update calls #

            # Collision Detection

            # Player to immovable object collision
            for wall in pygame.sprite.spritecollide(self.player, self.immovable_sprites, False):
                if self.player.delta_x > 0:
                    # Moving right
                    self.player.rect.right = wall.rect.left
                elif self.player.delta_x < 0:
                    # Moving left
                    self.player.rect.left = wall.rect.right
                if self.player.delta_y > 0:
                    # Moving down
                    self.player.rect.bottom = wall.rect.top
                elif self.player.delta_y < 0:
                    # Moving up
                    self.player.rect.top = wall.rect.bottom

            # Enemy to immovable object collision
            for enemy, immovable in pygame.sprite.groupcollide(self.enemy_sprites, self.immovable_sprites, False, False).items():
                if enemy.delta_x > 0:
                    enemy.rect.right = immovable[0].rect.left
                elif enemy.delta_x < 0:
                    enemy.rect.left = immovable[0].rect.right
                if enemy.delta_y > 0:
                    enemy.rect.bottom = immovable[0].rect.top
                elif enemy.delta_y < 0:
                    enemy.rect.top = immovable[0].rect.bottom

            # Enemy to Enemy collision
            for enemy in self.enemy_sprites:
                temp_grp = self.enemy_sprites.copy()
                temp_grp.remove(enemy)
                for colliding_enemy in pygame.sprite.spritecollide(enemy, temp_grp, False):
                    enemy.move_away = True
                    colliding_enemy.move_away = False

            # Weapon to enemy collision
            # enemy is an item of list of enemy_sprites which collide with weapon
            for enemy in pygame.sprite.spritecollide(self.player.weapon, self.enemy_sprites, False):
                enemy.take_dmg(self.player.weapon.dmg)

            # Player to enemy collision
            # sprite is an item of list of enemy_sprites which collide with player
            for sprite in pygame.sprite.spritecollide(self.player, self.enemy_sprites, False):
                self.player.take_dmg(sprite.dmg)

            # Exit collision
            if pygame.sprite.spritecollideany(self.player, self.exit):
                self.next_room()

            for weapon in pygame.sprite.spritecollide(self.player, self.weapon_sprites, False):
                if weapon != self.player.weapon:
                    self.weapon_sprites.remove(self.player.weapon)
                    self.player.pick_up_weapon(weapon)

            # Collsion Detection #

        # Draw commands
        self.exit.draw(screen)
        self.immovable_sprites.draw(screen)
        self.player_sprite.draw(screen)
        for sprite in self.player_sprite:
            sprite.draw_health()
        self.weapon_sprites.draw(screen)
        self.enemy_sprites.draw(screen)
        for sprite in self.enemy_sprites:
            sprite.draw_health()

        if self.player.health <= 0:
            for x in range(0, 10000):
                darken.set_alpha(x/100)
            screen.blit(darken, (0, 0))

            game_over = font.render("Game Over!", True, WHITE)
            screen.blit(game_over, (250, 200))

            restart = small_font.render("Press enter to restart.", True, WHITE)
            screen.blit(restart, (235, 250))

            if keys[pygame.K_RETURN]:
                self.restart()

        if self.menu == True:
            darken.set_alpha(100)
            screen.blit(darken, (0, 0))

            restart = small_font.render("R: Restart", True, WHITE)
            screen.blit(restart, (235, 250))

            main_menu = small_font.render("M: Main Menu", True, WHITE)
            screen.blit(main_menu, (235, 200))

            if keys[pygame.K_r]:
                self.restart()
                self.menu = False
            elif keys[pygame.K_m]:
                self.done = True
                self.next_state = "Main"

            if pygame.time.get_ticks() - self.hit_esc > 200:
                if keys[pygame.K_ESCAPE]:
                    print("esc")
                    self.menu = False
                    self.hit_esc = pygame.time.get_ticks()

        else:
            darken.set_alpha(0)
            screen.blit(darken, (0, 0))

        pygame.display.flip()
        # Draw commands #

        clock.tick(60)


def main():

    #     room, room_rect = load_image("arena.png")
    #     arena.blit(room, (0, 0))

    #     player_sprite = pygame.sprite.RenderPlain()
    #     weapon_sprites = pygame.sprite.RenderPlain()
    #     enemy_sprites = pygame.sprite.RenderPlain()

    #     global player
    #     player = Player(speed = 2, name = "player_right.png", group = player_sprite, pos = (SCRN_W/2, SCRN_H/2), health = 100)

    #     weapon = Sword("Base Sword", "base_sword", 20)
    #     weapon_sprites.add(weapon)

    #     player.pick_up_weapon(weapon)

    #     enemy = Zombie(name = "zombie.png", group = enemy_sprites, pos = (600, 300), health = 75)
    #     enemy = Zombie(name = "zombie.png", group = enemy_sprites, pos = (200, 250), health = 75)
    #     enemy = Zombie(name = "zombie.png", group = enemy_sprites, pos = (500, 200), health = 75)

    #     running = True
    #     while running:

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False

    #         keys = pygame.key.get_pressed()

    #         # Update calls
    #         player.update(keys)
    #         enemy_sprites.update()
    #         # Update calls #

    #         # Collision Detection
    #         # Weapon to enemy collision
    #         # enemy is an item of list of enemy_sprites which collide with weapon
    #         for enemy in pygame.sprite.spritecollide(weapon, enemy_sprites, False):
    #             enemy.take_dmg(player.weapon.dmg)

    #         # Player to enemy collision
    #         # sprite is an item of list of enemy_sprites which collide with player
    #         for sprite in pygame.sprite.spritecollide(player, enemy_sprites, False):
    #             player.take_dmg(sprite.dmg)
    #         # Collsion Detection #

    #         # Draw commands
    #         screen.fill((0, 0, 0))
    #         screen.blit(arena, (40, 40))
    #         player_sprite.draw(screen)
    #         weapon_sprites.draw(screen)
    #         enemy_sprites.draw(screen)
    #         pygame.display.flip()
    #         # Draw commands #

    #         clock.tick(60)

    states = {
        "Main": Main_Menu(),
        "Game": Main_Game()
    }

    controller = Game_Controller()
    controller.setup_states(states, "Main")

    while True:
        controller.state_update()


main()
