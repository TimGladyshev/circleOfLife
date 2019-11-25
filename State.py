import copy
import queue
import collections


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
        if self.board.__contains__((x - 1, y + 1, z)):
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
    """
    def getShapeRecursive(self, shape, position):
        if self.board.__contains__(position):
            tile = self.board[position]
            shape.append(position)
            for adj in self.getAdjacent(position):
                if self.board[adj] == tile:
                    if adj not in shape:
                        self.getShapeRecursive(shape, adj)
                        #shape.append(appendum)
                        #print(appendum)
        return shape

    def getShape(self, position):
        shape = []
        self.getShapeRecursive(shape, position)
        return shape
    """
    def getShape(self, position):
        player = self.board[position]
        shape = [position]
        q = queue.Queue()
        q.put(position)
        while not q.empty():
            tile = q.get()
            for adj in self.getAdjacent(tile):
                if self.board[adj] == player:
                    if adj not in shape:
                        shape.append(adj)
                        q.put(adj)

        return shape

    """
    def getPath(self, shape):
        edges = []
        startIndex = 1
        shape1 = copy.deepcopy(shape)
        while len(shape1) > 0:
            adj = self.getAdjacent(shape1[0])
            womboCombo = list(set(shape1 + adj))
            for i in range(len(womboCombo)):
                edges.append((startIndex, i + 1 + startIndex))
            shape1 = list(set(shape1 - adj))
            startIndex += 1
    """

    def getActions(self):
        """
        Remeber to add getPerimiter()
        :return:
        """
        actions = self.getTilePostions(0)
        playerPositions = self.getTilePostions(self.turn)
        while len(playerPositions) > 0:
            shape = self.getShape([], playerPositions[0])
            if len(shape) == 4:
                for tile in shape:
                    actions.remove(tile)
            playerPositions.remove(shape)
        return actions

    def getPerimiter(self, shape):
        perimiter = []
        for tile in shape:
            perimiter += list(set(self.getAdjacent(tile)) - set(perimiter))

    def getPath(self, shape):
        return

    def typeShape(self, shape):
        """
        Finds the name of the shape (list of locations)
        straight line means one of the coordinates is the same
        :param shape: list of locations
        :return: name of shape (index from 1 - 12)
        """
        length = len(shape)

        dim1 = collections.Counter([i[0] for i in shape])
        dim2 = collections.Counter([i[1] for i in shape])
        dim3 = collections.Counter([i[2] for i in shape])

        maxD = max(len(dim1), len(dim2), len(dim3))
        minD = min(len(dim1), len(dim2), len(dim3))

        if length == 1:
            return 1
        elif length == 2:
            return 2
        elif length == 3:
            if maxD == 3:
                return 3
            elif minD == 1:
                return 4
            else:
                return 5
        elif length == 4:
            if minD == 1:
                return 12
            elif len(dim1) == len(dim2) == len(dim3) == 3:
                return 11
            elif maxD == 4:
                if len(dim1) == 2:
                    if max([dim1[i] for i in dim1.elements()]) == 3:
                        return 7
                    else:
                        return 9
                elif len(dim2) == 2:
                    if max([dim2[i] for i in dim2.elements()]) == 3:
                        return 7
                    else:
                        return 9
                else:
                    if max([dim3[i] for i in dim3.elements()]) == 3:
                        return 7
                    else:
                        return 9
            else:
                if len(dim1) == 2:
                    if max([dim1[i] for i in dim1.elements()]) == 3:
                        return 6
                    else:
                        if len(dim1) == len(dim2) == 2 or len(dim2) == len(dim3) == 2 or len(dim1) == len(dim3) == 2:
                            return 10
                        else:
                            return 8
                elif len(dim2) == 2:
                    if max([dim2[i] for i in dim2.elements()]) == 3:
                        return 6
                    else:
                        if len(dim1) == len(dim2) == 2 or len(dim2) == len(dim3) == 2 or len(dim1) == len(dim3) == 2:
                            return 10
                        else:
                            return 8
                elif len(dim3) == 2:
                    if max([dim3[i] for i in dim3.elements()]) == 3:
                        return 6
                    else:
                        if len(dim1) == len(dim2) == 2 or len(dim2) == len(dim3) == 2 or len(dim1) == len(dim3) == 2:
                            return 10
                        else:
                            return 8

    def flip(self, shape, dimension):
        """
        flips ya shape around desired axis bruv
        :param shape: list of points
        :param dimension: 0 - x, 1 - y, 2 - z
        :return: set of points describing shape
        """
        newShape = []
        for tile in shape:
            new_tile = [None, None, None]
            new_tile[dimension] = tile[dimension]
            new_tile[(dimension + 1) % 3] = tile[(dimension + 2) % 3]
            new_tile[(dimension + 2) % 3] = tile[(dimension + 1) % 3]
            newShape.append(tuple(new_tile))

        return set(newShape)



    def takeAction(self, action):
        newBoard = copy.deepcopy(self.board)
        self.board[action] = self.turn
        nextTurn = self.turn % 2 + 1
        evolvedShape = self.getShape([], action)
        evolvedShapeName = self.typeShape(evolvedShape)
        perimeter = self.getPerimiter(evolvedShape)
        captured = []
        while perimeter:
            if self.board[perimeter[0]] == nextTurn:
                shape = self.getShape(perimeter[0])
                if evolvedShapeName == self.typeShape(shape) + 1:
                    captured.append(shape)
                perimeter = list(set(perimeter) - set(shape))
            else:
                perimeter.pop(0)

        for tile in captured:
            newBoard[tile] = 0
        newBoard[action] = self.turn
        self.board[action] = 0
        if self.turn == 1:
            newState = State(newBoard, nextTurn, self.p1Score + len(captured), self.p2Score)
            return newState
        else:
            newState = State(newBoard, nextTurn, self.p1Score, self.p2Score + len(captured))
            return newState

    def placeShape(self, shape, player):
        for tile in shape:
            self.board[tile] = player


if __name__ == '__main__':
    board = State()
    print(board)
    board.board[(-1, 1, 0)] = 1
    board.board[(-2, 1, 1)] = 1
    board.board[(-1, 0, 1)] = 1
    board.board[(-3, 1, 2)] = 1
    print("\n")
    print(board)

    shape = board.getShape((-1, 1, 0))
    print(shape)
    newShape = board.flip(shape, 0)
    board.placeShape(shape, 0)
    board.placeShape(newShape, 1)
    print(board)
    print(board.typeShape(newShape))
    """
    print(board.board.__contains__((-5, 0, 0)))
    print(State.getTilePostions(board, 1))
    newState = board.takeAction((2, 0, -2))
    print(newState)
    newActions = newState.getActions()
    shape1 = newState.getShape([], (2, 0, -2))
    print(shape1)
    print(len(newActions))
    print(len(list(set(newActions + shape1))))
    """



