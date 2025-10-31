from dataclasses import dataclass
from typing import Tuple
import pygame
import math

Number = int|float

@dataclass
class Resources:
    class HealthBar(pygame.sprite.Sprite):
        def __init__(self, max_health: int, current_health: int,pos: Tuple):
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
        
        def update_health(self, damage: Number):
            self.current_health -= damage
            health_ratio = (self.current_health / self.max_health) if self.current_health > 0 else 0
            self.healthbarvis = pygame.Surface((int(46 * health_ratio), 4))
            self.healthbarvis.fill("gray")
            self.healthbarvis_rect.width = int(46 * health_ratio)
        def draw(self, surface, pos = ""):
            surface.blit(self.image, self.rect)
            surface.blit(self.healthbarvis, self.healthbarvis_rect)
            if pos:
                self.rect.x, self.rect.y = pos
                self.rect.x -= 13
                self.healthbarbg_rect.x = self.healthbarvis_rect.x = self.rect.x + 3
                self.healthbarbg_rect.y = self.healthbarvis_rect.y = self.rect.y + 3
    
    class Projectile(pygame.sprite.Sprite):
        def __init__(self, pos: Tuple, direction: Number, damage: Number, speed: Number, color, enemies: pygame.sprite.Group):
            super().__init__()
            self.pos = list(pos)
            self.direction = direction
            self.damage = damage
            self.speed = speed
            self.enemies = enemies
            self.image = pygame.Surface((50,10), pygame.SRCALPHA)
            self.image = pygame.transform.rotate(self.image, direction * (180/math.pi))
            self.rect = self.image.get_rect()
            self.rect.center = pos
            self.image.fill(color)


        
        def move(self, speed: Number | None = None, direction: Tuple | None = None):
            if speed is None:
                speed = self.speed
            if direction is None:
                direction = self.direction
            
            

            self.pos[0] += math.cos(direction)*speed
            self.pos[1] -= math.sin(direction)*speed
            self.rect.centerx, self.rect.centery = self.pos
            for e in self.enemies:
                if e.rect.colliderect(self.rect):
                    e.health_bar.update_health(self.damage)
                    self.kill()
            


@dataclass
class Entity:
    
    

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos: Tuple, dims: Tuple, color):
            super().__init__()
            self.image = pygame.Surface(dims)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.health_bar = Resources.HealthBar(100, 100, (self.rect.x, self.rect.y - 20))
            self.weapons = []

        def draw(self,surface):
            surface.blit(self.image, self.rect)
            self.health_bar.draw(surface, pos=(self.rect.x, self.rect.y - 20))
    
    class Enemy(Player):
        def __init__(self, pos: Tuple, dims: Tuple, color):
            super().__init__(pos, dims, color)
        def advance(self,pos: Tuple, speed: int = 2):
            distVector = (pos[0]-self.rect.centerx,pos[1]-self.rect.centery)
            try:
                moveVector = [distVector[0]/(math.sqrt(math.pow(distVector[0],2) + math.pow(distVector[1],2))),distVector[1]/(math.sqrt(math.pow(distVector[0],2) + math.pow(distVector[1],2)))]
                self.rect.centerx += moveVector[0] *speed
                self.rect.centery += moveVector[1] *speed
            except ZeroDivisionError:
                pass

@dataclass            
class Weapons:
    class Aura(pygame.sprite.Sprite):
        def __init__(self, owner: Entity.Player, radius: int, color):
            super().__init__()
            self.owner = owner
            self.radius = radius
            self.color = color
            self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, color, (radius, radius), radius)
            self.rect = self.image.get_rect()
        
        def draw(self, surface):
            self.rect.center = self.owner.rect.center
            surface.blit(self.image, self.rect)

        def Attack(self, enemies: pygame.sprite.Group, player: Entity.Player = None):
            for enemy in enemies:
                if enemy.rect.colliderect(self.rect):
                    enemy.health_bar.update_health(1)
                    enemy.advance(player.rect.center, speed=-2)
                if enemy.health_bar.current_health <= 0:
                    enemy.kill()
    class bulletCross(pygame.sprite.Sprite):
        def __init__(self,owner: Entity.Player,cooldown: Number, color, speed: Number, damage:Number, projCount: int):
            super().__init__()
            self.owner = owner
            self.cooldown = cooldown
            self.color = color
            self.speed = speed
            self.damage = damage
            self.projCount = projCount
            self.bullets = pygame.sprite.Group()
        
        def Attack(self, enemies: pygame.sprite.Group, damage: Number|None = None, speed: Number|None = None, pos: Tuple|None = None, color = None, projCount: int | None = None):
            if not (pygame.time.get_ticks % self.cooldown == 0): return
            if damage == None:
                damage = self.damage
            if speed == None:
                speed = self.speed
            if pos == None:
                pos = self.pos
            if color == None:
                color = self.color
            if projCount == None:
                projCount = self.projCount
            for i in range(projCount):
                b = Resources.Projectile(self.owner.rect.center,2*math.pi*i/projCount,damage,speed,color, enemies)
                self.bullets.append(b)
        def draw(self, surface):
            for b in self.bullets:
                b.draw(surface)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()
    running = True

    health_bar = Resources.HealthBar(100, 75, (50, 50))

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("white")
        screen.blit(health_bar.image, health_bar.rect)
        screen.blit(health_bar.healthbarvis, health_bar.healthbarvis_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()