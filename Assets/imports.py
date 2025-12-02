from typing import Tuple, Iterable
import pygame
import math
class globs:
    Number = int|float
    dt = 0

    @classmethod
    def cooldownCheck(cls, cooldown: int) -> bool:
        return pygame.time.get_ticks() % cooldown < (pygame.time.get_ticks() - globs.dt) % cooldown

    @classmethod
    def tick(cls, dt: int) -> None:
        globs.dt = dt

    @staticmethod
    def moveTo(sprite: pygame.sprite.Sprite, target: tuple[Number, Number], speed: Number) -> None:
        if not hasattr(sprite, 'pos'): raise AttributeError('object must have a pos attribute')
        pos=target
        distVector = pygame.Vector2(pos[0] - sprite.rect.centerx, pos[1] - sprite.rect.centery)
        if distVector.length_squared() > float(0):
            direction = distVector.normalize()
            sprite.pos += direction * speed
            sprite.rect.centerx, sprite.rect.centery = sprite.pos[0], sprite.pos[1]

    @staticmethod
    def moveDirection(sprite: pygame.sprite.Sprite, direction: Number, speed: Number) -> None:
        sprite.pos = list(sprite.pos)
        sprite.pos[0] += math.cos(direction) * speed
        sprite.pos[1] -= math.sin(direction) * speed
        sprite.pos = tuple(sprite.pos)
        sprite.rect.centerx, sprite.rect.centery = sprite.pos

