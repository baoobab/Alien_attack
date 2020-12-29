import os
import sys

import pygame

size = width, height = 550, 650
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Alien Attack')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

x = 225
y = 550
ship_height = 90
ship_width = 80


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


background = load_image("bg.jpg")
ship = load_image("spaceship.png")

running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(ship, (x, y))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]

    clock.tick(30)
    pygame.display.flip()

pygame.quit()
