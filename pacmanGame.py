from BoardMaker import getInitialBoard
from Parameters import characterMap, isSafe
from random import randint, shuffle
import copy
import numpy as np

# Parameters
N = 5
M = 10
NUMBER_OF_WALLS = 15
NUMBER_OF_GHOSTS = 2
INF = 100340
dx = [0, 0,  0,  1, -1]
dy = [0, 1, -1,  0,  0]
CHANCE = [0.12, 0.22, 0.22, 0.22, 0.22]

prev_numberOfDots = N * M - NUMBER_OF_WALLS - 1

class moveSeq:
    class move:
        pass
    seq = []

def isPacmanAlive(state):
    pacPos = state["PacmanPos"]

    if state["board"][pacPos[0]][pacPos[1]] != characterMap["pacman"]:
        return False
    else:
        return True

def isGameOver(state):
    return (state["numberOfDots"] == 0 or 
            isPacmanAlive(state) == False)

def expectedUtility(state):
    if isPacmanAlive(state) == False:
        return -INF
    
    eVal = -(state["numberOfDots"])
    return eVal


def nextStep(state, playerNumber):
    res = []

    if playerNumber == 0:
        pacPos = state["PacmanPos"]
        
        for i in range(len(dx)):
            x = (pacPos[0] + N + dx[i]) % N
            y = (pacPos[1] + M + dy[i]) % M

            if isSafe(state["board"], N, M, x, y):
                newState = dict(copy.deepcopy(state)) # not so efficent

                newState["board"][pacPos[0]][pacPos[1]] = characterMap["emptyBlock"]
                if newState["board"][x][y] != characterMap["ghost"]:
                    newState["board"][x][y] = characterMap["pacman"]
                    
                if state["mark"][x][y] == False:
                    newState["numberOfDots"] = state["numberOfDots"] - 1
                    newState["mark"][x][y] = True
                
                newState["board"][pacPos[0]][pacPos[1]] = characterMap["emptyBlock"]
                newState["PacmanPos"] = (x, y)
                newState["age"] = state["age"] + 1
                newState["lastMoveId"] = i

                # print(">> ", newState["numberOfDots"], state["numberOfDots"])
                res.append(newState)
    
    else:
        ghostPos = state["ghostPosesArray"][playerNumber - 1]

        for i in range(len(dx)):
            x = (ghostPos[0] + N + dx[i]) % N
            y = (ghostPos[1] + M + dy[i]) % M

            if isSafe(state["board"], N, M, x, y):
                newState = dict(copy.deepcopy(state))

                if state["mark"][ghostPos[0]][ghostPos[1]] == False:
                    newState["board"][ghostPos[0]][ghostPos[1]] = characterMap["blockWithDot"]
                else:
                    newState["board"][ghostPos[0]][ghostPos[1]] = characterMap["emptyBlock"]
                newState["board"][x][y] = characterMap["ghost"]

                newState["ghostPosesArray"][playerNumber - 1] = (x, y)
                newState["age"] = state["age"] + 1
                newState["lastMoveId"] = i

                res.append(newState)

    shuffle(res)
    return res

def ExpectedMiniMax(state, depth, playerNumber):
    if depth == 0 or isGameOver(state) == True:
        return (state, expectedUtility(state))
    
    if playerNumber == 0:
        maxEval = -INF
        bestState = copy.deepcopy(state)
        for child in nextStep(state, playerNumber):
            eval = ExpectedMiniMax(child, depth - 1, (playerNumber + 1) % (NUMBER_OF_GHOSTS + 1))[1]
            if maxEval < eval:
                maxEval = eval
                bestState = copy.deepcopy(child)

        return (bestState, maxEval)

    else:
        minEval = INF
        bestState = copy.deepcopy(state)
        for child in nextStep(state, playerNumber):
            expectedEval = CHANCE[child["lastMoveId"]] * ExpectedMiniMax(child, depth - 1, (playerNumber + 1) % (NUMBER_OF_GHOSTS + 1))[1]
            if expectedEval < minEval:
                minEval = expectedEval
                bestState = copy.deepcopy(child)
            
        return (bestState, minEval)

def miniMax(state, depth, alpha, beta, playerNumber):
    if depth == 0 or isGameOver(state) == True:
        return (state, expectedUtility(state))
    
    if playerNumber == 0:
        maxEval = -INF
        bestState = copy.deepcopy(state)
        for child in nextStep(state, playerNumber):
            eval = miniMax(child, depth - 1, alpha, beta, (playerNumber + 1) % (NUMBER_OF_GHOSTS + 1))[1]
            if maxEval < eval:
                maxEval = eval
                bestState = copy.deepcopy(child)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break

        return (bestState, maxEval)

    else:
        minEval = INF
        bestState = copy.deepcopy(state)
        for child in nextStep(state, playerNumber):
            eval = miniMax(child, depth - 1, alpha, beta, (playerNumber + 1) % (NUMBER_OF_GHOSTS + 1))[1]
            if eval < minEval:
                minEval = eval
                bestState = copy.deepcopy(child)
            beta = min(beta, eval)
            if beta <= alpha:
                break
            
        return (bestState, minEval)

filter = {
    0 : ' ',
    1 : '.',
    2 : 'P',
    3 : 'G',
    4 : '#',
}

def printMove(state):

    for i in range(state['size']['N']):
        for j in range(state['size']['M']):
            print(filter[state["board"][i][j]], file=open("pac.txt", 'a'), end='')
        print(file=open("pac.txt", 'a'))

    #print(state["board"], file=open("pac.txt", 'a'))
    print("Dots left:", state["numberOfDots"], file=open("pac.txt", 'a'))
    print("State Number:", state["age"] // 3, file=open("pac.txt", 'a'))
    print("ExpectedUtility Of Move:", expectedUtility(state), file=open("pac.txt", 'a'))
    print("---------------------", file=open("pac.txt", 'a'))

open('pac.txt', 'w').close()
GameInfo = getInitialBoard(N, M, NUMBER_OF_GHOSTS, NUMBER_OF_WALLS)
GameInfo = (GameInfo, expectedUtility(GameInfo))
printMove(GameInfo[0])

while isGameOver(GameInfo[0]) == False:
    #GameInfo = miniMax(GameInfo[0], (NUMBER_OF_GHOSTS + 1) * 3, -INF, INF, 0)
    GameInfo = ExpectedMiniMax(GameInfo[0], (NUMBER_OF_GHOSTS + 1) * 2, 0)

    for i in range(NUMBER_OF_GHOSTS):
        options = nextStep(GameInfo[0], i + 1)
        newState = options[randint(0, len(options) - 1)]
        GameInfo = (newState, expectedUtility(newState))

    printMove(GameInfo[0])
