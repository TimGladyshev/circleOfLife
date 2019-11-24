print("Hello World")
boardSize = 5
initialBoard = {}
for x in range(boardSize * 2 - 1):
    for y in range(boardSize * 2 - 1):
        for z in range(boardSize * 2 - 1):
            if (x - 4) + (y - 4) + (z - 4) == 0:
                initialBoard[(x - 4, y - 4, z - 4)] = 0
initialBoardKeys = list(initialBoard.keys())



for j in range(9):
    if j == 0 or j == 8:
        print("", end=" ")
        print("", end=" ")
        print("", end=" ")
        print("", end=" ")
    if j == 1 or j == 7:
        print("", end=" ")
        print("", end=" ")
        print("", end=" ")
    if j == 2 or j == 6:
        print("", end=" ")
        print("", end=" ")
    if j == 3 or j == 5:
        print("", end=" ")
    for i in range(len(initialBoardKeys)):
        if initialBoardKeys[i][0] == j - 4:
            print(initialBoard[initialBoardKeys[i]], end =" ")
    print(" ")