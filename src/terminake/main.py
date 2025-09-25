import curses
import time

from game import GameContext, GameManager
from states import GameStatesEnum


def main(stdscr) -> None:
    curses.echo(False)
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    stdscr.nodelay(True)

    max_y, max_x = stdscr.getmaxyx()
    win: curses.window = curses.newwin(max_y - 2, max_x - 4, 1, 2)

    context = GameContext(max_y, max_x)
    game_manager = GameManager(GameStatesEnum.MENU, context)

    while True:
        key = stdscr.getch()
        if not game_manager.handle_input(key):
            break

        if not game_manager.update():
            break

        game_manager.render(win)
        win.refresh()
        stdscr.refresh()

        time.sleep(1 / 60)


if __name__ == "__main__":
    curses.wrapper(main)
