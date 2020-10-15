from itertools import count

from function import tree_tidy, tree_tidy2

def test_davids_first_example():
    """
    Verify the canoncial example from David.
    """
    tree = {1: [2, 3], 2: [4], 4: [5], 5: [6, 7], 3: [8, 9, 10]}
    root = tree_tidy(1, tree)
    assert root == 1
    assert tree == {1: [5, 3], 2: -1, 4: -1, 5: [6, 7], 3: [8, 9, 10]}

def test_degenerate_case():
    tree = {1: [2], 2: []}
    root = tree_tidy(1, tree)
    assert root == 2
    assert tree == {1: [2], 2: []}

def test_steves_rewrite():
    """
    Same data, different algorithm - we'll parameterise this later.
    """
    tree = {1: [2, 3], 2: [4], 4: [5], 5: [6, 7], 3: [8, 9, 10]}
    root = tree_tidy2(1, tree)
    assert root == 1
    assert tree == {1: [5, 3], 2: -1, 4: -1, 5: [6, 7], 3: [8, 9, 10]}

class Node:
    """
    Represent a node in a tree. Each node is the root of a tree with zero or
    more inessential nodes (defining a sequence of nodes from the root to the
    first essential node) and a set of zero, two or more child nodes (nodes
    with exactly one child are non-essential).

    Each node is identified by a number. If not assigned by the caller a
    seequence of ids is internall generated. To handle asynchronous
    parallelism there should be a lock around the class `ids` attribute.
    """
    ids = count(1)
    def __init__(self, nid=None, iness=None, children=None):
        self.iness = [] if iness is None else iness
        self.children = [] if children is None else children
        self.id = next(self.ids) if nid is None else nid

def test_nodes_are_sequenced():
    """
    If automatic numbering is used, care must be taken to avoid
    conflict between automatic numbers and those specified explicitly
    by the caller.
    """
    a = Node()
    b = Node()
    c = Node()
    assert (a.id, b.id, c.id) == (1, 2, 3)

if __name__ == '__main__':
    test_davids_first_example()
    test_steves_rewrite()
