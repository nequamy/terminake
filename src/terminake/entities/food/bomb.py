from entities.food.base import BaseFood


class Bomb(BaseFood):
    value: int = -1
    ascii_art: str = "💣"
    speed_up: float = 1.1
    chance: int = 0.1
