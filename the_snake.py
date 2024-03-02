from random import choice, randint

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

    def __init__(self, body_color=None) -> None:
        """Инициализирует базовые атрибуты объекта"""
        self.position = SCREEN_CENTER
        self.body_color = body_color

    def draw(self):
        """Это абстрактный метод для переопределения в дочерних классах"""

    def draw_cell(self, position, body_color=None):
        """Отрисовывает одну ячейку"""
        if body_color is not None:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        else:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, rect)


class Snake(GameObject):
    """Создание класса змейка"""

    def __init__(self, body_color=SNAKE_COLOR):
        super().__init__(body_color)
        super().draw_cell(self.position, body_color)
        self.positions = [self.position]
        self.last = None
        self.direction = RIGHT
        self.next_direction = None
        self.length = 5
        self.reset()

    def update_direction(self, next_direction):
        """Обновляет направление движения змейки"""
        if next_direction:
            self.direction = next_direction
            next_direction = None

    def move(self):
        """Обновляет позицию змейки"""
        x_head, y_head = self.get_head_position()
        new_head_position = ((x_head + self.direction[0]
                              * GRID_SIZE) % SCREEN_WIDTH,
                             (y_head + self.direction[1]
                              * GRID_SIZE) % SCREEN_HEIGHT)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.positions.insert(0, new_head_position)

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def draw(self):
        """Отрисовка змейки"""
        # Отрисовка головы
        self.draw_cell(self.positions[0], self.body_color)

        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last)

    def reset(self):
        """Сброс змейки в начальное состояние"""
        self.length = 15
        self.positions = [SCREEN_CENTER]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])


class Apple(GameObject):
    """Класс описывающий яблоко и действия с ним."""

    def __init__(self, body_color=APPLE_COLOR):
        """Задаёт цвет яблока и вызывает метод,"""
        """чтобы установить начальную позицию."""
        super().__init__(body_color)
        self.position = self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле"""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        self.draw_cell(self.position, self.body_color)


def handle_keys(game_object):
    """Управление змейкой"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
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
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()

        snake.move()
        apple.draw()
        snake.draw()

        snake.update_direction(snake.next_direction)
        if snake.positions[0] in snake.positions[3:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        pygame.display.update()


if __name__ == "__main__":
    main()
