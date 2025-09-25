from entities.food.base import BaseFood


class Banana(BaseFood):
    value: int = 2
    ascii_art: str = "🍌"
    chance: int = 0.4
    funny: bool = True
