import pygame
from sys import exit
pygame.init()

screen = pygame.display.set_mode((400,540))
pygame.display.set_caption('pie')

backdrop = pygame.image.load('graphics/planter.png')
start_button = pygame.image.load('graphics/start.png')

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.blit(backdrop, (0, 0))

    pygame.display.update()




