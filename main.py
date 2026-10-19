import pygame
from random import randint
from time import time

pygame.init()

gridSize = (20, 15)
tileSize = 30
window = pygame.display.set_mode((gridSize[0] * tileSize + 20, gridSize[1] * tileSize + 70))
pygame.display.set_caption("Alien Run")
clock = pygame.time.Clock()
font1 = pygame.font.SysFont("Consolas", 26)
font2 = pygame.font.SysFont("Consolas", 32)

grid = [[0] * gridSize[1] for x in range(gridSize[0])]

def addSpaceship(count = 1):
    if len(spaceships) + len(laserbeam) == gridSize[0] * gridSize[1]: 
        print(len(spaceships) + len(laserbeam))
        return
    for i in range(count):
        pos = laserbeam[0]
        while pos in laserbeam or pos in spaceships:
            pos = (randint(0, gridSize[0] - 1), randint(0, gridSize[1] - 1))
        spaceships.append(pos)

def play():
    global running, spaceships, laserbeam
    spaceships = list()
    laserbeam = [(i, gridSize[1] // 2) for i in range(1, 5)]
    addSpaceship(10)
    score = 0
    lastTime = time()
    direction = (1, 0)
    showWinScreen = False
    showLoseScreen = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]: return
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction = (0, -1)
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction = (-1, 0)
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction = (0, 1)
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction = (1, 0)

        if not showWinScreen and not showLoseScreen and time() - lastTime > 0.15:
            newPos = (laserbeam[-1][0] + direction[0], laserbeam[-1][1] + direction[1])
            if newPos in laserbeam or not (0 <= newPos[0] < gridSize[0] and 0 <= newPos[1] < gridSize[1]):
                print("Game lost")
                showLoseScreen = True
            else:
                laserbeam.append(newPos)
            if len(laserbeam) == gridSize[0] * gridSize[1]:
                print("Game won")
                showWinScreen = True
            if newPos in spaceships:
                spaceships.remove(newPos)
                score += 1
                addSpaceship(1)
            else:
                laserbeam.pop(0)
            lastTime = time()

        window.fill("grey")
        text = font1.render(f"Spaceships caught: {score}", True, "black")
        textRect = text.get_rect(midleft=(10, 30))
        window.blit(text, textRect)
        for i in range(gridSize[0]):
            for j in range(gridSize[1]):
                tileRect = pygame.Rect(10 + i * tileSize, 60 + j * tileSize, tileSize, tileSize)
                pygame.draw.rect(window, [(200, 200, 255), (170, 170, 255)][(i + j) % 2], tileRect)

        for i in spaceships:
            tileRect = pygame.Rect(12 + i[0] * tileSize, int(60 + (i[1] + 0.3) * tileSize), tileSize - 4, int(tileSize * 0.5))
            pygame.draw.rect(window, "blue", tileRect, 0, tileSize // 2, tileSize // 4, tileSize // 4)
            pygame.draw.circle(window, "green", (10 + (i[0] + 0.5) * tileSize, 60 + (i[1] + 0.3) * tileSize), tileSize // 5)

        for x in range(len(laserbeam) - 1):
            a, b = laserbeam[-1 - x], laserbeam[- 2 - x]
            tileRect = pygame.Rect(14 + min(a[0], b[0]) * tileSize, 64 + min(a[1], b[1]) * tileSize, (abs(b[0] - a[0]) + 1) * tileSize - 8, (abs(b[1] - a[1]) + 1) * tileSize - 8)
            pygame.draw.rect(window, (255, 255 - (x * 150 // len(laserbeam)), 0), tileRect, 0, (tileSize - 4) // 2)

        if showLoseScreen:
            text = font2.render(f"You lost!", True, "red")
            textRect = text.get_rect(center=(gridSize[0] / 2 * tileSize + 10, gridSize[1] / 2 * tileSize + 35))
            window.blit(text, textRect)
        if showWinScreen:
            text = font2.render(f"You win!", True, "green")
            textRect = text.get_rect(center=(gridSize[0] / 2 * tileSize + 10, gridSize[1] / 2 * tileSize + 35))
            window.blit(text, textRect)

        pygame.display.flip()
        clock.tick(60)

running = True
while running:
    ending = play()

pygame.quit()