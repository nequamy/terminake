from entities.food.base import BaseFood


class Strawberry(BaseFood):
    value: int = 1
    ascii_art: str = "🍓"
    chance: int = 1
