import math
import random

import monte_carlo_tree_searchV2
import STATE
import MiniMaxV2
import multiprocessing as mp


def play_game():
    pool = mp.Pool(processes=mp.cpu_count())
    tree = monte_carlo_tree_searchV2.MCTS(save_data=True, C=.5, alpha=.5, player=1,
                                          file1='pkl_sim50_heur1_children.marshal', file2='pkl_sim50_heur1_num_visit.marshal',
                                          file3='pkl_sim50_heur1_rewards.marshal', file4='pkl_sim50_heur1_heur.marshal', sim_num=1)
    board = STATE.State()
    print(board)
    seen = True


    while True:
        if seen == False:
            best_move = float("-inf")
            best_action = None
            for action in board.getActions():
                new_board = board.takeAction(action)
                move = MiniMaxV2.payoff(new_board, 0, board.turn % 2 + 1)
                if move > best_move:
                    best_move = move
                    best_action = action
            board = board.takeAction(best_action)
            seen = True
        else:
            for i in range(50):
                tree.do_iteration(board)
            board = tree.find_best_child(board)

        print(board)
        if board.terminal:
            tree.save_data_pickle()
            break

        print("your move --------- length tree->", end=" ")
        print(len(tree.Children), end=" - ")
        print("num actions", end=" ")
        print(len(board.getActions()))

        x_y_z = input("enter x,y,z:\n")

        if x_y_z == "e":
            tree.save_data_pickle()
            break

        x, y, z = map(int, x_y_z.split(","))

        if (x, y, z) not in board.getActions():
            print("action not in possible actions")
            continue

        new_board = board.takeAction((x, y, z))

        if new_board in tree.Children:
            print("already seen -- resistance is futile")
        else:
            print("this is new, let me think")
            seen = False
            tree.expand(new_board)

        board = new_board



if __name__ == "__main__":
    play_game()