import curses
import random
from typing import Dict, Optional, Tuple

from entities import Banana, BaseFood, Bomb, Coffee, Snake, Strawberry
from game import GameContext

from states.base_state import BaseState, GameStatesEnum


class GameState(BaseState):
    _head_oriented_chars: Dict[Tuple[int], str] = {
        (2, 0): "►",  # вправо
        (-2, 0): "◄",  # влево
        (0, -1): "▲",  # вверх
        (0, 1): "▼",  # вниз
    }
    _body_char: str = "■"
    _curr_food: Optional[BaseFood] = None
    _collision = False

    def __init__(self, context: GameContext):
        super().__init__(context)
        curses.init_pair(1, curses.COLOR_YELLOW, -1)

    def handle_input(self, key: int) -> Optional[GameStatesEnum]:
        if key == ord("p") or key == ("P"):
            return GameStatesEnum.PAUSE
        elif key == ord("q") or key == ("Q"):
            return GameStatesEnum.MENU
        elif key == curses.KEY_UP:
            self.context.snake.up()
        elif key == curses.KEY_DOWN:
            self.context.snake.down()
        elif key == curses.KEY_RIGHT:
            self.context.snake.right()
        elif key == curses.KEY_LEFT:
            self.context.snake.left()

    def update(self) -> Optional[GameStatesEnum]:
        self.context.snake.move()
        self.context.score = self.context.snake.get_score()

        if self._curr_food is None:
            self._generate_food()

        if (
            self._curr_food
            and tuple(self._curr_food.pos) == self.context.snake.get_head()
        ):
            self._collision = True
            self.context.snake.eat(self._curr_food)
            self._generate_food()

        if self._is_game_over():
            return GameStatesEnum.SCORE

        return None

    def _is_game_over(self) -> bool:
        max_x: int = self.context.max_x
        max_y: int = self.context.max_y

        head_x, head_y = self.context.snake.get_head()
        if head_x >= max_x or head_y >= max_y or head_x <= 0 or head_y <= 0:
            return True

        if self.context.snake.get_head() in self.context.snake.get_body():
            return True

        return False

    def _generate_food(self):
        selectable = [Bomb, Banana, Coffee]

        food: BaseFood = random.choice(selectable)(
            self.context.max_y - 5, self.context.max_x - 5, 5, 5
        )

        # если не сгенерилось то выплевываем клубничку
        if not food.get_chance():
            food: BaseFood = Strawberry(
                self.context.max_y - 5, self.context.max_x - 5, 5, 5
            )

        food.generate()

        self._curr_food = food

    def render(self, window: "curses.window") -> None:
        window.clear()
        window.border()
        window.addstr(
            0, 2, "  Score: {score}  ".format(score=self.context.score), curses.A_BOLD
        )
        window.addstr(
            0,
            15,
            "  Snake lenght: {x} ".format(x=self.context.snake.get_score()),
            curses.A_BOLD,
        )

        head: str = self._head_oriented_chars[self.context.snake.direction]
        head_x, head_y = self.context.snake.get_head()
        window.addstr(
            head_y,
            head_x,
            head,
            (curses.A_BOLD)
            if not self.context.snake.get_fun()
            else (curses.color_pair(1) | curses.A_BOLD),
        )

        body = self.context.snake.get_body()

        for i, coords in enumerate(body):
            if self.context.snake.get_fun():
                window.addstr(
                    coords[1],
                    coords[0],
                    self._body_char,
                    curses.color_pair(1) | curses.A_BOLD,
                )
            else:
                window.addstr(coords[1], coords[0], self._body_char, curses.A_BOLD)

        window.addstr(
            self._curr_food.pos[1], self._curr_food.pos[0], self._curr_food.ascii_art
        )

    def on_enter(self):
        self.context.reset_game_state()
        if not self.context.snake:
            self.context.snake = Snake(10, 10)
