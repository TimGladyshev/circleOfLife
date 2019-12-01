import monte_carlo_tree_searchV1
import STATE

def print_board(board):
    pass

def play_game():
    tree = monte_carlo_tree_searchV1.MCTS()
    board = STATE.State()
    print(board)

    while True:
        print("start --------- length tree->", end=" ")
        print(len(tree.Children), end=" ")
        print(len(tree.Rewards))
        print("num actions", end=" ")
        print(len(board.getActions()))

        x_y_z = input("enter x,y,z:\n")
        x, y, z = map(int, x_y_z.split(","))

        if (x, y, z) not in board.getActions():
            print("action not in possible actions")
            continue

        board = board.takeAction((x, y, z))

        print("expanded already -- ", end=" ")
        print(board in tree.Children)
        print(board)
        print("num actions AI", end=" ")
        print(len(board.getActions()))

        if board.terminal:
            break

        for i in range(100):
            tree.do_iteration(board)
        board = tree.find_best_child(board)

        print(board)
        if board.terminal:
            break


if __name__ == "__main__":
    play_game()
