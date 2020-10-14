def node_tidy(node, tree):
    """recursive routine to remove inessential nodes from a tree """
    if not node in tree: # terminal node
        return node
    # terminal (single) nodes (which in tree are [elements of] values but not keys) are always preserved
    
    for j, n in enumerate(tree[node]):
        m = node_tidy(n, tree)
        if not m == n:
            tree[node][j] = m # replace ref to inessential node
            tree[n] = -1 # mark as inessential (auxiliary)
        if len(tree[node]) == 1:
            return m #carry down the next node ref                                  
        else:            
            node_tidy(m, tree) # pick up where we left off, with the replacement node 
    return node # this line was the final piece of the jigsaw!
