import heapq
import math
from typing import Optional

Graph = dict[str, dict[str, int]]


def create_graph() -> Graph:
    """Create a weighted undirected graph of roads between cities."""
    roads = [
        ("Kyiv", "Zhytomyr", 140),
        ("Kyiv", "Vinnytsia", 290),
        ("Kyiv", "Poltava", 340),
        ("Kyiv", "Cherkasy", 190),
        ("Zhytomyr", "Rivne", 190),
        ("Zhytomyr", "Vinnytsia", 130),
        ("Rivne", "Lviv", 210),
        ("Vinnytsia", "Khmelnytskyi", 120),
        ("Khmelnytskyi", "Ternopil", 110),
        ("Ternopil", "Lviv", 130),
        ("Cherkasy", "Poltava", 240),
        ("Poltava", "Kharkiv", 140),
        ("Cherkasy", "Dnipro", 300),
        ("Poltava", "Dnipro", 190),
    ]
    graph: Graph = {}
    for city_a, city_b, distance in roads:
        graph.setdefault(city_a, {})[city_b] = distance
        graph.setdefault(city_b, {})[city_a] = distance
    graph["Uzhhorod"] = {}
    return graph


def dijkstra(
    graph: Graph, start: str
) -> tuple[dict[str, float], dict[str, Optional[str]]]:
    """Find the shortest distances from start to all vertices with a binary heap.

    Return the distances and the previous vertex on the shortest path.
    """
    if start not in graph:
        raise ValueError(f"Unknown start vertex: {start}")

    distances = {vertex: math.inf for vertex in graph}
    previous: dict[str, Optional[str]] = {vertex: None for vertex in graph}
    distances[start] = 0
    heap = [(0, start)]

    while heap:
        current_distance, vertex = heapq.heappop(heap)
        if current_distance > distances[vertex]:
            continue
        for neighbor, weight in graph[vertex].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = vertex
                heapq.heappush(heap, (distance, neighbor))

    return distances, previous


def get_path(previous: dict[str, Optional[str]], target: str) -> list[str]:
    """Restore the path to target from the previous vertex table."""
    path = []
    vertex: Optional[str] = target
    while vertex is not None:
        path.append(vertex)
        vertex = previous[vertex]
    return path[::-1]


if __name__ == "__main__":
    graph = create_graph()
    start = "Kyiv"
    distances, previous = dijkstra(graph, start)

    print(f"Shortest paths from {start}:")
    for city in sorted(graph, key=lambda name: distances[name]):
        if distances[city] == math.inf:
            print(f"  {city:<13} unreachable")
            continue
        path = " -> ".join(get_path(previous, city))
        print(f"  {city:<13} {distances[city]:>4} km  {path}")
