import random
import sys

import pygame

pygame.init()
pygame.font.init()

START_SPEED = 2

display_wight = 1000
display_height = 600

clock = pygame.time.Clock()

display = pygame.display.set_mode((display_wight, display_height))
pygame.display.set_caption('The best cars ever!')


car_wight = 100
car_height = 60
car_x = display_wight // 10
car_y = display_height - car_height - 260
car_image = pygame.image.load('asserts/car.webp')
conus_image = pygame.image.load('asserts/conus.png')
pygame.mixer.music.load('asserts/sound.mp3')

myfont15 = pygame.font.SysFont('Comic Sans MS', 15)


class Car:
    speed = 3

    def __init__(self, x, y, wight, height, image) -> None:
        self.x = x
        self.y = y
        self.wight = wight
        self.height = height
        self.image = image

    def move(self, key_action):
        global display_height

        if key_action[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if key_action[pygame.K_DOWN] and self.y < display_height - self.height:
            self.y += self.speed

    def draw(self, display):
        display.blit(self.image, (self.x, self.y, self.wight, self.height))

    @property
    def rect(self):
        return pygame.Rect(self.x, self.y, self.wight, self.height)


class Obstacle:
    def __init__(
        self,
        x: int,
        y: int,
        wight: int,
        height: int,
        image: pygame.Surface,
        speed: float,
    ) -> None:
        self.x = x
        self.y = y
        self.wight = wight
        self.height = height
        self.image = image
        self.speed = speed

    def move(self) -> bool:
        if self.x >= -self.wight:
            display.blit(self.image, (self.x, self.y, self.wight, self.height))
            self.x -= self.speed
            return True
        self.x = display_wight + 60 + random.randrange(-80, 60)
        self.y = display_height + 60 + random.randrange(-20, 0) * 50
        return False

    def change_speed(self, new_speed: int) -> None:
        self.speed = new_speed
        print(f'new speed: {new_speed}')

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.wight, self.height)


class ObstacleList:
    up_speed_every_sec = 2.5
    up_speed_by = 1.05

    def __init__(self, initial_speed: float) -> None:
        self.obstacles = []
        self.obstacles.append(
            Obstacle(
                display_wight + 20,
                display_height - 170,
                20,
                20,
                conus_image,
                initial_speed,
            ),
        )
        self.obstacles.append(
            Obstacle(
                display_wight + 100,
                display_height - 70,
                20,
                20,
                conus_image,
                initial_speed,
            ),
        )
        self.obstacles.append(
            Obstacle(
                display_wight - 380,
                display_height - 580,
                20,
                20,
                conus_image,
                initial_speed,
            ),
        )
        self.obstacles.append(
            Obstacle(
                display_wight - 100,
                display_height - 270,
                20,
                20,
                conus_image,
                initial_speed,
            ),
        )
        self.obstacles.append(
            Obstacle(
                display_wight - 170,
                display_height - 370,
                20,
                20,
                conus_image,
                initial_speed,
            ),
        )
        self.obstacles.append(
            Obstacle(
                display_wight - 280,
                display_height - 480,
                20,
                20,
                conus_image,
                initial_speed,
            ),
        )
        self.last_speed_update_sec = 0
        self.speed = initial_speed

    def change_speed(self, current_secounds: float) -> None:
        if (
            self.last_speed_update_sec + self.up_speed_every_sec
            < current_secounds
        ):
            self.last_speed_update_sec = current_secounds
            self.speed *= self.up_speed_by
            for obstacle in self.obstacles:
                obstacle.change_speed(self.speed)

    def draw(self) -> None:
        for obstacle in self.obstacles:
            obstacle.move()

    def to_rect(self) -> list:
        return [x.rect for x in self.obstacles]


def run_game():
    game = True
    global car_image
    start_speed = 3
    car = Car(10, 300, 100, 60, car_image)
    obstacles = ObstacleList(start_speed)
    time_seconds = 0
    pygame.mixer.music.play(-1)
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            pause()

        car.move(pygame.key.get_pressed())
        display.fill((255, 255, 255))
        obstacles.draw()
        car.draw(display)
        if car.rect.collidelist(obstacles.to_rect()) >= 0:
            game = False

        time_str = str(int(time_seconds * 10) / 10)
        label = myfont15.render(f'Time : {time_str}', 1, (0, 0, 0))
        display.blit(label, (20, 20))
        label = myfont15.render(f'Speed : {obstacles.speed:.2f}', 1, (0, 0, 0))
        display.blit(label, (20, 40))
        pygame.display.update()
        time_millis = clock.tick(60)
        if game:
            time_seconds += time_millis / 1000
            obstacles.change_speed(time_seconds)

    return game_over()


def print_text(
    message: str,
    x: int,
    y: int,
) -> None:
    font_type = pygame.font.Font(None, 30)
    text = font_type.render(message, False, (0, 180, 0))
    display.blit(text, (x, y))


def pause() -> None:
    paused = True
    pygame.time.wait(100)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        print_text('Нажми Enter для продолжения игры!', 160, 300)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            paused = False

        pygame.display.update()
        clock.tick(15)


def game_over():
    stoped = True
    while stoped:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        print_text(
            'Игра окончена. Нажми enter, '
            'чтобы сыграть заново или Esc, чтобы выйти.',
            160,
            300,
        )
        if pygame.key.get_pressed()[pygame.K_RETURN]:
            return True
        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            return False
        pygame.display.update()
        clock.tick(15)


if __name__ == '__main__':
    while True:
        if not run_game():
            pygame.quit()
            quit()
