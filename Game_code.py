import os
import random
import sys
import time

import pygame

pygame.init()
song1 = pygame.mixer.Sound('shoot.mp3')
song2 = pygame.mixer.Sound('boom.mp3')
song3 = pygame.mixer.Sound('sound.mp3')
song4 = pygame.mixer.Sound('next_lvl.mp3')
song5 = pygame.mixer.Sound('gmover.mp3')
song6 = pygame.mixer.Sound('game_music.mp3')
song7 = pygame.mixer.Sound('boss_shoot.mp3')
song8 = pygame.mixer.Sound('boss_death.mp3')
song9 = pygame.mixer.Sound('boss_fight.mp3')

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

bullets = []  # патроны
boss_bullets = []  # патроны босса
aliens = []  # пришельцы (набор цифр)

x_alien = 30  # коорды пришельцев
y_alien = 30
alien_speed = 0  # скорость пришельцев

boss_lvl = 10  # хп босса
lvl = 0  # текущий уровень
score = 0  # счет
best_score = 0  # лучший счёт

can_draw = True  # для правильной отрисовки кнопок в меню
boss = False  # проверка на босса
stop_game = False  # проверка на паузу
pause_timer = True  # пауза при сворачивании


# класс патронов
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


# отрисовка предисловия
def draw_rules(screen):
    global can_draw
    can_draw = False
    font = pygame.font.Font(None, 30)
    screen.blit(background, (0, 0))
    intro_text = ["ПРЕДИСЛОВИЕ", "",
                  "На дворе 2083 год.",
                  "Вы на своём космическом корабле возвращаетесь ",
                  "домой из межгалактического магазина,",
                  "но вдруг...",
                  "На вас нападает банда космических пиратов,",
                  " которое явно что-то от вас хотят.",
                  "Улететь - не выход, ведь они быстрее.",
                  '',
                  "Ваша цель - простоять как можно дольше.",
                  "",
                  "КАК ИГРАТЬ?",
                  "",
                  "Управление кораблем - ведение мышкой",
                  "Стрелять - ЛКМ",
                  "Пауза - ESC",
                  '',
                  "(кликните по экрану для возврата в меню)"]

    text_coord = 45
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                screen.blit(menu_bg, (0, 0))
                screen.blit(menu_btn1, (120, 270))
                screen.blit(menu_btn2, (120, 390))
                screen.blit(menu_bestscore, (120, 580))
                draw_score(screen, 0)
                can_draw = True
                pygame.mouse.set_visible(True)
                return
        pygame.display.flip()


# отрисовка патрон и уровня
def draw_txt(screen):
    font = pygame.font.Font(None, 100)
    font2 = pygame.font.Font(None, 25)
    text = font.render(f"{5 - len(bullets)}", True, (255, 0, 0))
    text2 = font2.render("Патроны", True, (255, 0, 0))
    text3 = font2.render(f"Уровень: {lvl}", True, (255, 0, 0))
    screen.blit(text, (500, 15))
    screen.blit(text2, (470, 5))
    screen.blit(text3, (420, 610))


# отрисовка ХП и названия босса
def draw_boss(screen, flag):
    global boss_hp
    if flag == 111:
        font = pygame.font.Font(None, 120)
        text = font.render("BOSS", True, (255, 0, 0))
        screen.blit(text, (150, 300))
    else:
        screen.blit(boss_hp_bg, (140, 10))
        boss_hp = pygame.transform.scale(boss_hp,
                                         ((200 // boss_lvl) * flag, 30))
        screen.blit(boss_hp, (145, 15))


# отрисовка счета
def draw_score(screen, flag):
    if flag == 1:
        font = pygame.font.Font(None, 25)
        text = font.render(f"Счёт: {score}", True, (255, 0, 0))
        screen.blit(text, (5, 610))
    else:
        count_score(1)
        font = pygame.font.Font(None, 50)
        text2 = font.render(f"{best_score}", True, (255, 255, 255))
        screen.blit(text2, (330, 600))


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


# считываем или записываем счёт в файл для сохранения
def count_score(flag):
    global best_score
    if flag == 1:
        with open("settings.txt", mode="r") as f:
            data = f.read()
            best_score = int(data)
    else:
        if score >= best_score:
            best_score = score
            with open("settings.txt", mode="w") as f:
                f.write(str(best_score))


# проверка на пересечение корабля и пришельцев
def is_cross(a, b):
    ax1, ay1, ax2, ay2 = a[0], a[1], a[2], a[3]  # прямоугольник А
    bx1, by1, bx2, by2 = b[0], b[1], b[2], b[3]  # прямоугольник B

    s1 = (bx1 <= ax1 <= bx2) or (ax2 >= bx1 and ax2 <= bx2)
    s2 = (by1 <= ay1 <= by2) or (ay2 >= by1 and ay2 <= by2)
    s3 = (ax1 <= bx1 <= ax2) or (bx2 >= ax1 and bx2 <= ax2)
    s4 = (ay1 <= by1 <= ay2) or (by2 >= ay1 and by2 <= ay2)
    if ((s1 and s2) or (s3 and s4)) or ((s1 and s4) or (s3 and s2)):
        return True
    else:
        return False


def terminate():  # выход
    pygame.quit()
    sys.exit()


# генерация уровня или босса
def lvl_generate():
    global alien_speed, x_alien, y_alien, lvl, boss_lvl
    x_alien = 30
    y_alien = 30
    aliens.clear()
    lvl += 1

    if lvl % 5 != 0 and lvl != 0:
        if random.randrange(0, 2) == 1:
            for i in range(6):
                _ = []
                for j in range(3):
                    if lvl < 5:
                        _.append(random.choice([0, 2]))
                    else:
                        _.append(2)
                aliens.append(_)
            alien_speed = alien_speed // 2

        else:
            for i in range(6):
                _ = []
                for j in range(3):
                    if lvl < 5:
                        _.append(random.choice([0, 3]))
                    else:
                        _.append(3)
                aliens.append(_)
    else:
        for i in range(6):
            _ = []
            for j in range(3):
                if i == 2 and j == 2:
                    _.append(boss_lvl)
                else:
                    _.append(0)
            aliens.append(_)
        alien_speed = alien_speed // 2

    alien_speed += 0.05


# стартовое меню
def start_menu():
    global running, GAME_OVER, stop_game
    clear_game()
    song6.stop()
    song3.play(-1)
    pygame.mouse.set_visible(True)
    screen.blit(menu_bg, (0, 0))
    screen.blit(menu_btn1, (120, 270))
    screen.blit(menu_btn2, (120, 390))
    screen.blit(menu_bestscore, (120, 580))
    draw_score(screen, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()

            elif event.type == pygame.MOUSEMOTION and can_draw:
                if 420 > pygame.mouse.get_pos()[0] > 120 and 370 > \
                        pygame.mouse.get_pos()[1] > 270:
                    screen.blit(menu_btn1a, (120, 270))
                else:
                    screen.blit(menu_btn1, (120, 270))
                if 420 > pygame.mouse.get_pos()[0] > 120 and 490 > \
                        pygame.mouse.get_pos()[1] > 390:
                    screen.blit(menu_btn2a, (120, 390))
                else:
                    screen.blit(menu_btn2, (120, 390))

            elif event.type == pygame.MOUSEBUTTONDOWN and (
                    420 > pygame.mouse.get_pos()[0] > 120 and 370 >
                    pygame.mouse.get_pos()[1] > 270) and can_draw:
                pygame.mouse.set_visible(False)
                running = True
                GAME_OVER = False
                stop_game = False
                song3.stop()
                song6.play(-1)
                return  # начинаем игру

            elif event.type == pygame.MOUSEBUTTONDOWN and (
                    420 > pygame.mouse.get_pos()[0] > 120 and 490 >
                    pygame.mouse.get_pos()[1] > 390):
                draw_rules(screen)

        pygame.display.flip()


# меню паузы
def pause_menu():
    global stop_game, pause_timer
    screen.blit(pause, (120, 210))
    screen.blit(pause_btns, (120, 380))
    stop_game = True
    pause_timer = False
    pygame.mouse.set_visible(True)


# игра окончена, выход и очистка
def gameover():
    global GAME_OVER, running
    pygame.mixer.pause()
    count_score(0)
    GAME_OVER = True
    running = False
    song5.play(0)
    screen.blit(game_over, (130, 250))
    pygame.display.flip()
    time.sleep(2)
    clear_game()
    start_menu()


# очистка игры и переменных
def clear_game():
    global boss_lvl, lvl, alien_speed, score, stop_game, GAME_OVER
    global best_score, aliens, running, x, y
    aliens.clear()
    boss_bullets.clear()
    bullets.clear()
    boss_lvl = 10
    lvl = 0
    alien_speed = 0
    x = 225
    y = 550
    if score > best_score:
        best_score = score
    score = 0
    lvl_generate()
    stop_game = False
    GAME_OVER = False
    pygame.mouse.set_visible(False)


background = load_image("bg.jpg")
ship = load_image("spaceship.png")
ship_2 = load_image("spaceship_2.png")
game_over = load_image("gameover.png", -1)

pause = load_image("pause.png")
pause = pygame.transform.scale(pause, (300, 160))
pause_btns = load_image("pause_btns.png")
pause_btns = pygame.transform.scale(pause_btns, (300, 160))

boss_hp_bg = load_image("boss_hp_bg.png")
boss_hp = load_image("boss_hp.png")
boss_hp_bg = pygame.transform.scale(boss_hp_bg, (210, 40))
boss_hp = pygame.transform.scale(boss_hp, (200, 30))

menu_bg = load_image("testbg.png")
menu_bg = pygame.transform.scale(menu_bg, (550, 650))
menu_btn1 = load_image("btn_1t.png")
menu_btn1a = load_image("btn_1ta.png")
menu_btn2 = load_image("btn_2t.png")
menu_btn2a = load_image("btn_2ta.png")
menu_bestscore = load_image("bestscore.png")
menu_bestscore = pygame.transform.scale(menu_bestscore, (200, 70))

alien4 = load_image("boss.png", -1)
alien1 = load_image("alien2.png", -1)
alien2 = load_image("alien.png", -1)
alien3 = load_image("alien3.png", -1)
alien5 = load_image("boss_kill.png")
alien1 = pygame.transform.scale(alien1, (50, 50))
alien2 = pygame.transform.scale(alien2, (50, 50))
alien3 = pygame.transform.scale(alien3, (50, 50))
alien4 = pygame.transform.scale(alien4, (150, 100))
alien5 = pygame.transform.scale(alien5, (150, 100))
aliens_img = {1: alien1, 2: alien2, 3: alien3, 10: alien4, 11: alien5}

lvl_generate()
start_menu()
count_score(1)
song6.play(-1)

GAME_OVER = False
running = True

# главный цикл игры
while running:
    if not stop_game:
        screen.blit(background, (0, 0))
        screen.blit(ship, (x, y))

    if score > best_score:
        best_score = score

    if GAME_OVER is True:
        time.sleep(2)
        clear_game()
        start_menu()
    else:
        for i in range(6):
            for j in range(3):
                if aliens[i][j] > 0:
                    # если пришельцы дошли до конца
                    if y_alien + j * 50 + 50 > 660:
                        gameover()
                        clear_game()
                    # если уровень обычный
                    if lvl % 5 != 0:
                        screen.blit(aliens_img[aliens[i][j]],
                                    (x_alien * 3 * i + 25, y_alien + j * 50))
                        for bullet in bullets:
                            if (
                                    x_alien * 3 * i + 25 + 50 >
                                    bullet.x > x_alien * 3 * i + 25) \
                                    and y_alien + j * 50 + 50 > \
                                    bullet.y > y_alien + j * 50:
                                if aliens[i][j] == 3:
                                    score += 1
                                    aliens[i][j] = 0
                                elif aliens[i][j] == 2:
                                    aliens[i][j] = 1
                                elif aliens[i][j] == 1:
                                    aliens[i][j] = 0
                                    score += 2
                                bullets.remove(bullet)
                                song2.play(0)

                    # если уровень с боссом
                    else:
                        if not boss:
                            song6.stop()
                            song9.play(0)
                        boss = True

                        if aliens[i][j] != 1:
                            screen.blit(aliens_img[10], (
                                x_alien * 3 * i + 25, y_alien + j * 50))
                        else:
                            screen.blit(aliens_img[11], (
                                x_alien * 3 * i + 25, y_alien + j * 50))

                        # выстрелы для босса
                        if random.randrange(0, 40) == 3 and not stop_game:
                            song7.play(0)
                            boss_bullets.append(
                                bulleti(round(x_alien * 3 * i + 60 + 80 // 2),
                                        round(y_alien + j * 50 + 100 // 2),
                                        10, (255, 0, 0), -1))

                        if aliens[i][j] > boss_lvl - 2 and not GAME_OVER:
                            draw_boss(screen, 111)
                            draw_boss(screen, boss_lvl)
                        else:
                            draw_boss(screen, aliens[i][j])

                        for bullet in bullets:
                            if (
                                    x_alien * 3 * i + 25 + 150 >
                                    bullet.x > x_alien * 3 * i + 25) \
                                    and y_alien + j * 50 + 100 > \
                                    bullet.y > y_alien + j * 50:
                                if aliens[i][j] > 1:
                                    aliens[i][j] -= 1
                                else:
                                    aliens[i][j] = 0
                                    score += 10
                                    boss_lvl += 10
                                    song9.stop()
                                    song8.play(0)
                                    song6.play(-1)
                                    boss = False
                                bullets.remove(bullet)

                        for bullet in boss_bullets:
                            if (
                                    x + ship_width > bullet.x > x) \
                                    and y + ship_height > bullet.y > y:
                                gameover()
                                boss_bullets.clear()

                    if is_cross([x, y, x + ship_width, y + ship_height],
                                [x_alien * 3 * i + 25 + 50,
                                 y_alien + j * 50 + 50, x_alien * 3 * i + 25,
                                 y_alien + j * 50]):
                        screen.blit(ship_2, (x, y))
                        gameover()
                        clear_game()

            if not stop_game:
                y_alien += alien_speed

                if aliens == [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0],
                              [0, 0, 0], [0, 0, 0]]:
                    lvl_generate()
                    song4.play(0)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not stop_game:
            song1.play(0)
            # если меньше 5 пуль на экране, то добавляем
            if len(bullets) < 5:
                bullets.append(bulleti(round(x + 80 // 2), round(y + 50 // 2),
                                       5, (255, 0, 0), 1))

    # если свернули - открытие паузы
    if not pygame.display.get_active():
        pause_menu()
    else:
        pause_timer = True

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        pause_menu()
    # кнопки для меню паузы
    if keys[pygame.K_SPACE] and stop_game:
        stop_game = False
        pygame.mouse.set_visible(False)

    if keys[pygame.K_r] and stop_game:
        clear_game()

    if keys[pygame.K_BACKSPACE] and stop_game:
        clear_game()
        start_menu()

    # отрисовка пуль
    if not stop_game:
        for bullet in bullets:
            bullet.draw(screen)
            if 650 > bullet.y > 0:
                bullet.y -= bullet.vel
            else:
                bullets.pop(bullets.index(bullet))

        for bullet in boss_bullets:
            bullet.draw(screen)
            if 650 > bullet.y > 0:
                bullet.y -= bullet.vel
            else:
                boss_bullets.pop(boss_bullets.index(bullet))

        x = pygame.mouse.get_pos()[0]
        y = pygame.mouse.get_pos()[1]

        draw_score(screen, 1)
        draw_txt(screen)

    clock.tick(40)
    pygame.display.flip()

count_score(0)
pygame.quit()
