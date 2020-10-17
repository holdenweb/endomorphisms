from itertools import count

def tree_tidy(root: int, tree: dict):
    """
    Remove inessential nodes from a tree.

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
            tree[n] = [] # mark as inessential (auxiliary)
        if len(tree[root]) == 1:
            return m #carry down the next node ref
        else:
            tree_tidy(m, tree) # pick up where we left off, with the replacement node
    return root # this line was the final piece of the jigsaw!


class Node:
    """
    Represents a node in a tree. The initial representation explicity includes
    all arcs of the tree. Calling the tidy operation on a tree truncates the
    representation by populating the inessential nodes collection.

    After tidying each node is the root of a tree with zero or more
    inessential nodes (defining a sequence of nodes from the root to the
    first essential node) and a set of zero, two or more child nodes (nodes
    with exactly one child are non-essential).

    Each node is identified by a number. If not assigned by the caller a
    sequence of ids is internall generated. To handle asynchronous
    parallelism there should be a lock around the class `ids` attribute.

    The class also maintains a dict of instances to guard against the
    duplication of ids. This is a slightly ugly implementation as it forces
    us to re-initialise the colection for each new tree, but it serves until
    we have time to implement something better.
    """
    ids = count(1)
    instances = {}

    @classmethod
    def reset(cls):
        """
        Forget about any existing nodes.
        """
        cls.ids = count(1)
        cls.instances = {}

    def __init__(self, nid:int=None, iness: list=None, children: list=None):
        """
        Create an instance with given inessential and child nodes.
        Most usually during tree construction nodes will be created
        empty and with automtic numbering, but this may not always be the case.
        """
        self.iness = [] if iness is None else iness
        self.children = [] if children is None else children
        self.id = next(self.ids) if nid is None else nid
        if self.id in self.instances:
            raise ValueError(f"Node with id {self.id} already exists!")
        self.instances[self.id] = self

    def add_child(self, n):
        """
        Provide an opaque way to manage inessentials, isolating the caller
        from the implementation details of the node collection.
        """
        self.children.append(n)

    def add_iness(self, n):
        """
        Provide an opaque way to manage inessentials, isolating the caller
        fron the implementation details of the node collection.
        """
        self.iness.append(n)

    def __repr__(self):
        """
        Represent node as a string
        """
        return f"""<Node {self.id} - {len(self.iness)} inessential(s), {len(self.children)} child(ren)>"""

    def tidied(self):
        """
        Restructure the tree, collecting inessential nodes and removing them
        from the main tree. This recasting should allow us to handle the
        case when the input root node is inessential, when the root node
        will be the first essential node encountered, any intermediate
        inessential nodes being utlimately collected in the new root's
        `iness` collection. Since the root node may change, the method
        returns the new root.
        """
        iness = []
        root = self
        while len(root.children) == 1:  # Node is inessential
            iness.append(root)
            root = root.children[0]
            root.iness = iness
        return root if not root.children else root.tidied()


    def _pretty(self, pad):
        """
        Prettify a node with each line padded on the left.
        """
        children = iness = ""
        if self.children:    # Give the full structure of the child tree
            children = "".join(f"\n{c._pretty(pad+'| ')}" for c in self.children)
        if self.iness:       # Just list the Node names of inessentials
            iness =  ", ".join(f"{n.id}" for n in self.iness)
        return f"{pad}Node {self.id}: ({iness}){children}"

    def pretty(self):
        """
        Prettify with no initial padding.
        """
        return self._pretty("")

def tree_to_nodes(tree, root):
    """
    Given a tree in David's dict representation, convert it to
    a node-based representation.
    """
    root_node = Node(root)
    if root not in tree:
        return root_node
    for child in tree[root]:
        if child in tree:
            children = [tree_to_nodes(tree, grandchild)
                        for grandchild in tree[child]]
        else:
            children = []
        root_node.add_child(Node(nid=child,
                                 children=children
                                 )
                            )
    return root_node

def nodes_to_tree(root, tree=None):
    """
    Given a node tree, produce the equivalent dict.
    If the root has inessential nodes, the first
    of these becomes the new root, whose only child
    is the next inessential node and so on. The
    child of the final inessential node is the
    original root. This formula is then repeated
    recursively across the children.

    I have a feeling this code is non-optimal and it certainly
    needs more testing than it currently has.

    I've added more comment than is strictly necessary more
    to check my own logic than to guide readers.
    """
    tree = {} if tree is None else tree
    result = tree
    #
    # Before assembling the children of this node, we
    # need to ensure that all subtrees are already
    # correctly represented in the result.
    #
    for child in root.children:
        result, treeroot = nodes_to_tree(child, result)
    # Assemble the child ids
    children = [node.id for node in root.children]
    # Now re-root the current tree by working back
    # along the chain of inessential nodes.
    current_root = root
    while root.iness:  # re-root the tree at its first inessential node
        new_root = root.iness.pop(-1)
        result[new_root.id] = children
        children = [current_root.id]
        current_root = new_root
    # Terminal nodes should not be explicitly represented
    if children:
        result[root.id] = children
    # The result is now complete for this tree
    return result, root.id


