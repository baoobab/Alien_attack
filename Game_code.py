import os
import sys

import pygame

pygame.font.init()
size = width, height = 550, 650
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Alien Attack')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()

x = 225
y = 550
ship_height = 90
ship_width = 80
bullets = []
x_alien = 30
y_alien = 30


class bulleti():
    def __init__(self, x, y, r, color, stor):
        self.x = x
        self.y = y
        self.r = 5
        self.color = color
        self.stor = stor
        self.vel = 8 * stor

    def draw(self, screen):
        self.win = screen
        pygame.draw.circle(self.win, self.color, (self.x, self.y), self.r)


def draw_ammo(screen):
    font = pygame.font.Font(None, 100)
    font2 = pygame.font.Font(None, 25)
    text = font.render(f"{5 - len(bullets)}", True, (255, 0, 0))
    text2 = font2.render("Патроны", True, (255, 0, 0))
    screen.blit(text, (500, 15))
    screen.blit(text2, (470, 5))


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
alien = load_image("alien.png", -1)
alien = pygame.transform.scale(alien, (50, 50))

running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(ship, (x, y))
    for i in range(6):
        for j in range(3):
            screen.blit(alien, (x_alien * 3 * i + 25, y_alien + j * 50))
            # проверка на совпадение координат пришельца и пули, удаление пули, нужно дописать, чтобы пропадал пришелец
            for bullet in bullets:
                if (
                        bullet.x < x_alien * 3 * i + 25 + 50 and bullet.x > x_alien * 3 * i + 25) \
                        and bullet.y < y_alien + j * 50 + 50 and bullet.y > y_alien + j * 50:
                    bullets.remove(bullet)
    y_alien += 0.3
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(bullets) < 5:
                bullets.append(bulleti(round(x + 80 // 2), round(y + 90 // 2),
                                       5, (255, 0, 0), 1))
    for bullet in bullets:
        if 550 > bullet.y > 0:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
        print(bullet.y, bullet.x)

    for bullet in bullets:
        bullet.draw(screen)

    draw_ammo(screen)
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]

    clock.tick(40)
    pygame.display.flip()

pygame.quit()
