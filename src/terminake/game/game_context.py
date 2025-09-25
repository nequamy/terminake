from typing import Any, Dict, Optional

from entities import Snake


class GameContext:
    def __init__(self, max_y: int, max_x: int) -> None:
        self.score: int = 0
        self.high_score: int = 0
        self.difficulty: int = 1
        self.snake: Optional[Snake] = None
        self.game_data: Dict[str, Any] = {}
        self.max_y = max_y
        self.max_x = max_x

    def reset_game_state(self) -> None:
        self.score = 0
        self.snake = None
        self.game_data.clear()
