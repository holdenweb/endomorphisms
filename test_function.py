from function import tipless, tree_tidy, Node, Tree, tree_to_nodes, nodes_to_tree, verify_mapping


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



def test_tree_to_nodes():
    tree = {1:[2]}
    ntree = tree_to_nodes(tree, 1)
    assert ntree.id == 1
    assert len(ntree.children) == 1
    assert ntree.children[0].id == 2
    tree = {1: [2, 3], 2: [4], 4: [5], 5: [6, 7], 3: [8, 9, 10]}
    ntree = tree_to_nodes(tree, 1)


def test_nodes_to_tree():
    tree = {1: [2, 3], 2: [4], 4: [5], 5: [6, 7], 3: [8, 9, 10]}
    root = 1
    ntree = tree_to_nodes(tree, root)
    nntree, nnroot =  nodes_to_tree(ntree)
    assert tipless(nntree) == tree
    assert nnroot == root

def test_various_manipulations():
    my_tree = {1: [2]}
    ntree = tree_to_nodes(my_tree, 1)
    nttree, new_root = nodes_to_tree(ntree)
    # print("Original tree", ntree.pretty(), sep='\n')
    assert len(nttree) == 2
    assert new_root == 1
    assert set(ntree.tree.instances.keys()) == {1, 2}
    assert tipless(nttree) == my_tree
    ntree = ntree.tidied()
    # print("Tidied version:", ntree.pretty(), sep='\n')
    assert set(ntree.tree.instances.keys()) == {1, 2}
    # Note the the tree correctly renders as "Node 2 (1)",
    # Implying the tidied tree has 2 as the root and that
    # Node 1 is inessential.
    ndtree, new_root = nodes_to_tree(ntree)
    assert len(ndtree) == 2
    assert new_root == 2
    assert len(ndtree) == 2
    assert nttree == {1: [2], 2: []}

def test_nodes_are_sequenced():
    """
    If automatic numbering is used, care must be taken to avoid
    conflict between automatic numbers and those specified explicitly
    by the caller.
    """
    tree = Tree()
    a = tree.node()
    b = tree.node()
    c = tree.node()
    assert (a.id, b.id, c.id) == (1, 2, 3)

if __name__ == '__main__':
    test_various_manipulations()
