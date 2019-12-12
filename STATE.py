import copy
import queue
import collections
import random
import sys
from _ctypes import sizeof

POINTLIST = [(-4, 0, 4), (-4, 1, 3), (-4, 2, 2), (-4, 3, 1), (-4, 4,0), (-3, -1, 4), (-3, 0, 3), (-3, 1, 2), (-3, 2, 1), (-3, 3, 0), (-3, 4, -1), (-2, -2, 4), (-2, -1, 3), (-2, 0,2), (-2, 1, 1), (-2, 2, 0), (-2, 3, -1), (-2, 4, -2), (-1, -3, 4), (-1, -2, 3), (-1, -1, 2), (-1, 0, 1), (-1, 1, 0), (-1, 2, -1), (-1, 3, -2), (-1, 4, -3), (0, -4, 4),(0, -3, 3), (0, -2, 2), (0, -1, 1), (0, 0, 0), (0, 1, -1), (0, 2, -2), (0, 3, -3), (0, 4, -4), (1, -4, 3), (1, -3, 2), (1, -2, 1), (1, -1, 0), (1, 0, -1), (1, 1, -2), (1, 2, -3), (1, 3, -4), (2, -4, 2), (2, -3, 1), (2, -2, 0), (2, -1, -1), (2, 0, -2), (2, 1, -3), (2, 2, -4), (3,-4, 1), (3, -3, 0), (3, -2, -1), (3, -1, -2), (3, 0, -3), (3, 1, -4), (4, -4, 0), (4, -3, -1), (4, -2, -2), (4,-1, -3), (4, 0, -4)]
POINTLIST_R1 = [(0, -4, 4), (-1, -3, 4), (-2, -2, 4), (-3, -1, 4), (-4, 0, 4), (1, -4, 3), (0, -3, 3), (-1, -2, 3), (-2, -1, 3), (-3, 0, 3), (-4, 1, 3), (2, -4, 2), (1, -3, 2), (0, -2, 2), (-1, -1, 2), (-2, 0, 2), (-3, 1, 2), (-4, 2, 2), (3, -4, 1), (2, -3, 1), (1, -2, 1), (0, -1, 1), (-1, 0, 1), (-2, 1, 1), (-3, 2, 1), (-4, 3, 1), (4, -4, 0), (3, -3, 0), (2, -2, 0), (1, -1, 0), (0, 0, 0), (-1, 1, 0), (-2, 2, 0), (-3, 3, 0), (-4, 4, 0), (4, -3, -1), (3, -2, -1), (2, -1, -1), (1, 0, -1), (0, 1, -1), (-1, 2, -1), (-2, 3, -1), (-3, 4, -1), (4, -2, -2), (3, -1, -2), (2, 0, -2), (1, 1, -2), (0, 2, -2), (-1, 3, -2), (-2, 4, -2), (4, -1, -3), (3, 0, -3), (2, 1, -3), (1, 2, -3), (0, 3, -3), (-1, 4, -3), (4, 0, -4), (3, 1, -4), (2, 2, -4), (1, 3, -4), (0, 4, -4)]
POINTLIST_R2 = [(4, -4, 0), (3, -4, 1), (2, -4, 2), (1, -4, 3), (0, -4, 4), (4, -3, -1), (3, -3, 0), (2, -3, 1), (1, -3, 2), (0, -3, 3), (-1, -3, 4), (4, -2, -2), (3, -2, -1), (2, -2, 0), (1, -2, 1), (0, -2, 2), (-1, -2, 3), (-2, -2, 4), (4, -1, -3), (3, -1, -2), (2, -1, -1), (1, -1, 0), (0, -1, 1), (-1, -1, 2), (-2, -1, 3), (-3, -1, 4), (4, 0, -4), (3, 0, -3), (2, 0, -2), (1, 0, -1), (0, 0, 0), (-1, 0, 1), (-2, 0, 2), (-3, 0, 3), (-4, 0, 4), (3, 1, -4), (2, 1, -3), (1, 1, -2), (0, 1, -1), (-1, 1, 0), (-2, 1, 1), (-3, 1, 2), (-4, 1, 3), (2, 2, -4), (1, 2, -3), (0, 2, -2), (-1, 2, -1), (-2, 2, 0), (-3, 2, 1), (-4, 2, 2), (1, 3, -4), (0, 3, -3), (-1, 3, -2), (-2, 3, -1), (-3, 3, 0), (-4, 3, 1), (0, 4, -4), (-1, 4, -3), (-2, 4, -2), (-3, 4, -1), (-4, 4, 0)]
POINTLIST_R3 = [(4, 0, -4), (4, -1, -3), (4, -2, -2), (4, -3, -1), (4, -4, 0), (3, 1, -4), (3, 0, -3), (3, -1, -2), (3, -2, -1), (3, -3, 0), (3, -4, 1), (2, 2, -4), (2, 1, -3), (2, 0, -2), (2, -1, -1), (2, -2, 0), (2, -3, 1), (2, -4, 2), (1, 3, -4), (1, 2, -3), (1, 1, -2), (1, 0, -1), (1, -1, 0), (1, -2, 1), (1, -3, 2), (1, -4, 3), (0, 4, -4), (0, 3, -3), (0, 2, -2), (0, 1, -1), (0, 0, 0), (0, -1, 1), (0, -2, 2), (0, -3, 3), (0, -4, 4), (-1, 4, -3), (-1, 3, -2), (-1, 2, -1), (-1, 1, 0), (-1, 0, 1), (-1, -1, 2), (-1, -2, 3), (-1, -3, 4), (-2, 4, -2), (-2, 3, -1), (-2, 2, 0), (-2, 1, 1), (-2, 0, 2), (-2, -1, 3), (-2, -2, 4), (-3, 4, -1), (-3, 3, 0), (-3, 2, 1), (-3, 1, 2), (-3, 0, 3), (-3, -1, 4), (-4, 4, 0), (-4, 3, 1), (-4, 2, 2), (-4, 1, 3), (-4, 0, 4)]
POINTLIST_R4 = [(0, 4, -4), (1, 3, -4), (2, 2, -4), (3, 1, -4), (4, 0, -4), (-1, 4, -3), (0, 3, -3), (1, 2, -3), (2, 1, -3), (3, 0, -3), (4, -1, -3), (-2, 4, -2), (-1, 3, -2), (0, 2, -2), (1, 1, -2), (2, 0, -2), (3, -1, -2), (4, -2, -2), (-3, 4, -1), (-2, 3, -1), (-1, 2, -1), (0, 1, -1), (1, 0, -1), (2, -1, -1), (3, -2, -1), (4, -3, -1), (-4, 4, 0), (-3, 3, 0), (-2, 2, 0), (-1, 1, 0), (0, 0, 0), (1, -1, 0), (2, -2, 0), (3, -3, 0), (4, -4, 0), (-4, 3, 1), (-3, 2, 1), (-2, 1, 1), (-1, 0, 1), (0, -1, 1), (1, -2, 1), (2, -3, 1), (3, -4, 1), (-4, 2, 2), (-3, 1, 2), (-2, 0, 2), (-1, -1, 2), (0, -2, 2), (1, -3, 2), (2, -4, 2), (-4, 1, 3), (-3, 0, 3), (-2, -1, 3), (-1, -2, 3), (0, -3, 3), (1, -4, 3), (-4, 0, 4), (-3, -1, 4), (-2, -2, 4), (-1, -3, 4), (0, -4, 4)]
POINTLIST_R5 = [(-4, 4, 0), (-3, 4, -1), (-2, 4, -2), (-1, 4, -3), (0, 4, -4), (-4, 3, 1), (-3, 3, 0), (-2, 3, -1), (-1, 3, -2), (0, 3, -3), (1, 3, -4), (-4, 2, 2), (-3, 2, 1), (-2, 2, 0), (-1, 2, -1), (0, 2, -2), (1, 2, -3), (2, 2, -4), (-4, 1, 3), (-3, 1, 2), (-2, 1, 1), (-1, 1, 0), (0, 1, -1), (1, 1, -2), (2, 1, -3), (3, 1, -4), (-4, 0, 4), (-3, 0, 3), (-2, 0, 2), (-1, 0, 1), (0, 0, 0), (1, 0, -1), (2, 0, -2), (3, 0, -3), (4, 0, -4), (-3, -1, 4), (-2, -1, 3), (-1, -1, 2), (0, -1, 1), (1, -1, 0), (2, -1, -1), (3, -1, -2), (4, -1, -3), (-2, -2, 4), (-1, -2, 3), (0, -2, 2), (1, -2, 1), (2, -2, 0), (3, -2, -1), (4, -2, -2), (-1, -3, 4), (0, -3, 3), (1, -3, 2), (2, -3, 1), (3, -3, 0), (4, -3, -1), (0, -4, 4), (1, -4, 3), (2, -4, 2), (3, -4, 1), (4, -4, 0)]
POINTLIST_F = [(-4, 4, 0), (-4, 3, 1), (-4, 2, 2), (-4, 1, 3), (-4, 0, 4), (-3, 4, -1), (-3, 3, 0), (-3, 2, 1), (-3, 1, 2), (-3, 0, 3), (-3, -1, 4), (-2, 4, -2), (-2, 3, -1), (-2, 2, 0), (-2, 1, 1), (-2, 0, 2), (-2, -1, 3), (-2, -2, 4), (-1, 4, -3), (-1, 3, -2), (-1, 2, -1), (-1, 1, 0), (-1, 0, 1), (-1, -1, 2), (-1, -2, 3), (-1, -3, 4), (0, 4, -4), (0, 3, -3), (0, 2, -2), (0, 1, -1), (0, 0, 0), (0, -1, 1), (0, -2, 2), (0, -3, 3), (0, -4, 4), (1, 3, -4), (1, 2, -3), (1, 1, -2), (1, 0, -1), (1, -1, 0), (1, -2, 1), (1, -3, 2), (1, -4, 3), (2, 2, -4), (2, 1, -3), (2, 0, -2), (2, -1, -1), (2, -2, 0), (2, -3, 1), (2, -4, 2), (3, 1, -4), (3, 0, -3), (3, -1, -2), (3, -2, -1), (3, -3, 0), (3, -4, 1), (4, 0, -4), (4, -1, -3), (4, -2, -2), (4, -3, -1), (4, -4, 0)]
POINTLIST_FR1 = [(-4, 0, 4), (-3, -1, 4), (-2, -2, 4), (-1, -3, 4), (0, -4, 4), (-4, 1, 3), (-3, 0, 3), (-2, -1, 3), (-1, -2, 3), (0, -3, 3), (1, -4, 3), (-4, 2, 2), (-3, 1, 2), (-2, 0, 2), (-1, -1, 2), (0, -2, 2), (1, -3, 2), (2, -4, 2), (-4, 3, 1), (-3, 2, 1), (-2, 1, 1), (-1, 0, 1), (0, -1, 1), (1, -2, 1), (2, -3, 1), (3, -4, 1), (-4, 4, 0), (-3, 3, 0), (-2, 2, 0), (-1, 1, 0), (0, 0, 0), (1, -1, 0), (2, -2, 0), (3, -3, 0), (4, -4, 0), (-3, 4, -1), (-2, 3, -1), (-1, 2, -1), (0, 1, -1), (1, 0, -1), (2, -1, -1), (3, -2, -1), (4, -3, -1), (-2, 4, -2), (-1, 3, -2), (0, 2, -2), (1, 1, -2), (2, 0, -2), (3, -1, -2), (4, -2, -2), (-1, 4, -3), (0, 3, -3), (1, 2, -3), (2, 1, -3), (3, 0, -3), (4, -1, -3), (0, 4, -4), (1, 3, -4), (2, 2, -4), (3, 1, -4), (4, 0, -4)]
POINTLIST_FR2 = [(0, -4, 4), (1, -4, 3), (2, -4, 2), (3, -4, 1), (4, -4, 0), (-1, -3, 4), (0, -3, 3), (1, -3, 2), (2, -3, 1), (3, -3, 0), (4, -3, -1), (-2, -2, 4), (-1, -2, 3), (0, -2, 2), (1, -2, 1), (2, -2, 0), (3, -2, -1), (4, -2, -2), (-3, -1, 4), (-2, -1, 3), (-1, -1, 2), (0, -1, 1), (1, -1, 0), (2, -1, -1), (3, -1, -2), (4, -1, -3), (-4, 0, 4), (-3, 0, 3), (-2, 0, 2), (-1, 0, 1), (0, 0, 0), (1, 0, -1), (2, 0, -2), (3, 0, -3), (4, 0, -4), (-4, 1, 3), (-3, 1, 2), (-2, 1, 1), (-1, 1, 0), (0, 1, -1), (1, 1, -2), (2, 1, -3), (3, 1, -4), (-4, 2, 2), (-3, 2, 1), (-2, 2, 0), (-1, 2, -1), (0, 2, -2), (1, 2, -3), (2, 2, -4), (-4, 3, 1), (-3, 3, 0), (-2, 3, -1), (-1, 3, -2), (0, 3, -3), (1, 3, -4), (-4, 4, 0), (-3, 4, -1), (-2, 4, -2), (-1, 4, -3), (0, 4, -4)]
POINTLIST_FR3 = [(4, -4, 0), (4, -3, -1), (4, -2, -2), (4, -1, -3), (4, 0, -4), (3, -4, 1), (3, -3, 0), (3, -2, -1), (3, -1, -2), (3, 0, -3), (3, 1, -4), (2, -4, 2), (2, -3, 1), (2, -2, 0), (2, -1, -1), (2, 0, -2), (2, 1, -3), (2, 2, -4), (1, -4, 3), (1, -3, 2), (1, -2, 1), (1, -1, 0), (1, 0, -1), (1, 1, -2), (1, 2, -3), (1, 3, -4), (0, -4, 4), (0, -3, 3), (0, -2, 2), (0, -1, 1), (0, 0, 0), (0, 1, -1), (0, 2, -2), (0, 3, -3), (0, 4, -4), (-1, -3, 4), (-1, -2, 3), (-1, -1, 2), (-1, 0, 1), (-1, 1, 0), (-1, 2, -1), (-1, 3, -2), (-1, 4, -3), (-2, -2, 4), (-2, -1, 3), (-2, 0, 2), (-2, 1, 1), (-2, 2, 0), (-2, 3, -1), (-2, 4, -2), (-3, -1, 4), (-3, 0, 3), (-3, 1, 2), (-3, 2, 1), (-3, 3, 0), (-3, 4, -1), (-4, 0, 4), (-4, 1, 3), (-4, 2, 2), (-4, 3, 1), (-4, 4, 0)]
POINTLIST_FR4 = [(4, 0, -4), (3, 1, -4), (2, 2, -4), (1, 3, -4), (0, 4, -4), (4, -1, -3), (3, 0, -3), (2, 1, -3), (1, 2, -3), (0, 3, -3), (-1, 4, -3), (4, -2, -2), (3, -1, -2), (2, 0, -2), (1, 1, -2), (0, 2, -2), (-1, 3, -2), (-2, 4, -2), (4, -3, -1), (3, -2, -1), (2, -1, -1), (1, 0, -1), (0, 1, -1), (-1, 2, -1), (-2, 3, -1), (-3, 4, -1), (4, -4, 0), (3, -3, 0), (2, -2, 0), (1, -1, 0), (0, 0, 0), (-1, 1, 0), (-2, 2, 0), (-3, 3, 0), (-4, 4, 0), (3, -4, 1), (2, -3, 1), (1, -2, 1), (0, -1, 1), (-1, 0, 1), (-2, 1, 1), (-3, 2, 1), (-4, 3, 1), (2, -4, 2), (1, -3, 2), (0, -2, 2), (-1, -1, 2), (-2, 0, 2), (-3, 1, 2), (-4, 2, 2), (1, -4, 3), (0, -3, 3), (-1, -2, 3), (-2, -1, 3), (-3, 0, 3), (-4, 1, 3), (0, -4, 4), (-1, -3, 4), (-2, -2, 4), (-3, -1, 4), (-4, 0, 4)]
POINTLIST_FR5 = [(0, 4, -4), (-1, 4, -3), (-2, 4, -2), (-3, 4, -1), (-4, 4, 0), (1, 3, -4), (0, 3, -3), (-1, 3, -2), (-2, 3, -1), (-3, 3, 0), (-4, 3, 1), (2, 2, -4), (1, 2, -3), (0, 2, -2), (-1, 2, -1), (-2, 2, 0), (-3, 2, 1), (-4, 2, 2), (3, 1, -4), (2, 1, -3), (1, 1, -2), (0, 1, -1), (-1, 1, 0), (-2, 1, 1), (-3, 1, 2), (-4, 1, 3), (4, 0, -4), (3, 0, -3), (2, 0, -2), (1, 0, -1), (0, 0, 0), (-1, 0, 1), (-2, 0, 2), (-3, 0, 3), (-4, 0, 4), (4, -1, -3), (3, -1, -2), (2, -1, -1), (1, -1, 0), (0, -1, 1), (-1, -1, 2), (-2, -1, 3), (-3, -1, 4), (4, -2, -2), (3, -2, -1), (2, -2, 0), (1, -2, 1), (0, -2, 2), (-1, -2, 3), (-2, -2, 4), (4, -3, -1), (3, -3, 0), (2, -3, 1), (1, -3, 2), (0, -3, 3), (-1, -3, 4), (4, -4, 0), (3, -4, 1), (2, -4, 2), (1, -4, 3), (0, -4, 4)]

POINTLISTS = [POINTLIST, POINTLIST_R1, POINTLIST_R2, POINTLIST_R3, POINTLIST_R4, POINTLIST_R5, POINTLIST_F, POINTLIST_FR1, POINTLIST_FR2, POINTLIST_FR3, POINTLIST_FR4, POINTLIST_FR5]

SHAPE_SUBSETS = {12:{1, 2, 4}, 11:{1,2,3}, 10:{1,2, 3}, 9:{1, 2, 3}, 8:{1, 2, 3}, 7:{1, 2, 3, 4}, 6:{1, 2, 3, 4, 5}, 5:{1, 2}, 4:{1, 2}, 3:{1, 2}, 2:{1}, 1:{}}
SHAPE_POTENTIAL = {1:{2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, 2:{3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, 3:{6, 7, 8, 9, 10, 11}, 4:{6, 7, 12}, 5:{6, 10}}

class iState:

    def makeNewBoard(self):
        pass

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

    def isTerminal(self):
        pass

    def getAdjacent(self, position):
        pass

    def getPerimeter(self, shape):
        pass


class State(iState):

    def __init__(self, boardGiven={}, player=1, score1=0, score2=0, tupleKey = None):
        # this happens only when read in
        if tupleKey != None:
            self.board = {}
            for i in range(len(POINTLIST)):
                self.board[POINTLIST[i]] = tupleKey[i]
            self.turn = tupleKey[len(POINTLIST)]
            self.p1Score = tupleKey[len(POINTLIST) + 1]
            self.p2Score = tupleKey[len(POINTLIST) + 2]
            self.terminal = self.isTerminal()
            self.key = tupleKey
        # new board
        elif len(boardGiven) == 0:
            self.makeNewBoard()
            self.p1Score = 0
            self.p2Score = 0
            self.turn = 1
            self.terminal = False
            self.key = None
        # take action
        else:
            self.board = boardGiven
            self.p1Score = score1
            self.p2Score = score2
            self.turn = player
            self.terminal = self.isTerminal()
            self.key = None

    def __key(self):
        if self.key == None:
            keys = []
            hashes = []
            maxHash = -9999999
            index = -1
            for i in range(len(POINTLISTS)):
                values = tuple(self.board[i] for i in POINTLISTS[i])
                key = values + (self.turn,) + (self.p1Score,) + (self.p2Score,)
                keys.append(key)
                h = hash(key)
                hashes.append(h)
                if h > maxHash:
                    maxHash = h
                    index = i

            self.key = keys[index]
        return self.key

    def write_key(self):
        split_string = str(self.key).split(" ")
        string = ''
        for i in split_string:
            string += i
        return string

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, State):
            return self.__key() == other.__key()
        else:
            return NotImplemented

    def __str__(self):
        printable = ""
        keys = list(sorted(self.board.keys()))
        print("Score: p1 -> %d  |  p2 -> %d" % (self.p1Score, self.p2Score))
        if self.turn == 1:
            print("Player 1 Turn")
        else:
            print("Player 2 Turn")
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
                if keys[i + 1][0] > keys[i][0]:
                    printable += "\n"
        printable += "\n"
        return printable

    def makeNewBoard(self):
        """
        Terribly inefficient, but hopefully one must only do this once
        :return: new board initiated to 0's
        """
        boardSize = 5
        initialBoard = {}
        for x in range(boardSize * 2 - 1):
            for y in range(boardSize * 2 - 1):
                for z in range(boardSize * 2 - 1):
                    if (x - 4) + (y - 4) + (z - 4) == 0:
                        initialBoard[(x - 4, y - 4, z - 4)] = 0
        self.board = initialBoard

    def getTilePostions(self, player):
        """
        Makes a set of player positions
        :param player: 0 1 or 2
        :return: set of positions
        """
        positions = set(i for i, j in self.board.items() if j == player)
        return positions

    def getScore(self, player):
        if player == 1:
            return self.p1Score
        else:
            return self.p2Score

    def isTerminal(self):
        """
        Decides if state is terminal. Marks as such for future
        :return: True or False
        """
        if self.p1Score >= 20 or self.p2Score >= 20:
            return True
        if len(self.getActions()) == 0:
            return True
        return False

    def is_terminal(self):
        return self.terminal

    def get_reward_adversarial(self):
        if self.terminal:
            if self.p2Score >= 20:
                return 1
            elif self.turn == 2 and self.p1Score < 20:
                return 1
        return -1

    def get_reward(self):
        if self.terminal:
            if self.p1Score >= 20:
                return 1
            elif self.turn == 1 and self.p2Score < 20:
                return 1
        return -1

    def getAdjacent(self, position):
        """
        Gets adjacent
        :param position: location to look from
        :return: Set of adjacent positions
        """
        adj = set()

        x = position[0]
        y = position[1]
        z = position[2]

        if (x + 1, y - 1, z) in self.board:
            adj.add((x + 1, y - 1, z))
        if (x - 1, y + 1, z) in self.board:
            adj.add((x - 1, y + 1, z))
        if (x + 1, y, z - 1) in self.board:
            adj.add((x + 1, y, z - 1))
        if (x - 1, y, z + 1) in self.board:
            adj.add((x - 1, y, z + 1))
        if (x, y + 1, z - 1) in self.board:
            adj.add((x, y + 1, z - 1))
        if (x, y - 1, z + 1) in self.board:
            adj.add((x, y - 1, z + 1))

        return adj

    def getShape(self, position):
        player = self.board[position]
        shape = set()
        shape.add(position)
        """
        q = queue.Queue()
        q.put(position)
        while not q.empty():
            tile = q.get()
            for adj in self.getAdjacent(tile):
                if adj not in shape:
                    if self.board[adj] == player:
                        shape.add(adj)
                        q.put(adj)
        """
        s = set()
        s.add(position)
        while s:
            tile = s.pop()
            adj = self.getAdjacent(tile) - shape
            for a in adj:
                if self.board[a] == player:
                    shape.add(a)
                    s.add(a)
        return shape

    def getActions(self):
        """
        Remeber to add getPerimeter()
        :return:
        """
        actions = self.getTilePostions(0)
        """
        playerPositionsCurrent = self.getTilePostions(self.turn)
        while len(playerPositionsCurrent) > 0:
            shape = self.getShape(playerPositionsCurrent.pop())
            if len(shape) == 4:
                perimeter = self.getPerimeter(shape)
                actions = actions - perimeter
            playerPositionsCurrent = playerPositionsCurrent - shape
        """
        duds = set()
        for action in actions:
            self.board[action] = self.turn
            shape = self.getShape(action)
            if self.typeShape(shape) == 0:
                    duds.add(action)
            self.board[action] = 0

        return actions - duds

    def getPerimeter(self, shape):
        perimeter = set()
        for tile in shape:
            perimeter = perimeter | (self.getAdjacent(tile) - shape)
        return perimeter

    def typeShape(self, shape):
        """
        Finds the name of the shape (list of locations)
        straight line means one dimension is the same for all tiles
        using this principle, we can name all the shapes by checking min and maximum amounts of dimensions they span
        :param shape: list of locations
        :return: name of shape (index from 1 - 12)
        """
        length = len(shape)
        dim1 = collections.Counter(i[0] for i in shape)
        dim2 = collections.Counter(i[1] for i in shape)
        dim3 = collections.Counter(i[2] for i in shape)

        maxD = max(len(dim1), len(dim2), len(dim3))
        minD = min(len(dim1), len(dim2), len(dim3))

        if length == 1:
            return 1
        elif length == 2:
            return 2
        elif length == 3:
            if maxD == 3:
                if minD == 1:
                    return 4
                else:
                    return 3
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
        else:
            return 0

    def flipAlong(self, shape, dimension):
        """
        flips ya shape along desired axis bruv
        (in normal 2 dimensions we might flip across the y-axis which is the same as flipping along the x-axis and vice versa)
        :param shape: list of points
        :param dimension: 0 - x, 1 - y, 2 - z
        :return: set of points describing flipped shape
        """
        newShape = []
        for tile in shape:
            new_tile = [None, None, None]
            new_tile[dimension] = tile[dimension]
            new_tile[(dimension + 1) % 3] = tile[(dimension + 2) % 3]
            new_tile[(dimension + 2) % 3] = tile[(dimension + 1) % 3]
            newShape.append(tuple(new_tile))

        return newShape

    def rotate(self, shape, angle):
        """
        rotates ya shape around by a desired angle bruv
        :param shape: list of points
        :param dimension: 1 - equivalent of 60 degrees counterclockwise, 2 - equivalent of 120 degrees counterclockwise, etc...
        :return: set of points describing rotated shape
        """
        newShape = []
        for tile in shape:
            new_tile = [None, None, None]
            new_tile[0] = (-1) ** (angle % 2) * tile[angle % 3]
            new_tile[1] = (-1) ** (angle % 2) * tile[(1 + angle) % 3]
            new_tile[2] = (-1) ** (angle % 2) * tile[(2 + angle) % 3]
            newShape.append(tuple(new_tile))

        return newShape

    def translate(self, shape, x=0, y=0, z=0):
        """
        translates ya shape in a desired direction bruv
        :param shape: list of points
        :param x: moves this many spaces parallel to the x-axis, increasing y and decreasing z (for positive number)
        :param y: moves this many spaces parallel to the y-axis, increasing x and decreasing z (for positive number)
        :param z: moves this many spaces parallel to the z-axis, increasing x and decreasing y (for positive number)
        :return: set of points describing translated shape
        """
        newShape = []
        for tile in shape:
            new_tile = [None, None, None]
            new_tile[0] = tile[0] + y + z
            new_tile[1] = tile[1] + x - z
            new_tile[2] = tile[2] - x - y
            if self.board.__contains__(tuple(new_tile)):
                newShape.append(tuple(new_tile))

        return newShape

    def flipAcross(self, shape, dimension):
        """
        flips ya shape across desired axis bruv
        :param shape: list of points
        :param dimension: 0 - x, 1 - y, 2 - z
        :return: set of points describing flipped shape
        """
        return self.rotate(self.flipAlong(shape, dimension), 3)

    def takeAction(self, action):
        newBoard = self.board.copy()
        self.board[action] = self.turn  # remember to flip back
        nextTurn = self.turn % 2 + 1
        evolvedShape = self.getShape(action)
        evolvedShapeName = self.typeShape(evolvedShape)
        perimeter = self.getPerimeter(evolvedShape)
        captured = set()
        while len(perimeter) > 0:
            tile = perimeter.pop()
            if self.board[tile] == nextTurn:
                shape = self.getShape(tile)
                if evolvedShapeName == self.typeShape(shape) % 12 + 1:
                    captured = captured | shape
                perimeter = perimeter - shape

        for tile in captured:
            newBoard[tile] = 0
        newBoard[action] = self.turn
        self.board[action] = 0

        if self.turn == 1:
            return State(newBoard, nextTurn, self.p1Score + len(captured), self.p2Score)
        else:
            return State(newBoard, nextTurn, self.p1Score, self.p2Score + len(captured))

    def placeShape(self, shape, player):
        for tile in shape:
            self.board[tile] = player

    def find_successors(self):
        return set(self.takeAction(i) for i in self.getActions())

    def get_all_shapes(self, player):
        shapes = collections.defaultdict()
        positions = self.getTilePostions(player)
        while positions:
            tile = positions.pop()
            shape = self.getShape(tile)
            name = self.typeShape(shape)
            if name in shapes:
                shapes[name] = shapes[name] | shape
            else:
                shapes[name] = shape

            positions = positions - shape
        return shapes

    def find_parents_fast(self):
        # Noticed that when the tree is playing with another agent, and a new node is introduced, the score will not
        #   back propagate all the way up, when (& if) a path is found from the root, the score has been bottleneck-ed.
        #   Not sure how much of an issue this is. Was thinking that we can introduce the find_parent(very slow any way
        #   I have found to make it) to back propagate until an expanded parent is found. Any parent should be able to
        #   carry score, so then we can just follow the tree. Weird bottom - up traversal.

        parents = set()

        for tile in self.getTilePostions(self.turn % 2 + 1):
            newBoard = self.board.copy()
            newBoard[tile] = 0
            parents.add(State(newBoard, player=self.turn%2 + 1, score1=self.p1Score, score2=self.p2Score))



if __name__ == '__main__':
    Board = State()
    # BigShape = Board.getShape((0, 0, 0))
    # Board.placeShape(BigShape, 2)
    # Board.placeShape([(0, 0, 0)], 0)
    # print(Board)
    # print(Board.isTerminal())
    # print(sys.getsizeof(Board.board))
    Board = Board.takeAction((-1,3,-2))

    Board2 = Board.takeAction(random.choice(tuple(Board.getActions())))
    Board3 = Board2.takeAction(random.choice(tuple(Board2.getActions())))
    Board4 = Board3.takeAction(random.choice(tuple(Board3.getActions())))
    Board4.placeShape(((0,0,0), (0, 1, -1), (0, 2, -2)), 2)
    print(len(Board4.getActions()))
    print(Board4.get_all_shapes(2))
    print(Board4)

    print(Board == Board2 == Board3 == Board4)

    dicT = dict()
    dicT[Board] = 1
    dicT[Board2] = 2
    print(dicT.keys())

    print(hash(Board))
    print(hash(Board2))
    print("getting here")

    """
    board1 = State()
    board2 = board1.takeAction((0, 0, 0))
    board3 = board2.takeAction((0, 1, -1))
    board4 = board3.takeAction((0, -1, +1))
    board5 = board4.takeAction((-1, 0, +1))
    print(board1)
    print(board2)
    print(board3)
    print(board4)
    print(board5)

    Tests 11.14.19 -->
    board = State()
    print(board)
    board.board[(2, 0, -2)] = 1
    board.board[(1, 1, -2)] = 1
    board.board[(0, 2, -2)] = 1
    board.board[(-1, 2, -1)] = 1
    print("\n Shape!")
    print(board)

    shape = board.getShape((1, 1, -2))
    print("\n Flip Along Shape (y)!")
    flipAlongShape = board.flipAlong(shape, 1)
    board.placeShape(shape, 0)
    board.placeShape(flipAlongShape, 1)
    print(board)
    print(board.typeShape(flipAlongShape))

    print("\n Flip Across Shape (y)!")
    flipAcrossShape = board.flipAcross(shape, 1)
    board.placeShape(flipAlongShape, 0)
    board.placeShape(flipAcrossShape, 1)
    print(board)    
    print(board.typeShape(flipAcrossShape))

    print("\n Rot Shape (1)!")
    rotShape = board.rotate(shape, 1)
    board.placeShape(flipAcrossShape, 0)
    board.placeShape(rotShape, 1)
    print(board)
    print(board.typeShape(rotShape))

    print("\n Rot Shape (-1)!")
    rotShape2 = board.rotate(shape, -1)
    board.placeShape(rotShape, 0)
    board.placeShape(rotShape2, 1)
    print(board)
    print(board.typeShape(rotShape2))

    print("\n Trans Shape (1,-1,0)!")
    transShape = board.translate(shape, x = 1, y = -1)
    board.placeShape(rotShape2, 0)
    board.placeShape(transShape, 1)
    print(board)
    print(board.typeShape(transShape))

    print("\n Perimeter Trans Shape (1,-1,0)!")
    perimShape = board.getPerimeter(transShape)
    board.placeShape(transShape, 0)
    board.placeShape(perimShape, 1)
    print(board)
    print(board.typeShape(perimShape))
    
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
