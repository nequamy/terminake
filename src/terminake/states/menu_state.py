import curses
import subprocess
from typing import List, Optional

from game import GameContext

from states.base_state import BaseState, GameStatesEnum


def detect_terminal_theme() -> Optional[str]:
    try:
        result: subprocess.CompletedProcess[str] = subprocess.run(
            ["defaults", "read", "-g", "AppleInterfaceStyle"],
            capture_output=True,
            text=True,
            timeout=2,
        )

        if result.returncode == 0 and "dark" in result.stdout.lower():
            return "dark"
        else:
            return "light"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass


class MenuState(BaseState):
    _ascii_logo: List[str] = [
        "████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗  ██╗███████╗",
        "╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║ ██╔╝██╔════╝",
        "   ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║█████╔╝ █████╗",
        "   ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██╔═██╗ ██╔══╝",
        "   ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║██║  ██╗███████╗",
        "   ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝",
    ]
    _start_logo: List[str] = [
        "░█▀▀░▀█▀░█▀█░█▀▄░▀█▀",
        "░▀▀█░░█░░█▀█░█▀▄░░█░",
        "░▀▀▀░░▀░░▀░▀░▀░▀░░▀░",
    ]
    _quit_logo: str = [
        "░▄▀▄░█░█░▀█▀░▀█▀",
        "░█\█░█░█░░█░░░█░",
        "░░▀\░▀▀▀░▀▀▀░░▀░",
    ]

    _selectable_color: int = (
        curses.COLOR_GREEN if detect_terminal_theme() == "dark" else curses.COLOR_BLACK
    )

    def __init__(self, context: GameContext) -> None:
        super().__init__(context)
        self._selected_item = 0  # 0 - start, 1 - quit
        self._color_initialized = False

    def _initialize_color(self) -> None:
        if not self._color_initialized and curses.has_colors():
            curses.start_color()

            theme: str | None = detect_terminal_theme()
            if theme == "dark":
                curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)  # default
                curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # selected
            else:
                curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # default
                curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)  # selected

            self._color_initialized = True

    def handle_input(self, key: int) -> Optional[GameStatesEnum]:
        if key == curses.KEY_UP and self._selected_item > 0:
            self._selected_item -= 1
        elif key == curses.KEY_DOWN and self._selected_item < 1:
            self._selected_item += 1
        elif key == ord("\n") or key == ord(" ") or key == curses.KEY_ENTER:
            if self._selected_item == 0:
                return GameStatesEnum.GAME
            elif self._selected_item == 1:
                return GameStatesEnum.QUIT

    def update(self) -> None:
        return None

    def render(self, window: "curses.window") -> None:
        self._initialize_color()

        window.clear()
        window.border()

        max_y, max_x = window.getmaxyx()

        # ASCII logo output
        pos_x: int = (max_x - len(self._ascii_logo[0])) // 2
        pos_y: int = (max_y // 3) - len(self._ascii_logo)
        for i in range(len(self._ascii_logo)):
            pos_y += 1
            window.addstr(pos_y, pos_x, self._ascii_logo[i])

        # START logo output
        pos_y += 3
        pos_x = (max_x - len(self._start_logo[0])) // 2
        for i in range(len(self._start_logo)):
            pos_y += 1
            window.addstr(
                pos_y,
                pos_x,
                self._start_logo[i],
                curses.color_pair(1 if self._selected_item == 1 else 2),
            )

        # QUIT logo output
        pos_y += 1
        pos_x = (max_x - len(self._quit_logo[0])) // 2
        for i in range(len(self._quit_logo)):
            pos_y += 1
            window.addstr(
                pos_y,
                pos_x,
                self._quit_logo[i],
                curses.color_pair(1 if self._selected_item == 0 else 2),
            )

        window.addstr(max_y - 2, 2, "Author: @nequamy")
