from itertools import count

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


class Node:
    """
    Represent a node in a tree. Each node is the root of a tree with zero or
    more inessential nodes (defining a sequence of nodes from the root to the
    first essential node) and a set of zero, two or more child nodes (nodes
    with exactly one child are non-essential).

    Each node is identified by a number. If not assigned by the caller a
    sequence of ids is internall generated. To handle asynchronous
    parallelism there should be a lock around the class `ids` attribute.

    The class also maintains a dict of instances to guard against the
    duplication of ids..
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
        Create an instance with given inessntial and child nodes.
        """
        self.iness = [] if iness is None else iness
        self.children = [] if children is None else children
        self.id = next(self.ids) if nid is None else nid
        if self.id in self.instances:
            raise ValueError(f"Node with id {self.id} already exists!")
        self.instances[self.id] = self

    def add_child(self, n):
        self.children.append(n)

    def add_iness(self, n):
        self.iness,append(n)

    def __repr__(self):
        return f"""<Node {self.id},
        iness={[i for i in self.iness]},
        children={[c for c in self.children]}>"""

    def tidy(self):
        assert not self.iness, "Cannot tidy a tree more than once"
        new_children = []
        for child in self.children:
            while len(child.children) == 1:
                self.iness.append(child)
                child = child.children[0]
            new_children.append(child)
        self.children = new_children


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

