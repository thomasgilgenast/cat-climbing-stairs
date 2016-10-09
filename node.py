from itertools import combinations_with_replacement
from math import factorial
from operator import mul


def explore(d, limit=None):
    """
    Explore what new collections of numbers can be created by summing two
    elements of the passed collection of numbers, represented as a dict.

    Parameters
    ----------
    d : Dict[int, int]
        Dict representation of a collection of numbers to explore sums of.
    limit : Optional[int]
        Don't allow any sums to be bigger than this number.

    Returns
    -------
    List[Dict[int, int]]
        Dicts representing all the possible unique results of summing two
        elements of the collection represented by ``d``, honoring ``limit``.
    """
    children = []
    for i, j in combinations_with_replacement(d.keys(), 2):
        if i == j and d[i] < 2:
            continue
        if limit is not None and i + j > limit:
            continue
        c = d.copy()
        c[i] -= 1
        if c[i] == 0:
            del c[i]
        c[j] -= 1
        if c[j] == 0:
            del c[j]
        if i+j not in c:
            c[i+j] = 0
        c[i+j] += 1
        children.append(c)
    return children


def build_tree(root_d, limit=None):
    """
    Builds out a tree of Nodes starting from a root collection, represented as
    a dict.

    Parameters
    ----------
    root_d : Dict[int, int]
        The root collection of numbers, repserented as a dict.
    limit : Optional[int]
        Don't allow any element in any Node in the tree to be bigger than this
        number.

    Returns
    -------
    Node
        The root node of the constructed tree.

    Notes
    -----
    This function will print out tkiz-compatible graph notation while
    constructing the graph. It will also print the total number of permutations
    for the cat jumping problem at the end of its output.
    """
    node_table = {}

    class Node(object):
        def __init__(self, d, p):
            self.d = d
            self.t = tuple(sorted([k for k in d for _ in xrange(d[k])]))
            if p is not None:
                print ('%s -> %s;' % (p.t, self.t)).replace('(', '"')\
                    .replace(')', '"')
            self.c = []
            self.p = []
            if self.t in node_table:
                node_table[self.t].p.append(p)
            else:
                if p is not None:
                    self.p.append(p)
                node_table[self.t] = self
                children = explore(d, limit=limit)
                for c in children:
                    self.c.append(Node(c, self))

        def __str__(self):
            return 'Node'+str(self.t)

        def __repr__(self):
            return 'Node'+str(self.t)

    root_node = Node(root_d, None)

    print sum([(factorial(sum(n.d.values()))) /
               (reduce(mul, [factorial(v) for v in n.d.values()]))
               for n in node_table.values()])

    return root_node
