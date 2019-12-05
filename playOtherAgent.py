import math

import monte_carlo_tree_searchV1
import STATE
import json


def print_board(board):
    pass

def play_game():
    tree2 = monte_carlo_tree_searchV1.MCTS(save_data=True, alpha=math.sqrt(2), player=2)
    tree1 = monte_carlo_tree_searchV1.MCTS(save_data=True, alpha=2, player=1, file1='childrenP1.txt',
                                           file2='num_visitedP1.txt', file3='rewardsP2.txt')
    board = STATE.State()
    print(board)

    while True:
        for i in range(50):
            tree1.do_iteration(board)
        board = tree1.find_best_child(board)

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
                print("player 1 wins!!!!")

            if board.get_reward_adversarial() == 1:
                print("player 2 has crushed")

            tree1.save_data()
            tree2.save_data()
            break

        for i in range(50):
            tree2.do_iteration(board)
        board = tree2.find_best_child(board)

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
                print("player 1 wins!!!!")
            if board.get_reward_adversarial() == 1:
                print("player 2 has crushed")
            tree1.save_data()
            tree2.save_data()
            break


if __name__ == "__main__":
    for i in range(10):
        play_game()
