from .imports import Iterable, pygame, globs
from .Resources import HealthBar, _isWeapon
Number = globs.Number


class Player(pygame.sprite.Sprite):
        def __init__(self, pos: Iterable, dims: Iterable, color):
            super().__init__()
            self.image = pygame.Surface(tuple(dims))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.centerx, self.rect.centery = pos
            self.pos = pos
            self.health_bar = HealthBar(100, 100, (self.rect.x, self.rect.y - 20))
            self.weapons = []
            self.points = 0

        def draw(self,surface, camera = None) -> None:
            for weapon in self.weapons:
                if camera:
                    weapon.draw(surface, camera = camera)
                else:
                    weapon.draw(surface)
            surface.blit(self.image, self.rect)
            self.health_bar.draw(surface, pos=(self.rect.x, self.rect.y - 20))

        def addWeapon(self,weapon: _isWeapon) -> None:
            self.weapons.append(weapon)

        def isDead(self) -> bool:
            return self.health_bar.current_health <= 0

            
    
class Enemy(Player):
        def __init__(self, pos: Iterable, dims: Iterable, color,speed: int):
            super().__init__(pos, dims, color)
            self.speed = speed
        def advance(self,pos: tuple[Number, Number], speed: Number | None = None) -> None:
            if speed is None: speed = self.speed
            globs.moveTo(self, pos, speed)

        def draw(self,surface,camera = None) -> None:
          super().draw(surface, camera = camera)

