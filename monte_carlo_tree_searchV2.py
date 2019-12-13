import math
import random
import STATE
from collections import defaultdict
import os
import pickle
import multiprocessing as mp


class HeuristicFunctions:

    def heur1( node, player):
        """
        :param node: STATE.State() node
        :return: A value between -1 and 1
        """
        p1_positions = node.getTilePostions(player)
        p2_positions = node.getTilePostions(player % 2 + 1)

        danger_to_shapes = 0
        attack_points = 0

        while p1_positions:
            shape = node.getShape(p1_positions.pop())
            shape_name = node.typeShape(shape)
            cloud = node.getPerimeter(shape)
            cloud = cloud | node.getPerimeter(shape | cloud)
            p2_in_cloud = cloud.intersection(p2_positions)
            while p2_in_cloud:
                p2_shape = node.getShape(cloud.pop())
                p2_shape_name = node.typeShape(p2_shape)
                if p2_shape_name in STATE.SHAPE_SUBSETS[shape_name % 12 + 1]:
                    danger_to_shapes += len(p2_shape)
                if shape_name in STATE.SHAPE_SUBSETS[p2_shape_name % 12 + 1]:
                    attack_points += len(shape)
                p2_in_cloud = p2_in_cloud - p2_shape
            p1_positions = p1_positions - shape

        sigmoid = 1/(1+ math.exp(-1 * (2 * danger_to_shapes + attack_points)))
        return sigmoid * 2 - 1

    def heur2( node, player):
        """
        :param node: STATE.State() node
        :return: A value between -1 and 1
        """
        p1_positions = node.getTilePostions(player)
        p2_positions = node.getTilePostions(player % 2 + 1)

        danger_to_shapes = 0
        attack_points = 0

        while p1_positions:
            shape = node.getShape(p1_positions.pop())
            shape_name = node.typeShape(shape)
            cloud = node.getPerimeter(shape)
            cloud = cloud | node.getPerimeter(shape | cloud)
            p2_in_cloud = cloud.intersection(p2_positions)
            while p2_in_cloud:
                p2_shape = node.getShape(cloud.pop())
                p2_shape_name = node.typeShape(p2_shape)
                if p2_shape_name in STATE.SHAPE_SUBSETS[shape_name % 12 + 1]:
                    danger_to_shapes += len(p2_shape)
                if shape_name in STATE.SHAPE_SUBSETS[p2_shape_name % 12 + 1]:
                    attack_points += len(shape)
                p2_in_cloud = p2_in_cloud - p2_shape
            p1_positions = p1_positions - shape

        sigmoid = 1/(1+ math.exp(-1 * (danger_to_shapes + 2 * attack_points)))
        return sigmoid * 2 - 1

    def heur3(node, player):
        """
        :param node: STATE.State() node
        :return: A value between -1 and 1
        """
        p1_positions = node.getTilePostions(player)
        p2_positions = node.getTilePostions(player % 2 + 1)

        danger_to_shapes = 0
        attack_points = 0

        while p1_positions:
            shape = node.getShape(p1_positions.pop())
            shape_name = node.typeShape(shape)
            cloud = node.getPerimeter(shape)
            cloud = cloud | node.getPerimeter(shape | cloud)
            p2_in_cloud = cloud.intersection(p2_positions)
            while p2_in_cloud:
                p2_shape = node.getShape(cloud.pop())
                p2_shape_name = node.typeShape(p2_shape)
                if p2_shape_name in STATE.SHAPE_SUBSETS[shape_name % 12 + 1]:
                    danger_to_shapes += len(p2_shape)
                if shape_name in STATE.SHAPE_SUBSETS[p2_shape_name % 12 + 1]:
                    attack_points += len(shape)
                p2_in_cloud = p2_in_cloud - p2_shape
            p1_positions = p1_positions - shape

        return danger_to_shapes + 2 * attack_points

    def heur4(node, player):
        """
        in progress - idea was to give future perception, but this favors upgrading the shape
        v3 heuristic
        for each shape in game, finds shapes in adjacent or 1-away spaces (min distance to take), then
        for each shape the shape of interest can become, finds if opponent's shape is in the subset of the conquering
        shape. attack points if shape of interest is player's, danger to shape points otherwise. The idea was to use
        sigmoid, but perhaps this is wrong. Score introduction?

        :param node: STATE.State() node
        :return: A value between -1 and 1
        """

        if node.is_terminal():
            if player == 1:
                return node.get_reward() * 1000
            else:
                return node.get_reward_adversarial() * 1000

        p1_positions = node.getTilePostions(player)
        p2_positions = node.getTilePostions(player % 2 + 1)
        empty_positions = node.getTilePostions(0)
        actions = node.getActions()

        danger_to_shapes = 0
        attack_points = 0

        if player == 1:
            player_score = node.p1Score
            op_score = node.p2Score
        else:
            player_score = node.p2Score
            op_score = node.p1Score

        while p1_positions:
            shape = node.getShape(p1_positions.pop())
            shape_name = node.typeShape(shape)
            cloud = node.getPerimeter(shape)
            cloud = cloud | node.getPerimeter(shape | cloud)
            p2_in_cloud = cloud.intersection(p2_positions)

            while p2_in_cloud:
                p2_shape = node.getShape(p2_in_cloud.pop())
                p2_shape_name = node.typeShape(p2_shape)
                shape_futures = set(STATE.SHAPE_POTENTIAL[shape_name])
                p2_shape_futures = set(STATE.SHAPE_POTENTIAL[p2_shape_name])

                if p2_shape_name in STATE.SHAPE_SUBSETS[shape_name % 12 + 1]:
                    inter_per = node.getPerimeter(shape).intersection(node.getPerimeter(p2_shape))
                    inter_per = inter_per - actions
                    if len(inter_per) > 0:
                        danger_to_shapes = danger_to_shapes + 10 * len(p2_shape)
                    else:
                        danger_to_shapes = danger_to_shapes + 5 * len(p2_shape)
                for future in shape_futures:
                    if p2_shape_name in STATE.SHAPE_SUBSETS[future % 12 + 1]:
                        danger_to_shapes += 1
                if shape_name in STATE.SHAPE_SUBSETS[p2_shape_name % 12 + 1]:
                    attack_points = attack_points + 5 * len(shape)
                for f in p2_shape_futures:
                    if shape_name in STATE.SHAPE_SUBSETS[f % 12 + 1]:
                        attack_points += 1
                p2_in_cloud = p2_in_cloud - p2_shape
            p1_positions = p1_positions - shape

        return 2 * attack_points * (1 + player_score) - danger_to_shapes * (1 + op_score)

class MCTS:
    """
    Second Edition of Monte Carlo Tree Search for 'Circle of Life'
    Deigned to work with - iState interface -

    Current things not in last version:
        Nodes now have an additional variable for heuristic approximation of subtrees
        Node selection for expansion is now (1 - alpha) * (reward / visits) + alpha * (heuristic)
            - heuristic must have the same range as reward function



    ->modeled after: https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
                    https://medium.com/@quasimik/monte-carlo-tree-search-applied-to-letterpress-34f41c86e238
                    https://www.aaai.org/Papers/AIIDE/2008/AIIDE08-036.pdf
                    https://www.analyticsvidhya.com/blog/2019/01/monte-carlo-tree-search-introduction-algorithm-deepmind-alphago/
    ->parallel processing: https://www.machinelearningplus.com/python/parallel-processing-python/
        https://stackabuse.com/parallel-processing-in-python/
        https://docs.python.org/2/library/collections.html
        https://stackoverflow.com/questions/52584142/mcts-tree-parallelization-in-python-possible
        https://docs.python.org/3.4/library/multiprocessing.html?highlight=process

    """

    def __init__(self, save_data=False, C=math.sqrt(2), alpha = .5, player=2, file1='V2children.txt', file2='V2num_visited.txt',
                 file3='V2rewards.txt', file4='V2heur.txt', heur_num=1, sim_num=50):

        self.file1 = file1
        self.file2 = file2
        self.file3 = file3
        self.file4 = file4

        self.heur_num=heur_num
        self.sim_num=sim_num

        if save_data == False:
            self.VisitCount = defaultdict(int)
            self.Rewards = defaultdict(float)
            self.Children = dict()
            self.Heur = defaultdict(float)
        else:
            file1_info = os.stat(file1)
            file2_info = os.stat(file2)
            file3_info = os.stat(file3)
            file4_info = os.stat(file4)
            if file1_info.st_size + file2_info.st_size + file3_info.st_size + file4_info.st_size > 2000000000:
                raise RuntimeError("file sizes over a gig my dood")
            self.VisitCount = defaultdict(int)
            self.Rewards = defaultdict(float)
            self.Children = dict()
            self.Heur = defaultdict(float)
            self.load_pickle()

        self.player = player
        self.alpha = alpha
        self.C = C

    def find_best_child(self, node):
        # remember to undo flips and rotates bruh
        # resolve holding vs calculating terminal --> what's beast for speed/size
        # Remove completely if slow?
        if node.terminal == True:
            raise RuntimeError(f"find_best_child called on terminal {node}")

        if node not in self.Children:
            _tuple = tuple(node.getActions())
            return node.takeAction(random.choice(_tuple))

        def scoreNode(n):
            if self.VisitCount[n] == 0:
                return float("-inf")  # we should use floats so that minor differences show up - worth space?
            return float(self.Rewards[n]) / self.VisitCount[n]

        return max(self.Children[node], key=scoreNode)

    def find_a_path(self, node, path_given):
        # NODE = node
        path = path_given.copy()
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

        def UCT_with_heur(n):
            heur = (1 - self.alpha) * (self.Rewards[n] / self.VisitCount[n]) + self.alpha * (self.Heur[n]/self.VisitCount[n])
            return heur + self.C * math.sqrt(ln_parent_n / self.VisitCount[n])

        return max(self.Children[node], key=UCT_with_heur)

    def expand(self, node):
        if node in self.Children:
            return
        self.Children[node] = node.find_successors()

    def do_iteration(self, node, path_given):
        path = self.find_a_path(node, path_given)
        leaf = path[-1]
        self.expand(leaf)
        reward = 0
        heur = self.find_heur(leaf)
        """
        pool = mp.Pool(processes=mp.cpu_count())
        results = [pool.apply(self.simulate, args=(STATE.State(tupleKey=leaf.key),)) for i in range(self.sim_num)]
        reward = float(sum(results)) / len(results)
        """
        for i in range(self.sim_num):
            reward += self.simulate(leaf)
        reward = float(reward) / self.sim_num

        self.back_propogate(path, reward, heur)

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

    def find_heur(self, node):
        if self.heur_num == 1:
            return HeuristicFunctions.heur1( node, self.player)
        elif self.heur_num == 2:
            return HeuristicFunctions.heur2( node, self.player)
        else:
            raise RuntimeError("this heuristic hasn't been made yet ya GOON")

    def back_propogate(self, path, reward, heur):
        length = len(path)
        for i in range(length):
            self.VisitCount[path[length - 1 - i]] += 1
            self.Rewards[path[length - 1 - i]] += float(reward)
            self.Heur[path[length - 1 - i]] += heur
            reward = -reward
            heur = -heur

    def save_data(self):
        children_out = self.file1
        num_visited_out = self.file2
        rewards_out = self.file3
        heur_out = self.file4

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

        heur = open(heur_out, "w")
        for key in self.Heur.keys():
            heur.write(key.write_key() + "  ")
            heur.write(str(self.Heur[key]) + "\n")
        heur.close()

    def load(self):
        """
        loads Dictionaries that work with STATE and MCTS. If none had yet, MCTS creates blank tree.
        :param file1: text file for children
        :param file2: text file for rewards
        :param file3: test file for num visited
        :return: dictionaries for Children, Rewards, and NumVisited
        """

        children_out = self.file1
        num_visited_out = self.file2
        rewards_out = self.file3
        heur_out = self.file4

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

        heur_file = open(heur_out, 'r')
        heur_line = heur_file.readline()
        while heur_line:
            heur_line = heur_line.split("  ")
            state_of_being = STATE.State(tupleKey=eval(heur_line[0]))
            num_heur = eval(heur_line[1])
            self.Heur[state_of_being] = num_heur
            heur_line = heur_file.readline()
        vis_file.close()

    def load_pickle(self):
        with open(self.file1, 'rb') as child:
            self.Children = pickle.load(child)
        with open(self.file2, 'rb') as reward:
            self.Rewards = pickle.load(reward)
        with open(self.file3, 'rb') as numv:
            self.VisitCount = pickle.load(numv)
        with open(self.file4, 'rb') as heur:
            self.Heur = pickle.load(heur)

    def save_data_pickle(self):
        with open(self.file1, 'wb') as children_dump:
            pickle.dump(self.Children, children_dump)
        with open(self.file2, 'wb') as reward_dump:
            pickle.dump(self.Rewards, reward_dump)
        with open(self.file3, 'wb') as vis_dump:
            pickle.dump(self.VisitCount, vis_dump)
        with open(self.file4, 'wb') as heur_dump:
            pickle.dump(self.Heur, heur_dump)