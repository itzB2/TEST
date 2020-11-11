import pygame
from GameEssentials import Vector2
from chip8 import CHIP8
import numpy as np

pygame.init()

pixelSize = 1
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ScreenSize = Vector2(640,320)
ConsoleSize = Vector2(64,32)
center = (int(ConsoleSize[0]/2), int(ConsoleSize[1]/2))

user_x = ScreenSize.x
user_y = ScreenSize.y

design_x = ConsoleSize.x
design_y = ConsoleSize.y

window = pygame.display.set_mode([user_x, user_y])
w = pygame.Surface([design_x, design_y])

machine = CHIP8()
machine.loadROM("./ROMS/IBM Logo.ch8")
while True:
    try:
        machine.Cycle()
    except IndexError:
        break

gameView = machine.video
f = open("DEBUG.txt", "w")
f.write(str(gameView))
f.close()

def pixel(surface, Pixelcolor, pos, scale):
    pygame.draw.rect(surface, Pixelcolor, pygame.Rect(pos[0], pos[1], scale, scale)) 

def draw(array, rotate=False):
    rowID = 0
    colID = 0
    color = BLACK
    for rows in array:
        colID = 0
        for cols in rows:
                if cols == 0:
                    color = BLACK
                elif cols >= 1:
                    color = WHITE
                pixel(w, color, Vector2(colID, rowID), pixelSize)
                colID += 1
        rowID += 1
    frame = pygame.transform.scale(w, (user_x, user_y))
    window.blit(frame, frame.get_rect())

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw(gameView)

    pygame.display.flip()

pygame.quit()