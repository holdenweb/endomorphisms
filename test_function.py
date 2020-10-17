from function import tree_tidy, Node, tree_to_nodes, nodes_to_tree

def test_davids_first_example():
    """
    Verify the canoncial example from David.
    """
    tree = {1: [2, 3], 2: [4], 4: [5], 5: [6, 7], 3: [8, 9, 10]}
    assert verify_mapping(tree, 1) == ""
    root = tree_tidy(1, tree)
    assert root == 1
    assert tree == {1: [5, 3], 2: [], 4: [], 5: [6, 7], 3: [8, 9, 10]}

def test_degenerate_case():
    tree = tree_to_nodes({1: [2]}, 1)
    new_tree = tree.tidied()
    assert new_tree.id  == 2
    assert len(new_tree.iness) == 1
    assert new_tree.iness[0].id ==1


def verify_mapping(m, root):
    keys = set()
    values = set()
    for k, v in m.items():
        keys.add(k)
        for vv in v:
            values.add(vv)
    keys.discard(root)
    if all(k in values for k in keys):
        return ""
    else:
        return f"Keys {sorted(keys-{root})} Values {sorted(values)}"


def test_tree_to_nodes():
    Node.reset()
    tree = {1:[2]}
    ntree = tree_to_nodes(tree, 1)
    assert ntree.id == 1
    assert len(ntree.children) == 1
    assert ntree.children[0].id == 2
    Node.reset()
    tree = {1: [2, 3], 2: [4], 4: [5], 5: [6, 7], 3: [8, 9, 10]}
    ntree = tree_to_nodes(tree, 1)


def test_nodes_to_tree():
    Node.reset()
    tree = {1: [2, 3], 2: [4], 4: [5], 5: [6, 7], 3: [8, 9, 10]}
    root = 1
    ntree = tree_to_nodes(tree, root)
    nntree, nnroot =  nodes_to_tree(ntree)
    assert nntree == tree
    assert nnroot == root

def test_nodes_are_sequenced():
    """
    If automatic numbering is used, care must be taken to avoid
    conflict between automatic numbers and those specified explicitly
    by the caller.
    """
    Node.reset()
    a = Node()
    b = Node()
    c = Node()
    assert (a.id, b.id, c.id) == (1, 2, 3)

if __name__ == '__main__':
    test_nodes_to_tree()
