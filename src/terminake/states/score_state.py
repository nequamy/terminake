import curses

from game import GameContext

from states.base_state import BaseState, GameStatesEnum


class ScoreState(BaseState):
    _score_art: list = [
        "███████╗ ██████╗ ██████╗ ██████╗ ███████╗",
        "██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝",
        "███████╗██║     ██║   ██║██████╔╝█████╗",
        "╚════██║██║     ██║   ██║██╔══██╗██╔══╝",
        "███████║╚██████╗╚██████╔╝██║  ██║███████╗",
        "╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝",
    ]

    _0_art: list = [
        "  ██████╗  ",
        " ██╔═████╗ ",
        " ██║██╔██║ ",
        " ████╔╝██║ ",
        " ╚██████╔╝ ",
        "  ╚═════╝  ",
    ]
    _1_art: list = ["  ██╗ ", " ███║ ", " ╚██║ ", "  ██║ ", "  ██║ ", "  ██║ "]
    _2_art: list = [
        " ██████╗  ",
        " ╚════██╗ ",
        " █████╔╝  ",
        " ██╔═══╝  ",
        " ███████╗ ",
        " ╚══════╝ ",
    ]
    _3_art: list = [
        " ██████╗  ",
        " ╚════██╗ ",
        " █████╔╝  ",
        " ╚═══██╗  ",
        " ██████╔╝ ",
        " ╚═════╝  ",
    ]
    _4_art: list = [
        " ██╗  ██╗ ",
        " ██║  ██║ ",
        " ███████║ ",
        " ╚════██║ ",
        "      ██║ ",
        "      ╚═╝ ",
    ]
    _5_art: list = [
        " ███████╗ ",
        " ██╔════╝ ",
        " ███████╗ ",
        " ╚════██║ ",
        " ███████║ ",
        " ╚══════╝ ",
    ]
    _6_art: list = [
        "  ██████╗  ",
        " ██╔════╝  ",
        " ███████╗  ",
        " ██╔═══██╗ ",
        " ╚██████╔╝ ",
        "  ╚═════╝  ",
    ]
    _7_art: list = [
        " ███████╗ ",
        " ╚════██║ ",
        "    ██╔╝  ",
        "   ██╔╝   ",
        "  ██║     ",
        "  ╚═╝     ",
    ]
    _8_art: list = [
        "  █████╗  ",
        " ██╔══██╗ ",
        " ╚█████╔╝ ",
        " ██╔══██╗ ",
        " ╚█████╔╝ ",
        "  ╚════╝  ",
    ]
    _9_art: list = [
        "  █████╗  ",
        " ██╔══██╗ ",
        " ╚██████║ ",
        "  ╚═══██║ ",
        "  █████╔╝ ",
        "  ╚════╝  ",
    ]

    _hint_art: list = [
        "░█▀█░█▀▄░█▀▀░█▀▀░█▀▀░░░▄▀▄░░░█▀█░█▀▄░░░▄▀▄░░░█▀▀░█▀█░█▀▄░░░█▄█░█▀▀░█▀█░█░█",
        "░█▀▀░█▀▄░█▀▀░▀▀█░▀▀█░░░█\█░░░█░█░█▀▄░░░█\█░░░█▀▀░█░█░█▀▄░░░█░█░█▀▀░█░█░█░█",
        "░▀░░░▀░▀░▀▀▀░▀▀▀░▀▀▀░░░░▀\░░░▀▀▀░▀░▀░░░░▀\░░░▀░░░▀▀▀░▀░▀░░░▀░▀░▀▀▀░▀░▀░▀▀▀",
    ]

    def handle_input(self, key: int):
        if key == ord("q") or key == ord("Q"):
            return GameStatesEnum.MENU

    def update(self) -> None:
        return None

    def render(self, window: "curses.window"):
        window.clear()
        window.border()

        max_y, max_x = window.getmaxyx()

        # ASCII Score Logo Output
        pos_x: int = (max_x - len(self._score_art[0])) // 2
        pos_y: int = (max_y // 3) - len(self._score_art)
        for i in range(len(self._score_art)):
            pos_y += 1
            window.addstr(pos_y, pos_x, self._score_art[i], curses.A_BOLD)

        score_str = str(self.context.score)
        pos_y += 3
        for i in range(len(score_str)):
            num = self.__getattribute__("_{key}_art".format(key=score_str[i]))
            pos_x = (max_x - len(num[0])) // 2
            for line_idx, line in enumerate(num):
                window.addstr(pos_y + line_idx, pos_x, line, curses.A_BOLD)

        pos_y += 10
        pos_x = (max_x - len(self._hint_art[0])) // 2
        for i in range(len(self._hint_art)):
            window.addstr(pos_y + i, pos_x, self._hint_art[i], curses.A_BOLD)
