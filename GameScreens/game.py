import pygame
import math
from Assets import Entity, Resources, Weapons, globs
import random
from pygGUI import Text, Menu, Button
import logging
import random

import asyncio

pygame.init()


async def main() -> dict | None:
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    camera = Resources.Camera(screen.get_width(), screen.get_height())
    enemies = pygame.sprite.Group()

    points = 0
    pointsL = Text(f"Points: {points}", pygame.font.Font("8bitFONT.ttf", 70), "yellow", (10, 10))

    for i in range(10):
        enemy = Entity.Enemy((screen.get_height() * math.cos(i * math.pi / 10) + screen.get_width() / 3,
                              screen.get_height() * math.sin(i * math.pi / 10) + screen.get_height() / 3), (25, 25),
                             "red", 1)
        enemies.add(enemy)
    camera.add(enemies)
    player = Entity.Player((screen.get_width() / 2, screen.get_height() / 2), (25, 25), "white")
    camera.add(player)

    #player.addWeapon(Weapons.Aura(player, 60, 1, (0, 0, 255, 100)))
    player.addWeapon(Weapons.Revolver(player, 1000, (0, 0, 255, 200), 20, 10, 1))
    player.addWeapon(Weapons.Lightning(player, 1000, (200, 200, 255, 200), 25, 1))

    running = True

    logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] - %(message)s')


    upgradeMenu = Menu("Upgrade", "white", pygame.font.Font("8bitFONT.ttf", 70), 2 / 3 * screen.get_width(),
                       4 / 5 * screen.get_height(), "grey", pos=(screen.get_width() / 2, screen.get_height() / 2),
                       anchor="center")

    def damageMult(percent: int) -> None:
        for weapon in player.weapons:
            weapon.damage = math.ceil(weapon.damage * (1 + percent / 100))

    def addProjectile(count: int) -> None:
        for weapon in player.weapons:
            if hasattr(weapon, 'projCount'):
                weapon.projCount += count
    
    def addWeapon(weapon: Resources._isWeapon):
        if not weapon in player.weapons:
            raise NotImplementedError('weapons need default cases first')
            player.addWeapon(weapon(player))
        

    damageUpgrades = {f"{percent+5}% Damage Increase": lambda: damageMult(percent+5) for percent in range(0, 15, 5)}
    projCountUpgrades = {f"+{count+1} Projectiles": lambda: addProjectile(count+1) for count in range(2)}
    upgrades = {**damageUpgrades, **projCountUpgrades}
    upgradeButtons = []
    for i in range(3):
        upgrade = random.choice(list(upgrades.items()))
        button = Button(upgrade[0], pygame.font.Font("8bitFONT.ttf", 40), "black",
                        pos=(upgradeMenu.width / 2, upgradeMenu.height / 6 + (i + 1) * upgradeMenu.height / 6),
                        anchor="center", command=upgrade[1], bgcolor="lime", bgcolorHover="grey")
        upgradeMenu.add(button)
        upgradeButtons.append(button)

    async def upgradeFunc() -> dict | None:
        for i in upgradeButtons:
            upgrade = random.choice(list(upgrades.items()))
            i.command = upgrade[1]
            i.text = upgrade[0]
            i.update()

        runnin2 = True  # doom reference?
        while runnin2:
            for event in pygame.event.get():
                outputs = upgradeMenu.input(event)
                if outputs:
                    runnin2 = False
                await upgradeMenu.hover()
                if event.type == pygame.QUIT:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
                    return

            upgradeMenu.draw(screen)

            pygame.display.flip()
            clock.tick(60)
            await asyncio.sleep(0)

    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {'case': "QUIT"}
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F2:
                    for i in player.weapons:
                        print(f"{str(i).upper()} - damage: {i.damage}, projectiles: {i.projCount}")
                if event.key == pygame.K_F1:
                    returndict: dict = {'case': "DEAD", 'points': points}
                    logging.debug(returndict)
                    return returndict
                if event.key == pygame.K_F3:
                    await upgradeFunc()


        if keys[pygame.K_d]:
            globs.moveDirection(player, 0, math.ceil(player.rect.width / 10))
            camera.update((math.ceil(player.rect.width / 10), 0))
        if keys[pygame.K_a]:
            globs.moveDirection(player, math.pi, math.ceil(player.rect.width / 10))
            camera.update((-math.ceil(player.rect.width / 10), 0))
        if keys[pygame.K_w]:
            globs.moveDirection(player, math.pi / 2, math.ceil(player.rect.width / 10))
            camera.update((0, -math.ceil(player.rect.width / 10)))
        if keys[pygame.K_s]:
            globs.moveDirection(player, -math.pi / 2, math.ceil(player.rect.width / 10))
            camera.update((0, math.ceil(player.rect.width / 10)))


        for enemy in enemies:
            enemy.advance(player.rect.center, speed=1)
            if enemy.rect.colliderect(player.rect):
                player.health_bar.damage(0.5)
            if player.isDead():
                returndict: dict = {'case': "DEAD", 'points': points}
                logging.debug(returndict)
                return returndict
            if enemy.isDead():
                points += 1
                pointsL.text = f"Points: {points}"
                pointsL.update()
                enemy.kill()
                if points%10 == 0:
                    await upgradeFunc()



        if globs.cooldownCheck(1000) and len(enemies) < 30:
            for i in range(25):
                enemy = Entity.Enemy((player.rect.centerx + random.randint(-1000, 1000),
                                      player.rect.centery + random.randint(-1000, 1000)), (25, 25), "red", 3)
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

