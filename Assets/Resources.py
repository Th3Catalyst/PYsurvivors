from .imports import Tuple, Iterable, pygame, math, globs
Number = globs.Number
class Camera:
    def __init__(self,width,height,*args):
        self.screen = pygame.Rect(0,0,width,height)
        self.sprites = pygame.sprite.Group()
        for i in args:
            if type(i) == pygame.sprite.Group:
                for k in i:
                    self.sprites.add(k)
            else:
                self.sprites.add(i)
    def __iadd__(self, other):
        if type(other) == pygame.sprite.Group:
            for k in other:
                self.sprites.add(k)
        else:
            self.sprites.add(other)
        return self
    def update(self,pos: Tuple):
        self.screen = self.screen.move(*pos)
    
    def __str__(self):
        return f"rect: {self.screen}, sprites: {self.sprites}"
    def draw(self,surface):
        for i in self.sprites:
            if self.screen.colliderect(i.rect):
                i.rect.x -= self.screen.x
                i.rect.y -= self.screen.y
                try:
                    i.draw(surface, self)
                except TypeError:
                    i.draw(surface)
                i.rect.x += self.screen.x
                i.rect.y += self.screen.y
                
class HealthBar(pygame.sprite.Sprite):
    def __init__(self, max_health: int, current_health: int,pos: Tuple[Number, Number]):
        super().__init__()
        self.max_health = max_health
        self.current_health = current_health
        self.image = pygame.Surface((52, 10))
        self.rect = self.image.get_rect()
        self.image.fill("white")
        self.rect.x, self.rect.y = pos
        self.rect.x -= 13

        self.healthbarbg = pygame.Surface((46, 4))
        self.healthbarbg.fill("black")
        self.healthbarbg_rect = self.healthbarbg.get_rect()
        self.healthbarbg_rect.x = self.rect.x + 3
        self.healthbarbg_rect.y = self.rect.y + 3

        self.healthbarvis = pygame.Surface((46, 4))
        self.healthbarvis.fill("gray")
        self.healthbarvis_rect = self.healthbarvis.get_rect()
        self.healthbarvis_rect.x = self.rect.x + 3
        self.healthbarvis_rect.y = self.rect.y + 3
    
    def __repr__(self) -> str:
        return f"Resources.HealthBar(max_health={self.max_health}, current_health={self.current_health}, pos={self.rect.topleft})"
    
    def damage(self, damage: Number) -> None:
        self.current_health -= damage
        health_ratio = (self.current_health / self.max_health) if self.current_health > 0 else 0
        self.healthbarvis = pygame.Surface((int(46 * health_ratio), 4))
        self.healthbarvis.fill("gray")
        self.healthbarvis_rect.width = int(46 * health_ratio)

    def draw(self, surface, pos = "") -> None:
        surface.blit(self.image, self.rect)
        surface.blit(self.healthbarvis, self.healthbarvis_rect)
        if pos:
            self.rect.x, self.rect.y = pos
            self.rect.x -= 13
            self.healthbarbg_rect.x = self.healthbarvis_rect.x = self.rect.x + 3
            self.healthbarbg_rect.y = self.healthbarvis_rect.y = self.rect.y + 3


class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos: Tuple[int,int], direction: int|float, damage: int|float, speed: Number, color, enemies: pygame.sprite.Group):
        super().__init__()
        self.pos = list(pos)
        self.direction = direction
        self.damage = damage
        self.speed = speed
        self.enemies = enemies
        self.image = pygame.Surface((50,10), pygame.SRCALPHA)
        self.image.fill(color)
        self.image = pygame.transform.rotate(self.image, direction * (180/math.pi))
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def __repr__(self) -> str:
        return f"Resources.Projectile(pos={Tuple(self.pos)},direction={self.direction}, damage={self.damage}, speed={self.speed}, color={self.image.fill}, enemies={self.enemies})"
        
    
    def move(self, speed: Number | None = None, direction: Iterable | None = None) -> None:
        if speed is None:
            speed = self.speed
        if direction is None:
            direction = self.direction

        self.pos[0] += math.cos(direction)*speed
        self.pos[1] -= math.sin(direction)*speed
        self.rect.centerx, self.rect.centery = self.pos
        for e in self.enemies:
            if e.rect.colliderect(self.rect):
                e.health_bar.damage(self.damage)
                self.kill()
    
    def draw(self, surface) -> None:
        surface.blit(self.image, self.rect)
        if abs(self.rect.centerx) > 5*surface.get_width() or abs(self.rect.centery) > 5*surface.get_height():
            self.kill()
        
