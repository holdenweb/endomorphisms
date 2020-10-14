def tree_tidy(root, tree):
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

