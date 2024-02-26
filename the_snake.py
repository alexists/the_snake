from random import choice, randint
import pytest_timeout

import pygame


# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

SCREEN_CENTER = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Это базовый класс, от которого наследуются другие игровые объекты"""

    def __init__(self, body_color=APPLE_COLOR or SNAKE_COLOR) -> None:
        """Инициализирует базовые атрибуты объекта"""
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        """Это абстрактный метод, который предназначен"""
        """для переопределения в дочерних классах"""
        """как объект будет отрисовываться на экране."""
        pass


class Snake(GameObject):
    """Создание класса змейка"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.body_color = body_color
        self.length = 1

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Обновляет позицию змейки"""
        self.head_position = self.get_head_position()
        self.new_head_position = ((self.head_position[0] + self.direction[0]
                                  * GRID_SIZE) % SCREEN_WIDTH,
                                  (self.head_position[1] + self.direction[1]
                                  * GRID_SIZE) % SCREEN_HEIGHT
                                  )
        if self.new_head_position in self.positions[1:]:
            self.reset()
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.positions.insert(0, self.new_head_position)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def draw(self, surface):
        """Отрисовка змейки"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сброс змейки в начальное состояние"""
        self.length = 1
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


class Apple(GameObject):
    """Класс описывающий яблоко и действия с ним."""

    def __init__(self, body_color=APPLE_COLOR):
        """Задаёт цвет яблока и вызывает метод,"""
        """чтобы установить начальную позицию."""
        super().__init__(body_color)
        self.body_color = body_color
        self.position = self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле"""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Управление змейкой"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры"""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.position = apple.randomize_position()

        apple.draw(screen)
        snake.draw(screen)
        snake.move()
        snake.update_direction()

        pygame.display.update()


if __name__ == "__main__":
    main()
