import STATE
VICTORY_WEIGHT = 40
DEPTH = 2

def evaluateSimpleP1(State):
    """
    Simplest Evalution Function. If not terminal returns between -20 and 20 (for score), else +-Victory_Weight
    :param State: State of board
    :return: Score
    """
    if State.isTerminal():
        if State.p1Score == 20:
            return VICTORY_WEIGHT
        elif State.p2Score == 20:
            return -VICTORY_WEIGHT
        else:
            if State.turn == 1:
                return VICTORY_WEIGHT
            else:
                return -VICTORY_WEIGHT
    else:
        return State.p1Score - State.p2Score

def payoff(State, depth):
    if depth == DEPTH or State.isTerminal():
        return evaluateSimpleP1(State)
    else:
        payoffs = list(payoff(State.takeAction(action), depth + 1) for action in State.getActions())
        if(State.turn == 1):
            return max(payoffs)
        else:
            return min(payoffs)

if __name__ == '__main__':
    State = STATE.State()
    actions = State.getActions()
    maxPayoff = -60
    maxAction = None
    for action in actions:
        payoffs = payoff(State.takeAction(action), 0)
        if payoffs > maxPayoff:
            maxPayoff = payoffs
            maxAction = action
    print(maxPayoff)
    print(maxAction)