import math
import random
import STATE
from collections import defaultdict
import os


class MCTS:
    """
    First Edition of Monte Carlo Tree Search for 'Circle of Life'
    Deigned to work with - iState interface -

    Current things to know:
        MCTS with random simulation
        Nodes for expansion are selected by Upper Confidence Bound Tree Selection
        Rotations and Flips of a state are hashed the same, and thus not repeated
                - Rewards are propagated all through one path to the current node
                - this may be an issue as its weight is multiplied for the parent but visits increase as well
                - multiple sequences can lead to identical nodes, these are hashed the same also



    ->modeled after: https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
    ->parallel processing: https://www.machinelearningplus.com/python/parallel-processing-python/
        https://stackabuse.com/parallel-processing-in-python/
        https://docs.python.org/2/library/collections.html
        https://stackoverflow.com/questions/52584142/mcts-tree-parallelization-in-python-possible
        https://docs.python.org/3.4/library/multiprocessing.html?highlight=process

    """

    def __init__(self, save_data=False, alpha=1, player=2, file1='Children.txt', file2='num_visited.txt',
                 file3='rewards.txt'):

        self.file1 = file1
        self.file2 = file2
        self.file3 = file3

        if save_data == False:
            self.VisitCount = defaultdict(int)
            self.Rewards = defaultdict(int)
            self.Children = dict()
        else:
            file1_info = os.stat(file1)
            file2_info = os.stat(file2)
            file3_info = os.stat(file3)
            if file1_info.st_size + file2_info.st_size + file3_info.st_size > 1000000000:
                raise RuntimeError("filesize over a gig :(")
            self.VisitCount = defaultdict(int)
            self.Rewards = defaultdict(int)
            self.Children = dict()
            self.load(file1, file2, file3)
        self.player = player
        self.alpha = alpha

    def find_best_child(self, node):
        # remember to undo flips and rotates bruh
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
            # add pruning --> Those children that get removed by above and have no score?
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
        for i in range(25):
            reward += self.simulate(leaf)
        reward /= 25
        self.back_propogate(path, reward)

    def simulate(self, node):
        # 90 turns maximum according to my calculations
        while True:
            if node.terminal:
                if self.player == 2:
                    return node.get_reward_adversarial()
                else:
                    return node.get_reward()
            _tuple = tuple(node.getActions())
            node = node.takeAction(random.choice(_tuple))

    def back_propogate(self, path, reward):
        length = len(path)
        for i in range(length):
            self.VisitCount[path[length - 1 - i]] += 1
            self.Rewards[path[length - 1 - i]] += float(reward)
            reward = -reward

    def save_data(self):
        children_out = self.file1
        num_visited_out = self.file2
        rewards_out = self.file3

        child = open(children_out, "w")
        for key in self.Children.keys():
            child.write(key.write_key() + "   ")
            for value in self.Children[key]:
                child.write(value.write_key() + "  ")
            child.write("\n")
        child.close()

        num_visited = open(num_visited_out, "w")
        for key in self.VisitCount.keys():
            num_visited.write(key.write_key() + "  ")
            num_visited.write(str(self.VisitCount[key]) + "\n")
        num_visited.close()

        rewards = open(rewards_out, "w")
        for key in self.Rewards.keys():
            rewards.write(key.write_key() + "  ")
            rewards.write(str(self.Rewards[key]) + "\n")
        rewards.close()

    def load(self, file1, file2, file3):
        """
        loads Dictionaries that work with STATE and MCTS. If none had yet, MCTS creates blank tree.
        :param file1: text file for children
        :param file2: text file for rewards
        :param file3: test file for num visited
        :return: dictionaries for Children, Rewards, and NumVisited
        """

        children_out = file1
        num_visited_out = file2
        rewards_out = file3

        child_file = open(children_out, 'r')
        child_line = child_file.readline()
        while child_line:
            child_line = child_line.split("   ")
            parent = STATE.State(tupleKey=eval(child_line[0]))
            children = child_line[1].split("  ")
            children.pop(len(children) - 1)
            set_children = set()
            for child in children:
                set_children.add(STATE.State(tupleKey=eval(child)))
            self.Children[parent] = set_children
            child_line = child_file.readline()
        child_file.close()

        reward_file = open(rewards_out, 'r')
        reward_line = reward_file.readline()
        while reward_line:
            reward_line = reward_line.split("  ")
            state_of_being = STATE.State(tupleKey=eval(reward_line[0]))
            reward = eval(reward_line[1])
            self.Rewards[state_of_being] = reward
            reward_line = reward_file.readline()
        reward_file.close()

        vis_file = open(num_visited_out, 'r')
        vis_line = vis_file.readline()
        while vis_line:
            vis_line = vis_line.split("  ")
            state_of_being = STATE.State(tupleKey=eval(vis_line[0]))
            num_vis = eval(vis_line[1])
            self.VisitCount[state_of_being] = num_vis
            vis_line = vis_file.readline()
        vis_file.close()










