import pygame
import pygame_gui
import random
import time

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
FPS = 60
MAX_COUNT_OF_ENEMIES = 5
ENEMY_EVENT_TYPE = 30


# класс главного героя
class Hero(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        # координаты главного героя
        self.x, self.y = position

        # здоровье главного героя
        self.health = 100

        # скорость главного героя
        self.speed = 10

        # количество пуль от игрока на экране
        self.bullets_count = 0

        # наносимый урон
        self.damage = 1

        # уровень игрока
        self.lvl = 1

        # радиус главного героя
        self.radius = 30

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
            size = (60, 70)
        global images_enemiesa
        image_enemy = images_enemies[self.type - 1]

        self.image = pygame.transform.scale(image_enemy, size)
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
        self.buffs = []
        # статус босса(неактивен, создан, побежден)
        self.boss_status = 0

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
            bullet.set_position((bullet.get_position()[0], bullet.get_position()[1] + bullet.direction * 4))
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

            # вражеские пули
            else:
                if abs(self.hero.get_position()[0] - bullet.get_position()[0]) < self.hero.radius + bullet.radius \
                    and abs(self.hero.get_position()[1] - bullet.get_position()[1]) < self.hero.radius + bullet.radius:

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

                # вывод показателя здоровья главного героя в консоль
                print(f"HEALTH: {self.hero.health}")

            # движение астероида
            asteroid.set_position(
                (asteroid.get_position()[0] + asteroid.dx, asteroid.get_position()[1] + asteroid.dy))

    # движение баффов
    def move_buffs(self):
        for i, buff in enumerate(self.buffs):
            if not (0 <= buff.get_position()[1] <= WINDOW_HEIGHT):
                del self.buffs[i]

            # столкновение баффа с главным героем
            if abs(buff.get_position()[0] - self.hero.get_position()[0]) < buff.radius + self.hero.radius and abs(
                    buff.get_position()[1] - self.hero.get_position()[1]) < buff.radius + self.hero.radius:

                # активация баффа
                if buff.type == "HP":
                    self.hero.health = 100
                elif buff.type == "LVL UP":
                    self.hero.lvl += 1
                    print(f"LVL UP")
                elif buff.type == "SPEED UP":
                    self.hero.speed += 1
                    print(f"SPEED UP")

                # удалаение баффа
                del self.buffs[i]

            # движение баффа
            if buff.mode == "dinamic":
                buff.set_position(
                    (buff.get_position()[0], buff.get_position()[1] + buff.speed))

    # добавить врага
    def add_enemy(self, *enemies):
        for enemy in enemies:
            if len(self.enemies) <= MAX_COUNT_OF_ENEMIES:
                self.enemies.append(enemy)

    # добавить астероид
    def add_asteroid(self, asteroid):
        self.asteroids.append(asteroid)

    # добавить бафф
    def add_buff(self, buff):
        self.buffs.append(buff)


def show_message(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, (255,20, 147))
    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (30, 144, 255), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def main():
    global image_player, images_enemies, image_asteroid, image_bullet, image_bullet_2, image_bg, image_buff
    pygame.init()
    manager = pygame_gui.UIManager((800, 600),'settings_for_endgame/theme.json')
    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((WINDOW_WIDTH // 2 - 75, 480), (150, 40)),
                                                text='Try again',
                                                manager=manager)
    # скрыть кнопку
    hello_button.hide()

    clock = pygame.time.Clock()
    time_delta = clock.tick(60) / 1000.0
    screen = pygame.display.set_mode(WINDOW_SIZE)
    # ---------изображение объектов---------
    image_player = pygame.image.load('img/ship-min.png').convert_alpha()

    # !! заменить три последних изображения врага на другие
    images_enemies = [
        pygame.image.load('img/shipB1.png').convert_alpha(),  # враг 1 класса(самый слабый)
        pygame.image.load('img/shipB2.png').convert_alpha(),  # враг 2 класса
        pygame.image.load('img/shipB3.png').convert_alpha(),  # враг 3 класса
        pygame.image.load('img/shipB4.png').convert_alpha()  # враг 4 класса (БОСС)
    ]

    image_asteroid = pygame.image.load('img/asteroid.png').convert_alpha()
    image_bullet = pygame.image.load('img/bullet_N.png').convert_alpha()
    image_bullet_2 = pygame.image.load('img/bullet_N2.png').convert_alpha()
    image_bg = pygame.image.load("img/bg-min.png").convert_alpha()
    image_buff = pygame.image.load("img/buff.png").convert_alpha()
    # ----------

    hero = Hero((WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    bg = BG((0, 0))
    game = Game(hero, screen)

    # часы
    clock = pygame.time.Clock()
    running = True
    # игровой цикл
    while running:

        for event in pygame.event.get():
            # закрытие окна
            if event.type == pygame.QUIT:
                running = False
            if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED and
                    event.ui_element == hello_button):

                game.hero.health = 100
                game.hero.score = 0
                game.hero.lvl = 1
                game.hero.speed = 10

                game.enemies = []
                game.buffs = []
                game.bullets = []
                game.asteroids = []
                game.boss_status = 0
                hello_button.hide()

            manager.process_events(event)

            manager.update(time_delta)


            manager.draw_ui(screen)

        # герой жив
        if game.hero.health > 99:

            # движение всех динамичных объектов
            game.move_bullets()
            game.move_hero()
            game.move_enemies()
            game.move_asteroids()
            game.move_buffs()

            if game.boss_status != 1:
                # генерация события например создание врага
                event = random.randint(0, 100000)
            else:
                event = 11

            # создание врага
            if hero.score >= 10 and game.boss_status == 0:
                # удаление всех врагов, астероидов, пуль
                game.enemies = []
                game.buffs = []
                game.bullets = []
                game.asteroids = []

                # босс
                enemy = Enemy((random.randint(0, 600), random.randint(0, 50)), 4)

                game.add_enemy(enemy)
                game.boss_status = 1
            elif event % 100 == 1:
                # враг 2 класса
                if event % 400 == 1:
                    enemy = Enemy((random.randint(0, 600), random.randint(0, 50)), 2)

                # враг 3 класса
                elif event % 1000 == 1:
                    enemy = Enemy((random.randint(0, 600), random.randint(0, 50)), 3)

                # враг 1 класса
                else:
                    enemy = Enemy((random.randint(0, 600), random.randint(0, 50)), 1)

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
            screen.blit(bg.render(screen)[0], bg.render(screen)[1])
            # применение спрайта для героя
            screen.blit(hero.render(screen)[0], hero.render(screen)[1])
            # применение спрайтов для врагов
            for enemy in game.enemies:
                screen.blit(enemy.render(screen)[0], enemy.render(screen)[1])
            for asteroid in game.asteroids:
                screen.blit(asteroid.render(screen)[0], asteroid.render(screen)[1])
            for bullet in game.bullets:
                screen.blit(bullet.render(screen)[0], bullet.render(screen)[1])
                screen.blit(bullet.render(screen)[0], bullet.render(screen)[1])
            for buff in game.buffs:
                screen.blit(buff.render(screen)[0], buff.render(screen)[1])
                screen.blit(buff.render(screen)[0], buff.render(screen)[1])
            # --------
            game.render(screen)
            clock.tick(FPS)

        # конец игры
        else:
            show_message(screen, f"GAME OVER SCORE: {hero.score}")
            hello_button.show()
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
