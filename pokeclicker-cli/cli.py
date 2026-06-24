# to be replaced with database (supabase)
state = {
    "points": 0,
    "pokemon": [],
}


def display_status():
    print("\n=== Status ===")
    print(f"\nPoints: {state['points']}")
    print(f"Pokemon caught: {len(state['pokemon'])}")


def on_click():
    state["points"] += 1


def main():
    print("\n")
    print("=== PokeClicker ===\n")
    print("Press Enter to click. Type 'q' to quit.\n")
    print("Press enter to earn points. Type 'catch' to catch a Pokemon (costs 50 points).")

    while True:
        display_status()
        user_input = input("\n> ").strip().lower()

        if user_input == "q":
            break
        if user_input == "":
            on_click()
        if user_input == "catch":
            if state["points"] >= 50:
                state["points"] -= 50
                print("You caught a Pokemon!")
            else:
                print("Not enough points to catch a Pokemon.")



if __name__ == "__main__":
    main()
