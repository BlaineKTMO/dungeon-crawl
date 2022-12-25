# Class : ITCS 1950 T/TH
# Student Name : Blaine Oania
# Last Edit Date : 28/4/2020
# File Name : Dungeon Crawl.py
# Description : Beta Release of Dungeon Crawl

import pygame
import os
import random
import Character
import Immovables
import Weapons
import Interactables
import CharacterGroup
import ImagePlugin
import AudioPlugin

SCRN_W = 700
SCRN_H = 400

pygame.init()
screen = pygame.display.set_mode((SCRN_W, SCRN_H))
arena = pygame.Surface((700, 400))

font_path = os.path.join('data', 'PressStart2P-vaV7.ttf')
font = pygame.font.Font(font_path, 20)
small_font = pygame.font.Font(font_path, 10)

clock = pygame.time.Clock()

player = None

WHITE = (255, 255, 255)


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

        self.player_sprite = CharacterGroup.CharacterGroup()
        self.weapon_sprites = pygame.sprite.RenderPlain()
        self.text_options = pygame.sprite.RenderPlain()

    def start(self):
        self.done = False
        # Loads Main Menu Room
        path = os.path.join('data', 'arena.png')
        self.background = pygame.image.load(path)
        arena.blit(self.background, (0, 0))

        # Background Music
        path = os.path.join('music', 'main_menu.ogg')
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        pygame.mixer.music.set_volume(0.1)

        self.player = Character.Player(speed=2, name="player_right.png",
                                       group=self.player_sprite, pos=(200, SCRN_H/2), health=100, )

        weapon = Weapons.Sword("Base Sword", "base_sword", 20)
        self.weapon_sprites.add(weapon)

        self.player.pick_up_weapon(weapon)

        self.startText = Interactables.Text("start", "start.png", (300, 150))
        self.credits = Interactables.Text("credits", "credits.png", (300, 180))

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

        self.player_sprite = CharacterGroup.CharacterGroup()
        self.enemy_sprites = pygame.sprite.RenderPlain()
        self.weapon_sprites = pygame.sprite.RenderPlain()
        self.immovable_sprites = pygame.sprite.RenderPlain()
        self.exit = pygame.sprite.RenderPlain()

        self.room_num = 1

        self.menu = False
        self.hit_esc = 0

    def create_room(self):
        """Creates next room"""
        num_enemies = random.randint(3, 6)
        room_layout = random.randint(0, 2)

        objects_in_room = []

        if room_layout == 0:
            # 12 torches spaced evenly in center of room

            x, y = 300, 75
            for j in range(4):
                for i in range(3):
                    new_object = Immovables.Immovable(
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
                new_object = Immovables.Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)
            for i in range(3):
                x += offset
                y -= offset
                new_object = Immovables.Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)

            x = 250
            for i in range(3):
                x += offset
                y -= offset
                new_object = Immovables.Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)

            for i in range(3):
                x += offset
                y += offset
                new_object = Immovables.Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)

        elif room_layout == 2:
            offset_x = 35
            offset_y = 20

            x, y = 200, 60
            for i in range(4):
                x -= offset_x
                y += offset_y
                new_object = Immovables.Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)

            x, y = 475, 310
            for i in range(4):
                x += offset_x
                y -= offset_y
                new_object = Immovables.Immovable(
                    "torch_1.png", (x, y), self.immovable_sprites)
                objects_in_room.append(new_object)

            weapon = Weapons.Hammer("hammer", "base_hammer", 30)
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
                new_enemy = Character.Mage(name="mage.png", player=self.player,
                                           group=self.enemy_sprites, pos=pos, health=100)
            elif enemy <= 5:
                new_enemy = Character.Slime(name="slime.png", player=self.player,
                                            group=self.enemy_sprites, pos=pos, health=50)
            elif enemy <= 10:
                new_enemy = Character.Zombie(name="Zombie.png", player=self.player,
                                             group=self.enemy_sprites, pos=pos, health=150)
            objects_in_room.append(new_enemy)

        print(len(self.enemy_sprites.sprites()))

        # Room exit
        self.exit.add(Interactables.Interactables(
            "exit", "right_exit.png", (670, 190)))

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
        path = os.path.join('data', 'arena.png')
        self.room = pygame.image.load(path)

        arena.blit(self.room, (0, 0))

        self.room_num = 1

        # Background Music
        bg_music = AudioPlugin.Audio.load_music("main_game.ogg")
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0.3)

        self.player = Character.Player(speed=4, name="player_right.png",
                                       group=self.player_sprite, pos=(150, SCRN_H/2), health=250)
        weapon = Weapons.Sword("Base Sword", "base_sword", 20)
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
                if weapon == self.player.weapon:
                    continue

                self.weapon_sprites.remove(self.player.weapon)
                self.player.pick_up_weapon(weapon)

        # Collsion Detection #

        # Draw commands
        self.exit.draw(screen)
        self.immovable_sprites.draw(screen)
        self.player_sprite.draw(screen)
        self.weapon_sprites.draw(screen)
        self.enemy_sprites.draw(screen)

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

    #     For previous testing          #
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
