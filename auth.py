import json
from pathlib import Path
from typing import Optional, Dict, Any


DATA_DIR = Path(__file__).parent
USERS_FILE = DATA_DIR / "users.json"
LEADERBOARD_FILE = DATA_DIR / "leaderboard.json"


def _load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return default


def _save_json(path: Path, data: Any) -> None:
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except OSError:
        pass


class AuthManager:
    """Handles user registration, login and persistent storage."""

    def __init__(self) -> None:
        self.users: Dict[str, Dict[str, Any]] = _load_json(USERS_FILE, {})
        self.leaderboard: Dict[str, Dict[str, int]] = _load_json(LEADERBOARD_FILE, {})

    # --------- User management ---------
    def _ensure_leaderboard_entry(self, username: str) -> None:
        if username not in self.leaderboard:
            self.leaderboard[username] = {"wins": 0, "games": 0}
            _save_json(LEADERBOARD_FILE, self.leaderboard)

    def signup(self, ui) -> Optional[str]:
        ui.print_title("Sign Up")
        username = ui.prompt("Choose a username (blank to cancel): ").strip()
        if not username:
            return None
        if username in self.users:
            ui.print_message("Username already exists.", error=True)
            return None
        password = ui.prompt_password("Choose a password: ")
        if not password:
            ui.print_message("Password cannot be empty.", error=True)
            return None
        self.users[username] = {"password": password}
        _save_json(USERS_FILE, self.users)
        self._ensure_leaderboard_entry(username)
        ui.print_message(f"Account created for '{username}'.")
        return username

    def login(self, ui) -> Optional[str]:
        ui.print_title("Login")
        username = ui.prompt("Username (blank to cancel): ").strip()
        if not username:
            return None
        password = ui.prompt_password("Password: ")
        if username not in self.users or self.users[username].get("password") != password:
            ui.print_message("Invalid username or password.", error=True)
            return None
        self._ensure_leaderboard_entry(username)
        ui.print_message(f"Welcome back, {username}!")
        return username

    # --------- Leaderboard ---------
    def record_game_result(self, winner: Optional[str], players: Dict[int, str]) -> None:
        """Update leaderboard after a game.

        :param winner: username of winning player (or None for draw/abort)
        :param players: mapping seat index -> username
        """
        for _, username in players.items():
            if not username:
                continue
            self._ensure_leaderboard_entry(username)
            self.leaderboard[username]["games"] += 1
        if winner:
            self._ensure_leaderboard_entry(winner)
            self.leaderboard[winner]["wins"] += 1
        _save_json(LEADERBOARD_FILE, self.leaderboard)

    def get_leaderboard(self) -> Dict[str, Dict[str, int]]:
        return dict(self.leaderboard)


