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

aliens_lvl1 = []
aliens_lvl2 = []
x_alien_lvl1 = x_alien_lvl2 = 30
y_alien_lvl1 = y_alien_lvl2 = 30
alien_speed_lvl1 = 0.4
alien_speed_lvl2 = 1.2


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


def is_cross(a, b):
    ax1, ay1, ax2, ay2 = a[0], a[1], a[2], a[3]  # прямоугольник А
    bx1, by1, bx2, by2 = b[0], b[1], b[2], b[3]  # прямоугольник B

    s1 = (ax1 >= bx1 and ax1 <= bx2) or (ax2 >= bx1 and ax2 <= bx2)
    s2 = (ay1 >= by1 and ay1 <= by2) or (ay2 >= by1 and ay2 <= by2)
    s3 = (bx1 >= ax1 and bx1 <= ax2) or (bx2 >= ax1 and bx2 <= ax2)
    s4 = (by1 >= ay1 and by1 <= ay2) or (by2 >= ay1 and by2 <= ay2)
    if ((s1 and s2) or (s3 and s4)) or ((s1 and s4) or (s3 and s2)):
        return True
    else:
        return False


def terminate():
    pygame.quit()
    sys.exit()


def start_menu():
    pygame.mouse.set_visible(True)
    screen.blit(menu_bg, (0, 0))
    screen.blit(menu_btn1, (120, 270))
    screen.blit(menu_btn2, (120, 390))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEMOTION:
                if 420 > pygame.mouse.get_pos()[0] > 120 and 370 > pygame.mouse.get_pos()[1] > 270:
                    screen.blit(menu_btn1a, (120, 270))
                else:
                    screen.blit(menu_btn1, (120, 270))
                if 420 > pygame.mouse.get_pos()[0] > 120 and 490 > pygame.mouse.get_pos()[1] > 390:
                    screen.blit(menu_btn2a, (120, 390))
                else:
                    screen.blit(menu_btn2, (120, 390))

            elif event.type == pygame.MOUSEBUTTONDOWN and (
                    420 > pygame.mouse.get_pos()[0] > 120 and 370 > pygame.mouse.get_pos()[1] > 270):
                pygame.mouse.set_visible(False)
                return  # начинаем игру

            elif event.type == pygame.KEYDOWN:
                pygame.mouse.set_visible(False)
                return  # начинаем игру

        pygame.display.flip()


background = load_image("bg.jpg")
ship = load_image("spaceship.png")
alien = load_image("alien.jpg", -1)
game_over = load_image("gameover.jpg", -1)
name = load_image("name.png", -1)
alien2 = load_image("alien2.jpg", -1)
alien3 = load_image("alien3.jpg", -1)
menu_bg = load_image("menu_bg3.png")
menu_bg = pygame.transform.scale(menu_bg, (550, 650))
menu_btn1 = load_image("btn_1t.png")  # "t" означает что это тестовая кнопка
menu_btn1a = load_image("btn_1ta.png")  # "a" означает что это активная кнопка (меняется на неё при наведении)
menu_btn2 = load_image("btn_2t.png")
menu_btn2a = load_image("btn_2ta.png")

alien = pygame.transform.scale(alien, (50, 50))
alien2 = pygame.transform.scale(alien2, (50, 50))
alien3 = pygame.transform.scale(alien3, (50, 50))

lvl = 1

for i in range(6):
    _ = []
    for j in range(3):
        _.append(2)
    aliens_lvl1.append(_)

for i in range(6):
    _ = []
    for j in range(2):
        _.append(1)
    aliens_lvl2.append(_)
# print(aliens)

start_menu()
running = True
while running:
    screen.blit(background, (0, 0))
    screen.blit(name, (125, 0))
    screen.blit(ship, (x, y))

    if lvl == 1:
        for i in range(6):
            for j in range(3):
                if aliens_lvl1[i][j] == 2:
                    screen.blit(alien, (x_alien_lvl1 * 3 * i + 25, y_alien_lvl1 + j * 50))
                    for bullet in bullets:
                        if (x_alien_lvl1 * 3 * i + 25 + 50 > bullet.x > x_alien_lvl1 * 3 * i + 25) \
                                and y_alien_lvl1 + j * 50 + 50 > bullet.y > y_alien_lvl1 + j * 50:
                            if aliens_lvl1[i][j] == 1:
                                aliens_lvl1[i][j] = 0
                            else:
                                aliens_lvl1[i][j] = 1
                            bullets.remove(bullet)

                elif aliens_lvl1[i][j] == 1:
                    screen.blit(alien2, (x_alien_lvl1 * 3 * i + 25, y_alien_lvl1 + j * 50))
                    for bullet in bullets:
                        if (x_alien_lvl1 * 3 * i + 25 + 50 > bullet.x > x_alien_lvl1 * 3 * i + 25) \
                                and y_alien_lvl1 + j * 50 + 50 > bullet.y > y_alien_lvl1 + j * 50:
                            if aliens_lvl1[i][j] == 1:
                                aliens_lvl1[i][j] = 0
                            else:
                                aliens_lvl1[i][j] = 1
                            bullets.remove(bullet)

                    # ф-я для отслеживания столкновений
                if is_cross([x, y, x + ship_width, y + ship_height],
                            [x_alien_lvl1 * 3 * i + 25 + 50, y_alien_lvl1 + j * 50 + 50, x_alien_lvl1 * 3 * i + 25, y_alien_lvl1 + j * 50]):
                    # если врезались во врага, то игра окончена
                    screen.blit(game_over, (130, 250))
                    # running = False

        y_alien_lvl1 += alien_speed_lvl1
        if aliens_lvl1 == [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]:
            lvl += 1
    if lvl == 2:
        for i in range(6):
            for j in range(2):
                if aliens_lvl2[i][j] == 1:
                    screen.blit(alien3, (x_alien_lvl2 * 3 * i + 25, y_alien_lvl2 + j * 50))
                    for bullet in bullets:
                        if (x_alien_lvl2 * 3 * i + 25 + 50 > bullet.x > x_alien_lvl2 * 3 * i + 25) \
                                and y_alien_lvl2 + j * 50 + 50 > bullet.y > y_alien_lvl2 + j * 50:
                            if aliens_lvl2[i][j] == 1:
                                aliens_lvl2[i][j] = 0
                            else:
                                aliens_lvl2[i][j] = 1
                            bullets.remove(bullet)

                    # ф-я для отслеживания столкновений
                if is_cross([x, y, x + ship_width, y + ship_height],
                            [x_alien_lvl2 * 3 * i + 25 + 50, y_alien_lvl2 + j * 50 + 50, x_alien_lvl2 * 3 * i + 25, y_alien_lvl2 + j * 50]):
                    # если врезались во врага, то игра окончена
                    screen.blit(game_over, (130, 250))
                    # running = False

        y_alien_lvl2 += alien_speed_lvl2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(bullets) < 5:
                bullets.append(bulleti(round(x + 80 // 2), round(y + 50 // 2),
                                       5, (255, 0, 0), 1))
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False

    for bullet in bullets:
        if 550 > bullet.y > 0:
            bullet.y -= bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    for bullet in bullets:
        bullet.draw(screen)

    draw_ammo(screen)
    x = pygame.mouse.get_pos()[0]
    y = pygame.mouse.get_pos()[1]

    clock.tick(40)
    pygame.display.flip()

pygame.quit()
