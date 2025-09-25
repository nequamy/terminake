from entities.food.base import BaseFood


class Coffee(BaseFood):
    value: int = 0
    ascii_art: str = "☕️"
    chance: int = 0.25
