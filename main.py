import json
from auth import AuthManager
from game import GameController
from ui import UI, Theme

# #region agent log
LOG_PATH = "/Users/amirali/PycharmProjects/Quoridor G/.cursor/debug.log"
def _log(session_id, run_id, hypothesis_id, location, message, data):
    try:
        with open(LOG_PATH, "a") as f:
            f.write(json.dumps({"sessionId": session_id, "runId": run_id, "hypothesisId": hypothesis_id, "location": location, "message": message, "data": data, "timestamp": __import__("time").time() * 1000}) + "\n")
    except: pass
# #endregion

def main() -> None:
    # #region agent log
    _log("debug-session", "run1", "A", "main.py:main", "main() entry", {})
    # #endregion
    ui = UI()
    auth = AuthManager()

    current_user = None

    while True:
        # #region agent log
        _log("debug-session", "run1", "A", "main.py:main_loop", "before main_menu()", {"current_user": current_user})
        # #endregion
        choice = ui.main_menu()
        # #region agent log
        _log("debug-session", "run1", "A", "main.py:main_loop", "after main_menu()", {"choice": choice})
        # #endregion

        if choice == "1":
            if current_user is None:
                ui.print_message("Please log in or sign up first.", error=True)
                continue
            # #region agent log
            _log("debug-session", "run1", "B", "main.py:choice_1", "before choose_game_mode()", {"current_user": current_user})
            # #endregion
            mode = ui.choose_game_mode()
            # #region agent log
            _log("debug-session", "run1", "B", "main.py:choice_1", "after choose_game_mode()", {"mode": mode})
            # #endregion
            if mode is None:
                continue
            # #region agent log
            _log("debug-session", "run1", "B", "main.py:choice_1", "before GameController()", {"mode": mode, "current_user": current_user})
            # #endregion
            controller = GameController(ui, auth, current_user, mode)
            # #region agent log
            _log("debug-session", "run1", "B", "main.py:choice_1", "after GameController()", {})
            # #endregion
            controller.run()
        elif choice == "2":
            # #region agent log
            _log("debug-session", "run1", "A", "main.py:choice_2", "before show_how_to_play()", {})
            # #endregion
            ui.show_how_to_play()
            # #region agent log
            _log("debug-session", "run1", "A", "main.py:choice_2", "after show_how_to_play()", {})
            # #endregion
            # #region agent log
            _log("debug-session", "run1", "A", "main.py:choice_2", "waiting for input before loop continues", {})
            # #endregion
            input(f"{Theme.FG_CYAN}Press Enter to return to menu...{Theme.RESET}")
        elif choice == "3":
            # #region agent log
            _log("debug-session", "run1", "A", "main.py:choice_3", "before show_leaderboard()", {})
            # #endregion
            ui.show_leaderboard()
            # #region agent log
            _log("debug-session", "run1", "A", "main.py:choice_3", "after show_leaderboard()", {})
            # #endregion
            # #region agent log
            _log("debug-session", "run1", "A", "main.py:choice_3", "waiting for input before loop continues", {})
            # #endregion
            input(f"{Theme.FG_CYAN}Press Enter to return to menu...{Theme.RESET}")
        elif choice == "4":
            current_user = auth.signup(ui)
        elif choice == "5":
            current_user = auth.login(ui)
        elif choice == "6":
            ui.print_message("Goodbye!")
            break
        else:
            ui.print_message("Invalid option. Please try again.", error=True)


if __name__ == "__main__":
    main()


