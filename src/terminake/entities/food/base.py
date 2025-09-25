import random
from typing import List


class BaseFood:
    value: int = 0
    ascii_art: str = ""
    chance: int = 1
    pos: List[int] = (0, 0)

    def __init__(self, max_y, max_x, min_y, min_x) -> None:
        self.min = (min_x, min_y)
        self.max = (max_x, max_y)

    def generate(self) -> tuple:
        self.pos = [
            random.randint(self.min[0], self.max[0]),
            random.randint(self.min[1], self.max[1]),
        ]

        if self.pos[0] % 2:
            self.pos[0] -= 1

    def get_chance(self) -> bool:
        if random.random() < self.chance:
            return True

        return False
