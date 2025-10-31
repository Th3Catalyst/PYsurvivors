import pygame
from typing import Tuple
import math
from Assets import *
import time
import random
# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


enemies = pygame.sprite.Group()
for i in range(20):
  enemy = Entity.Enemy((100,100+i*40),(25,25),"red")
  enemies.add(enemy)
player = Entity.Player((screen.get_width()/2,screen.get_height()/2),(25,25), "white")
aura = Weapons.Aura(player, 60, (0, 0, 255, 100))
player.weapons.append(aura)
projectiles = pygame.sprite.Group()
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
          if event.key ==  pygame.K_q:
            test = Resources.Projectile((player.rect.centerx,player.rect.centery),math.pi/2, 10, 4, (0, 0, 255, 200))
            projectiles.add(test)
             
    
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
    
    
    for enemy in enemies:
      enemy.advance(player.rect.center,speed=random.randrange(2,5))
      if enemy.rect.colliderect(player.rect):
          player.health_bar.update_health(0.5)
      if player.health_bar.current_health <= 0:
          print("Player Defeated!")
          running = False
    
    for p in projectiles:
       p.move()

    aura.Attack(enemies, player)  

    screen.fill("black")

    
    for weapon in player.weapons:
      weapon.draw(screen)
    player.draw(screen)

    for enemy in enemies:
      enemy.draw(screen)
    
    projectiles.draw(screen)

    pygame.display.flip()

    clock.tick(60)  

pygame.quit()