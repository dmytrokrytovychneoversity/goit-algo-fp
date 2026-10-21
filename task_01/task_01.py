from typing import Iterable, Optional


class Node:
    """A node of a singly linked list."""

    def __init__(self, data: int) -> None:
        self.data = data
        self.next: Optional["Node"] = None


class LinkedList:
    """A singly linked list."""

    def __init__(self, values: Iterable[int] = ()) -> None:
        self.head: Optional[Node] = None
        for value in values:
            self.insert_at_end(value)

    def insert_at_beginning(self, data: int) -> None:
        """Add a node to the beginning of the list."""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data: int) -> None:
        """Add a node to the end of the list."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def to_list(self) -> list[int]:
        """Return the list values as a Python list."""
        values = []
        current = self.head
        while current:
            values.append(current.data)
            current = current.next
        return values

    def __str__(self) -> str:
        values = " -> ".join(str(value) for value in self.to_list())
        return values if values else "empty"


def reverse(linked_list: LinkedList) -> None:
    """Reverse the list in place by changing the node links."""
    previous = None
    current = linked_list.head
    while current:
        next_node = current.next
        current.next = previous
        previous = current
        current = next_node
    linked_list.head = previous


def merge_nodes(first: Optional[Node], second: Optional[Node]) -> Optional[Node]:
    """Merge two sorted chains of nodes and return the new head."""
    dummy = Node(0)
    tail = dummy
    while first and second:
        if first.data <= second.data:
            tail.next = first
            first = first.next
        else:
            tail.next = second
            second = second.next
        tail = tail.next
    tail.next = first if first else second
    return dummy.next


def split(head: Node) -> Optional[Node]:
    """Cut the chain in the middle and return the head of the second half."""
    slow = head
    fast = head.next
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    middle = slow.next
    slow.next = None
    return middle


def merge_sort_nodes(head: Optional[Node]) -> Optional[Node]:
    """Sort a chain of nodes with merge sort and return the new head."""
    if head is None or head.next is None:
        return head
    middle = split(head)
    left = merge_sort_nodes(head)
    right = merge_sort_nodes(middle)
    return merge_nodes(left, right)


def merge_sort(linked_list: LinkedList) -> None:
    """Sort the list in place with merge sort."""
    linked_list.head = merge_sort_nodes(linked_list.head)


def merge_sorted(first: LinkedList, second: LinkedList) -> LinkedList:
    """Merge two sorted lists into one sorted list.

    The nodes are moved to the new list, so both input lists become empty.
    """
    result = LinkedList()
    result.head = merge_nodes(first.head, second.head)
    first.head = None
    second.head = None
    return result


if __name__ == "__main__":
    print("Reverse")
    for values in ([1, 2, 3, 4, 5], [7], []):
        linked_list = LinkedList(values)
        print(f"  {linked_list}", end="")
        reverse(linked_list)
        print(f"  =>  {linked_list}")

    print("\nMerge sort")
    for values in ([5, 2, 9, 1, 5, 6, -3], [3, 2, 1], [1], []):
        linked_list = LinkedList(values)
        print(f"  {linked_list}", end="")
        merge_sort(linked_list)
        print(f"  =>  {linked_list}")

    print("\nMerge two sorted lists")
    for first_values, second_values in (
        ([1, 4, 7, 10], [2, 3, 8]),
        ([1, 2], []),
        ([], []),
    ):
        first = LinkedList(first_values)
        second = LinkedList(second_values)
        print(f"  {first}  +  {second}", end="")
        print(f"  =>  {merge_sorted(first, second)}")
