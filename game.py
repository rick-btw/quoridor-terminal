from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple

from auth import AuthManager
from board import Board, BOARD_SIZE
from entities import Player, Wall, Position


@dataclass
class GameState:
    positions: Dict[int, Position]
    walls: List[Wall]
    walls_remaining: Dict[int, int]
    current_player_id: int


class GameController:
    """High-level game controller managing turns, moves, undo and win detection."""

    def __init__(self, ui, auth: AuthManager, current_user: str, mode: int) -> None:
        self.ui = ui
        self.auth = auth
        self.mode = mode  # 2 or 4 players
        self.current_user = current_user

        self.players: Dict[int, Player] = self._create_players()
        self.board = Board(list(self.players.values()))
        self.turn_order: List[int] = sorted(self.players.keys())
        self.current_turn_index: int = 0

        self.history: List[GameState] = []
        self._push_state()

    # --------- Setup ---------
    def _create_players(self) -> Dict[int, Player]:
        if self.mode == 2:
            wall_count = 10
            p1 = Player(1, "P1", (BOARD_SIZE - 1, BOARD_SIZE // 2), range(0, 1))
            p2 = Player(2, "P2", (0, BOARD_SIZE // 2), range(BOARD_SIZE - 1, BOARD_SIZE))
            return {1: p1, 2: p2}
        else:
            wall_count = 5
            center = BOARD_SIZE // 2
            return {
                1: Player(1, "P1", (BOARD_SIZE - 1, center), range(0, 1)),
                2: Player(2, "P2", (0, center), range(BOARD_SIZE - 1, BOARD_SIZE)),
                3: Player(3, "P3", (center, 0), range(0, BOARD_SIZE)),
                4: Player(4, "P4", (center, BOARD_SIZE - 1), range(0, BOARD_SIZE)),
            }

    # --------- State history / undo ---------
    def _snapshot(self) -> GameState:
        positions = {pid: p.position for pid, p in self.players.items()}
        walls = list(self.board.walls)
        walls_remaining = {pid: p.walls_remaining for pid, p in self.players.items()}
        current_player_id = self.turn_order[self.current_turn_index]
        return GameState(positions, walls, walls_remaining, current_player_id)

    def _restore(self, state: GameState) -> None:
        for pid, pos in state.positions.items():
            self.players[pid].position = pos
        for pid, count in state.walls_remaining.items():
            self.players[pid].walls_remaining = count
        self.board.walls = list(state.walls)
        self.board.blocked_edges.clear()
        for w in self.board.walls:
            self.board._add_wall_edges(w)
        self.current_turn_index = self.turn_order.index(state.current_player_id)

    def _push_state(self) -> None:
        self.history.append(self._snapshot())

    def undo(self) -> bool:
        # Need at least two states: current and previous
        if len(self.history) < 2:
            return False
        # pop current
        self.history.pop()
        prev = self.history[-1]
        self._restore(prev)
        return True

    # --------- Turn helpers ---------
    def current_player(self) -> Player:
        pid = self.turn_order[self.current_turn_index]
        return self.players[pid]

    def _advance_turn(self) -> None:
        self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)

    def _check_winner(self) -> Optional[Player]:
        for p in self.players.values():
            if p.position[0] in p.goal_rows:
                return p
        return None

    # --------- Game loop ---------
    def run(self) -> None:
        self.ui.print_title("Quoridor")

        # Player mapping for leaderboard: for simplicity, all seats use current_user
        leaderboard_players = {pid: self.current_user for pid in self.players.keys()}

        while True:
            self.ui.render_board(self.board, self.players, self.current_player())
            winner = self._check_winner()
            if winner:
                self.ui.print_message(f"{winner.name} wins!", highlight=True)
                self.auth.record_game_result(self.current_user, leaderboard_players)
                break

            action = self.ui.prompt_turn_action(self.current_player())

            if action == "m":
                self._handle_move()
            elif action == "w":
                self._handle_wall()
            elif action == "u":
                if not self.undo():
                    self.ui.print_message("Nothing to undo.", error=True)
                continue  # same player turn after undo
            elif action == "q":
                self.auth.record_game_result(None, leaderboard_players)
                break
            else:
                self.ui.print_message("Invalid action.", error=True)
                continue

            self._push_state()
            self._advance_turn()

    # --------- Actions ---------
    def _handle_move(self) -> None:
        p = self.current_player()
        row, col = self.ui.prompt_move()
        if not self.board.move_player(p.id, (row, col)):
            self.ui.print_message("Illegal move.", error=True)

    def _handle_wall(self) -> None:
        p = self.current_player()
        if p.walls_remaining <= 0:
            self.ui.print_message("No walls remaining.", error=True)
            return
        row, col, orient = self.ui.prompt_wall()
        wall = Wall(row=row, col=col, horizontal=(orient == "h"))
        if self.board.place_wall(wall):
            p.walls_remaining -= 1
        else:
            self.ui.print_message("Invalid wall placement.", error=True)


