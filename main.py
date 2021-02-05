import pygame
import random

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 800
FPS = 60
MAX_COUNT_OF_ENEMIES = 5
ENEMY_EVENT_TYPE = 30


# класс главного героя
class Hero(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = position
        self.health = 100
        self.bullets_count = 0
        self.damage = 1

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), 12)


# класс пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, position, direction, damage):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = position
        self.direction = direction

        # наносимый урон
        self.damage = damage

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        if self.direction == -1:
            pygame.draw.circle(screen, (0, 0, 255), (self.x, self.y), 5)
        else:
            pygame.draw.circle(screen, (255, 0, 255), (self.x, self.y), 5)


# класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y = position
        self.direction = 1

        # счетчик для выстрела
        self.kd_counter = 0

        # продолжительность перезарядки
        self.reload = random.randint(15, 45)

        # здоровье врага
        self.hp = 1

        # наносимый урон
        self.damage = 1

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), 12)


# класс астероида
class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # координаты астероида
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = 0

        # изменение координат за один цикл
        self.dx = random.randint(-10, 10)
        self.dy = random.randint(1, 10)

        # здоровье астероида
        self.hp = random.randint(1, 4)

    # получить координату
    def get_position(self):
        return self.x, self.y

    # установить координату
    def set_position(self, position):
        self.x, self.y = position

    # отрисовка
    def render(self, screen):
        pygame.draw.circle(screen, (110, 110, 110), (self.x, self.y), (self.hp+2) * 5)


# класс игры
class Game:
    def __init__(self, hero):
        self.hero = hero
        self.bullets = []
        self.enemies = []
        self.asteroids = []

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

    # движение главного геро7я
    def move_hero(self):
        # импорт текущих координат из класса hero
        next_x, next_y = self.hero.get_position()
        if next_x < 0:
            next_x = WINDOW_WIDTH
        if next_x > WINDOW_WIDTH:
            next_x = 0
        if pygame.key.get_pressed()[pygame.K_a]:
            next_x -= 10
        if pygame.key.get_pressed()[pygame.K_d]:
            next_x += 10
        if pygame.key.get_pressed()[pygame.K_w] and self.hero.get_position()[1] > 10:
            next_y -= 10
        if pygame.key.get_pressed()[pygame.K_s] and self.hero.get_position()[1] < WINDOW_HEIGHT - 10:
            next_y += 10
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            if self.hero.bullets_count < 20:
                self.bullets.append(Bullet((next_x, next_y), -1, self.hero.damage))
                self.hero.bullets_count += 1
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
                    if abs(enemy.get_position()[0] - bullet.get_position()[0]) < 10 and abs(
                            enemy.get_position()[1] - bullet.get_position()[1]) < 10:
                        # уничтожение пули и нанесение урона врагу
                        del self.bullets[i]
                        enemy.hp -= self.hero.damage

                        # уничтожение астероида
                        if enemy.hp == 0:
                            del self.enemies[j]
                        # увеличение счетчика пуль главного героя
                        self.hero.bullets_count -= 1
                # стрельба по астероидам
                for j, asteroid in enumerate(self.asteroids):
                    if abs(asteroid.get_position()[0] - bullet.get_position()[0]) < 10 and abs(
                            asteroid.get_position()[1] - bullet.get_position()[1]) < 10:
                        # уничтожение пули и нанесение урона астероиду
                        del self.bullets[i]
                        asteroid.hp -= self.hero.damage

                        # уничтожение астероида
                        if asteroid.hp == 0:
                            del self.asteroids[j]
                        # увеличение счетчика пуль главного героя
                        self.hero.bullets_count -= 1
            # вражеские пули
            else:
                if abs(self.hero.get_position()[0] - bullet.get_position()[0]) < 10 and abs(
                        self.hero.get_position()[1] - bullet.get_position()[1]) < 10:
                    # cнятие здоровья у героя и уничтожение пули
                    self.hero.health -= bullet.damage
                    if self.hero.health < 0:
                        self.hero.health = 0
                    del self.bullets[i]
                    print(f"HEALTH: {self.hero.health}")

    # движение врагов
    def move_enemies(self):
        # просмотр каждого врага по отдельности
        for i, enemy in enumerate(self.enemies):
            # движение от одной части экрана к другой
            if enemy.get_position()[0] > WINDOW_WIDTH:
                enemy.direction = -1
            elif enemy.get_position()[0] < 0:
                enemy.direction = 1
            # увеличение счетчика стрельбы врага
            enemy.kd_counter += 1
            # выстрел врага
            if enemy.kd_counter == enemy.reload:
                self.bullets.append(Bullet(enemy.get_position(), 1, enemy.damage))
                enemy.kd_counter = 0
            # движение врага
            enemy.set_position((enemy.get_position()[0] + enemy.direction * 3, enemy.get_position()[1]))

    # движение астероидов
    def move_asteroids(self):
        # просмотр каждого астероида по отдельности
        for i, asteroid in enumerate(self.asteroids):
            # удаление астероида который вышел за пределы экрана
            if not (0 <= asteroid.get_position()[0] <= WINDOW_WIDTH) or not (
                    0 <= asteroid.get_position()[1] <= WINDOW_HEIGHT):
                del self.asteroids[i]
            # столкновение астероида с главным героем
            if abs(asteroid.get_position()[0] - self.hero.get_position()[0]) < (asteroid.hp+2)* 5 and abs(
                            asteroid.get_position()[1] - self.hero.get_position()[1]) < (asteroid.hp+2)* 5:
                # уничтожение астероида и нанесение урона главному герою
                del self.asteroids[i]
                self.hero.health -= asteroid.hp
                print(f"HEALTH: {self.hero.health}")
            # движение астероида
            asteroid.set_position(
                (asteroid.get_position()[0] + asteroid.dx, asteroid.get_position()[1] + asteroid.dy))

    # добавить врага
    def add_enemy(self, enemy):
        if len(self.enemies) <= MAX_COUNT_OF_ENEMIES:
            self.enemies.append(enemy)

    # добавить астероид
    def add_asteroid(self, asteroid):

        self.asteroids.append(asteroid)

    #
    # def check_win(self):
    #     return self.labyrinth.get_tile_id(self.hero.get_position()) == self.labyrinth.finish_tile
    # def check_lose(self):
    #     return self.hero.get_position() == self.enemy.get_position()


#
def show_message(screen, message):
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, (50, 70, 0))
    text_x = WINDOW_WIDTH // 2 - text.get_width() // 2
    text_y = WINDOW_HEIGHT // 2 - text.get_height() // 2
    text_w = text.get_width()
    text_h = text.get_height()
    pygame.draw.rect(screen, (200, 150, 50), (text_x - 10, text_y - 10, text_w + 20, text_h + 20))
    screen.blit(text, (text_x, text_y))


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    # all_sprites = pygame.sprite.Group()
    hero = Hero((WINDOW_SIZE[0] // 2, WINDOW_SIZE[1] // 2))
    game = Game(hero)
    # all_sprites.add(labyrinth)
    # all_sprites.add(hero)
    # all_sprites.add(enemy)
    clock = pygame.time.Clock()
    counter = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # герой жив
        if game.hero.health > 99:
            pass
        if game.hero.health > 0:
            game.move_bullets()
            game.move_hero()

            game.move_enemies()
            game.move_asteroids()
            # print(counter)
            event = random.randint(0, 100)
            if event == 1:
                enemy = Enemy((random.randint(0, 600), random.randint(0, 50)))
                game.add_enemy(enemy)
            elif event == 2:
                asteroid = Asteroid()
                game.add_asteroid(asteroid)
            # if counter % 100 == 0:
            #     counter = 0
            #     enemy = Enemy((random.randint(0, 600), random.randint(0, 50)))
            #     game.add_enemy(enemy)
            screen.fill((0, 0, 0))
            game.render(screen)
            clock.tick(FPS)
            counter += 1
        # конец игры
        else:
            show_message(screen, "GAME OVER")
        # Обновление
        # all_sprites.update()
        # for sprite in all_sprites:
        #     sprite.x -= 5
        # if game.check_win():
        #     game_over = True
        #     show_message(screen, "YOU WON!")
        # elif game.check_lose():
        #     game_over = True
        #     show_message(screen, "YOU LOST!")
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
