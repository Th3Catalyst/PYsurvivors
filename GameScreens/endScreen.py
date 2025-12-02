import asyncio
import pygame
from pygGUI import Menu, Button, Text

pygame.init()


async def main(points = 0) -> dict | None:
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    def runGame() -> bool: return True
    endMenu = Menu("YOU LOSE", "white", pygame.font.Font("8bitFONT.ttf", 200),screen.get_width(), screen.get_height(),"black",hrcolor="black")
    pointsText = Text(f"Points: {points}",pygame.font.Font("8bitFONT.ttf", 100), "white")
    endButton = Button("MAIN MENU",pygame.font.Font("8bitFONT.ttf", 100), "black",command=runGame, bordercolor="white",bgcolor="white",bgcolorHover="grey",borderWidth=2, margin=30)
    endMenu.add(pointsText)
    endMenu.add(endButton)
    while running:
        for event in pygame.event.get():
            outputs = endMenu.input(event)
            if endButton in outputs:
                return {'case': "Main Menu", 'points': points}
            await endMenu.hover()
            if event.type == pygame.QUIT:
                return {'case': "QUIT"}


        screen.fill("black")
        endMenu.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())