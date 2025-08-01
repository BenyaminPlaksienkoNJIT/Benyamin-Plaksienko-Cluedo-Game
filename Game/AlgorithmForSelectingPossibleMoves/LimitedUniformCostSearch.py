import json
from typing import Dict, List, Tuple
import heapq

#lucs for finding what rooms can go
def limited_uniform_cost_search(
        graph: Dict[str, Dict[str, int]],
        start: str,
        max_cost: int
) -> List[Tuple[str, int]]:

    frontier = []
    heapq.heappush(frontier, (0, start, False))

    reached = {(start, False): 0}
    results = {}

    while frontier:
        current_cost, current_node, used_secret = heapq.heappop(frontier)


        if current_node not in results or current_cost < results[current_node]:
            results[current_node] = current_cost

        for neighbor, step_cost in graph.get(current_node, {}).items():
            if step_cost == 0:
                if used_secret:
                    continue
                next_used_secret = True
            else:
                next_used_secret = False

            path_cost = current_cost + step_cost
            if path_cost > max_cost:
                continue

            state = (neighbor, next_used_secret)
            if state not in reached or path_cost < reached[state]:
                reached[state] = path_cost
                heapq.heappush(frontier, (path_cost, neighbor, next_used_secret))


    if start in results:
        del results[start]

    return sorted(results.items(), key=lambda x: x[1])



if __name__ == "__main__":
    graph_json = """
    {
      "Hall": {
        "Conservatory": 0,
        "Lounge": 1,
        "Dining Room": 7,
        "Kitchen": 8,
        "Ballroom": 0,
        "Billiard Room": 8
      },
      "Lounge": {
        "Conservatory": 6,
        "Hall": 1,
        "Library": 0,
        "Ballroom": 6
      },
      "Dining Room": {
        "Kitchen": 2,
        "Hall": 7,
        "Conservatory": 5,
        "Billiard Room": 9
      },
      "Kitchen": {
        "Dining Room": 2,
        "Hall": 8,
        "Conservatory": 7,
        "Study": 5
      },
      "Ballroom": {
        "Lounge": 6,
        "Hall": 0,
        "Library": 9,
        "Study": 3
      },
      "Conservatory": {
        "Hall": 0,
        "Lounge": 6,
        "Kitchen": 7,
        "Dining Room": 5,
        "Billiard Room": 6,
        "Study": 2
      },
      "Billiard Room": {
        "Hall": 8,
        "Library": 0,
        "Dining Room": 9,
        "Conservatory": 6
      },
      "Library": {
        "Lounge": 0,
        "Billiard Room": 0,
        "Ballroom": 9,
        "Study": 1
      },
      "Study": {
        "Library": 1,
        "Ballroom": 3,
        "Conservatory": 2,
        "Kitchen": 5
      }
    }
    """

    graph = json.loads(graph_json)

    start_room = "Hall"
    max_steps = 3

    reachable = limited_uniform_cost_search(graph, start_room, max_steps)
    print(f"Rooms reachable from '{start_room}' with cost ≤ {max_steps}:")
    for room, cost in reachable:
        print(f"  {room} at cost {cost}")
