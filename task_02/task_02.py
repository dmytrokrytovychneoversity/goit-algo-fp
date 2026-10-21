import argparse
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

PLOT_PATH = Path(__file__).with_name("pythagoras_tree.png")
MAX_LEVEL = 15
DEFAULT_LEVEL = 8
BRANCH_ANGLE = math.pi / 4
LENGTH_RATIO = math.sqrt(2) / 2

Point = tuple[float, float]
Segment = tuple[Point, Point]


def build_tree(
    x: float,
    y: float,
    angle: float,
    length: float,
    level: int,
    segments: list[Segment],
) -> None:
    """Add a branch and recursively add two smaller branches on its end."""
    end_x = x + length * math.cos(angle)
    end_y = y + length * math.sin(angle)
    segments.append(((x, y), (end_x, end_y)))
    if level == 0:
        return
    next_length = length * LENGTH_RATIO
    build_tree(end_x, end_y, angle + BRANCH_ANGLE, next_length, level - 1, segments)
    build_tree(end_x, end_y, angle - BRANCH_ANGLE, next_length, level - 1, segments)


def draw_tree(level: int) -> None:
    """Draw the Pythagoras tree with the given recursion level."""
    segments: list[Segment] = []
    build_tree(0, 0, math.pi / 2, 1, level, segments)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.add_collection(LineCollection(segments, colors="brown", linewidths=1))
    ax.autoscale()
    ax.set_title(f"Pythagoras tree, recursion level {level}")
    ax.set_aspect("equal")
    ax.axis("off")
    fig.savefig(PLOT_PATH, dpi=120)
    print(f"Branches: {len(segments)}. Plot saved to {PLOT_PATH.name}")
    plt.show()


def read_level() -> int:
    """Ask the user for the recursion level."""
    answer = input(f"Enter recursion level 0-{MAX_LEVEL} [{DEFAULT_LEVEL}]: ")
    return int(answer) if answer.strip() else DEFAULT_LEVEL


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Draw the Pythagoras tree.")
    parser.add_argument("--level", type=int, help=f"recursion level 0-{MAX_LEVEL}")
    args = parser.parse_args()

    try:
        level = args.level if args.level is not None else read_level()
    except ValueError:
        parser.error("the level must be an integer")
    if not 0 <= level <= MAX_LEVEL:
        parser.error(f"the level must be from 0 to {MAX_LEVEL}")

    draw_tree(level)
