import math
import random

import monte_carlo_tree_searchV1
import STATE


def play_game():
    tree = monte_carlo_tree_searchV1.MCTS(save_data=False, alpha=math.sqrt(2), player=1,
                                          file1='v1_sim1_children.txt', file2='v1_sim1_num_visit.txt',
                                          file3='vi_sim1_rewards.txt', sim_num=1)
    board = STATE.State()
    print(board)

    for i in range(100000):
        if i % 1000 == 0:
            tree.save_data()
        tree.do_iteration(board)
        if i % 100 == 0:
            print("----------------------------------iteration running now", end=' ')
            print(i)
            print(tree.find_best_child)

    print("done ya lucky bastard")

if __name__ == "__main__":
    play_game()