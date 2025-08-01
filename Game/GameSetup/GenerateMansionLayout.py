import random
import json

def load_rooms(filename):
    with open(filename, 'r') as f:
        rooms = [line.strip() for line in f if line.strip()]
    return rooms

def generate_random_weighted_graph_with_secrets(rooms, seed=42, max_edges_per_room=5, max_cost=10, secret_chance=0.2):
    random.seed(seed)
    graph = {room: {} for room in rooms}

    for room in rooms:
        num_edges = random.randint(1, max_edges_per_room)
        possible_targets = [r for r in rooms if r != room and r not in graph[room]]
        edges = random.sample(possible_targets, min(num_edges, len(possible_targets)))

        for target in edges:
            # Decide if this edge is a secret passage (cost = 0)
            if random.random() < secret_chance:
                cost = 0  # secret passage
            else:
                cost = random.randint(1, max_cost)
            graph[room][target] = cost
            graph[target][room] = cost
    return graph

def print_weighted_graph(graph):
    for room, neighbors in graph.items():
        edges_str = ', '.join([f"{nbr} (cost: {cost}{' - Secret Passage' if cost == 0 else ''})"
                               for nbr, cost in neighbors.items()])
        print(f"{room}: {edges_str}")

def save_graph_to_json(graph, filename):
    with open(filename, 'w') as f:
        json.dump(graph, f, indent=2)

def load_graph_from_json(filename):
    with open(filename, 'r') as f:
        graph = json.load(f)
    return graph

if __name__ == "__main__":
    rooms = load_rooms("Room.txt")
    mansion_graph = generate_random_weighted_graph_with_secrets(rooms, seed=123, secret_chance=0.25)
    save_graph_to_json(mansion_graph, "mansion_layout.json")
    loaded_graph = load_graph_from_json("mansion_layout.json")
    print_weighted_graph(loaded_graph)
