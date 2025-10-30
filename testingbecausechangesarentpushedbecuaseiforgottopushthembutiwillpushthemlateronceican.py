import pygame
import math
from typing import Tuple
import time
import random
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
class Player(pygame.sprite.Sprite):
  def __init__(self, pos: Tuple, dims: Tuple, color):
    super().__init__()
    self.image = pygame.Surface(dims)
    self.image.fill(color)
    self.rect = self.image.get_rect()
    self.rect.x, self.rect.y = pos

  def draw(self,surface):
     surface.blit(self.image, self.rect)
class Enemy(Player):
    def __init__(self,*args,**kwargs):
      super().__init__(*args,**kwargs)
    def advance(self,pos: Tuple, speed: int = 2):
      distVector = (player.rect.centerx-self.rect.centerx,player.rect.centery-self.rect.centery)
    
      moveVector = [distVector[0]/(math.sqrt(math.pow(distVector[0],2) + math.pow(distVector[1],2))),distVector[1]/(math.sqrt(math.pow(distVector[0],2) + math.pow(distVector[1],2)))]
      self.rect.centerx += moveVector[0] *speed
      self.rect.centery += moveVector[1] *speed
       
player = Player((25,25),(25,25), "white")
enemies = pygame.sprite.Group()
for i in range(20):
  enemy = Enemy((100,100+i*40),(25,25),"red")
  enemies.add(enemy)
running = True
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
    
    for enemy in enemies:
      enemy.advance((player.rect.centerx,player.rect.centery),speed=random.randrange(2,5))
    
    screen.fill("black")

    player.draw(screen)
    enemies.draw(screen)

    pygame.display.flip()
    clock.tick(60)  

pygame.quit()