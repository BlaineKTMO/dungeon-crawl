import pygame


class CharacterGroup(pygame.sprite.RenderPlain):
    def draw(self, surface):
        RED = (255, 0, 0)
        BLACK = (0, 0, 0)

        super().draw(surface)
        for sprite in self.sprites():
            # Draw Health
            health_percent = sprite.health/sprite.max_hp

            total = pygame.Rect(sprite.rect.left, sprite.rect.top - 7, 15, 3)
            current = pygame.Rect(
                sprite.rect.left, sprite.rect.top - 7, 15 * health_percent, 3)

            pygame.draw.rect(surface, BLACK, total)
            pygame.draw.rect(surface, RED, current)
