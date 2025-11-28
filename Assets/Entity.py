from .imports import Iterable, pygame, math, globs
from .Resources import HealthBar
Number = globs.Number


playerObj = None
class Player(pygame.sprite.Sprite):
        def __init__(self, pos: Iterable, dims: Iterable, color):
            super().__init__()
            self.image = pygame.Surface(tuple(dims))
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.health_bar = HealthBar(100, 100, (self.rect.x, self.rect.y - 20))
            self.weapons = []
            self.points = 0
            #globs.playerObj = self

        def draw(self,surface, camera = None) -> None:
            for weapon in self.weapons:
                if camera:
                    weapon.draw(surface, camera = camera)
                else:
                    weapon.draw(surface)
            surface.blit(self.image, self.rect)
            self.health_bar.draw(surface, pos=(self.rect.x, self.rect.y - 20))
            
    
class Enemy(Player):
        def __init__(self, pos: Iterable, dims: Iterable, color,speed: int):
            super().__init__(pos, dims, color)
            self.speed = speed
        def advance(self,pos: Iterable, speed: Number | None = None) -> None:
            if speed == None: speed = self.speed
            distVector = (pos[0]-self.rect.centerx,pos[1]-self.rect.centery)
            try:
                moveVector = [distVector[0]/(math.sqrt(math.pow(distVector[0],2) + math.pow(distVector[1],2))),distVector[1]/(math.sqrt(math.pow(distVector[0],2) + math.pow(distVector[1],2)))]
                self.rect.centerx += moveVector[0] *speed
                self.rect.centery += moveVector[1] *speed
            except ZeroDivisionError:
                pass
        def draw(self,surface,camera = None) -> None:
          super().draw(surface, camera = camera)
          if self.health_bar.current_health <= 0:
            self.kill()
        def kill(self) -> None:
            super().kill()
            if type(globs.playerObj) == Player:
                globs.playerObj.points += 1
