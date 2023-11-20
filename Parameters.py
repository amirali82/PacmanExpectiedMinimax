from random import randint
from queue import Queue

characterMap = {
    "emptyBlock" : 0,
    "blockWithDot" : 1,
    "pacman" : 2,
    "ghost" : 3,
    "wall" : 4,
}

def generateRandomPair(numberOfPairs, N, M):
    if numberOfPairs == 1:
        x = randint(0, N - 1)
        y = randint(0, M - 1)
        return (x, y)
    
    mark = set()
    while len(mark) < numberOfPairs:
        x = randint(0, N - 1)
        y = randint(0, M - 1)

        if (x, y) not in mark:
            mark.add((x, y))
    
    return mark

def isSafe(board, N, M, x, y):
    x = (x + N) % N
    y = (y + M) % M
    return (board[x][y] != characterMap["wall"])

def numOfReachableNodes(v, board, N, M):
    mark = Queue(maxsize=N*M)
    flag = [[False for i in range(M)] for j in range(N)]
    
    cnt = 0
    mark.put(v)
    flag[v[0]][v[1]]  = True
    
    dx = [0,  0, 1, -1]
    dy = [1, -1, 0,  0]
    while mark.empty() != True:
        v = mark.get()
        for i in range(4):
            u = ((v[0] + dx[i] + N) % N, (v[1] + dy[i] + M) % M)
            if isSafe(board, N, M, u[0], u[1]) and flag[u[0]][u[1]] != True:
                cnt += 1
                mark.put(u)
                flag[u[0]][u[1]] = True

    return cnt

def getEmptyPos(board, N, M):
    flag = False
    pos = (0, 0)
    while flag == False:
        pos = generateRandomPair(1, N, M)

        flag = (board[pos[0]][pos[1]] == characterMap["emptyBlock"])
    
    return pos