import math
import monte_carlo_tree_searchV2
import STATE
import time

def play_game(log_file_p1, log_file_p2, game_log):
    # num_visit and rewards were flipped during da pickle
    tree2 = monte_carlo_tree_searchV2.MCTS(save_data=True, C=math.sqrt(2), alpha=.5, player=2,
                                           file1='pkl_sim50_heur2_children.marshal',
                                           file2='pkl_sim50_heur2_num_visit.marshal',
                                           file3='pkl_sim50_heur2_rewards.marshal',
                                           file4='pkl_sim50_heur2_heur.marshal', sim_num=1)
    tree1 = monte_carlo_tree_searchV2.MCTS(save_data=True, C=math.sqrt(2), alpha=.5, player=1,
                                           file1='pkl_sim50_heur1_children.marshal',
                                           file2='pkl_sim50_heur1_num_visit.marshal',
                                           file3='pkl_sim50_heur1_rewards.marshal',
                                           file4='pkl_sim50_heur1_heur.marshal', sim_num=1)
    board = STATE.State()
    print(board)

    start_time = time.time()
    with open(game_log, 'w') as gl:
        gl.write("log start: ")
        gl.write(str(time.time() - start_time))
        gl.write("\n")

    with open(log_file_p1, 'w') as pl:
        pl.write("log start: ")
        pl.write(str(time.time() - start_time))
        pl.write("\n")

    with open(log_file_p2, 'w') as p2:
        p2.write("log start: ")
        p2.write(str(time.time() - start_time))
        p2.write("\n")


    while True:
        board = STATE.State()
        tree1.save_data_pickle()
        tree2.save_data_pickle()
        num_moves = 0
        path_given = []
        path_given.append(board)

        while True:
            for i in range(25):
                tree1.do_iteration(board, path_given)
            board = tree1.find_best_child(board)
            path_given.append(board)
            num_moves += 1
            with open(game_log, 'a') as gl:
                gl.write(board.__str__())
                gl.write("\n")

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
                break

            for i in range(25):
                tree2.do_iteration(board, path_given)
            board = tree2.find_best_child(board)
            path_given.append(board)
            num_moves += 1
            with open(game_log, 'a') as gl:
                gl.write(board.__str__())
                gl.write("\n")

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

                break
        if time.time() - start_time >= 39600:
            with open(game_log, 'a') as gl:
                gl.write(str(time.time() - start_time))
                gl.write(str(num_moves))
                gl.write("\n")
            break

if __name__ == "__main__":
        play_game('p1_log_sim50_heur2.txt', 'p2_log_sim50_heur1.txt', 'game_log_sim50_heur.txt')