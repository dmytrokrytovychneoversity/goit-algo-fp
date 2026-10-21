import random
from pathlib import Path

import matplotlib.pyplot as plt

PLOT_PATH = Path(__file__).with_name("dice_probabilities.png")
SEED = 42
THROWS = 1_000_000
SUMS = range(2, 13)


def simulate_throws(throws: int, rng: random.Random) -> dict[int, int]:
    """Throw two dice many times and count how often each sum appears."""
    counts = {total: 0 for total in SUMS}
    for _ in range(throws):
        total = rng.randint(1, 6) + rng.randint(1, 6)
        counts[total] += 1
    return counts


def monte_carlo_probabilities(throws: int, rng: random.Random) -> dict[int, float]:
    """Estimate the probability of each sum with the Monte Carlo method."""
    if throws <= 0:
        raise ValueError("The number of throws must be positive")
    counts = simulate_throws(throws, rng)
    return {total: count / throws for total, count in counts.items()}


def analytical_probabilities() -> dict[int, float]:
    """Count the exact probabilities over all 36 outcomes."""
    counts = {total: 0 for total in SUMS}
    for first in range(1, 7):
        for second in range(1, 7):
            counts[first + second] += 1
    return {total: count / 36 for total, count in counts.items()}


def print_table(simulated: dict[int, float], exact: dict[int, float]) -> None:
    """Print simulated and exact probabilities side by side."""
    print(f"{'Sum':>3} | {'Monte Carlo':>11} | {'Analytical':>10} | {'Difference':>10}")
    print("-" * 45)
    for total in SUMS:
        difference = simulated[total] - exact[total]
        print(
            f"{total:>3} | {simulated[total]:>11.2%} | {exact[total]:>10.2%} "
            f"| {difference:>+10.2%}"
        )


def draw_plot(simulated: dict[int, float], exact: dict[int, float]) -> None:
    """Draw simulated probabilities as bars and exact ones as points."""
    sums = list(SUMS)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(sums, [simulated[total] * 100 for total in sums], label="Monte Carlo")
    ax.plot(
        sums,
        [exact[total] * 100 for total in sums],
        "o--",
        color="red",
        label="Analytical",
    )
    ax.set_xticks(sums)
    ax.set_xlabel("Sum of two dice")
    ax.set_ylabel("Probability, %")
    ax.set_title(f"Two dice, {THROWS:,} throws")
    ax.legend()
    fig.savefig(PLOT_PATH, dpi=100)
    plt.show()


if __name__ == "__main__":
    rng = random.Random(SEED)
    exact = analytical_probabilities()

    simulated = monte_carlo_probabilities(THROWS, rng)
    print(f"Throws: {THROWS:,}\n")
    print_table(simulated, exact)

    print("\nMax difference from the analytical values:")
    for throws in (100, 1_000, 10_000, 100_000, THROWS):
        estimate = monte_carlo_probabilities(throws, random.Random(SEED))
        max_difference = max(abs(estimate[total] - exact[total]) for total in SUMS)
        print(f"  {throws:>9,} throws: {max_difference:.2%}")

    draw_plot(simulated, exact)
