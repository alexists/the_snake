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

    def __init__(self, position=None, body_color=None) -> None:
        """Инициализирует базовые атрибуты объекта"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Это абстрактный метод для переопределения в дочерних классах"""

    def draw_cell(self, position, body_color=None):
        """Отрисовывает одну ячейку"""
        rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
        if body_color is None:
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        else:
            pygame.draw.rect(screen, body_color, rect)


class Snake(GameObject):
    """Создание класса змейка"""

    def __init__(self, position=SCREEN_CENTER, body_color=SNAKE_COLOR):
        super().__init__(position, body_color)
        self.last = None
        self.reset()

    def update_direction(self, next_direction):
        """Обновляет направление движения змейки"""
        self.direction = next_direction

    def move(self):
        """Обновляет позицию змейки"""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head_position = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def draw(self):
        """Отрисовка змейки"""
        # Отрисовка головы
        self.draw_cell(self.positions[0])
        # Затирание последнего сегмента
        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def reset(self):
        """Сброс змейки в начальное состояние"""
        self.length = 1
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.positions = [SCREEN_CENTER]


class Apple(GameObject):
    """Класс описывающий яблоко и действия с ним."""

    def __init__(self, position=SCREEN_CENTER, body_color=APPLE_COLOR):
        """Задаёт цвет яблока и вызывает метод,"""
        """чтобы установить начальную позицию."""
        super().__init__(position, body_color)
        self.randomize_position()

    def randomize_position(self, block_grid=[SCREEN_CENTER]):
        """Устанавливает случайное положение яблока на игровом поле"""
        cor_x, cor_y = self.position

        while (cor_x, cor_y) in block_grid:
            cor_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            cor_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = cor_x, cor_y

    def draw(self):
        """Отрисовывает яблоко на игровой поверхности"""
        self.draw_cell(self.position)


def handle_keys(game_object):
    """Управление змейкой"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Основной цикл игры"""
    snake = Snake()
    apple = Apple(SCREEN_CENTER)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        snake.move()
        if snake.positions[0] in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        apple.draw()
        snake.draw()

        pygame.display.update()


if __name__ == "__main__":
    main()
