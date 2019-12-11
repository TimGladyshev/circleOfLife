import STATE
import monte_carlo_tree_searchV2
DEPTH = 2

def payoff(State, depth, player):
    if depth == DEPTH or State.isTerminal():
        return monte_carlo_tree_searchV2.HeuristicFunctions.heur3(State)
    else:
        payoffs = list(payoff(State.takeAction(action), depth + 1, player % 2 + 1) for action in State.getActions())
        if(State.turn == player):
            return max(payoffs)
        else:
            return min(payoffs)
