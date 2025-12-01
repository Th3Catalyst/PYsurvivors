import pygame
import math
from Assets import Entity, Resources, Weapons, globs
import random
from pygGUI import Text

import asyncio

pygame.init()


async def main():
  screen = pygame.display.set_mode((1280, 720))
  clock = pygame.time.Clock()


  camera = Resources.Camera(screen.get_width(),screen.get_height())
  enemies = pygame.sprite.Group()

  points = 0
  pointsL = Text(f"Points: {points}",pygame.font.Font("8bitFONT.ttf", 70), "yellow", (10,10))

  for i in range(10):
    enemy = Entity.Enemy((screen.get_height()*math.cos(i*math.pi/10)+screen.get_width()/3,screen.get_height()*math.sin(i*math.pi/10) + screen.get_height()/3),(25,25),"red", 1)
    enemies.add(enemy)
  camera.add(enemies)
  player = Entity.Player((screen.get_width()/2,screen.get_height()/2),(25,25), "white")
  camera.add(player)

  player.addWeapon(Weapons.Aura(player, 60, 1,(0, 0, 255, 100)))
  player.addWeapon(Weapons.Revolver(player,1000, (0, 0, 255, 200), 20, 10, 5))
  player.addWeapon(Weapons.Lightning(player,1000, (200, 200, 255, 200), 25, 2))

  running = True
  
  while running:
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_q:
              #bullets.projCount *= 2
              pass
            
              
    
    if keys[pygame.K_d]:
        globs.moveDirection(player, 0, math.ceil(player.rect.width/10))
        camera.update((math.ceil(player.rect.width/10),0))
    if keys[pygame.K_a]:
        globs.moveDirection(player, math.pi, math.ceil(player.rect.width/10))
        camera.update((-math.ceil(player.rect.width/10),0))
    if keys[pygame.K_w]:
        globs.moveDirection(player, math.pi/2, math.ceil(player.rect.width/10))
        camera.update((0,-math.ceil(player.rect.width/10)))
    if keys[pygame.K_s]:
        globs.moveDirection(player, -math.pi/2, math.ceil(player.rect.width/10))
        camera.update((0,math.ceil(player.rect.width/10)))
    
    for enemy in enemies:
        enemy.advance(player.rect.center, speed=1)
        if enemy.rect.colliderect(player.rect):
            player.health_bar.damage(0.5)
        if player.isDead():
            print("Player Defeated!")
            running = False
        if enemy.isDead():
            points += 1
            pointsL.text = f"Points: {points}"
            pointsL.update()
            enemy.kill()



    if globs.cooldownCheck(1000) and len(enemies) < 30:
        for i in range(25):
            enemy = Entity.Enemy((player.rect.centerx + random.randint(-1000,1000),player.rect.centery + random.randint(-1000,1000)),(25,25),"red", 3)
            enemies.add(enemy)
            camera.add(enemy)
            if camera.screen.colliderect(enemy.rect):
                enemy.kill()
    elif globs.cooldownCheck(1000):
      for i in enemies:
        if not camera.screen.colliderect(i.rect):
          i.kill()

    screen.fill("black")

    camera.draw(screen)
    for weapon in player.weapons:
      weapon.Attack(enemies)
      

    pointsL.draw(screen)

    

    pygame.display.flip()

    globs.tick(clock.tick(60))
    await asyncio.sleep(0)
  
  
if __name__ == "__main__":
    asyncio.run(main())

