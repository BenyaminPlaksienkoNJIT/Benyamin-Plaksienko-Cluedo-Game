import random
import json
from pathlib import Path
import argparse

def read_cards(filename):
    path = Path(filename)
    if not path.is_file():
        raise FileNotFoundError(f"{filename} does not exist.")
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def deal_cards(room_file, weapon_file, character_file,
               solution_file, hands_file, seed=None, active_players=None):
    if seed is not None:
        random.seed(seed)

    rooms = read_cards(room_file)
    weapons = read_cards(weapon_file)
    characters = read_cards(character_file)

    if not rooms or not weapons or not characters:
        raise ValueError("One of the input files is empty.")

    # Choose solution cards
    solution_room = random.choice(rooms)
    solution_weapon = random.choice(weapons)
    solution_character = random.choice(characters)

    # Prepare remaining cards (excluding solution)
    remaining = []
    remaining += [r for r in rooms if r != solution_room]
    remaining += [w for w in weapons if w != solution_weapon]
    remaining += [c for c in characters if c != solution_character]

    random.shuffle(remaining)

    # Determine active players
    if active_players is None:
        players = characters[:]
    else:
        if isinstance(active_players, int):
            if active_players > len(characters):
                raise ValueError(f"Requested {active_players} players but only {len(characters)} characters available.")
            players = random.sample(characters, active_players)
        else:
            players = active_players

    hands = {player: [] for player in players}

    # Deal cards evenly among active players (round-robin)
    for idx, card in enumerate(remaining):
        player = players[idx % len(players)]
        hands[player].append(card)

    # Sort each player's hand
    for hand in hands.values():
        hand.sort()


    solution_data = {
        "room": solution_room,
        "weapon": solution_weapon,
        "character": solution_character
    }
    with open(solution_file, "w", encoding="utf-8") as f:
        json.dump(solution_data, f, indent=2)

    # Save hands
    with open(hands_file, "w", encoding="utf-8") as f:
        json.dump(hands, f, indent=2)


    return solution_data, hands

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Cluedo solution and deal remaining cards (excluding the solution)."
    )
    parser.add_argument("--rooms", default="Room.txt",
                        help="Path to rooms list file.")
    parser.add_argument("--weapons", default="Weapon.txt",
                        help="Path to weapons list file.")
    parser.add_argument("--characters", default="Character.txt",
                        help="Path to characters list file (also the players).")
    parser.add_argument("--solution-out", default="solution.json",
                        help="Output file for the hidden solution.")
    parser.add_argument("--hands-out", default="hands.json",
                        help="Output file for dealt hands.")
    parser.add_argument("--seed", type=int, default=None,
                        help="Optional random seed for reproducibility.")
    parser.add_argument("--players", type=int, default=None,
                        help="Number of active players to deal cards to (default all).")
    args = parser.parse_args()

    deal_cards(
        room_file=args.rooms,
        weapon_file=args.weapons,
        character_file=args.characters,
        solution_file=args.solution_out,
        hands_file=args.hands_out,
        seed=args.seed,
        active_players=args.players
    )
