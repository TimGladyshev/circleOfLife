import math
import random

import monte_carlo_tree_searchV2
import STATE


def play_game():
    tree = monte_carlo_tree_searchV2.MCTS(save_data=False, C=math.sqrt(2), alpha=.5, player=1,
                                          file1='v2_sim50_heur2_children.txt', file2='v2_sim50_heur2_num_visit.txt',
                                          file3='v2_sim50_heur2_rewards.txt', file4='v2_sim50_heur2_heur.txt',heur_num=2, sim_num=50)
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