Items = dict[str, dict[str, int]]

ITEMS: Items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350},
}


def check_budget(budget: int) -> None:
    """Raise ValueError for a negative budget."""
    if budget < 0:
        raise ValueError("The budget cannot be negative")


def greedy_algorithm(items: Items, budget: int) -> list[str]:
    """Choose dishes with the best calories to cost ratio first."""
    check_budget(budget)
    ranked = sorted(
        items,
        key=lambda name: items[name]["calories"] / items[name]["cost"],
        reverse=True,
    )
    chosen = []
    money_left = budget
    for name in ranked:
        if items[name]["cost"] <= money_left:
            chosen.append(name)
            money_left -= items[name]["cost"]
    return chosen


def dynamic_programming(items: Items, budget: int) -> list[str]:
    """Find the dishes with the maximum total calories within the budget.

    Each dish can be taken only once (0/1 knapsack problem).
    """
    check_budget(budget)
    names = list(items)
    # table[i][b] - max calories with the first i dishes and budget b
    table = [[0] * (budget + 1) for _ in range(len(names) + 1)]

    for i, name in enumerate(names, start=1):
        cost = items[name]["cost"]
        calories = items[name]["calories"]
        for money in range(budget + 1):
            table[i][money] = table[i - 1][money]
            if cost <= money:
                with_dish = table[i - 1][money - cost] + calories
                table[i][money] = max(table[i][money], with_dish)

    chosen = []
    money = budget
    for i in range(len(names), 0, -1):
        if table[i][money] != table[i - 1][money]:
            name = names[i - 1]
            chosen.append(name)
            money -= items[name]["cost"]
    return chosen[::-1]


def describe(items: Items, chosen: list[str]) -> str:
    """Return the dishes with their total cost and calories."""
    cost = sum(items[name]["cost"] for name in chosen)
    calories = sum(items[name]["calories"] for name in chosen)
    return f"{chosen}, cost {cost}, calories {calories}"


if __name__ == "__main__":
    for budget in (0, 30, 50, 100, 150):
        print(f"Budget {budget}")
        print(f"  greedy: {describe(ITEMS, greedy_algorithm(ITEMS, budget))}")
        print(f"  DP:     {describe(ITEMS, dynamic_programming(ITEMS, budget))}")

    try:
        greedy_algorithm(ITEMS, -10)
    except ValueError as error:
        print(f"Budget -10: {error}")
