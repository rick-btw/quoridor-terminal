from __future__ import annotations

from collections import deque
from typing import List, Tuple, Dict, Set

from entities import Player, Position, Wall


BOARD_SIZE = 9


class Board:
    """Represents the 9x9 grid, players and walls, and validates moves."""

    def __init__(self, players: List[Player]) -> None:
        self.players: Dict[int, Player] = {p.id: p for p in players}
        # Walls are represented as set of blocked edges between cells
        self.blocked_edges: Set[Tuple[Position, Position]] = set()
        self.walls: List[Wall] = []

    # --------- Helpers ---------
    @staticmethod
    def in_bounds(pos: Position) -> bool:
        r, c = pos
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    def is_occupied(self, pos: Position) -> bool:
        return any(p.position == pos for p in self.players.values())

    def neighbors(self, pos: Position) -> List[Position]:
        r, c = pos
        candidates = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]
        results: List[Position] = []
        for nr, nc in candidates:
            npos = (nr, nc)
            if self.in_bounds(npos) and not self.is_blocked(pos, npos):
                results.append(npos)
        return results

    def is_blocked(self, a: Position, b: Position) -> bool:
        return (a, b) in self.blocked_edges or (b, a) in self.blocked_edges

    # --------- Movement ---------
    def can_move(self, player_id: int, target: Position) -> bool:
        player = self.players[player_id]
        r, c = player.position
        tr, tc = target

        if not self.in_bounds(target):
            return False

        # Adjacent move
        dr, dc = tr - r, tc - c
        if abs(dr) + abs(dc) == 1:
            return not self.is_blocked(player.position, target) and not self.is_occupied(target)

        # Jump over opponent
        if abs(dr) + abs(dc) == 2 and (abs(dr) == 2 or abs(dc) == 2):
            mid = (r + dr // 2, c + dc // 2)
            if not self.in_bounds(mid):
                return False
            if not self.is_occupied(mid):
                return False
            if self.is_blocked(player.position, mid) or self.is_blocked(mid, target):
                return False
            return True

        return False

    def move_player(self, player_id: int, target: Position) -> bool:
        if not self.can_move(player_id, target):
            return False
        self.players[player_id].position = target
        return True

    # --------- Walls ---------
    def _add_wall_edges(self, wall: Wall) -> None:
        r, c = wall.row, wall.col
        if wall.horizontal:
            # Block between (r, c)-(r+1, c) and (r, c+1)-(r+1, c+1)
            a1, b1 = (r, c), (r + 1, c)
            a2, b2 = (r, c + 1), (r + 1, c + 1)
        else:
            # Vertical: block (r, c)-(r, c+1) and (r+1, c)-(r+1, c+1)
            a1, b1 = (r, c), (r, c + 1)
            a2, b2 = (r + 1, c), (r + 1, c + 1)
        self.blocked_edges.update({(a1, b1), (b1, a1), (a2, b2), (b2, a2)})

    def _remove_wall_edges(self, wall: Wall) -> None:
        r, c = wall.row, wall.col
        if wall.horizontal:
            a1, b1 = (r, c), (r + 1, c)
            a2, b2 = (r, c + 1), (r + 1, c + 1)
        else:
            a1, b1 = (r, c), (r, c + 1)
            a2, b2 = (r + 1, c), (r + 1, c + 1)
        for edge in ((a1, b1), (b1, a1), (a2, b2), (b2, a2)):
            self.blocked_edges.discard(edge)

    def can_place_wall(self, wall: Wall) -> bool:
        # Check within groove limits (0..7) for starting cell
        if not (0 <= wall.row < BOARD_SIZE - 1 and 0 <= wall.col < BOARD_SIZE - 1):
            return False

        # Avoid overlapping same wall
        for existing in self.walls:
            if (existing.row, existing.col, existing.horizontal) == (
                wall.row,
                wall.col,
                wall.horizontal,
            ):
                return False

        # Temporarily place wall and check path connectivity
        self._add_wall_edges(wall)
        try:
            for player in self.players.values():
                if not self._has_path_to_goal(player):
                    return False
        finally:
            self._remove_wall_edges(wall)
        return True

    def place_wall(self, wall: Wall) -> bool:
        if not self.can_place_wall(wall):
            return False
        self.walls.append(wall)
        self._add_wall_edges(wall)
        return True

    # --------- Pathfinding ---------
    def _has_path_to_goal(self, player: Player) -> bool:
        start = player.position
        queue: deque[Position] = deque([start])
        visited: Set[Position] = {start}

        while queue:
            pos = queue.popleft()
            r, _ = pos
            if r in player.goal_rows:
                return True
            for n in self.neighbors(pos):
                if n not in visited:
                    visited.add(n)
                    queue.append(n)
        return False


