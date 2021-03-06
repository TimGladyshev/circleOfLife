import monte_carlo_tree_searchV1
import STATE


def play_game():

    # raise RuntimeError("Bruv you were fucking with this, don't run it")

    tree = monte_carlo_tree_searchV1.MCTS(save_data=True, alpha=math.sqrt(2), player=1, )
    board = STATE.State()
    print(board)

    while True:
        print("start --------- length tree->", end=" ")
        print(len(tree.Children), end=" ")
        print(len(tree.Rewards))
        print("num actions", end=" ")
        print(len(board.getActions()))

        x_y_z = input("enter x,y,z:\n")

        if x_y_z == "e":
            tree.save_data()
            break

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

        for i in range(50):
            tree.do_iteration(board)
        board = tree.find_best_child(board)

        print(board)
        if board.terminal:
            tree.save_data()
            break


if __name__ == "__main__":
    play_game()
