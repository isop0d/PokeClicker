import os
from dotenv import load_dotenv
from supabase import create_client
import requests
import random

load_dotenv()

SUPABASE_URL = "https://qhjrldbntaqyggpugatc.supabase.co"
PUB_KEY = "sb_publishable_ksEnYRe0jmnWrCEDchF3Tg__7bWYhpe"
SUPA_SECRET = os.environ.get("SUPA_SECRET")

client = create_client(SUPABASE_URL, SUPA_SECRET)



#local game state
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

# save game to supabase logic
def save_state(user_id):
    client.table("game_state").update({
        "points": state["points"],
        "pokemon": state["pokemon"]
    }).eq("user_id", user_id).execute()



def load_state(user_id):
    
    # send a request to Supabase to get the game state for the given user_id
    response = client.table("game_state").select("*").eq("user_id", user_id).execute()

    # check for user data 
    if len(response.data) == 0:
        # if not found create new user
        client.table("game_state").insert({
            "user_id": user_id, 
            "points": 0, 
            "pokemon": []
            }).execute()
        
        print(f"{user_id} has been created.")
    else:
        # if user is found load data to game state declared 
        user_data = response.data[0]
        state["points"] = user_data["points"]
        state["pokemon"] = user_data["pokemon"]
        print(f"Welcome back, {user_id}!")


def get_random_pokemon():
    pokemon_id = random.randint(1, 1025)
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}")
    if response.status_code == 200:
        data = response.json()
        pokemon_name = data["name"]
        if pokemon_name in state["pokemon"]:
            get_random_pokemon()  # Try again if the Pokemon is already caught
        else:
            print(f"You caught {pokemon_name} !!")
            state["pokemon"].append(pokemon_name)


def main():


    print("Enter your user ID:")
    user_id = input("> ").strip()
    
    # load game function call
    load_state(user_id)

    print("\n")
    print("=== PokeClicker ===\n")
    print("Press Enter to click. Type 'q' to quit.\n")
    print("Press enter to earn points. Type 'catch' to catch a Pokemon (costs 50 points).")
    print("Type 'pokedex' to view your caught Pokemon.\n")
    print("Type 'q' to quit the game and save your progress.\n")


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
                get_random_pokemon()
            else:
                print("Not enough points to catch a Pokemon.")
        if user_input == "pokedex":
            print("\n=== Pokedex ===")
            for i, pokemon in enumerate(state["pokemon"], start=1):
                print(f"{i}. {pokemon}")

    # save game here when user quits the game
    save_state(user_id)



if __name__ == "__main__":
    main()
