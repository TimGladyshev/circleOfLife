import STATE
import monte_carlo_tree_searchV2
import operator
DEPTH = 2

def payoff(board_instance, depth, player):
    if board_instance.is_terminal():
        if player == 1:
            return board_instance.get_reward() * 100
        else:
            return board_instance.get_reward_adversarial() * 100
    elif depth == DEPTH:
        return (monte_carlo_tree_searchV2.HeuristicFunctions.heur4(board_instance, player), board_instance)
    else:
        payoffs = [payoff(board_instance.takeAction(action), depth + 1, player) for action in board_instance.getActions()]
        if(board_instance.turn == player):
            return max(payoffs, key=lambda x: x[0])[0], board_instance
        else:
            return min(payoffs, key=lambda x: x[0])[0], board_instance
