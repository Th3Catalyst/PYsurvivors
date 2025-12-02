import json

from GameScreens import game, endScreen
import asyncio
import pygame
from pygGUI import Menu, Button, Text

pygame.init()


async def parseOutput(output: dict) -> dict:
    match output['case']:
        case "DEAD":
            return await parseOutput(await endScreen.main(output['points']))
        case "Main Menu":
            return {"case": "MAIN MENU", "points": output['points']}
        case _:
            return output


async def main() -> None:
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    running = True
    with open("score.json",'r') as file:
        config = json.load(file)
        highscore = config["highscore"]


    def runGame() -> bool: return True

    startMenu = Menu("PYsurvivors", "white", pygame.font.Font("8bitFONT.ttf", 200),screen.get_width(), screen.get_height(),"black",hrcolor="black")
    startButton = Button("PLAY",pygame.font.Font("8bitFONT.ttf", 100), "black",command=runGame, bordercolor="white",bgcolor="white",bgcolorHover="grey",borderWidth=2)
    highscoreText = Text(f"HIGHSCORE: {highscore}", pygame.font.Font("8bitFONT.ttf", 100), "gold", pos=(screen.get_width()/2,screen.get_height()-10), anchor="s")
    startMenu.add(startButton)
    startMenu.add(highscoreText)
    while running:
        for event in pygame.event.get():
            
            if startButton in (outputs := startMenu.input(event)):
                if output := await parseOutput(await game.main()):
                    match output['case']:
                        case "QUIT":
                            running = False
                        case "MAIN MENU":
                            if output['points'] > highscore:
                                highscore = output['points']
                                highscoreText.text = f"HIGHSCORE: {highscore}"
                                highscoreText.update()
                                with open("score.json",'w') as file:
                                    file.write(json.dumps({"highscore": highscore},indent=4))



            await startMenu.hover()
            if event.type == pygame.QUIT:
                running = False


        screen.fill("black")
        startMenu.draw(screen)

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)


if __name__ == "__main__":
    asyncio.run(main())