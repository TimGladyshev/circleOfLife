import math
import monte_carlo_tree_search_small1
import SmallState
import json
import time


def print_board(board):
    pass

def play_game(log_file_p1, log_file_p2, game_log):
    tree2 = monte_carlo_tree_search_small1.MCTS(save_data=True, alpha=math.sqrt(2), player=2, file1='children_small_alpha_sqrt2_p2.txt',
                                            file2='num_visited_small_alpha_sqrt2_p2.txt', file3='rewards_small_alpha_sqrt2_p2.txt')
    tree1 = monte_carlo_tree_search_small1.MCTS(save_data=True, alpha=2, player=1, file1='children_small_alpha2_p1.txt',
                                           file2='num_visited_small_alpha2_p1.txt', file3='rewards_small_alpha2_p1.txt')
    board = SmallState.State()
    print(board)

    start_time = time.time()
    with open(game_log, 'w') as g1:
        g1.write("log start: ")
        g1.write(str(time.time() - start_time))
        g1.write("\n")

    with open(log_file_p1, 'w') as p1:
        p1.write("log start: ")
        p1.write(str(time.time() - start_time))
        p1.write("\n")

    with open(log_file_p2, 'w') as p2:
        p2.write("log start: ")
        p2.write(str(time.time() - start_time))
        p2.write("\n")
    
    while True:
        board = SmallState.State()
        # tree1.save_data_pickle()
        # tree2.save_data_pickle()
        num_moves = 0
        root_path = []

        while True:
            for i in range(50):
                tree1.do_iteration(board, root_path)
            tree2.expand(board)
            board = tree1.find_best_child(board)
            tree2.expand(board)
            num_moves += 1
            root_path.append(board)
            with open(game_log, 'a') as g1:
                g1.write(board.__str__())
                g1.write("\n")

            if board in tree2.Children:
                print("-------------------------------->SEEN")

                print("tree2 valuation-->", end='')
                print(tree2.Rewards[board], end=' ')
                print("#visit:", end=' ')
                print(tree2.VisitCount[board])

                print("tree1 valuation-->", end='')
                print(tree1.Rewards[board], end=' ')
                print("#visit:", end=' ')
                print(tree1.VisitCount[board])

                print("num moves-->", end='')
                print(num_moves, end=' ')
                print("root path-->", end=' ')
                print(root_path)

            else:
                print("--------------------------------->new")
            print(board)

            if board.terminal:
                if board.get_reward() == 1:
                    with open(log_file_p1, 'a') as p1:
                        p1.write(str(1))
                        p1.write(" ")
                        p1.write(str(board.p1Score))
                        p1.write(" ")
                        p1.write(str(num_moves))
                        p1.write("\n")

                    with open(log_file_p2, 'a') as p2:
                        p2.write(str(0))
                        p2.write(" ")
                        p2.write(str(board.p2Score))
                        p2.write(" ")
                        p2.write(str(num_moves))
                        p2.write("\n")

                if board.get_reward_adversarial() == 1:
                    print("player 2 has crushed")
                    with open(log_file_p1, 'a') as p1:
                        p1.write(str(0))
                        p1.write(" ")
                        p1.write(str(board.p1Score))
                        p1.write(" ")
                        p1.write(str(num_moves))
                        p1.write("\n")

                    with open(log_file_p2, 'a') as p2:
                        p2.write(str(1))
                        p2.write(" ")
                        p2.write(str(board.p2Score))
                        p2.write(" ")
                        p2.write(str(num_moves))
                        p2.write("\n")

                tree1.save_data()
                tree2.save_data()
                break

            for i in range(50):
                tree2.do_iteration(board, root_path)
            tree1.expand(board)
            board = tree2.find_best_child(board)
            tree1.expand(board)
            num_moves += 1
            root_path.append(board)
            with open(game_log, 'a') as g1:
                g1.write(board.__str__())
                g1.write("\n")

            if board in tree1.Children:
                print("-------------------------------->SEEN")

                print("tree2 valuation-->", end='')
                print(tree2.Rewards[board], end=' ')
                print("#visit:", end=' ')
                print(tree2.VisitCount[board])

                print("tree1 valuation-->", end='')
                print(tree1.Rewards[board], end=' ')
                print("#visit:", end=' ')
                print(tree1.VisitCount[board])

                print("num moves-->", end='')
                print(num_moves, end=' ')
                print("root path-->", end=' ')
                print(root_path)
            else:
                print("--------------------------------->new")
            print(board)

            if board.terminal:
                if board.get_reward() == 1:
                    with open(log_file_p1, 'a') as p1:
                        p1.write(str(1))
                        p1.write(" ")
                        p1.write(str(board.p1Score))
                        p1.write(" ")
                        p1.write(str(num_moves))
                        p1.write("\n")

                    with open(log_file_p2, 'a') as p2:
                        p2.write(str(0))
                        p2.write(" ")
                        p2.write(str(board.p2Score))
                        p2.write(" ")
                        p2.write(str(num_moves))
                        p2.write("\n")

                if board.get_reward_adversarial() == 1:
                    with open(log_file_p1, 'a') as p1:
                        p1.write(str(0))
                        p1.write(" ")
                        p1.write(str(board.p1Score))
                        p1.write(" ")
                        p1.write(str(num_moves))
                        p1.write("\n")

                    with open(log_file_p2, 'a') as p2:
                        p2.write(str(1))
                        p2.write(" ")
                        p2.write(str(board.p2Score))
                        p2.write(" ")
                        p2.write(str(num_moves))
                        p2.write("\n")

                    
                tree1.save_data()
                tree2.save_data()
                break

        if time.time() - start_time >= 39600:
            with open(game_log, 'a') as g1:
                g1.write(str(time.time() - start_time))
                g1.write(str(num_moves))
                g1.write("\n")
            break


if __name__ == "__main__":
    for i in range(10):
        play_game("log_file_p1_small_alphasqrt2v2.txt", "log_file_p2_small_alphasqrt2v2.txt", "game_log_small_alphasqrt2v2.txt")
