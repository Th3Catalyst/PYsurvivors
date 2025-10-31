import pygame
from typing import Tuple
import math
from Assets import Entity
import time
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True



player = Entity.Player((25,25),(25,25), "white")
while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:
            if keys[pygame.K_d]:
              player.rect.centerx += 20
            if keys[pygame.K_a]:
              player.rect.centerx -= 20
            if keys[pygame.K_w]:
              player.rect.centery -= 20
            if keys[pygame.K_s]:
              player.rect.centery += 20
          if event.key == pygame.K_h:
            player.health_bar.update_health(10)
             
    
    if keys[pygame.K_d]:
      for i in range(math.ceil(player.rect.width/10)):
          player.rect.centerx += 1
    if keys[pygame.K_a]:
      for i in range(math.ceil(player.rect.width/10)):
          player.rect.centerx -= 1
    if keys[pygame.K_w]:
      for i in range(math.ceil(player.rect.width/10)):
          player.rect.centery -= 1
    if keys[pygame.K_s]:
      for i in range(math.ceil(player.rect.width/10)):
          player.rect.centery += 1
    

    screen.fill("black")

    
    player.draw(screen)

    pygame.display.flip()

    clock.tick(60)  

pygame.quit()