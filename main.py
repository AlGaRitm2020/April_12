import pygame
import pygame_gui
import random
import time

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
FPS = 60

START_HEALTH = 1
START_SPEED = 10


# класс главного героя
class Hero(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # координаты главного героя
        self.x, self.y = position

        # максимальное здоровье главного героя
        self.max_health = 30
        # здоровье главного героя
        self.health = self.max_health

        # скорость главного героя
        self.speed = 10

        # количество пуль от игрока на экране
        self.bullets_count = 0

        # наносимый урон
        self.damage = 1

        # уровень игрока
        self.lvl = 1

        # радиус главного героя
        self.radius = 20

        # заработанные очки
        self.score = 0

        # блокировка телепорта боссом
        self.locked_teleport = False

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        global image_player
        self.image = pygame.transform.scale(image_player, (60, 70))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        return (self.image, self.rect)


# класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, damage):
        pygame.sprite.Sprite.__init__(self)

        # координаты пули
        self.x, self.y = position

        # направление пули (вверх или вниз)
        self.direction = direction

        # наносимый урон
        self.damage = damage

        # радиус пули
        self.radius = 7

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        global image_bullet, image_bullet_2
        if self.direction == -1:
            self.image = pygame.transform.scale(image_bullet, (25, 60))
            self.rect = self.image.get_rect(center=(self.x, self.y))
            return (self.image, self.rect)
        else:
            self.image = pygame.transform.scale(image_bullet_2, (25, 60))
            self.rect = self.image.get_rect(center=(self.x, self.y))
            return (self.image, self.rect)


# класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, position, type):
        pygame.sprite.Sprite.__init__(self)

        # класс врага(1,2, 3 или 4)
        self.type = type

        # координаты врага
        self.x, self.y = position

        # изменение координат во времени
        self.dx = 0
        self.dy = 0

        # скорость врага
        self.speed = self.type * 2

        # счетчик времени для событий врага
        self.timer = 0

        # счетчик для выстрела
        self.kd_counter = 0

        # продолжительность перезарядки
        self.reload = 60 - self.type * 10

        self.attack_duration = None

        # здоровье врага
        self.hp = 1

        # наносимый урон
        self.damage = self.type

        # радиус врага
        self.radius = 35

        # удерживаимая дистанция до главного героя по оси x
        self.distanse = random.randint(-150, 150)

        # параметры босса
        if self.type == 4:
            self.hp = 100
            self.speed = 1
            self.distanse = 0
            self.radius = 100

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        if self.type == 4:
            size = (180, 210)
        else:
            size = (120, 70)
        global images_enemiesa
        image_enemy = images_enemies[self.type - 1]

        self.image = pygame.transform.scale(image_enemy, size)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        return (self.image, self.rect)


# класс астероида
class SuperAsteroid(pygame.sprite.Sprite):
    def __init__(self, type, *position):
        pygame.sprite.Sprite.__init__(self)

        # уровень астероида 5- изначальный, 1- почти уничтоженный
        self.type = type

        # радиус суперастероида
        radius = [30, 50, 75, 110, 150]
        self.radius = radius[self.type - 1]

        # координаты астероида
        if position:
            self.x, self.y = position[0]
        else:
            self.x = random.randint(0, WINDOW_WIDTH)
            self.y = self.radius + 10


        # урон от столкновения
        self.damage = self.type

        # изменение координат за один цикл
        self.dx = random.random() + 2.5
        self.dy = random.random() + 2.5

        # здоровье астероида
        self.hp = 2 ** (self.type + 1)

        # радиус суперастероида
        radius = [30, 50, 75, 110, 150]
        self.radius = radius[self.type - 1]

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):

        global image_superasteroid
        size = [(84, 84), (120, 120), (170, 170), (240, 240), (340, 340)]

        self.image = pygame.transform.scale(image_superasteroid, size[self.type - 1])
        self.rect = self.image.get_rect(center=(self.x, self.y))
        return (self.image, self.rect)


# класс астероида
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # координаты астероида
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = 0
        # тип астероида: 1 - 70%, 2 - 25%, 3 - 5%
        self.type = random.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3])

        # изменение координат за один цикл
        self.dx = random.randint(-10, 10)
        self.dy = random.randint(1, 10)

        # здоровье астероида
        self.hp = self.type

        # радиус астероида
        self.radius = self.type * 30

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        global image_asteroid
        size = [(60, 60), (120, 120), (180, 180)]
        self.image = pygame.transform.scale(image_asteroid, size[self.type - 1])
        self.rect = self.image.get_rect(center=(self.x, self.y))
        return (self.image, self.rect)


# класс баффов
class Buff(pygame.sprite.Sprite):
    def __init__(self, type, *position):

        pygame.sprite.Sprite.__init__(self)

        # координаты баффа
        if position:
            self.mode = "static"
            self.x, self.y = position[0]
        else:
            self.mode = "dinamic"
            self.x = random.randint(10, WINDOW_WIDTH - 10)
            self.y = 0

        # радиус баффа
        self.radius = 15

        # скорость баффа
        self.speed = random.randint(1, 5)

        # тип баффа
        self.type = type

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        global image_buff
        if self.type == 0:
            self.image = pygame.transform.scale(image_buff, (50, 50))
            self.rect = self.image.get_rect()
            return (self.image, self.rect)
        else:
            self.image = pygame.transform.scale(image_buff, (50, 50))
            self.rect = self.image.get_rect(center=(self.x, self.y))
            return (self.image, self.rect)


class BG(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # координаты фона
        self.x, self.y = position

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        global image_bg
        self.image = pygame.transform.scale(image_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.rect = self.image.get_rect()
        return (self.image, self.rect)


# класс игры
class Game:
    def __init__(self, hero, screen):
        # холст
        self.screen = screen
        # все динамичные объекты
        self.hero = hero
        self.bullets = []
        self.enemies = []
        self.asteroids = []
        self.superasteroids = []
        self.buffs = []

        self.max_count_of_enemies = 5

        # статус босса(неактивен, создан, побежден)
        self.boss_status = 0
        # статус суперастероида (неактивен, создан, побежден)
        self.superasteroid_status = 0

    # отрисовка всех динамичных объектов
    def render(self, screen):
        # отрисовка главного героя
        self.hero.render(screen)

        # отрисовка всех врагов
        for enemy in self.enemies:
            enemy.render(screen)

        # отрисовка всех астероидов
        for asteroid in self.asteroids:
            asteroid.render(screen)

        # отрисовка всех суперастероидов
        for superasteroid in self.superasteroids:
            superasteroid.render(screen)

        # отрисовка всех пуль
        for bullet in self.bullets:
            bullet.render(screen)

        # отрисовка всех баффов
        for buff in self.buffs:
            buff.render(screen)



    # движение главного героя
    def move_hero(self):
        # импорт текущих координат из класса hero
        next_x, next_y = self.hero.get_position()

        # телепортация из левого края в правый
        if next_x < 0:
            if self.hero.locked_teleport:
                next_x = 0
            else:
                next_x = WINDOW_WIDTH
        if next_x > WINDOW_WIDTH:
            if self.hero.locked_teleport:
                next_x = WINDOW_WIDTH
            else:
                next_x = 0

        if pygame.key.get_pressed()[pygame.K_a]:
            next_x -= self.hero.speed
        if pygame.key.get_pressed()[pygame.K_d]:
            next_x += self.hero.speed
        if pygame.key.get_pressed()[pygame.K_w] and self.hero.get_position()[1] > 10:
            next_y -= self.hero.speed
        if pygame.key.get_pressed()[pygame.K_s] and self.hero.get_position()[1] < WINDOW_HEIGHT - 10:
            next_y += self.hero.speed

        if pygame.key.get_pressed()[pygame.K_SPACE] or pygame.mouse.get_pressed() == (1, 0, 0):
            if self.hero.bullets_count < 320:
                for i in range(1, self.hero.lvl + 1):
                    self.bullets.append(Bullet((next_x + i * 10 - self.hero.lvl * 7, next_y), -1, self.hero.damage))
                self.hero.bullets_count += 32
        if self.hero.bullets_count >= 0:
            self.hero.bullets_count -= 1

        # изменить координаты
        self.hero.set_position((next_x, next_y))

    # движение пули
    def move_bullets(self):
        # проход по всем действующим пулям
        for i, bullet in enumerate(self.bullets):
            bullet.set_position((bullet.get_position()[0], bullet.get_position()[1] + bullet.direction * 8))
            # выход пули за пределы экрана
            if bullet.get_position()[1] < 0 or bullet.get_position()[1] > WINDOW_HEIGHT:
                if bullet.direction == -1:
                    # уменьшение счетчика пуль главного героя
                    self.hero.bullets_count -= 1
                del self.bullets[i]
            # свои пули
            if bullet.direction == -1:
                # стрельба по врагам
                for j, enemy in enumerate(self.enemies):
                    if abs(enemy.get_position()[0] - bullet.get_position()[0]) < enemy.radius + bullet.radius and abs(
                            enemy.get_position()[1] - bullet.get_position()[1]) < enemy.radius + bullet.radius:
                        # уничтожение пули и нанесение урона врагу
                        del self.bullets[i]
                        enemy.hp -= self.hero.damage

                        # уничтожение врага
                        if enemy.hp == 0:
                            # уничтожение босса
                            if enemy.type == 4:
                                self.boss_status = 2

                                # дополнительные очки за уничтожение босса
                                self.hero.score += 96

                            del self.enemies[j]
                            self.hero.score += enemy.type
                            # вывод показателя очков
                            print(f"SCORE: {self.hero.score}")
                        # увеличение счетчика пуль главного героя
                        # self.hero.bullets_count -= 1
                # стрельба по астероидам
                for j, asteroid in enumerate(self.asteroids):
                    if abs(asteroid.get_position()[0] - bullet.get_position()[
                        0]) < asteroid.radius + bullet.radius and abs(
                        asteroid.get_position()[1] - bullet.get_position()[1]) < asteroid.radius + bullet.radius:
                        # уничтожение пули и нанесение урона астероиду
                        del self.bullets[i]
                        asteroid.hp -= self.hero.damage

                        # уничтожение астероида
                        if asteroid.hp == 0:

                            # выпадение лута с астероидов
                            event = random.randint(0, 100000)
                            # малый астероид
                            if asteroid.type == 1:
                                if event % 20 == 1:
                                    buff = Buff("HP", asteroid.get_position())
                                    self.add_buff(buff)
                            # большой астероид
                            elif asteroid.type == 2:
                                if event % 3 == 1:
                                    buff = Buff("HP", asteroid.get_position())
                                    self.add_buff(buff)
                                elif event % 10 == 1:
                                    buff = Buff("SPEED UP", asteroid.get_position())
                                    self.add_buff(buff)

                            # гигантский астероид
                            elif asteroid.type == 3:
                                if event % 5 == 1:
                                    buff = Buff("LVL UP", asteroid.get_position())
                                    self.add_buff(buff)
                                elif event % 2 == 1:
                                    buff = Buff("SPEED UP", asteroid.get_position())
                                    self.add_buff(buff)
                                else:
                                    buff = Buff("HP", asteroid.get_position())
                                    self.add_buff(buff)

                            # уничтожить астероид
                            del self.asteroids[j]
                            self.hero.score += asteroid.type

                            # вывод показателя очков
                            print(f"SCORE: {self.hero.score}")

                        # бонус за уничтожение( ускорение перезарядки)
                        self.hero.bullets_count -= 32

                # стрельба по суперастероидам
                for j, superasteroid in enumerate(self.superasteroids):
                    if abs(superasteroid.get_position()[0] - bullet.get_position()[
                        0]) < superasteroid.radius + bullet.radius and abs(
                        superasteroid.get_position()[1] - bullet.get_position()[
                            1]) < superasteroid.radius + bullet.radius:

                        # уничтожение пули и нанесение урона астероиду
                        try:
                            del self.bullets[i]
                        except Exception:
                            pass
                        superasteroid.hp -= self.hero.damage

                        # уничтожение cуперастероида
                        if superasteroid.hp == 0:
                            # выпадение лута с астероидов
                            event = random.randint(0, 100000)

                            # 1 класс
                            if superasteroid.type == 1:
                                if event % 80 == 1:
                                    buff = Buff("LVL UP", superasteroid.get_position())
                                    self.add_buff(buff)
                                elif event % 10 == 1:
                                    buff = Buff("SPEED UP", superasteroid.get_position())
                                    self.add_buff(buff)
                                else:
                                    buff = Buff("HP", superasteroid.get_position())
                                    self.add_buff(buff)
                            # 2 класс
                            elif superasteroid.type == 2:
                                if event % 40 == 1:
                                    buff = Buff("LVL UP", superasteroid.get_position())
                                    self.add_buff(buff)
                                elif event % 5 == 1:
                                    buff = Buff("SPEED UP", superasteroid.get_position())
                                    self.add_buff(buff)
                                else:
                                    buff = Buff("HP", superasteroid.get_position())
                                    self.add_buff(buff)
                            # 3 класс
                            elif superasteroid.type == 3:
                                if event % 4 == 1:
                                    buff = Buff("LVL UP", superasteroid.get_position())
                                    self.add_buff(buff)
                                elif event % 2 == 1:
                                    buff = Buff("SPEED UP", superasteroid.get_position())
                                    self.add_buff(buff)
                                else:
                                    buff = Buff("HP", superasteroid.get_position())
                                    self.add_buff(buff)
                            # 4 класс
                            elif superasteroid.type == 4:
                                if event % 2 == 1:
                                    buff = Buff("LVL UP", superasteroid.get_position())
                                    self.add_buff(buff)
                                elif event % 2 == 1:
                                    buff = Buff("SPEED UP", superasteroid.get_position())
                                    self.add_buff(buff)
                                else:
                                    buff = Buff("HP", superasteroid.get_position())
                                    self.add_buff(buff)
                            # 5 класс
                            elif superasteroid.type == 5:
                                buff = Buff("COMBO", superasteroid.get_position())
                                self.add_buff(buff)

                            # распад суперастероида на 2 меньшего класса
                            if superasteroid.type > 1:
                                self.add_superasteroid(SuperAsteroid(superasteroid.type - 1, superasteroid.get_position()),
                                                        SuperAsteroid(superasteroid.type - 1, superasteroid.get_position()))

                            # получение очков за уничтожение
                            self.hero.score += superasteroid.type * 8

                            # вывод показателя очков
                            print(f"SCORE: {self.hero.score}")
                            # уничтожить суперастероид
                            del self.superasteroids[j]

                            # конец режима суперастеродида
                            if not self.superasteroids:
                                self.superasteroid_status = 2


            # вражеские пули
            else:
                if abs(self.hero.get_position()[0] - bullet.get_position()[0]) < self.hero.radius + bullet.radius \
                        and abs(
                    self.hero.get_position()[1] - bullet.get_position()[1]) < self.hero.radius + bullet.radius:

                    # уничтожение пули
                    self.hero.health -= bullet.damage

                    # снятие здоровья у героя
                    if self.hero.health < 0:
                        self.hero.health = 0
                    del self.bullets[i]

                    # вывод показателя здоровья главного героя в консоль
                    print(f"HEALTH: {self.hero.health}")

    # движение врагов
    def move_enemies(self):
        # просмотр каждого врага по отдельности
        for i, enemy in enumerate(self.enemies):

            # генерация события
            event = random.randint(0, 100000)

            # если атака не активирована
            if enemy.timer == 0:

                # применить ульту
                if event % 150 == 1:
                    # обычный враг
                    if enemy.type != 4:
                        enemy.attack_duration = random.randint(100, 300)
                        enemy.dy = enemy.speed
                        enemy.timer += 1
                    # босс
                    else:
                        # ульта 1 (гернерация врагов) без таймера
                        if event % 1200 == 1:
                            # созадание врагов 3 класса
                            boss_support_1 = Enemy((enemy.get_position()[0] + 10, enemy.get_position()[1]), 3)
                            boss_support_2 = Enemy((enemy.get_position()[0] - 10, enemy.get_position()[1]), 3)
                            boss_support_3 = Enemy((enemy.get_position()[0], enemy.get_position()[1] + 20), 3)
                            self.add_enemy(boss_support_1, boss_support_2, boss_support_3)

                        # запуск ульты 2 (запрет на телепортацию)
                        if event % 1500 == 1:
                            self.hero.locked_teleport = True
                            enemy.timer += 1

                # состояние полной боеготовности
                # удерживание постоянной дистанции до главного героя
                if enemy.get_position()[0] > self.hero.get_position()[0] + enemy.distanse:
                    enemy.dx = -1 * enemy.speed
                else:
                    enemy.dx = enemy.speed

            # ульта у врага
            else:
                # ульта у обычного врага
                if enemy.type != 4:
                    # счетчик времени на атаку
                    enemy.timer += 1

                    # половина атаки
                    if enemy.timer == enemy.attack_duration // 2:
                        # возвращение на исходную позицию
                        enemy.dy = -1 * enemy.speed

                    # прекращение атаки
                    if enemy.timer == enemy.attack_duration:
                        enemy.timer = 0
                        enemy.dy = 0
                # 2 ульта у босса ( запрет на телепортацию)
                else:
                    # счетчик времени на атаку
                    enemy.timer += 1

                    # прекращение ульты
                    if enemy.timer == 600:
                        enemy.timer = 0
                        self.hero.locked_teleport = False

            # увеличение счетчика стрельбы врага
            enemy.kd_counter += 1
            # выстрел врага
            if enemy.kd_counter == enemy.reload:
                self.bullets.append(Bullet(enemy.get_position(), 1, enemy.damage))
                # дополнительные выстрелы у босса
                if enemy.type == 4:
                    self.bullets.append(
                        Bullet((enemy.get_position()[0] - 10, enemy.get_position()[1] + 10), 1, enemy.damage))
                    self.bullets.append(
                        Bullet((enemy.get_position()[0] + 10, enemy.get_position()[1] + 10), 1, enemy.damage))
                    self.bullets.append(
                        Bullet((enemy.get_position()[0] - 20, enemy.get_position()[1] + 20), 1, enemy.damage))
                    self.bullets.append(
                        Bullet((enemy.get_position()[0] + 20, enemy.get_position()[1] + 20), 1, enemy.damage))

                enemy.kd_counter = 0
            # движение врага
            enemy.set_position((enemy.get_position()[0] + enemy.dx, enemy.get_position()[1] + enemy.dy))

            if not (0 <= enemy.get_position()[0] <= WINDOW_WIDTH):
                enemy.dx *= -1

    # движение астероидов
    def move_asteroids(self):
        # просмотр каждого астероида по отдельности
        for i, asteroid in enumerate(self.asteroids):
            # удаление астероида который вышел за пределы экрана
            if not (0 <= asteroid.get_position()[0] <= WINDOW_WIDTH) or not (
                    0 <= asteroid.get_position()[1] <= WINDOW_HEIGHT):
                del self.asteroids[i]
            # столкновение астероида с главным героем
            if abs(asteroid.get_position()[0] - self.hero.get_position()[
                0]) < asteroid.radius + self.hero.radius and abs(
                asteroid.get_position()[1] - self.hero.get_position()[1]) < asteroid.radius + self.hero.radius:
                # уничтожение астероида
                del self.asteroids[i]

                # нанесение урона главному герою
                self.hero.health -= asteroid.hp

                # снятие здоровья у героя
                if self.hero.health < 0:
                    self.hero.health = 0

                # вывод показателя здоровья главного героя в консоль
                print(f"HEALTH: {self.hero.health}")

            # движение астероида
            asteroid.set_position(
                (asteroid.get_position()[0] + asteroid.dx, asteroid.get_position()[1] + asteroid.dy))

    # движение астероидов
    def move_superasteroids(self):
        # просмотр каждого супреастероида по отдельности
        for i, superasteroid in enumerate(self.superasteroids):
            if superasteroid.get_position()[0] > WINDOW_WIDTH - superasteroid.radius or superasteroid.get_position()[0] < superasteroid.radius:
                superasteroid.dx *= -1
            if superasteroid.get_position()[1] > WINDOW_HEIGHT - superasteroid.radius or superasteroid.get_position()[1] < superasteroid.radius:
                superasteroid.dy *= -1

            # просмотр других суперастероидов
            for superasteroid_2 in self.superasteroids:
                if superasteroid != superasteroid_2:
                    # столкновение двух суперастероидов
                    if abs(superasteroid.get_position()[0] - superasteroid_2.get_position()[
                        0]) < superasteroid.radius + superasteroid_2.radius and abs(
                        superasteroid.get_position()[1] - superasteroid_2.get_position()[
                        1]) < superasteroid.radius + superasteroid_2.radius:

                        # отталкивание суперастероидов друг от друга по оси х
                        if superasteroid.get_position()[0] > superasteroid_2.get_position()[0]:
                            superasteroid.dx = abs(superasteroid.dx)
                            superasteroid_2.dx = -abs(superasteroid_2.dx)
                        else:
                            superasteroid.dx = -abs(superasteroid.dx)
                            superasteroid_2.dx = abs(superasteroid_2.dx)

                        # отталкивание суперастероидов друг от друга по оси у
                        if superasteroid.get_position()[1] > superasteroid_2.get_position()[1]:
                            superasteroid.dx = abs(superasteroid.dx)
                            superasteroid_2.dx = -abs(superasteroid_2.dx)
                        else:
                            superasteroid.dx = -abs(superasteroid.dx)
                            superasteroid_2.dx = abs(superasteroid_2.dx)

            # столкновение астероида с главным героем
            if abs(superasteroid.get_position()[0] - self.hero.get_position()[
                0]) < superasteroid.radius + self.hero.radius and abs(
                superasteroid.get_position()[1] - self.hero.get_position()[
                    1]) < superasteroid.radius + self.hero.radius:
                # нанесение урона главному герою
                self.hero.health -= superasteroid.damage

                # снятие здоровья у героя
                if self.hero.health < 0:
                    self.hero.health = 0

                # вывод показателя здоровья главного героя в консоль
                print(f"HEALTH: {self.hero.health}")

            # движение астероида
            superasteroid.set_position(
                (superasteroid.get_position()[0] + superasteroid.dx,
                 superasteroid.get_position()[1] + superasteroid.dy))

    # движение баффов
    def move_buffs(self):
        # просмотр каждого баффа в отдельности
        for i, buff in enumerate(self.buffs):

            # удаление в случае выхода за пределы экрана
            if not (0 <= buff.get_position()[1] <= WINDOW_HEIGHT):
                del self.buffs[i]

            # столкновение баффа с главным героем
            if abs(buff.get_position()[0] - self.hero.get_position()[0]) < buff.radius + self.hero.radius and abs(
                    buff.get_position()[1] - self.hero.get_position()[1]) < buff.radius + self.hero.radius:

                # активация баффа
                # восстановление здоровья
                if buff.type == "HP":
                    # шанс на увеличение максимального кол-ва здоровья
                    event = random.randint(1, 5)
                    if event == 4:
                        self.hero.max_health += 1
                    self.hero.health += 5

                # увеличение уровня( кол-во пуль, скорость стрельбы)
                elif buff.type == "LVL UP":
                    self.hero.lvl += 1
                    print(f"LVL UP")

                # увеличение скорости передвижения
                elif buff.type == "SPEED UP":
                    self.hero.speed += 1
                    print(f"SPEED UP")

                # комбо-бафф
                elif buff.type == "COMBO":
                    self.hero.max_health += 1
                    self.hero.health = self.hero.max_health
                    self.hero.lvl += 1
                    self.hero.speed += 1

                # удалаение баффа
                del self.buffs[i]

            # движение баффа
            if buff.mode == "dinamic":
                buff.set_position(
                    (buff.get_position()[0], buff.get_position()[1] + buff.speed))

    # добавить врага
    def add_enemy(self, *enemies):
        # максимальное количество врагов на экране( увеличивается с возрастанием очков)
        self.max_count_of_enemies = 5 + self.hero.score // 100
        # добавление врагов
        for enemy in enemies:
            # проверка на превышение макс кол-ва
            if len(self.enemies) <= self.max_count_of_enemies:
                # добавить врага
                self.enemies.append(enemy)

    # добавить суперастероид
    def add_superasteroid(self, *superasteroids):
        # цикл по всем переданным суперастероидам
        for superasteroid in superasteroids:
            # добавить суперастероид
            self.superasteroids.append(superasteroid)

    # добавить астероид
    def add_asteroid(self, asteroid):
        self.asteroids.append(asteroid)

    # добавить бафф
    def add_buff(self, buff):
        self.buffs.append(buff)

# показать сообщение
def show_message(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, (255, 20, 147))
    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (30, 144, 255), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def main():
    # переменные изображения спрайтов
    global image_player, images_enemies, image_asteroid, image_bullet, image_bullet_2, image_bg, image_buff, image_superasteroid

    # инитилизация PyGame
    pygame.init()
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    # создание менеджера для элементов интерфейса
    manager = pygame_gui.UIManager((800, 600), 'settings_for_endgame/theme.json')

    # создание кнопки начать игру заново
    try_again_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH // 2 - 75, 480), (150, 40)),
                                                text='Try again',
                                                manager=manager)
    # создание надписи в конце игры "GAME OVER" или "YOU WIN!"
    end_game_label = pygame_gui.elements.UILabel(
        relative_rect=pygame.Rect((WINDOW_WIDTH // 2 - 125, WINDOW_HEIGHT // 2 - 25), (250, 50)),
        text='',
        manager=manager)

    # скрыть кнопку
    try_again_button.hide()

    # часы для менеджера интерфейса
    clock = pygame.time.Clock()
    time_delta = clock.tick(60) / 1000.0

    # создание холста
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # ---------изображение объектов---------
    image_player = pygame.image.load('img/ship-min.png').convert_alpha()
    images_enemies = [
        pygame.image.load('img/shipB1.png').convert_alpha(),  # враг 1 класса(самый слабый)
        pygame.image.load('img/shipB2.png').convert_alpha(),  # враг 2 класса
        pygame.image.load('img/shipB3.png').convert_alpha(),  # враг 3 класса
        pygame.image.load('img/shipB4.png').convert_alpha()  # враг 4 класса (БОСС)
    ]
    image_asteroid = pygame.image.load('img/asteroid.png').convert_alpha()
    image_superasteroid = pygame.image.load('img/superasteroid.png').convert_alpha()
    image_bullet = pygame.image.load('img/bullet_N.png').convert_alpha()
    image_bullet_2 = pygame.image.load('img/bullet_N2.png').convert_alpha()
    image_bg = pygame.image.load("img/bg-min.png").convert_alpha()
    image_buff = pygame.image.load("img/buff.png").convert_alpha()
    # ----------

    # создание главного героя
    hero = Hero((WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))

    # создание фона
    bg = BG((0, 0))

    # создание игры
    game = Game(hero, screen)

    # часы для игры
    clock = pygame.time.Clock()

    # включить игровой цикл
    running = True

    # переменные завершения игры
    gameover = False
    win = False

    # игровой цикл
    while running:
        # обработка событий
        for event in pygame.event.get():
            # закрытие окна
            if event.type == pygame.QUIT:
                running = False
            # нажатие на кнопку try again
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                    event.ui_element == try_again_button):

                # переменные окончания игры
                gameover = False
                win = False

                # дефолтные параметры игрока
                game.hero.health = START_HEALTH
                game.hero.score = 0
                game.hero.lvl = 1
                game.hero.speed = START_SPEED

                # удаление всех объектов
                game.enemies = []
                game.buffs = []
                game.bullets = []
                game.asteroids = []
                game.superasteroids = []
                game.boss_status = 0
                game.superasteroid_status = 0
                try_again_button.hide()

            # менеджер pygame_gui (для интерфейса)
            manager.process_events(event)
            manager.update(time_delta)
            manager.draw_ui(screen)

        # герой жив
        if not gameover:
            if game.hero.health <= 0:
                gameover = True

            # движение всех динамичных объектов
            game.move_bullets()
            game.move_hero()
            game.move_enemies()
            game.move_asteroids()
            game.move_buffs()
            game.move_superasteroids()

            # боссы неактивны
            if game.boss_status != 1 and game.superasteroid_status != 1:
                # генерация события например создание врага
                event = random.randint(0, 100000)
                enemies_generation_time = 101 - (hero.score // 20)
            else:
                # задание неизменяемого события, которое ничего не делает
                event = 11

            # создание босса
            if hero.score >= 300 and game.boss_status == 0 and game.superasteroid_status != 1:
                # удаление всех врагов, астероидов, пуль
                game.enemies = []
                game.buffs = []
                game.bullets = []
                game.asteroids = []

                # добавить босса
                enemy = Enemy((random.randint(0, 600), random.randint(0, 50)), 4)
                game.add_enemy(enemy)
                # включить режим босса
                game.boss_status = 1

            # создание суперастероида
            elif hero.score > 1200 and game.superasteroid_status == 0:
                # удаление всех врагов, астероидов, пуль
                game.enemies = []
                game.buffs = []
                game.bullets = []
                game.asteroids = []

                # добавить суперастероид основатель( 5 класс)
                superasteroid = SuperAsteroid(5)
                game.add_superasteroid(superasteroid)
                # включить режим суперастероида
                game.superasteroid_status = 1

            elif hero.score >= 2000:
                gameover = True
                win = True


            # создание врага 1, 2, 3 класса
            elif event % enemies_generation_time == 1:
                # соотношение классов врагов
                ratio_of_enemies = [enemies_generation_time * 10 - (hero.score // 50) * enemies_generation_time, enemies_generation_time * 4 - (hero.score // 50) * enemies_generation_time]

                # задание минимального значения
                if ratio_of_enemies[0] < enemies_generation_time:
                    ratio_of_enemies[0] = enemies_generation_time
                if ratio_of_enemies[1] < enemies_generation_time:
                    ratio_of_enemies[1] = enemies_generation_time

                # враг 2 класса
                if event % ratio_of_enemies[0] == 1:
                    print(ratio_of_enemies)
                    enemy = Enemy((random.randint(0, 600), random.randint(0, 50)), 3)

                # враг 3 класса
                elif event % ratio_of_enemies[1] == 1:
                    enemy = Enemy((random.randint(0, 600), random.randint(0, 50)), 2)

                # враг 1 класса
                else:
                    enemy = Enemy((random.randint(0, 600), random.randint(0, 50)), 1)

                # добавить врага
                game.add_enemy(enemy)
            # создание астероида
            if event % 100 == 2:
                asteroid = Asteroid()
                game.add_asteroid(asteroid)
            if event % 3000 == 0:
                buff = Buff("HP")
                game.add_buff(buff)

            screen.fill((0, 0, 0))
            # ---- СПРАЙТЫ----
            # начальноне окно

            # применение спрайта фона
            screen.blit(bg.render(screen)[0], bg.render(screen)[1])
            try:
                if game.boss_status == 1:
                    # спрайт lvl
                    game_font_boss_health = pygame.font.Font('settings_for_endgame/pixel_font.ttf', 70)
                    boss_health_surface = game_font_boss_health.render(f'Boss HP: {game.enemies[0].hp}', True, (0, 255, 252))
                    boss_health_rect = boss_health_surface.get_rect(center=(WINDOW_WIDTH - 640, WINDOW_HEIGHT - 40))
                    screen.blit(boss_health_surface, boss_health_rect)
            except IndexError:
                pass

            # спрайт lvl
            game_font_lvl = pygame.font.Font('settings_for_endgame/pixel_font.ttf', 70)
            lvl_surface = game_font_lvl.render(f'lvl: {hero.lvl}', True, (255, 20, 147))
            lvl_rect = lvl_surface.get_rect(center=(WINDOW_WIDTH - 440, WINDOW_HEIGHT - 40))
            screen.blit(lvl_surface, lvl_rect)

            # спрайт fps
            game_font_fps = pygame.font.Font('settings_for_endgame/pixel_font.ttf', 70)
            fps_surface = game_font_fps.render(f'FPS: {int(clock.get_fps())}', True, (0, 255, 252))
            fps_rect = fps_surface.get_rect(center=(70, 40))
            screen.blit(fps_surface, fps_rect)

            # спрайт колво очков
            game_font_score = pygame.font.Font('settings_for_endgame/pixel_font.ttf', 70)
            score_surface = game_font_score.render(f'Score: {hero.score}', True, (0, 255, 252))
            score_rect = score_surface.get_rect(center=(WINDOW_WIDTH - 120, WINDOW_HEIGHT - 40))
            screen.blit(score_surface, score_rect)

            # спрайт здоровье
            game_font_health = pygame.font.Font('settings_for_endgame/pixel_font.ttf', 70)
            health_surface = game_font_health.render(str(hero.health), True, (0, 255, 0))
            health_rect = health_surface.get_rect(center=(WINDOW_WIDTH - 270, WINDOW_HEIGHT - 40))
            screen.blit(health_surface, health_rect)

            image_heart = pygame.image.load('img/heart.png').convert_alpha()
            heart_image = pygame.transform.scale(image_heart, (45, 45))
            heart_rect = heart_image.get_rect(center=(WINDOW_WIDTH - 330, WINDOW_HEIGHT - 40))

            screen.blit(heart_image, heart_rect)

            # применение спрайта для героя
            screen.blit(hero.render(screen)[0], hero.render(screen)[1])

            # применение спрайтов для врагов
            for enemy in game.enemies:
                screen.blit(enemy.render(screen)[0], enemy.render(screen)[1])

            # применение спрайтов для астероидов
            for asteroid in game.asteroids:
                screen.blit(asteroid.render(screen)[0], asteroid.render(screen)[1])

            # применение спрайтов для суперастероидов
            for superasteroid in game.superasteroids:
                screen.blit(superasteroid.render(screen)[0], superasteroid.render(screen)[1])

            # применение спрайтов для пуль
            for bullet in game.bullets:
                screen.blit(bullet.render(screen)[0], bullet.render(screen)[1])
                screen.blit(bullet.render(screen)[0], bullet.render(screen)[1])

            # # применение спрайтов для баффов
            for buff in game.buffs:
                screen.blit(buff.render(screen)[0], buff.render(screen)[1])
                screen.blit(buff.render(screen)[0], buff.render(screen)[1])
            # --------

            # прорисовать все объекты
            game.render(screen)
            clock.tick(FPS)

        # конец игры
        else:
            # проверка на победу
            if win:
                end_game_label.set_text("YOU WIN!")
            else:
                end_game_label.set_text("GAME OVER")

            # показать кнопку попробовать еще
            try_again_button.show()

            # показать надпись
            end_game_label.show()

        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
