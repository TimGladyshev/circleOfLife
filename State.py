class iState:

    def getTilePostions(self, player):
        pass

    def getScore(self, player):
        pass

    def getActions(self):
        pass

    def getBoard(self):
        pass

    def takeAction(self, action):
        pass


class State(iState):

    def __init__(self, board = {}, player = 1, score1 = 0, score2 = 0 ):
        if len(board) == 0:
            self.makeNewBoard()
            self.p1Score = 0
            self.p2Score = 0
            self.turn = 1
        else:
            self.board = board
            self.p1Score = score1
            self.p2Score = score2
            self.turn = player

    def __str__(self):
        printable = ""
        keys = list(sorted(self.board.keys()))
        for i in range(len(keys)):
            if i == 0 or i == len(keys) - 5:
                printable += "        "
            if i == 5 or i == len(keys) - 11:
                printable += "      "
            if i == 11 or i == len(keys) - 18:
                printable += "    "
            if i == 18 or i == len(keys) - 26:
                printable += "  "
            printable += str(self.board[keys[i]]) + "   "
            if (i + 1) < len(keys) - 1:
                if keys[i+1][0] > keys[i][0]:
                    printable += "\n"
        return printable

    def makeNewBoard(self):
        boardSize = 5
        initialBoard = {}
        for x in range(boardSize * 2 - 1):
            for y in range(boardSize * 2 - 1):
                for z in range(boardSize * 2 - 1):
                    if (x - 4) + (y - 4) + (z - 4) == 0:
                        initialBoard[(x - 4, y - 4, z - 4)] = 0
        self.board = initialBoard

    def getTilePostions(self, player):
        positions = [i for i,j in self.board.items() if j == player]
        return positions

    def getScore(self, player):
        if player == 1:
            return self.p1Score
        else:
            return self.p2Score

    def getAdjacent(self, position):
        adj = []
        x = position[0]
        y = position[1]
        z = position[2]
        if self.board.__contains__((x + 1, y - 1, z)):
            adj.append((x + 1, y - 1, z))
        if self.board.__contains__(x - 1, y + 1, z):
            adj.append((x - 1, y + 1, z))
        if self.board.__contains__((x + 1, y, z - 1)):
            adj.append((x + 1, y, z - 1))
        if self.board.__contains__((x - 1, y, z + 1)):
            adj.append((x - 1, y, z + 1))
        if self.board.__contains__((x, y + 1, z - 1)):
            adj.append((x, y + 1, z - 1))
        if self.board.__contains__((x, y - 1, z + 1)):
            adj.append((x, y - 1, z + 1))

        return adj

    def getShape(self, shape, position):
        if self.board.__contains__(position):
            tile = board[position]
            shape.append(position)
            for adj in self.getAdjacent(position):
                if self.board[adj] == tile:
                    if adj not in shape:
                        shape = self.getShape(shape, adj)
        return shape


    def getActions(self):
        actions = self.getTilePostions(0)
        playerPositions = self.getTilePostions(self.turn)
        while len(playerPositions) > 0:
            shape = self.getShape([], playerPositions[0])
            if len(shape) == 4:
                for tile in shape:
                    actions.remove(tile)
            playerPositions.remove(shape)
        return actions

    def takeAction(self, action):
        self.board[action] = self.turn
        evolvedShape = self.getShape(action)
        for tile in evolvedShape:

        newState = State(self.board[action] == self.turn, self.turn % 2 + 1, )





if __name__ == '__main__':
    board = State()
    print(board)
    print(board.board.__contains__((-5, 0, 0)))
    print(State.getTilePostions(board, 1))





