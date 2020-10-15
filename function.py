def tree_tidy(root: int, tree: dict):
    """
    recursive routine to remove inessential nodes from a tree

    The tree is represented as a dict of nodes, whose keys are the node
    numbers and whose values are either a list of keys of connectyed nodes or
    -1.
    """
    if root not in tree: # terminal node
        return root
    # terminal (single) nodes (which in tree are [elements of] values but not keys) are always preserved

    for j, n in enumerate(tree[root]):
        m = tree_tidy(n, tree)
        if m != n:
            tree[root][j] = m # replace ref to inessential node
            tree[n] = -1 # mark as inessential (auxiliary)
        if len(tree[root]) == 1:
            return m #carry down the next node ref
        else:
            tree_tidy(m, tree) # pick up where we left off, with the replacement node
    return root # this line was the final piece of the jigsaw!

def tree_tidy2(root, i_tree):
    """
    Take a rooted tree and return another rooted tree in which all essential
    nodes index an empty list.
    """
    if root not in i_tree:
        return root
    for current in i_tree[root]:
        while len(i_tree[current]) == 1:
            i_tree[current], current = [], i_tree[current][0]
        i_tree[current] = tree_tidy(current, i_tree[current])
    return root
