import json
import os
import random


from Game.AlgorithmForSelectingPossibleMoves.LimitedUniformCostSearch import (
    limited_uniform_cost_search
)

from Game.GameSetup.GenerateMansionLayout import (
    load_rooms,
    generate_random_weighted_graph_with_secrets,
    save_graph_to_json,
    load_graph_from_json,
    print_weighted_graph
)

from Game.GameSetup.GenerateSolutionAndDistributeCards import (
    deal_cards
)


def generate_mansion():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    room_file_path = os.path.join(base_dir, "GameSetup", "Room.txt")

    rooms = load_rooms(room_file_path)
    mansion_graph = generate_random_weighted_graph_with_secrets(
        rooms, seed=123, secret_chance=0.25
    )

    mansion_file_path = os.path.join(base_dir, "mansion_layout.json")
    save_graph_to_json(mansion_graph, mansion_file_path)

    loaded_graph = load_graph_from_json(mansion_file_path)
    print_weighted_graph(loaded_graph)
    return rooms, loaded_graph


def get_number_of_players():
    while True:
        answer = input("How many players are playing? (3-6): ").strip()
        if not answer.isdigit():
            print("Error: Please enter a valid number.")
            continue

        num_players = int(answer)
        if 3 <= num_players <= 6:
            return num_players
        else:
            print("Error: Number of players must be between 3 and 6.")


def generate_solution_and_deal_cards(num_players):
    base_dir = os.path.dirname(os.path.abspath(__file__))

    room_file = os.path.join(base_dir, "GameSetup", "Room.txt")
    weapon_file = os.path.join(base_dir, "GameSetup", "Weapon.txt")
    character_file = os.path.join(base_dir, "GameSetup", "Character.txt")
    solution_file = os.path.join(base_dir, "solution.json")
    hands_file = os.path.join(base_dir, "hands.json")

    solution_data, hands = deal_cards(
        room_file=room_file,
        weapon_file=weapon_file,
        character_file=character_file,
        solution_file=solution_file,
        hands_file=hands_file,
        seed=123,
        active_players=num_players
    )

    selected_players = list(hands.keys())
    print(f"Solution and hands generated for {num_players} player(s).")
    print("Selected players:", ", ".join(selected_players))
    return solution_data, hands, selected_players


def init_player_locations(player_names, rooms, seed=123):
    random.seed(seed)
    start_room = random.choice(rooms)
    print(f"All players starting in: {start_room}")

    players = {
        name: {"location": start_room, "history": []}
        for name in player_names
    }
    return players


def load_list_from_file(path):
    with open(path, "r") as f:

        return [line.strip() for line in f if line.strip()]


def prompt_suggestion(current_player, characters, weapons, current_room):
    print(f"\n{current_player} is making a suggestion in room '{current_room}'.")
    print(f"Available characters: {', '.join(characters)}")
    suspect = input("Suggest suspect: ").strip()
    while suspect not in characters:
        print("Invalid suspect. Try again.")
        suspect = input("Suggest suspect: ").strip()

    print(f"Available weapons: {', '.join(weapons)}")
    weapon = input("Suggest weapon: ").strip()
    while weapon not in weapons:
        print("Invalid weapon. Try again.")
        weapon = input("Suggest weapon: ").strip()


    return suspect, weapon, current_room


def process_suggestion(current_player, suggestion, player_states, selected_players, weapons_locations):
    suspect, weapon, room = suggestion
    print(f"\n{current_player} suggests it was {suspect} with the {weapon} in the {room}.")


    if suspect in player_states:
        if player_states[suspect]["location"] != room:
            print(f"Moving suggested character '{suspect}' into {room}.")
            player_states[suspect]["location"] = room
            player_states[suspect]["history"].append(room)


    weapons_locations[weapon] = room
    print(f"The weapon '{weapon}' is now in {room}.")


    start_idx = selected_players.index(current_player)
    num = len(selected_players)
    for offset in range(1, num):
        responder = selected_players[(start_idx + offset) % num]

        hand = player_states[responder]["hand"]
        matching = [card for card in (suspect, weapon, room) if card in hand]
        if matching:
            shown_card = random.choice(matching)
            print(f"{responder} can disprove the suggestion and shows a card to {current_player} (private).")

            print(f"[PRIVATE to {current_player}]: {shown_card}")
            player_states[current_player]["seen_cards"].append(shown_card)
            return
    print("No one could disprove the suggestion.")


def prompt_accusation(current_player, characters, weapons, rooms):
    print(f"\n{current_player} is making an accusation.")
    print(f"Available characters: {', '.join(characters)}")
    suspect = input("Accuse suspect: ").strip()
    while suspect not in characters:
        print("Invalid suspect. Try again.")
        suspect = input("Accuse suspect: ").strip()

    print(f"Available weapons: {', '.join(weapons)}")
    weapon = input("Accuse weapon: ").strip()
    while weapon not in weapons:
        print("Invalid weapon. Try again.")
        weapon = input("Accuse weapon: ").strip()

    print(f"Available rooms: {', '.join(rooms)}")
    room = input("Accuse room: ").strip()
    while room not in rooms:
        print("Invalid room. Try again.")
        room = input("Accuse room: ").strip()

    return suspect, weapon, room


def check_accusation(accusation, solution_data):

    keys = {k.lower(): v for k, v in solution_data.items()}
    suspect, weapon, room = accusation
    correct_character = keys.get("character") or keys.get("suspect") or keys.get("person")
    correct_weapon = keys.get("weapon")
    correct_room = keys.get("room")
    return (
        suspect == correct_character
        and weapon == correct_weapon
        and room == correct_room
    )


if __name__ == "__main__":
    rooms, mansion_graph = generate_mansion()
    print("--------------- Mansion Generated ---------------")
    num_players = get_number_of_players()
    print(f"Number of players selected: {num_players}")

    solution_data, hands, selected_players = generate_solution_and_deal_cards(num_players)


    base_dir = os.path.dirname(os.path.abspath(__file__))
    character_file = os.path.join(base_dir, "GameSetup", "Character.txt")
    weapon_file = os.path.join(base_dir, "GameSetup", "Weapon.txt")
    characters = load_list_from_file(character_file)
    weapons = load_list_from_file(weapon_file)


    player_locations = init_player_locations(selected_players, rooms)
    player_states = {}
    for name in selected_players:
        player_states[name] = {
            "location": player_locations[name]["location"],
            "history": player_locations[name]["history"],
            "hand": hands.get(name, []),
            "active": True,
            "seen_cards": [],
        }


    weapons_locations = {w: random.choice(rooms) for w in weapons}

    print("Initial player locations:")
    for p, info in player_states.items():
        print(f"  {p}: {info['location']}")

    print("Initial weapon locations:")
    for w, loc in weapons_locations.items():
        print(f"  {w}: {loc}")

    print("--------------- Players Setup and Solution Generated ---------------")
    index = 0
    game_over = False

    while not game_over:
        # Check if any active players remain
        active_players = [p for p, s in player_states.items() if s["active"]]
        if not active_players:
            print("\nAll players have been eliminated. No one solved the case. Game ends with no winner.")
            game_over = True
            break

        current_player = selected_players[index]
        state = player_states[current_player]

        if not state["active"]:
            print(f"\n{current_player} has been eliminated from making suggestions/accusations; skipping turn.")
            index = (index + 1) % len(selected_players)
            continue

        print("\n------------------------------")
        print("Current player:", current_player)

        print(f"{current_player}'s cards: {', '.join(state['hand'])}")

        if state["seen_cards"]:
            print(f"{current_player} has previously seen: {', '.join(state['seen_cards'])}")

        acc_choice = input(f"{current_player}, do you want to make an accusation now? (y/N): ").strip().lower()
        if acc_choice == "y":
            accusation = prompt_accusation(current_player, characters, weapons, rooms)
            if check_accusation(accusation, solution_data):
                print(f"\nAccusation correct! {current_player} wins the game! 🎉")
                game_over = True
                break
            else:
                print(f"\nAccusation incorrect. {current_player} is eliminated from future suggestions/accusations.")
                state["active"] = False

                # Re-check if anyone remains active after elimination
                active_players = [p for p, s in player_states.items() if s["active"]]
                if not active_players:
                    print("\nAll players have been eliminated. No one solved the case. Game ends with no winner.")
                    game_over = True
                    break

                index = (index + 1) % len(selected_players)
                continue

        input(f"{current_player}, press Enter to roll the die.")
        die_roll = random.randint(1, 6)
        print(f"You rolled: {die_roll}")

        current_location = state["location"]
        reachable_rooms = limited_uniform_cost_search(mansion_graph, current_location, die_roll)

        print(f"From '{current_location}', you can move to these rooms (cost ≤ {die_roll}):")
        for room, cost in reachable_rooms:
            print(f"  - {room} (cost {cost})")

        valid_moves = {room for room, cost in reachable_rooms}
        while True:
            move_choice = input(f"{current_player}, enter the room you want to move to: ").strip()
            if move_choice in valid_moves:
                state["location"] = move_choice
                state["history"].append(move_choice)
                print(f"{current_player} moved to {move_choice}")
                break
            else:
                print("Invalid move. Please choose a room from the list above.")

        current_room = state["location"]
        suggestion = prompt_suggestion(current_player, characters, weapons, current_room)
        process_suggestion(current_player, suggestion, player_states, selected_players, weapons_locations)

        acc_after = input(f"{current_player}, do you want to make an accusation now? (y/N): ").strip().lower()
        if acc_after == "y":
            accusation = prompt_accusation(current_player, characters, weapons, rooms)
            if check_accusation(accusation, solution_data):
                print(f"\nAccusation correct! {current_player} wins the game! 🎉")
                game_over = True
                break
            else:
                print(f"\nAccusation incorrect. {current_player} is eliminated from future suggestions/accusations.")
                state["active"] = False

                # Re-check for last active player
                active_players = [p for p, s in player_states.items() if s["active"]]
                if not active_players:
                    print("\nAll players have been eliminated. No one solved the case. Game ends with no winner.")
                    game_over = True
                    break

        index = (index + 1) % len(selected_players)

