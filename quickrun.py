from function import tree_tidy, Node, tree_to_nodes

tree = {1: [2, 3], 2: [4], 4: [5], 5: [6, 7], 3: [8, 9, 10]}
ntree = tree_to_nodes(tree, 1)
print("\n\n--- Raw ---", ntree.pretty(), sep="\n")
ntree.tidy()
print("\n\n--- Tidy ---", ntree.pretty(), sep="\n")

Node.reset()
ntree = tree_to_nodes({1: [2]}, 1)
print("\n\n--- Raw problem case ---", ntree.pretty(), sep="\n")
ntree.tidy()
print("\n\n--- Tidied problem case ---", ntree.pretty(), sep="\n")
