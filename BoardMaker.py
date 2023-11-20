
# setting up the board
from Parameters import *
import numpy as np



def checkConnectivity(board, N, M, numberOfwalls):
    startPoint = (0, 0)
    for i in range(N):
        for j in range(M):
            if board[i][j] == characterMap["wall"]:
                startPoint = (i, j)
                break
    
    x = numOfReachableNodes(startPoint, board, N, M)
    return x + numberOfwalls == N * M
 
def getInitialBoard(N, M, numberOfGhosts, numberOfWalls):
    board = np.zeros([N, M], dtype=int)
    
    isConnected = False
    while isConnected == False:
        board = np.zeros([N, M], dtype=int)
        for (x, y) in generateRandomPair(numberOfWalls, N, M):
            board[x][y] = characterMap["wall"]

        isConnected = checkConnectivity(board, N, M, numberOfWalls)

        pacPos = getEmptyPos(board, N, M)
        board[pacPos[0]][pacPos[1]] = characterMap["pacman"]

        ghostPoses = []
        for i in range(numberOfGhosts):
            ghostPoses.append(getEmptyPos(board, N, M))
            board[ghostPoses[i][0]][ghostPoses[i][1]] = characterMap["ghost"]

        for i in range(N):
            for j in range(M):
                if board[i][j] == characterMap["emptyBlock"]:
                    board[i][j] = characterMap["blockWithDot"]

    mark = np.zeros((N, M), dtype=bool)
    mark[pacPos[0]][pacPos[1]] = True

    return {
        "board": board,
        "size": {
            "N": N,
            "M": M
        },
        "PacmanPos": pacPos,
        "lastMoveId": 0,
        "ghostPosesArray": ghostPoses,
        "numberOfDots": N * M - (numberOfWalls + 1),
        "mark": mark,
        "age": 0
    }
