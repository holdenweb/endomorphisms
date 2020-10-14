from function import tree_tidy

def test_davids_first_example():
    """
    Verify the canoncial example from David.
    """
    tree = {1: [2, 3], 2: [4], 4: [5], 5: [6, 7], 3: [8, 9, 10]}
    root = tree_tidy(1, tree)
    assert root == 1
    assert tree == {1: [5, 3], 2: -1, 4: -1, 5: [6, 7], 3: [8, 9, 10]}
