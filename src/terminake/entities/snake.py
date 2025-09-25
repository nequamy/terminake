import curses
import time
from turtle import speed
from typing import List, Tuple

from entities.food import BaseFood


class Snake:
    def __init__(self, y: int, x: int) -> None:
        self._length = 3

        # Direction types:
        # (0, 1) - to up
        # (0, -1) - to down
        # (2, 0) - to right
        # (-2, 0) - to left
        self.direction = (2, 0)

        self.pos = [(x, y - i) for i in range(self._length)]
        self.grow = 0

        self._coffee_speed_up = 1
        self._fun_coef = False

        self._base_speed = 0.2
        self._speed_up_coef = 0.95
        self._prev_time = time.time()

    def eat(self, food: BaseFood) -> None:
        self._length += food.value
        self.grow += food.value

        if hasattr(food, "speed_up"):
            self._speed_up_coef = food.speed_up
        else:
            self._speed_up_coef = 1

        if hasattr(food, "funny"):
            self._fun_coef = True
        else:
            self._fun_coef = False

    def up(self) -> None:
        if self.direction != (0, 1):
            self.direction = (0, -1)

    def down(self) -> None:
        if self.direction != (0, -1):
            self.direction = (0, 1)

    def right(self) -> None:
        if self.direction != (-2, 0):
            self.direction = (2, 0)

    def left(self) -> None:
        if self.direction != (2, 0):
            self.direction = (-2, 0)

    def move(self) -> None:
        if time.time() - self._prev_time <= (
            self._base_speed
            * (self._speed_up_coef ** self.get_score())
            / self._coffee_speed_up
        ):
            return None

        self._prev_time = time.time()
        head_y, head_x = self.get_head()
        new_head: Tuple[int] = (
            head_y + self.direction[0],
            head_x + self.direction[1],
        )

        self.pos.insert(0, new_head)

        if self.grow > 0:
            self.grow -= 1
        else:
            self.pos.pop()
            if self.grow < 0:
                self.pos.pop()
                self.grow += 1

    def get_head(self) -> Tuple[int]:
        return self.pos[0]

    def get_body(self) -> List[Tuple[int]]:
        return self.pos[1:]

    def get_score(self) -> int:
        return self._length - 3

    def get_fun(self) -> int:
        return self._fun_coef
