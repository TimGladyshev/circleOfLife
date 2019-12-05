import random

import monte_carlo_tree_searchV2
import STATE


def play_game():
    tree = monte_carlo_tree_searchV2.MCTS(save_data=False, alpha=.5, player=1)
    board = STATE.State()
    print(board)

    for i in range(1):
        board = STATE.State()
        while True:
            for i in range(50):
                tree.do_iteration(board)

            board = tree.find_best_child(board)
            print(board)
            if board.isTerminal():
                break
            _tuple = tuple(board.getActions())
            board = board.takeAction(random.choice(_tuple))
            if board.isTerminal():
                break

    tree.save_data()
    print("done ya lucky bastard")

if __name__ == "__main__":
    play_game()