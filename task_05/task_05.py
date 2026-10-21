import heapq
import uuid
from collections import deque
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import networkx as nx

DFS_PATH = Path(__file__).with_name("dfs.png")
BFS_PATH = Path(__file__).with_name("bfs.png")
STEP_DELAY = 0.7
UNVISITED_COLOR = "#FFFFFF"
DARK_COLOR = (0x0B, 0x24, 0x4A)
LIGHT_COLOR = (0xCF, 0xEA, 0xFF)


class Node:
    """A binary tree node with a color and a unique id for drawing."""

    def __init__(self, key: int, color: str = UNVISITED_COLOR) -> None:
        self.left: Optional["Node"] = None
        self.right: Optional["Node"] = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(
    graph: nx.DiGraph,
    node: Optional[Node],
    pos: dict[str, tuple[float, float]],
    x: float = 0,
    y: float = 0,
    layer: int = 1,
) -> nx.DiGraph:
    """Add the node, its children and their positions to the graph."""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            left_x = x - 1 / 2**layer
            pos[node.left.id] = (left_x, y - 1)
            add_edges(graph, node.left, pos, x=left_x, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            right_x = x + 1 / 2**layer
            pos[node.right.id] = (right_x, y - 1)
            add_edges(graph, node.right, pos, x=right_x, y=y - 1, layer=layer + 1)
    return graph


def heap_to_tree(heap: list[int], index: int = 0) -> Optional[Node]:
    """Build a tree from a heap array."""
    if index >= len(heap):
        return None
    node = Node(heap[index])
    node.left = heap_to_tree(heap, 2 * index + 1)
    node.right = heap_to_tree(heap, 2 * index + 2)
    return node


def dfs(root: Optional[Node]) -> list[Node]:
    """Return the nodes in depth-first order. Use a stack."""
    order = []
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        order.append(node)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order


def bfs(root: Optional[Node]) -> list[Node]:
    """Return the nodes in breadth-first order. Use a queue."""
    order = []
    queue = deque([root] if root else [])
    while queue:
        node = queue.popleft()
        order.append(node)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return order


def generate_colors(count: int) -> list[str]:
    """Return count colors in #RRGGBB format from dark to light."""
    colors = []
    for step in range(count):
        ratio = step / (count - 1) if count > 1 else 0
        channels = [
            round(dark + (light - dark) * ratio)
            for dark, light in zip(DARK_COLOR, LIGHT_COLOR)
        ]
        colors.append("#{:02X}{:02X}{:02X}".format(*channels))
    return colors


def is_dark(color: str) -> bool:
    """Check if a #RRGGBB color needs white text on it."""
    red, green, blue = (int(color[i : i + 2], 16) for i in (1, 3, 5))
    return 0.299 * red + 0.587 * green + 0.114 * blue < 140


def draw_step(ax: plt.Axes, root: Node, title: str) -> None:
    """Draw the tree with the current node colors."""
    tree = nx.DiGraph()
    pos = {root.id: (0, 0)}
    tree = add_edges(tree, root, pos)
    nodes = tree.nodes(data=True)

    ax.clear()
    ax.set_title(title)
    nx.draw_networkx_edges(tree, pos=pos, ax=ax, arrows=False)
    nx.draw_networkx_nodes(
        tree,
        pos=pos,
        ax=ax,
        node_size=2000,
        node_color=[data["color"] for _, data in nodes],
        edgecolors="#0B244A",
    )
    for dark in (True, False):
        labels = {
            node_id: data["label"]
            for node_id, data in nodes
            if is_dark(data["color"]) == dark
        }
        nx.draw_networkx_labels(
            tree,
            pos=pos,
            ax=ax,
            labels=labels,
            font_color="white" if dark else "black",
        )
    ax.margins(0.1)
    ax.axis("off")


def visualize_traversal(root: Node, order: list[Node], name: str, path: Path) -> None:
    """Color the nodes one by one in traversal order and show every step."""
    colors = generate_colors(len(order))
    fig, ax = plt.subplots(figsize=(8, 5))
    draw_step(ax, root, f"{name}: start")
    plt.pause(STEP_DELAY)
    for step, (node, color) in enumerate(zip(order, colors), start=1):
        node.color = color
        draw_step(ax, root, f"{name}: step {step}, node {node.val}, color {color}")
        plt.pause(STEP_DELAY)

    draw_step(ax, root, f"{name}: " + " -> ".join(str(node.val) for node in order))
    fig.savefig(path, dpi=100)
    plt.show()


if __name__ == "__main__":
    heap = [7, 3, 15, 1, 9, 20, 4, 12, 5, 8]
    heapq.heapify(heap)
    print(f"Heap: {heap}")

    for name, traversal, path in (("DFS", dfs, DFS_PATH), ("BFS", bfs, BFS_PATH)):
        root = heap_to_tree(heap)
        order = traversal(root)
        colors = generate_colors(len(order))
        print(f"\n{name} order: {[node.val for node in order]}")
        print(f"{name} colors: {colors}")
        visualize_traversal(root, order, name, path)
