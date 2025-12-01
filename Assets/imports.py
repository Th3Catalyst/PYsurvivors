from typing import Tuple, Iterable
import pygame
import math
class globs():
    Number = int|float
    dt = 0
    @classmethod
    def cooldownCheck(cls, cooldown: int) -> bool:
        return pygame.time.get_ticks() % cooldown < (pygame.time.get_ticks() - globs.dt) % cooldown

    @classmethod
    def tick(cls, dt: int) -> None:
        globs.dt = dt

    @staticmethod
    def moveTo(object: pygame.sprite.Sprite, target: tuple[Number, Number], speed: Number) -> None:
        pos=target
        distVector = pygame.Vector2(pos[0] - object.rect.centerx, pos[1] - object.rect.centery)
        if distVector.length_squared() > float(0):
            direction = distVector.normalize()
            object.pos += direction * speed
            object.rect.centerx, object.rect.centery = object.pos[0], object.pos[1]

    @staticmethod
    def moveDirection(object: pygame.sprite.Sprite, direction: Number, speed: Number) -> None:
        object.pos = list(object.pos)
        object.pos[0] += math.cos(direction) * speed
        object.pos[1] -= math.sin(direction) * speed
        object.pos = tuple(object.pos)
        object.rect.centerx, object.rect.centery = object.pos

