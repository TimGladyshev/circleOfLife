import math
import random
import SmallState
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

    def __init__(self, save_data=False, alpha=math.sqrt(2), player=2, file1='Children.txt', file2='num_visited.txt',
                 file3='rewards.txt', sim_num=25):

        # Files are imported at instantiation of a MCTSV1 object. If save_data is True we will import from these files. Even if False, we will still write to these files.
        # file1 corresponds to the dictionary of lists of children states for each state.
        self.file1 = file1
        # file2 corresponds to dictionary of visit counts for each state.
        self.file2 = file2
        # file3 corresponds to the dictionary of rewards or totally victories reached from each state.
        self.file3 = file3

        # sim_num is given at the instantiation of a MCTSV1 object and has a default value of 50.
        # sim_num corresponds to the number of simulations run from any given node.
        self.sim_num = sim_num

        # save_data is given at the instantiation of a MCTSV1 object. If save_data is False it means we will not import saved data.
        # If we are not going to import saved data...
        if save_data == False:
            # Instantiate the visit counts, the rewards, and the children as empty dictionaries to be filled.
            self.VisitCount = defaultdict(int)
            self.Rewards = defaultdict(int)
            self.Children = dict()
        # If we are going to import saved data...
        else:
            # Get file info.
            file1_info = os.stat(file1)
            file2_info = os.stat(file2)
            file3_info = os.stat(file3)
            # If all the file sizes sum up to over a Gigabyte...
            if file1_info.st_size + file2_info.st_size + file3_info.st_size > 1000000000:
                # Raise an error.
                raise RuntimeError("filesize over a gig :(")
            # Instantiate visit counts, rewards, and children as empty dictionaries to be filled.
            self.VisitCount = defaultdict(int)
            self.Rewards = defaultdict(int)
            self.Children = dict()
            # Fill these empty dictionaries with our input files with the custom load method.
            self.load(file1, file2, file3)
        # If player is 2 the reward is the "adversarial" reward.
        self.player = player
        # Alpha is a parameter used to modify the behavior of the MCTS.
        self.alpha = alpha

    # Given a node, this method will return the child with the maximum score.
    def find_best_child(self, node):
        # remember to undo flips and rotates bruh
        # resolve holding vs calculating terminal --> what's beast for speed/size
        # Remove completely if slow?

        # If the node is terminal...
        if node.terminal == True:
            # Raise an error. We can't find the best child of a terminal node.
            raise RuntimeError(f"find_best_child called on terminal {node}")

        # If the node is not in our children dictionary, it has no children. Our children dictionary keeps track of which nodes have children and which children they have.
        if node not in self.Children:
            # Take a random action from that node. 
            return node.takeAction(random.choice(node.getActions()))

        # This is a helper method which returns a score for a given node.
        def scoreNode(n):
            # If the node has not been visited...
            if self.VisitCount[n] == 0:
                # The score is the worst possible score, negative infinity.
                return float("-inf")  # we should use floats so that minor differences show up - worth space?
            # Otherwise, the score is the average score, the total victories divided by the total visits.
            return float(self.Rewards[n]) / self.VisitCount[n]

        # Return the child with the largest score.
        return max(self.Children[node], key=scoreNode)

    # Find a path from a node to a leaf...
    def find_a_path(self, node, root_path):
        # 
        path = root_path.copy()
        # Loop...
        while True:
            # Append this node to the path.
            path.append(node)
            # If the node has no expanded children or if it is a terminal node (so it has no children at all)...
            if node not in self.Children or node.terminal:
                # You've reached a leaf, so return the path from the original node to this leaf.
                return path
            # Unexplored is the children of the current node excluding all those nodes which have children of their own.
            unexplored = set(self.Children[node] - self.Children.keys())
            # If this node has unexplored children.
            if unexplored:
                # Pick an unexplored child node...
                n = unexplored.pop()
                # And add it to the path.
                path.append(n)
                # This is a leaf node, so return the path, we've reached a leaf.
                return path
            # Pick the next node according to the upper confidence bound 1.
            node = self.upper_conf_bound_tree_select(node)

    # Select the next node from a given node according to Upper Confidence Bound 1.
    def upper_conf_bound_tree_select(self, node):

        assert all(n in self.Children for n in self.Children[node])
        # Get the log of the visit count of the node in question.
        if self.VisitCount > 1:
            ln_parent_n = math.log(self.VisitCount[node])
        else:
            ln_parent_n = 0

        # Define Upper Confidence Bound 1 according to the formula:
        def UCT(n):
            return self.Rewards[n] / self.VisitCount[n] + self.alpha \
                   * math.sqrt(ln_parent_n / self.VisitCount[n])

        # Pick the child which maximizes Upper Confidence Bound 1.
        return max(self.Children[node], key=UCT)

    # Expand a node.
    def expand(self, node):
        # If the node already has children, don't expand it.
        if node in self.Children:
            return
        # Otherwise, add all of its children to the tree.
        self.Children[node] = node.find_successors()

    # Run an iteration from a node.
    def do_iteration(self, node, root_path):
        # Path finds a path from this node to a leaf.
        path = self.find_a_path(node, root_path)
        # leaf is the last node of a path.
        leaf = path[-1]
        # Expand that leaf.
        self.expand(leaf)
        # Set the reward to zero.
        reward = 0
        # Simulate sim_num number of times.
        for i in range(self.sim_num):
            # Add whether we have a victory or a loss after simulating from this leaf.
            reward += self.simulate(leaf)
        # Divide by the simulation number to get the average number of losses if it were one simulation.
        reward /= self.sim_num
        # Backpropagate the information gained from the simulations.
        self.back_propogate(path, reward)

    # Simulate a game from a node to a terminal node.
    def simulate(self, node):
        # 90 turns maximum according to my calculations
        # Loop...
        while True:
            # If the node is a terminal node...
            if node.terminal:
                # If the player is player 2, we give the "adversarial" (P2) reward.
                if self.player == 2:
                    return node.get_reward_adversarial()
                # Otherwise we give the regular (P1) reward.
                else:
                    return node.get_reward()
            # If the node isn't terminal, get the possible actions from here.
            _tuple = tuple(node.getActions())
            # Choose a random action and continue to loop through.
            node = node.takeAction(random.choice(_tuple))

    # Given a path and a reward, backpropagate the reward up the path.
    def back_propogate(self, path, reward):
        # Get the length of the path.
        length = len(path)
        # Loop once for every node in the path... Iterate from the leaf to the root.
        for i in range(length):
            # Add 1 to the visit count of the node under consideration.
            self.VisitCount[path[length - 1 - i]] += 1
            # Add the reward to the reward of the node under considerations.
            self.Rewards[path[length - 1 - i]] += float(reward)
            # Flip the reward negative and positive as you go through, knowing that players alternate turns and we are in a zero-sum game.
            reward = -reward

    # 
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

    # This is a method to load the files we input to the instantiation of an MCTS object.
    def load(self, file1, file2, file3):
        """
        loads Dictionaries that work with STATE and MCTS. If none had yet, MCTS creates blank tree.
        :param file1: text file for children
        :param file2: text file for rewards
        :param file3: test file for num visited
        :return: dictionaries for Children, Rewards, and NumVisited
        """

        # These are placeholder variables for the external files we are importing.
        children_out = file1
        num_visited_out = file2
        rewards_out = file3

        child_file = open(children_out, 'r')
        child_line = child_file.readline()
        while child_line:
            child_line = child_line.split("   ")
            parent = SmallState.State(tupleKey=eval(child_line[0]))
            children = child_line[1].split("  ")
            children.pop(len(children) - 1)
            set_children = set()
            for child in children:
                set_children.add(SmallState.State(tupleKey=eval(child)))
            self.Children[parent] = set_children
            child_line = child_file.readline()
        child_file.close()

        reward_file = open(rewards_out, 'r')
        reward_line = reward_file.readline()
        while reward_line:
            reward_line = reward_line.split("  ")
            state_of_being = SmallState.State(tupleKey=eval(reward_line[0]))
            reward = eval(reward_line[1])
            self.Rewards[state_of_being] = reward
            reward_line = reward_file.readline()
        reward_file.close()

        vis_file = open(num_visited_out, 'r')
        vis_line = vis_file.readline()
        while vis_line:
            vis_line = vis_line.split("  ")
            state_of_being = SmallState.State(tupleKey=eval(vis_line[0]))
            num_vis = eval(vis_line[1])
            self.VisitCount[state_of_being] = num_vis
            vis_line = vis_file.readline()
        vis_file.close()










