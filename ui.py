import getpass
import os
from typing import Dict

from auth import AuthManager
from board import Board, BOARD_SIZE
from entities import Player


class Theme:
    # Base
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    # Foreground colors
    FG_BLACK = "\033[30m"
    FG_RED = "\033[31m"
    FG_GREEN = "\033[32m"
    FG_YELLOW = "\033[33m"
    FG_BLUE = "\033[34m"
    FG_MAGENTA = "\033[35m"
    FG_CYAN = "\033[36m"
    FG_WHITE = "\033[37m"
    FG_BRIGHT_BLACK = "\033[90m"
    FG_BRIGHT_RED = "\033[91m"
    FG_BRIGHT_GREEN = "\033[92m"
    FG_BRIGHT_YELLOW = "\033[93m"
    FG_BRIGHT_BLUE = "\033[94m"
    FG_BRIGHT_MAGENTA = "\033[95m"
    FG_BRIGHT_CYAN = "\033[96m"
    FG_BRIGHT_WHITE = "\033[97m"

    # Background colors
    BG_RED = "\033[41m"
    BG_BLUE = "\033[44m"
    BG_BLACK = "\033[40m"

    # Semantic colors / roles
    HEADER = BOLD + FG_BRIGHT_CYAN
    BORDER = BOLD + FG_BRIGHT_BLUE
    SHADOW = DIM + FG_BRIGHT_BLACK

    PLAYER1 = FG_BRIGHT_RED
    PLAYER2 = FG_BRIGHT_BLUE
    PLAYER3 = FG_BRIGHT_GREEN
    PLAYER4 = FG_BRIGHT_YELLOW

    WALL = FG_BRIGHT_WHITE

    SUCCESS = BOLD + FG_BRIGHT_GREEN
    ERROR = BOLD + FG_BRIGHT_RED
    ERROR_BG = BG_RED + FG_WHITE

    TABLE_HEADER = BOLD + FG_BRIGHT_CYAN
    TABLE_ROW_ALT = DIM + FG_WHITE


PLAYER_COLORS = [
    Theme.PLAYER1,
    Theme.PLAYER2,
    Theme.PLAYER3,
    Theme.PLAYER4,
]


class UI:
    def __init__(self) -> None:
        self.auth = AuthManager()

    # --------- Basic I/O / Frame control ---------
    def clear_screen(self) -> None:
        # Use ANSI clear to avoid platform-specific system calls
        print("\033[2J\033[H", end="")

    def render_banner(self) -> None:
        self.clear_screen()
        # Top border in Bold Cyan (same as header)
        top = (
            f"{Theme.HEADER} ╔══════════════════════════════════════════════════════════════════════╗{Theme.RESET}"
        )
        # Main banner lines (text and borders) in Bold Cyan
        lines = [
            " ║  ██████╗ ██╗   ██╗ ██████╗ ██████╗ ██╗██████╗  ██████╗ ██████╗       ║",
            " ║ ██╔═══██╗██║   ██║██╔═══██╗██╔══██╗██║██╔══██╗██╔═══██╗██╔══██╗      ║",
            " ║ ██║   ██║██║   ██║██║   ██║██████╔╝██║██║  ██║██║   ██║██████╔╝      ║",
            " ║ ██║▄▄ ██║██║   ██║██║   ██║██╔══██╗██║██║  ██║██║   ██║██╔══██╗      ║",
            " ║ ╚██████╔╝╚██████╔╝╚██████╔╝██║  ██║██║██████╔╝╚██████╔╝██║  ██║      ║",
            " ║  ╚══▀▀═╝  ╚═════╝  ╚═════╝ ╚═╝  ╚═╝╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝      ║",
        ]
        # Underscore separator line in Dim Gray
        separator_line = " ╚═╗__________________________________________________________________  ║"
        # Bottom border line in Dim Gray
        bottom_border = "   ╚══════════════════════════════════════════════════════════════════╝ ║"
        # Shadow line in Dim Gray (extends slightly to the right)
        shadow_line = "    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀"
        
        print(top)
        # Print main text lines in Bold Cyan
        for line in lines:
            print(f"{Theme.HEADER}{line}{Theme.RESET}")
        # Print separator line in Dim Gray
        print(f"{Theme.SHADOW}{separator_line}{Theme.RESET}")
        # Print bottom border in Dim Gray
        print(f"{Theme.SHADOW}{bottom_border}{Theme.RESET}")
        # Print shadow line in Dim Gray
        print(f"{Theme.SHADOW}{shadow_line}{Theme.RESET}\n")

    def print_title(self, text: str) -> None:
        print(f"\n{Theme.HEADER}{text}{Theme.RESET}")
        print(f"{Theme.BORDER}{'─' * len(text)}{Theme.RESET}")

    def print_message(self, text: str, error: bool = False, highlight: bool = False) -> None:
        if error:
            color = Theme.ERROR
        elif highlight:
            color = Theme.SUCCESS
        else:
            color = Theme.FG_CYAN
        print(f"{color}{text}{Theme.RESET}")

    def prompt(self, text: str) -> str:
        return input(text)

    def prompt_password(self, text: str) -> str:
        try:
            return getpass.getpass(text)
        except Exception:
            return input(text)

    # --------- Menus ---------
    def main_menu(self) -> str:
        self.render_banner()
        self.print_title("Main Menu")
        print(f"{Theme.FG_WHITE}1){Theme.RESET} New Game")
        print(f"{Theme.FG_WHITE}2){Theme.RESET} How to Play")
        print(f"{Theme.FG_WHITE}3){Theme.RESET} Leaderboard")
        print(f"{Theme.FG_WHITE}4){Theme.RESET} Sign Up")
        print(f"{Theme.FG_WHITE}5){Theme.RESET} Login")
        print(f"{Theme.FG_WHITE}6){Theme.RESET} Exit")
        return input(f"{Theme.FG_CYAN}Choose an option: {Theme.RESET}").strip()

    def choose_game_mode(self) -> int | None:
        self.print_title("Choose Game Mode")
        print("1) 2 Players")
        print("2) 4 Players")
        choice = input("Select (1-2, blank to cancel): ").strip()
        if not choice:
            return None
        if choice == "1":
            return 2
        if choice == "2":
            return 4
        self.print_message("Invalid mode.", error=True)
        return None

    def show_how_to_play(self) -> None:
        self.clear_screen()
        self.print_title("How to Play Quoridor (Terminal Edition)")
        print(
            f"{Theme.FG_WHITE}Goal:{Theme.RESET} Reach the opposite side of the board before your opponents.\n"
            "- On your turn, choose to move (m), place a wall (w), undo (u), or quit (q).\n"
            "- Moves: one square up/down/left/right, or jump over an adjacent pawn.\n"
            "- Walls: block paths but must not completely prevent any player from reaching their goal.\n"
            "- You have 10 walls in 2-player mode, 5 in 4-player mode."
        )

    def show_leaderboard(self) -> None:
        self.clear_screen()
        self.print_title("Leaderboard")
        data = self.auth.get_leaderboard()
        if not data:
            print(f"{Theme.DIM}No games played yet.{Theme.RESET}")
            return
        rows = sorted(data.items(), key=lambda kv: (-kv[1]["wins"], kv[0]))
        header = f"{'User':15} {'Wins':>6} {'Games':>7}"
        print(f"{Theme.TABLE_HEADER}{header}{Theme.RESET}")
        print(f"{Theme.BORDER}{'═' * len(header)}{Theme.RESET}")
        for idx, (user, stats) in enumerate(rows):
            color = Theme.TABLE_ROW_ALT if idx % 2 else Theme.FG_WHITE
            print(
                f"{color}{user:15} {stats['wins']:>6} {stats['games']:>7}{Theme.RESET}"
            )

    # --------- In-game prompts ---------
    def prompt_turn_action(self, player: Player) -> str:
        color = PLAYER_COLORS[(player.id - 1) % len(PLAYER_COLORS)]
        print(
            f"{color}Player {player.id} ({player.name}) turn. "
            f"Position: {player.position}, Walls: {player.walls_remaining}{Theme.RESET}"
        )
        print("Actions: [m]ove, [w]all, [u]ndo, [q]uit")
        return input("Choose action: ").strip().lower()

    def prompt_move(self) -> tuple[int, int]:
        raw = input("Enter move target as 'row col' (0-based): ").strip()
        try:
            r_s, c_s = raw.split()
            r, c = int(r_s), int(c_s)
            return r, c
        except Exception:
            print("Invalid input, defaulting to (0, 0).")
            return 0, 0

    def prompt_wall(self) -> tuple[int, int, str]:
        raw = input(
            "Enter wall as 'row col orientation', row/col 0-7, orientation h/v (e.g., '3 4 h'): "
        ).strip()
        try:
            r_s, c_s, o_s = raw.split()
            r, c = int(r_s), int(c_s)
            o = o_s.lower()
            if o not in ("h", "v"):
                raise ValueError
            return r, c, o
        except Exception:
            print("Invalid input, defaulting to (0, 0, h).")
            return 0, 0, "h"

    # --------- Board Rendering ---------
    def render_board(self, board: Board, players: Dict[int, Player], current: Player) -> None:
        self.clear_screen()
        self.print_title("Board")
        # Prepare quick lookup
        pawn_cells: Dict[tuple[int, int], Player] = {
            p.position: p for p in players.values()
        }

        def cell_blocked(a: tuple[int, int], b: tuple[int, int]) -> bool:
            return board.is_blocked(a, b)

        # Column indices header
        print("    " + "  ".join(f"{c}" for c in range(BOARD_SIZE)))

        # Top border
        top_border = "   " + Theme.BORDER + "╔" + "╦".join(
            ["══"] * BOARD_SIZE
        ) + "╗" + Theme.RESET
        print(top_border)

        for r in range(BOARD_SIZE):
            # Row of cells
            row_str = f"{r:2} {Theme.BORDER}║{Theme.RESET}"
            for c in range(BOARD_SIZE):
                pos = (r, c)
                if pos in pawn_cells:
                    p = pawn_cells[pos]
                    color = PLAYER_COLORS[(p.id - 1) % len(PLAYER_COLORS)]
                    char = "P"
                    if p.id == current.id:
                        char = "@"
                    cell_repr = f"{color}{char}{Theme.RESET}"
                else:
                    cell_repr = " "

                # Right boundary of cell
                if c < BOARD_SIZE - 1:
                    # If there's a wall between (r, c) and (r, c+1), draw a colored double bar
                    if cell_blocked((r, c), (r, c + 1)):
                        sep = f"{Theme.WALL}║{Theme.RESET}"
                    else:
                        sep = f"{Theme.BORDER}║{Theme.RESET}"
                    row_str += f"{cell_repr}{sep}"
                else:
                    row_str += f"{cell_repr}{Theme.BORDER}║{Theme.RESET}"

            print(row_str)

            # Horizontal edges between rows
            if r < BOARD_SIZE - 1:
                edge_row = "   " + Theme.BORDER + "╠"
                segments = []
                for c in range(BOARD_SIZE):
                    if cell_blocked((r, c), (r + 1, c)):
                        seg = f"{Theme.WALL}══{Theme.BORDER}"
                    else:
                        seg = "══"
                    segments.append(seg)
                edge_row += "╬".join(segments) + "╣" + Theme.RESET
                print(edge_row)

        # Bottom border
        bottom_border = "   " + Theme.BORDER + "╚" + "╩".join(
            ["══"] * BOARD_SIZE
        ) + "╝" + Theme.RESET
        print(bottom_border)

