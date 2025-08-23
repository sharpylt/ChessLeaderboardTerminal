import requests
import os

SETTINGS_FILE = "settings.txt"
leaderboard = []
modes = {
    "daily": "chess_daily",
    "rapid": "chess_rapid",
    "blitz": "chess_blitz",
    "bullet": "chess_bullet"
}
current_mode = "chess_rapid"
rating_type = "last"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def show_disclaimer():
    print("=======================================")
    print("  Chess.com Leaderboard (Terminal)")
    print("=======================================")
    print("NOTE: This program uses your internet connection")
    print("to fetch the latest stats from chess.com.")
    print("You do NOT need admin rights to run it.")
    print("=======================================\n")

def check_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            line = f.read().strip()
            if line == "hide_disclaimer":
                return False
    return True

def ask_to_hide():
    choice = input("Do you want to see this message every time? (y/n): ").strip().lower()
    if choice == "n":
        with open(SETTINGS_FILE, "w") as f:
            f.write("hide_disclaimer")
        print("Okay, disclaimer will be hidden next time.\n")
    else:
        print("Disclaimer will continue to show.\n")

def fetch_rating(username, mode, rating_type):
    username = username.strip().lower()
    url = f"https://api.chess.com/pub/player/{username}/stats"
    try:
        response = requests.get(url, headers=HEADERS, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if mode in data:
                if rating_type in data[mode]:
                    return data[mode][rating_type]["rating"]
                else:
                    return None
            else:
                return None
        else:
            return None
    except Exception:
        return None

def show_leaderboard():
    os.system("cls" if os.name == "nt" else "clear")
    mode_name = list(modes.keys())[list(modes.values()).index(current_mode)]
    print("=== Chess.com Leaderboard ===")
    print(f"Current mode: {mode_name} | Rating type: {rating_type.upper()}")

    if not leaderboard:
        print("No players added yet.")
    else:
        players_with_ratings = []
        for user in leaderboard:
            rating = fetch_rating(user, current_mode, rating_type)
            if rating is None:
                players_with_ratings.append((user, "N/A"))
            else:
                players_with_ratings.append((user, rating))

        sorted_players = sorted(
            players_with_ratings,
            key=lambda x: (x[1] if isinstance(x[1], int) else -1),
            reverse=True
        )

        for i, (user, rating) in enumerate(sorted_players, start=1):
            print(f"{i}. {user} - {rating}")
    print("\n")

def main():
    global current_mode, rating_type
    if check_settings():
        show_disclaimer()
        ask_to_hide()
    while True:
        show_leaderboard()
        print("Options:")
        print("1. Add username")
        print("2. Remove username")
        print("3. Clear all")
        print("4. Change mode")
        print("5. Change rating type (current/best)")
        print("6. Quit")
        choice = input("Choose: ")
        if choice == "1":
            user = input("Enter chess.com username: ").strip().lower()
            if user not in leaderboard:
                leaderboard.append(user)
            else:
                print("Already in leaderboard.")
        elif choice == "2":
            user = input("Enter username to remove: ").strip().lower()
            if user in leaderboard:
                leaderboard.remove(user)
                print("Removed.")
            else:
                print("User not found in list.")
        elif choice == "3":
            leaderboard.clear()
            print("Leaderboard cleared.")
        elif choice == "4":
            print("Available modes:", ", ".join(modes.keys()))
            mode_choice = input("Choose mode: ").strip().lower()
            if mode_choice in modes:
                current_mode = modes[mode_choice]
                print(f"Mode changed to {mode_choice}")
            else:
                print("Invalid mode.")
        elif choice == "5":
            rating_type = "best" if rating_type == "last" else "last"
            print(f"Rating type changed to {rating_type.upper()}")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
