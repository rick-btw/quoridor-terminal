from dataclasses import dataclass
from typing import Tuple


Position = Tuple[int, int]  # (row, col)


@dataclass
class Player:
    id: int
    name: str
    position: Position
    walls_remaining: int
    goal_rows: range  # rows that count as winning


@dataclass
class Wall:
    row: int
    col: int
    horizontal: bool  # True = horizontal, False = vertical


