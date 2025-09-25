from entities.food.base import BaseFood


class Coffee(BaseFood):
    value: int = 0
    ascii_art: str = "☕️"
    speed_up: int = 0.85
    chance: int = 0.25
