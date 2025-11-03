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
        
        def Damage(self, damage: Number):
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
            self.image.fill(color)
            self.image = pygame.transform.rotate(self.image, direction * (180/math.pi))
            self.rect = self.image.get_rect()
            self.rect.center = pos
            


        
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
                    e.health_bar.Damage(self.damage)
                    self.kill()
        
        def draw(self,surface):
            surface.blit(self.image, self.rect)
            if abs(self.rect.centerx) > 5*surface.get_width() or abs(self.rect.centery) > 5*surface.get_height():
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
        def __init__(self, pos: Tuple, dims: Tuple, color,speed: int):
            super().__init__(pos, dims, color)
            self.speed = speed
        def advance(self,pos: Tuple, speed: int | None = None):
            if not speed: speed = self.speed
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
            if not player: player = self.owner
            for enemy in enemies:
                if enemy.rect.colliderect(self.rect):
                    enemy.health_bar.Damage(1)
                    enemy.advance(player.rect.center, speed=-2)
                if enemy.health_bar.current_health <= 0:
                    enemy.kill()
    class bulletCross:
        def __init__(self,owner: Entity.Player,cooldown: Number, color, speed: Number, damage:Number, projCount: int):
            self.owner = owner
            self.cooldown = cooldown
            self.color = color
            self.speed = speed
            self.damage = damage
            self.projCount = projCount
            self.bullets = pygame.sprite.Group()
            self.oldMod = 0
        
        def Attack(self, enemies: pygame.sprite.Group, damage: Number|None = None, speed: Number|None = None, pos: Tuple|None = None, color = None, projCount: int | None = None):
            if not (pygame.time.get_ticks() % self.cooldown < self.oldMod): 
                self.oldMod = pygame.time.get_ticks() % self.cooldown
                return
            self.oldMod = pygame.time.get_ticks() % self.cooldown
            
            if damage == None:
                damage = self.damage
            if speed == None:
                speed = self.speed
            if pos == None:
                pos = self.owner.rect.center
            if color == None:
                color = self.color
            if projCount == None:
                projCount = self.projCount
            for i in range(projCount):
                b = Resources.Projectile(self.owner.rect.center,2*math.pi*i/projCount,damage,speed,color, enemies)
                self.bullets.add(b)
        def draw(self, surface):
            for b in self.bullets:
                b.draw(surface)  
                b.move()
    
    class Lightning:
        class LightningProjectile(pygame.sprite.Sprite):
            def __init__(self,pos: Tuple, color, deathTimer: int):
                super().__init__()
                self.image = pygame.Surface((10,pos[1]), pygame.SRCALPHA)
                self.image.fill(color)
                self.rect = self.image.get_rect()
                self.rect.bottomleft = (pos[0]-5,pos[1])
                self.deathTimer = deathTimer

            def draw(self, surface):
                if self.deathTimer <=0:
                    self.kill()
                else:
                    surface.blit(self.image, self.rect)
                self.deathTimer -= 1

        
        def __init__(self, owner: Entity.Player,cooldown: Number, color, damage:Number, projCount: int):
            self.owner = owner
            self.cooldown = cooldown
            self.damage = damage
            self.color = color
            self.projCount = projCount
            self.projectiles = pygame.sprite.Group()
            self.oldMod = 0
        
        def Attack(self, enemies: pygame.sprite.Group, damage: Number|None = None, color = None, projCount: int | None = None):
            if not (pygame.time.get_ticks() % self.cooldown < self.oldMod): 
                self.oldMod = pygame.time.get_ticks() % self.cooldown
                return
            self.oldMod = pygame.time.get_ticks() % self.cooldown
            
            if damage == None:
                damage = self.damage
            if color == None:
                color = self.color
            if projCount == None:
                projCount = self.projCount
            try:
                enemiesNew = sorted(enemies, key=lambda e:math.sqrt(math.pow(e.rect.centerx-self.owner.rect.centerx,2)+math.pow(e.rect.centery-self.owner.rect.centery,2)))
                for i in range(projCount):
                    enemiesNew[i].health_bar.Damage(damage)
                    
                    try:
                        lightning = self.LightningProjectile(enemiesNew[i].rect.center,color,20)
                        self.projectiles.add(lightning)
                    except pygame.error:
                        pass
            except IndexError:
                pass
        
        def draw(self, surface):
            for p in self.projectiles:
                p.draw(surface)
                
    class Revolver:
        
        def __init__(self, owner: Entity.Player,cooldown: Number, color, damage:Number, speed: Number, projCount: int):
            self.owner = owner
            self.cooldown = cooldown
            self.damage = damage
            self.color = color
            self.projCount = projCount
            self.projectiles = pygame.sprite.Group()
            self.speed = speed
            self.oldMod = 0
        
        def Attack(self, enemies: pygame.sprite.Group, damage: Number|None = None, color = None, speed: Number  | None = None, projCount: int | None = None):
            if not (pygame.time.get_ticks() % self.cooldown < self.oldMod): 
                self.oldMod = pygame.time.get_ticks() % self.cooldown
                return
            self.oldMod = pygame.time.get_ticks() % self.cooldown
            
            if damage == None:
                damage = self.damage
            if color == None:
                color = self.color
            if projCount == None:
                projCount = self.projCount
            if projCount == None:
                speed = self.speed
            try:
                enemiesNew = sorted(enemies, key=lambda e:math.sqrt(math.pow(e.rect.centerx-self.owner.rect.centerx,2)+math.pow(e.rect.centery-self.owner.rect.centery,2)))
                for i in range(projCount):
                    
                    try:
                        bullet = Resources.Projectile(self.owner.rect.center, math.atan((enemiesNew[i].rect.centery-self.owner.rect.centery)/(enemiesNew[i].rect.centerx-self.owner.rect.centerx)), damage, speed, color, enemies):
                        self.projectiles.add(bullet)
                    except pygame.error:
                        pass
            except IndexError:
                pass
        
        def draw(self, surface):
            for p in self.projectiles:
                p.draw(surface)

