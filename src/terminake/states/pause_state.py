import curses

from game import GameContext

from states.base_state import BaseState


class PauseState(BaseState):
    def handle_input(self, key: int):
        pass

    def update(self):
        pass

    def render(self, window: "curses.window"):
        pass
