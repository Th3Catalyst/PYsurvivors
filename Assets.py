from dataclasses import dataclass
from typing import Tuple
import pygame

@dataclass
class Entity:
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
        
        def update_health(self, damage: int):
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
    

    class Player(pygame.sprite.Sprite):
        def __init__(self, pos: Tuple, dims: Tuple, color):
            super().__init__()
            self.image = pygame.Surface(dims)
            self.image.fill(color)
            self.rect = self.image.get_rect()
            self.rect.x, self.rect.y = pos
            self.health_bar = Entity.HealthBar(100, 100, (self.rect.x, self.rect.y - 20))

        def draw(self,surface):
            surface.blit(self.image, self.rect)
            self.health_bar.draw(surface, pos=(self.rect.x, self.rect.y - 20))
    
    class Enemy(Player):
        def __init__(self, pos: Tuple, dims: Tuple, color):
            super().__init__(pos, dims, color)
            


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    clock = pygame.time.Clock()
    running = True

    health_bar = Entity.HealthBar(100, 75, (50, 50))

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