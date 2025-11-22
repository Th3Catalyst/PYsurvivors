import pygame
from typing import Tuple
import math
from Assets import Resources, Entity, Weapons
import time
import random

def main():
  # pygame setup
  pygame.init()
  screen = pygame.display.set_mode((1280, 720))
  clock = pygame.time.Clock()
  running = True
  
  camera = Resources.Camera(screen.get_width(),screen.get_height())
  enemies = pygame.sprite.Group()
  for i in range(20):
    enemy = Entity.Enemy((screen.get_height()*math.cos(i*math.pi/10)+screen.get_width()/3,screen.get_height()*math.sin(i*math.pi/10) + screen.get_height()/3),(25,25),"red", 3)
    enemies.add(enemy)
  camera += enemies
  player = Entity.Player((screen.get_width()/2,screen.get_height()/2),(25,25), "white")
  camera += player
  aura = Weapons.Aura(player, 60, (0, 0, 255, 100))
  player.weapons.append(aura)
  revolver = Weapons.Revolver(player,1000, (0, 0, 255, 200), 0, 20, 2)
  player.weapons.append(revolver)
  lightning = Weapons.Lightning(player,1000, (200, 200, 255, 200), 5, 2)
  player.weapons.append(lightning)
  
  while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_SPACE:

            print(camera)
            if keys[pygame.K_d]:
              player.rect.centerx += 20
              camera.update((20,0))
            if keys[pygame.K_a]:
              player.rect.centerx -= 20
              camera.update((-20,0))
            if keys[pygame.K_w]:
              player.rect.centery -= 20
              camera.update((0,-20))
            if keys[pygame.K_s]:
              player.rect.centery += 20
              camera.update((0,20))
          if event.key == pygame.K_q:
              #bullets.projCount *= 2
              pass
            
              
    
    if keys[pygame.K_d]:
      for i in range(math.ceil(player.rect.width/10)):
          player.rect.centerx += 1
          camera.update((1,0))
    if keys[pygame.K_a]:
      for i in range(math.ceil(player.rect.width/10)):
          player.rect.centerx -= 1
          camera.update((-1,0))
    if keys[pygame.K_w]:
      for i in range(math.ceil(player.rect.width/10)):
          player.rect.centery -= 1
          camera.update((0,-1))
    if keys[pygame.K_s]:
      for i in range(math.ceil(player.rect.width/10)):
          player.rect.centery += 1
          camera.update((0,1))
    
    for enemy in enemies:
      enemy.advance(player.rect.center, speed=0)
      if enemy.rect.colliderect(player.rect):
          player.health_bar.Damage(0.5)
      if player.health_bar.current_health <= 0:
          print("Player Defeated!")
          running = False
    
    
  

    screen.fill("black")

    camera.draw(screen)
    for weapon in player.weapons:
      weapon.Attack(enemies)
      

    
    

    pygame.display.flip()

    clock.tick(60)  
  
  pygame.quit()
  
if __name__ == "__main__":
  main()
