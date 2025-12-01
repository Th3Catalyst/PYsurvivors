from .imports import Tuple, Iterable, pygame, math, globs
from .Resources import Projectile, _isWeapon
Number = globs.Number
Player = pygame.sprite.Sprite #PLACEHOLDER



class Aura(pygame.sprite.Sprite, _isWeapon):
        def __init__(self, owner: Player, radius: int, damage: Number, color, cooldown: Number = 5):
            pygame.sprite.Sprite.__init__(self)
            _isWeapon.__init__(self, owner, damage, color, cooldown)
            self.radius = radius
            self.image = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, color, (radius, radius), radius)
            self.rect = self.image.get_rect()
        
        def draw(self, surface, camera = None) -> None:
            self.rect.center = self.owner.rect.center
            surface.blit(self.image, self.rect)

        def Attack(self, enemies: pygame.sprite.Group, player: Player | None = None) -> None:
            if not player: player = self.owner
            self.rect.center = player.rect.center
            for enemy in enemies:
                if enemy.rect.colliderect(self.rect):
                    enemy.health_bar.damage(self.damage)
                    if globs.cooldownCheck(self.cooldown):
                      enemy.advance(player.rect.center, speed=-3)

class bulletCross(_isWeapon):
        def __init__(self,owner: Player,cooldown: Number, color, speed: Number, damage:Number, projCount: int):
            super().__init__(owner,damage,color,cooldown)
            self.speed = speed
            self.projCount = projCount
            self.bullets = pygame.sprite.Group()
        
        def Attack(self, enemies: pygame.sprite.Group, damage: Number|None = None, speed: Number|None = None, pos: Iterable|None = None, color = None, projCount: int | None = None) -> None:
            if not globs.cooldownCheck(self.cooldown):
                return
            
            if damage is None:
                damage = self.damage
            if speed is None:
                speed = self.speed
            if pos == None:
                pos = self.owner.rect.center
            if color == None:
                color = self.color
            if projCount == None:
                projCount = self.projCount
                projCount: int
            for i in range(projCount):
                b = Projectile(pos,2*math.pi*i/projCount,damage,speed,color, enemies)
                self.bullets.add(b)
        def draw(self, surface, camera = None) -> None:
            for b in self.bullets:
                if camera:
                    b.rect.x -= camera.screen.x
                    b.rect.y -= camera.screen.y
                b.draw(surface)
                if camera:
                    b.rect.x += camera.screen.x
                    b.rect.y += camera.screen.y  
                b.move()
    
class Lightning(_isWeapon):
        class LightningProjectile(pygame.sprite.Sprite):
            def __init__(self,pos: Tuple, color, deathTimer: int):
                super().__init__()
                self.image = pygame.Surface((10,700), pygame.SRCALPHA)
                self.image.fill(color)
                self.rect = self.image.get_rect()
                self.rect.bottomleft = (pos[0]-5,pos[1])
                self.deathTimer = deathTimer

            def draw(self, surface) -> None:
                if self.deathTimer <=0:
                    self.kill()
                else:
                    surface.blit(self.image, self.rect)
                self.deathTimer -= 1

        
        def __init__(self, owner: Player,cooldown: Number, color, damage:Number, projCount: int):
            super().__init__(owner,damage,color,cooldown)
            self.projCount = projCount
            self.projectiles = pygame.sprite.Group()
            self.oldMod = 0
        
        def Attack(self, enemies: pygame.sprite.Group, damage: Number|None = None, color = None, projCount: int | None = None) -> None:
            if not globs.cooldownCheck(self.cooldown):
                return
            
            if damage == None:
                damage = self.damage
            if color == None:
                color = self.color
            if projCount == None:
                projCount = self.projCount
            try:
                enemiesNew = sorted(enemies, key=lambda e:math.sqrt(math.pow(e.rect.centerx-self.owner.rect.centerx,2)+math.pow(e.rect.centery-self.owner.rect.centery,2)))
                for i in range(projCount):
                    enemiesNew[i].health_bar.damage(damage)
                    
                    try:
                        lightning = self.LightningProjectile(enemiesNew[i].rect.center,color,20)
                        self.projectiles.add(lightning)
                    except pygame.error:
                        pass
            except IndexError:
                pass
        
        def draw(self, surface, camera = None) -> None:
            for p in self.projectiles:
                if camera:
                    p.rect.x -= camera.screen.x
                    p.rect.y -= camera.screen.y
                p.draw(surface)
                if camera:
                    p.rect.x += camera.screen.x
                    p.rect.y += camera.screen.y
                
class Revolver(_isWeapon):
        
        def __init__(self, owner: Player,cooldown: Number, color, damage:Number, speed: Number, projCount: int):
            super().__init__(owner,damage,color,cooldown)
            self.projCount = projCount
            self.projectiles = pygame.sprite.Group()
            self.speed = speed
            self.oldMod = 0
        
        def Attack(self, enemies: pygame.sprite.Group, damage: Number|None = None, color = None, speed: Number  | None = None, projCount: int | None = None) -> None:
            if not globs.cooldownCheck(self.cooldown):
                return
            
            if damage == None:
                damage = self.damage
            if color == None:
                color = self.color
            if projCount == None:
                projCount = self.projCount
            if speed == None:
                speed = self.speed
            try:
                enemiesNew = sorted(enemies, key=lambda e:math.sqrt(math.pow(e.rect.centerx-self.owner.rect.centerx,2)+math.pow(e.rect.centery-self.owner.rect.centery,2)))
                for i in range(projCount):
                    
                    try:
                        bullet = Projectile(self.owner.rect.center, (math.pi if (enemiesNew[i].rect.centerx-self.owner.rect.centerx) <= 0 else 0) - math.atan((enemiesNew[i].rect.centery-self.owner.rect.centery)/(enemiesNew[i].rect.centerx-self.owner.rect.centerx)), damage, speed, color, enemies)

                        self.projectiles.add(bullet)
                    except pygame.error:
                        pass
                    except ZeroDivisionError:
                      try:
                        bullet = Projectile(self.owner.rect.center, (math.pi if (enemiesNew[i].rect.centerx-self.owner.rect.centerx) <= 0 else 0) + ((enemiesNew[i].rect.centery-self.owner.rect.centery)/abs(enemiesNew[i].rect.centery-self.owner.rect.centery))*math.pi/2, damage, speed, color, enemies)
                        self.projectiles.add(bullet)
                      except ZeroDivisionError:
                        pass
            except IndexError:
                pass
        
        def draw(self, surface, camera = None) -> None:
            for p in self.projectiles:
                if camera:
                    p.rect.x -= camera.screen.x
                    p.rect.y -= camera.screen.y
                p.draw(surface)
                if camera:
                    p.rect.x += camera.screen.x
                    p.rect.y += camera.screen.y
                p.move()
        
        
