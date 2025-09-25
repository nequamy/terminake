from entities.food.base import BaseFood


class Bomb(BaseFood):
    value: int = -1
    ascii_art: str = "💣"
    chance: int = 0.1
