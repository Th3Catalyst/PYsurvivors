import pygame
from typing import Tuple
import math
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
class Player(pygame.sprite.Sprite):
  def __init__(self, pos: Tuple, dims: Tuple, color):
    super().__init__()
    self.image = pygame.Surface(dims)
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = pos

  def draw(self,surface):
     surface.blit(self.image, self.rect)


player = Player((25,25),(25,25), "white")
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
      for i in range(math.ceil(player.rect.width/4)):
          player.rect.centerx += 1
    if keys[pygame.K_a]:
      for i in range(math.ceil(player.rect.width/4)):
          player.rect.centerx -= 1
    if keys[pygame.K_w]:
      for i in range(math.ceil(player.rect.width/4)):
          player.rect.centery -= 1
    if keys[pygame.K_s]:
      for i in range(math.ceil(player.rect.width/4)):
          player.rect.centery += 1
    

    screen.fill("black")

    player.draw(screen)

    pygame.display.flip()

    clock.tick(60)  

pygame.quit()