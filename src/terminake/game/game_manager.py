from typing import Dict, Optional

from states import (
    BaseState,
    GameState,
    GameStatesEnum,
    MenuState,
    PauseState,
    ScoreState,
)

from game import GameContext


class GameManager:
    def __init__(self, initial_state: GameStatesEnum, context: GameContext) -> None:
        self.context: GameContext = context
        self.current_state_enum: GameStatesEnum = initial_state

        self.current_state: Optional[BaseState] = None
        self.previous_state_enum: Optional[GameStatesEnum] = None

        self.states: Dict[GameStatesEnum, type] = {
            GameStatesEnum.MENU: MenuState,
            GameStatesEnum.GAME: GameState,
            GameStatesEnum.SCORE: ScoreState,
            GameStatesEnum.PAUSE: PauseState,
        }

        self._transition_to_state(initial_state)

    def _transition_to_state(self, state: GameStatesEnum):
        if self.current_state:
            self.current_state.on_exit()

        self.previous_state_enum = self.current_state_enum
        self.current_state_enum = state

        if state in self.states:
            state_class: type = self.states[state]
            self.current_state = state_class(self.context)
            self.current_state.on_enter()

    def handle_input(self, key: int) -> bool:
        if self.current_state:
            new_state = self.current_state.handle_input(key)
            if new_state == GameStatesEnum.QUIT:
                return False
            elif new_state:
                self._transition_to_state(new_state)

        return True

    def update(self) -> bool:
        if self.current_state:
            new_state = self.current_state.update()
            if new_state == GameStatesEnum.QUIT:
                return False
            elif new_state:
                self._transition_to_state(new_state)

        return True

    def render(self, window) -> None:
        if self.current_state:
            self.current_state.render(window)
