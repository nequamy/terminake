import curses
from abc import ABC, abstractmethod
from enum import Enum

from game import GameContext


class GameStatesEnum(Enum):
    MENU = "menu"
    GAME = "game"
    PAUSE = "pause"
    SCORE = "score"
    QUIT = "quit"


class BaseState(ABC):
    def __init__(self, context: GameContext):
        self.context = context

    @abstractmethod
    def handle_input(self, key: int): ...

    @abstractmethod
    def update(self): ...

    @abstractmethod
    def render(self, window: "curses.window"): ...

    def on_enter(self) -> None: ...

    def on_exit(self) -> None: ...
