import math
import random
from collections import defaultdict


class MCTS:
    """
    First Edition of Monte Carlo Tree Search for Circle of Life
    Deigned to work with iState interface
    ->modeled after: https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
    ->parallel processing: https://www.machinelearningplus.com/python/parallel-processing-python/
        https://stackabuse.com/parallel-processing-in-python/
        https://docs.python.org/2/library/collections.html
        https://stackoverflow.com/questions/52584142/mcts-tree-parallelization-in-python-possible
        https://docs.python.org/3.4/library/multiprocessing.html?highlight=process

    """

    def __init__(self, alpha=1):
        # Rewards of nodes seen
        self.Rewards = defaultdict(int)  # like dictionary but has default value for unseen key
        # Visit count of nodes seen
        self.VisitCount = defaultdict(int)
        # dictionary of nodes
        self.Children = dict()
        # exploration likelyhood
        self.alpha = alpha

    def find_best_child(self, node):
        # resolve holding vs calculating terminal --> what's beast for speed/size
        # Remove completely if slow?
        if node.terminal == True:
            raise RuntimeError(f"find_best_child called on terminal {node}")

        if node not in self.Children:
            return node.takeAction(random.choice(node.getActions()))

        def scoreNode(n):
            if self.VisitCount[n] == 0:
                return float("-inf")  # we should use floats so that minor differences show up - worth space?
            return float(self.Rewards[n]) / self.VisitCount[n]

        return max(self.Children[node], key=scoreNode)

    def find_a_path(self, node):
        # NODE = node
        path = []
        while True:
            path.append(node)
            if node not in self.Children or node.terminal:
                return path  # node has either never been expanded or isTerminal
            unexplored = set(self.Children[node] - self.Children.keys())
            if unexplored:
                n = unexplored.pop()
                path.append(n)
                return path
            node = self.upper_conf_bound_tree_select(node)

    def upper_conf_bound_tree_select(self, node):
        # do only if all children are expanded
        assert all(n in self.Children for n in self.Children[node])

        ln_parent_n = math.log(self.VisitCount[node])

        def UCT(n):
            return self.Rewards[n] / self.VisitCount[n] + self.alpha \
                   * math.sqrt(ln_parent_n / self.VisitCount[n])

        return max(self.Children[node], key=UCT)

    def expand(self, node):
        if node in self.Children:
            return
        self.Children[node] = node.find_successors()

    def do_iteration(self, node):
        path = self.find_a_path(node)
        leaf = path[-1]
        self.expand(leaf)
        reward = 0
        for i in range(50):
            reward += self.simulate(leaf)
        reward /= 50
        self.back_propogate(path, reward)

    def simulate(self, node):
        # 90 turns maximum according to my calculations
        player = node.turn
        while True:
            if node.terminal:
                return node.get_reward_adversarial()
            _tuple = tuple(node.getActions())
            node = node.takeAction(random.choice(_tuple))

    def back_propogate(self, path, reward):
        length = len(path)
        for i in range(length):
            self.VisitCount[path[length - 1 - i]] += 1
            self.Rewards[path[length - 1 - i]] += reward
            reward = 1 - reward

