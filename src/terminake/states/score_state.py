import curses

from game import GameContext

from states.base_state import BaseState, GameStatesEnum


class ScoreState(BaseState):
    def handle_input(self, key: int):
        if key == ord("q") or key == ord("Q"):
            return GameStatesEnum.MENU

    def update(self) -> None:
        return None

    def render(self, window: "curses.window"):
        window.clear()
        window.border()

        max_y, max_x = window.getmaxyx()

        window.addstr(10, 10, "SCORE: {score}".format(score=self.context.score))
        window.addstr(11, 10, "Press Q or q to out")
