from auth import AuthManager
from game import GameController
from ui import UI


def main() -> None:
    ui = UI()
    auth = AuthManager()

    current_user = None

    while True:
        choice = ui.main_menu()

        if choice == "1":
            if current_user is None:
                ui.print_message("Please log in or sign up first.", error=True)
                continue
            mode = ui.choose_game_mode()
            if mode is None:
                continue
            controller = GameController(ui, auth, current_user, mode)
            controller.run()
        elif choice == "2":
            ui.show_how_to_play()
        elif choice == "3":
            ui.show_leaderboard()
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


