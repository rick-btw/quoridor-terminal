



## Quoridor (Terminal Edition)

A fully-playable, terminal-based implementation of the board game **Quoridor**, built with **modular Object-Oriented Python** and a **themed CLI UI**.  
Features include authentication, persistent leaderboard, undo, and a pathfinding-safe wall system on a 9×9 board.

---

## Features

- **Board & Rules**
  - 9×9 Quoridor board with **2-player** and **4-player** modes.
  - Players move **one square orthogonally** (up/down/left/right).
  - **Jumping**: if a pawn is directly adjacent, you can jump over it to the square behind (when not blocked by walls).
  - Each player has:
    - **2 players**: 10 walls each.
    - **4 players**: 5 walls each.
  - **Walls**:
    - Horizontal or vertical, placed in grooves between squares.
    - Can never completely block any player’s path to their goal (enforced by BFS).
  - **Win condition**: first player whose pawn reaches their goal side (opposite or assigned goal rows) wins.

- **Game Engine**
  - `Board` manages grid, players, walls, adjacency, and pathfinding.
  - `GameController` manages:
    - Turn order and current player.
    - Validating and applying moves and wall placements.
    - Win detection.
    - **Undo** via a history stack of game states (positions, walls, wall counts, and turn index).

- **Authentication & Persistence**
  - **Sign Up / Login** system:
    - Users stored in `users.json`.
    - Simple username + password (plaintext) storage (easy to swap to hashing later).
  - **Leaderboard**:
    - Persistent in `leaderboard.json`.
    - Tracks **wins** and **games played** per user.
    - Automatically updated when a game ends (win or quit).

- **Terminal UI & Aesthetics**
  - **Hero banner** for the main menu:
    - Large ASCII art QUORIDOR logo with a **shadow effect** (using `▀` blocks).
    - Bold cyan for primary text and dim gray for drop shadow.
  - **Central `Theme` class** for all colors:
    - Headers/Borders: bold blue/cyan.
    - Players:
      - Player 1: bright red.
      - Player 2: bright blue.
      - Player 3: bright green.
      - Player 4: bright yellow.
    - Walls: bright white.
    - Success/Win: bold bright green.
    - Errors: bold red / red background.
  - **Board Rendering**:
    - Uses **double-line box characters** (`╔ ═ ╦ ║ ╬ ╚ ╩ ╝`) to mimic a physical board.
    - Walls visually represented as **highlighted segments** along the grid:
      - Vertical walls: bright white `║`.
      - Horizontal walls: bright white `══`.
    - Pawns:
      - Colored `P` for non-active players.
      - Colored `@` for the current player.
    - Coordinates displayed (rows and columns) for input guidance.
  - **Leaderboard UI**:
    - Clean, tabular layout.
    - Colored header with `═` underline.
    - Alternating row styles for readability (normal / dim).
  - **No ghosting**:
    - `clear_screen()` called before large updates (banner, board, leaderboard, etc.).

---

## Project Structure

```text
.
├── main.py          # Entry point, main menu and high-level app loop
├── auth.py          # AuthManager: signup, login, JSON user & leaderboard storage
├── game.py          # GameController: turn management, game loop, undo, win detection
├── board.py         # Board: 9x9 grid, movement rules, walls, BFS pathfinding
├── entities.py      # Player and Wall data classes
└── ui.py            # UI: theme, banner, menus, board rendering, prompts
```

### Key Components

- **`AuthManager` (`auth.py`)**
  - Loads/saves `users.json` and `leaderboard.json`.
  - `signup(ui)`, `login(ui)` for user flows via the UI.
  - `record_game_result(winner, players)` to track wins and games played.
  - `get_leaderboard()` returns sorted leaderboard data for rendering.

- **`Player` & `Wall` (`entities.py`)**
  - `Player`: `id`, `name`, `position`, `walls_remaining`, and `goal_rows`.
  - `Wall`: `row`, `col`, `horizontal`.

- **`Board` (`board.py`)**
  - Knows about:
    - `players` dictionary.
    - `walls` list.
    - `blocked_edges` as a set of blocked cell-to-cell links.
  - Movement:
    - Validates adjacency and jump moves with `can_move`.
  - Walls:
    - Calculates which edges to block when a wall is placed.
    - `can_place_wall` temporarily applies a wall and runs **BFS** from every player to ensure a valid path remains.
  - Pathfinding:
    - `_has_path_to_goal(player)` uses BFS across unblocked neighbors.

- **`GameController` (`game.py`)**
  - Initializes the correct player layout for 2- or 4-player mode.
  - Maintains:
    - `turn_order` and `current_turn_index`.
    - `history` of `GameState` for undo.
  - Handles:
    - `run()` main game loop.
    - `_handle_move()` and `_handle_wall()` for user actions.
    - `undo()` to revert the previous full state.
    - `_check_winner()` to determine if anyone has reached their goal rows.

- **`UI` & `Theme` (`ui.py`)**
  - `Theme`:
    - Centralized ANSI color and style definitions.
    - Semantic roles for headers, borders, players, walls, success, errors, and table rows.
  - `UI`:
    - `clear_screen()` to reset the terminal frame.
    - `render_banner()` for the main QUORIDOR hero section with shadows.
    - `main_menu()`, `show_how_to_play()`, `show_leaderboard()` for non-game navigation.
    - `prompt_turn_action()`, `prompt_move()`, `prompt_wall()` for in-game input.
    - `render_board()` for the double-line box board with colored players and walls.

---

## Installation

### Requirements

- **Python 3.8+** (tested on Python 3+; no external dependencies).

### Clone the Repository

```bash
git clone https://github.com/<your-username>/<your-repo-name>.git
cd <your-repo-name>
```

*(Replace `<your-username>` and `<your-repo-name>` with your actual GitHub values.)*

---

## Running the Game

From the project root:

```bash
python3 main.py
```

On Windows, you may use:

```bash
python main.py
```

---

## Gameplay Guide

### Main Menu

Once you run `main.py`, you’ll see the **ASCII banner** and the main menu:

- `1) New Game`
- `2) How to Play`
- `3) Leaderboard`
- `4) Sign Up`
- `5) Login`
- `6) Exit`

#### Recommended Flow

1. **Sign Up** (option 4) to create an account.
2. **Login** (option 5).
3. **New Game** (option 1) to start playing.
4. After games, check the **Leaderboard** (option 3).

### Starting a Game

1. Choose **New Game**.
2. Select:
   - `1` → **2-player mode**
   - `2` → **4-player mode**

Each player is represented by a colored pawn:
- Player 1: bright red
- Player 2: bright blue
- Player 3: bright green
- Player 4: bright yellow  
The **current player** is shown as `@`; others as `P`.

### In-Game Controls

On your turn, you’ll see:

- **Actions**: `[m]ove, [w]all, [u]ndo, [q]uit`

#### Move

- Choose `m`
- Enter a target coordinate:

```text
Enter move target as 'row col' (0-based):
```

Examples:
- `4 4` to move to row 4, col 4.

Moves must be:
- One step up/down/left/right; OR
- A legal jump over an adjacent pawn (straight line, not blocked by walls).

#### Place Wall

- Choose `w`
- Enter wall coordinates:

```text
Enter wall as 'row col orientation', row/col 0-7, orientation h/v (e.g., '3 4 h'):
```

- `row`, `col`: the top-left groove coordinate (0–7).
- `orientation`:
  - `h` for horizontal.
  - `v` for vertical.

The engine will **reject**:
- Overlapping walls in the same spot and orientation.
- Any wall placement that blocks all paths for any player.

#### Undo

- Choose `u` to **undo** the last move or wall placement.
- Game state (positions, walls, wall counts, and turn) is restored from the previous snapshot.
- If there’s no previous state, the UI will tell you there’s nothing to undo.

#### Quit

- Choose `q` to concede/quit the current game.
- The game records the session as played (no winner) on the leaderboard.

### Win Condition

- The game ends immediately when a player reaches one of their goal rows.
- The UI displays a **green highlighted win message**.
- The **winner’s account** gets `wins + 1` and `games + 1`; other participating accounts get `games + 1`.

---

## Leaderboard

From the main menu, choose **Leaderboard**:

- Shows a table of:
  - `User`
  - `Wins`
  - `Games`
- Sorted by:
  - **Wins (descending)**, then
  - **Username** (ascending) as a tie-breaker.
- Styled with:
  - Colored header and `═` underline.
  - Alternating row styles for easier scanning.

Data is stored in `leaderboard.json` in the project directory.

---

## Notes & Future Improvements

- **Passwords** are currently stored in plaintext in `users.json` for simplicity; in a production scenario, they should be hashed (e.g., with `bcrypt`).
- Coordinate input is **0-based** and text-based; this can be extended to support notation like `A5` in the future.
- Jump rules and corner-jumps could be further refined to exactly mirror the official Quoridor rulebook if desired.

---

## License

Add your preferred license here, for example:

```text
MIT License
```

---

## Contributing

Pull requests and suggestions are welcome:

1. Fork the repo.
2. Create a feature branch.
3. Open a PR with a clear description of your change.

---

