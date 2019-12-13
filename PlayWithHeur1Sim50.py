import math
import operator
import random

import monte_carlo_tree_searchV2
import STATE
import MiniMaxV2
import multiprocessing as mp


def play_game(your_player_num):
    pool = mp.Pool(processes=mp.cpu_count() - 1)
    tree = monte_carlo_tree_searchV2.MCTS(save_data=True, C=.5, alpha=.5, player=your_player_num % 2 + 1,
                                          file1='pkl_sim50_heur1_children.marshal', file2='pkl_sim50_heur1_num_visit.marshal',
                                          file3='pkl_sim50_heur1_rewards.marshal', file4='pkl_sim50_heur1_heur.marshal', sim_num=1)
    board = STATE.State()
    print(board)
    seen = True
    path_given = []
    path_given.append(board)

    if your_player_num == 2:
        while True:
            if seen == False:
                best_move = float("-inf")
                best_action = None

                results = [pool.apply_async(MiniMaxV2.payoff, args=(board.takeAction(i), 0, board.turn)) for i in board.getActions()]
                output = [p.get() for p in results]
                new_board = max(output, key=lambda x: x[0])[1]
                action = new_board.getTilePostions(board.turn) - board.getTilePostions(board.turn)
                board = board.takeAction(action.pop())
                seen = True
            else:
                for i in range(50):
                    tree.do_iteration(board, path_given)
                board = tree.find_best_child(board)
                path_given.append(board)

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
            path_given.append(new_board)
            if new_board in tree.Children:
                print("already seen -- resistance is futile")
            else:
                print("this is new, let me think")
                seen = False
                tree.expand(new_board)

            board = new_board
    else:
        while True:
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
            path_given.append(new_board)
            if new_board in tree.Children:
                print("already seen -- resistance is futile")
            else:
                print("this is new, let me think")
                seen = False
                tree.expand(new_board)

            board = new_board

            if seen == False:
                best_move = float("-inf")
                best_action = None

                results = [pool.apply_async(MiniMaxV2.payoff, args=(board.takeAction(i), 0, board.turn)) for i in
                           board.getActions()]
                output = [p.get() for p in results]
                new_board = max(output, key=lambda x: x[0])[1]
                action = new_board.getTilePostions(board.turn) - board.getTilePostions(board.turn)
                board = board.takeAction(action.pop())
                seen = True
            else:
                for i in range(50):
                    tree.do_iteration(board, path_given)
                board = tree.find_best_child(board)
                path_given.append(board)

            print(board)
            if board.terminal:
                tree.save_data_pickle()
                break





if __name__ == "__main__":
    player_num = int(input("what player are you?"))
    play_game(player_num)