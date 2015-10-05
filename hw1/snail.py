# Usage: python snail.py input.txt
import itertools
import sys

class Node(object):
    def __init__(self, nodeid, parent_id, has_worm):
        self.nodeid = nodeid
        self.parent_id = parent_id
        self.has_worm = has_worm
        self.children = [] # list of node IDs
        # expectation[i] keeps the expectation of this node's subtree
        self.expectation = None
        # wasted_steps keeps the steps of traveling this node's subtree
        # WITHOUT finding the house
        self.wasted_steps = None
        # number of leaves in the subtree of this node
        self.num_leaves = None

    def __str__(self):
        return ','.join(['nodeid:', str(self.nodeid),
                     'parent_id:', str(self.parent_id),
                     'has_worm:', str(self.has_worm),
                     'children:', str([node.nodeid for node in self.children]),
                     'expectation:', str(self.expectation),
                     'wasted_steps:', str(self.wasted_steps),
                     'num_leaves:', str(self.num_leaves)
                     ])

def build_tree(nodes):
    tree_nodes = [None for i in range(len(nodes) + 1)]
    for nodeid, keypoint in enumerate(nodes, 1):
        parent_id = int(keypoint[0])
        has_worm = keypoint[1] == 'Y'
        node = Node(nodeid = nodeid, parent_id = parent_id,
                has_worm = has_worm)
        tree_nodes[nodeid] = node
        if parent_id != -1:
            tree_nodes[parent_id].children.append(node)

    # for node in tree_nodes:
        # print node

    return tree_nodes

def calc_expectation(node):
    """
    node is of class Node.
    """
    # check if node is a leaf (where the house might be)
    if len(node.children) == 0:
        # It is a leaf
        node.expectation = 0
        node.wasted_steps = 0
        node.num_leaves = 1
        return

    # This is NOT a leaf
    # We calculate the expectation and wasted_steps here

    # After this loop, every child should have node info ready
    for child in node.children:
        calc_expectation(child)
        # print child.nodeid

    node.num_leaves = sum([child.num_leaves for child in node.children])

    # We try all orders of child nodes and find the order that minimizes
    # the current node's expectation
    min_exp = None
    for strategy in itertools.permutations(node.children,
            len(node.children)):
        # strategy is a list: [Node, Node, Node ..]
        e_sum = 0.0 # e is the sum of expectations
        wasted = 0 # wasted steps for this strategy so far
        for i, child in enumerate(strategy):
            if i == 0:
                wasted = 1
            else:
                if strategy[i-1].has_worm == True:
                    # previous child has a worm, we don't need to go into
                    # the subtree
                    wasted += 0 + 2 # 2 is for going back from previous child and
                                    # then into the currennt child
                else:
                    # previous child has a worm, we need to travel into it
                    wasted += strategy[i-1].wasted_steps + 2
            e_sum += (child.expectation + wasted) * child.num_leaves

            if i == len(strategy) - 1:
                # this is the last child
                if strategy[i].has_worm == True:
                    wasted += 0 + 1 # 1 is for going back from previous child
                                    # to root node of the subtree
                else:
                    wasted += strategy[i].wasted_steps + 1

        e_avg = float(e_sum) / node.num_leaves
        if node.expectation == None or e_avg < node.expectation:
            node.expectation = e_avg
            node.wasted_steps = wasted

def worker(nodes):
    tree_nodes = build_tree(nodes)
    calc_expectation(tree_nodes[1]) # tree_nodes[1] is the root
    print '{0:.4f}'.format(tree_nodes[1].expectation)

    # for node in tree_nodes:
        # print node

def main():
    if len(sys.argv) != 2:
        print "Usage: python snail.py input.txt"
        exit(1)
    f = open(sys.argv[1], 'r')
    # assuming file is not empty
    while True:
        line = f.readline()
        items = line.split()
        if len(items) == 1:
            n = int(items[0])
            if n == 0:
                break
            nodes = []
            for i in range(n):
                line = f.readline()
                nodeinfo = line.split()
                nodes.append(nodeinfo)
            worker(nodes)
            # break

    f.close()

if __name__ == '__main__':
    main()
