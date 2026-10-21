import heapq
import uuid
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import networkx as nx

MIN_HEAP_PATH = Path(__file__).with_name("min_heap.png")
MAX_HEAP_PATH = Path(__file__).with_name("max_heap.png")


class Node:
    """A binary tree node with a color and a unique id for drawing."""

    def __init__(self, key: int, color: str = "skyblue") -> None:
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


def draw_tree(tree_root: Node, title: str, save_path: Path) -> None:
    """Draw the binary tree, save the picture and show it."""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    plt.figure(figsize=(8, 5))
    plt.title(title)
    nx.draw(
        tree, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors
    )
    plt.margins(0.1)
    plt.savefig(save_path, dpi=100)
    plt.show()


def heap_to_tree(heap: list[int], index: int = 0) -> Optional[Node]:
    """Build a tree from a heap array.

    The children of the item with index i have indexes 2 * i + 1 and 2 * i + 2.
    """
    if index >= len(heap):
        return None
    node = Node(heap[index])
    node.left = heap_to_tree(heap, 2 * index + 1)
    node.right = heap_to_tree(heap, 2 * index + 2)
    return node


def draw_heap(heap: list[int], title: str, save_path: Path) -> None:
    """Visualize a binary heap as a tree."""
    root = heap_to_tree(heap)
    if root is None:
        print("The heap is empty, nothing to draw")
        return
    draw_tree(root, title, save_path)


if __name__ == "__main__":
    values = [7, 3, 15, 1, 9, 20, 4, 12, 5, 8]
    print(f"Values:   {values}")

    min_heap = values.copy()
    heapq.heapify(min_heap)
    print(f"Min-heap: {min_heap}")
    draw_heap(min_heap, "Min-heap", MIN_HEAP_PATH)

    max_heap = [-value for value in values]
    heapq.heapify(max_heap)
    max_heap = [-value for value in max_heap]
    print(f"Max-heap: {max_heap}")
    draw_heap(max_heap, "Max-heap", MAX_HEAP_PATH)

    draw_heap([], "Empty heap", MIN_HEAP_PATH)
