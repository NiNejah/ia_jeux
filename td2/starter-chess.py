# -*- coding: utf-8 -*-
import math
import time
import chess
from random import randint, choice
from math import sqrt, inf, pow


def randomMove(b):
    '''Renvoie un mouvement au hasard sur la liste des mouvements possibles. Pour avoir un choix au hasard, il faut
    construire explicitement tous les mouvements. Or, generate_legal_moves() nous donne un itérateur.'''
    return choice([m for m in b.generate_legal_moves()])


def deroulementRandom(b):
    '''Déroulement d'une partie d'échecs au hasard des coups possibles. Cela va donner presque exclusivement
    des parties très longues et sans gagnant. Cela illustre cependant comment on peut jouer avec la librairie
    très simplement.'''
    print("----------")
    print(b)
    if b.is_game_over():
        print("Resultat : ", b.result())
        return
    b.push(randomMove(b))
    deroulementRandom(b)
    b.pop()


##aux function
def displayTime(start: float, end: float, functionName: str):
    print(f" {functionName} function ", end=" ")
    m = 0
    s = end - start
    if s > 60:
        m = s / 60
        s %= 60
    print("take {} Minutes {:.2} Seconds as a run time".format(m, s))


'''************************************* EXO1 *************************************'''


def possibleGamesAux(b: chess.Board, depth: int, games: list, nodes: list):
    if b.is_game_over() or depth == 0:
        # eval(b)
        games.append(1)
    else:
        for m in b.generate_legal_moves():
            b.push(m)
            nodes.append(1)
            possibleGamesAux(b, depth - 1, games, nodes)
            b.pop()


def possibleGames(b: chess.Board, depth: int = 3):
    game = []
    nodes = []
    possibleGamesAux(b, depth, game, nodes)
    return len(game), len(nodes)


def possibleGamesTest(b: chess.Board):
    for depth in range(1, 10):
        start = time.time()
        g, n = possibleGames(b, depth)
        end = time.time()
        print(f"for depth = {depth} we have {g} games and {n} nodes \ntime of execution {(end - start)} s");
        print("-----------------------")


'''********************************************************************************'''

'''************************************* EXO2 *************************************'''


def dist(pos1: int, pos2: int):
    x1 = pos1 % 8
    y1 = pos1 // 8
    x2 = pos2 % 8
    y2 = pos2 // 8
    return sqrt((pow(x1 - x2, 2)) + (pow(y1 - y2, 2)))


def findPos(b: chess.Board, piece: str) -> int:
    for k, p in b.piece_map().items():
        if p.symbol() == piece:
            return k
    return -1


def evaluation(b: chess.Board) -> float:
    value = {
        'K': 200,
        'Q': 9,
        'R': 5,
        'B': 3,
        'N': 3,
        'P': 1,
        '.': 0
    }
    score, posfac = 0, .2
    for k, p in b.piece_map().items():
        l = p.symbol()
        u = l.upper()
        pos = k // 8
        # upper AMI ;
        if l == u:
            score += value[l]
            if l != 'K':
                score += (pos * posfac)
                kingPos = findPos(b, 'k')
                if kingPos != -1:
                    score -= dist(k, kingPos) * .3
        # lower ENNEMI :
        else:
            score -= value[u]
            if l != 'k':
                score += ((1 - pos) * posfac)
                kingPos = findPos(b, 'K')
                if kingPos != -1:
                    score += dist(k, kingPos) * .3
    return score


def minMax(b: chess.Board, depth: int = 3) -> float:
    if depth == 0:
        return evaluation(b)
    if b.is_game_over():
        return evaluationGameOver(b)
    worstScore = inf
    for m in b.generate_legal_moves():
        b.push(m)
        eval = maxMin(b, depth - 1)
        b.pop()
        worstScore = min(eval, worstScore)
    return worstScore


def maxMin(b: chess.Board, depth: int = 3) -> float:
    if depth == 0:
        return evaluation(b)
    if b.is_game_over():
        return evaluationGameOver(b)
    bestScore = - inf
    for m in b.generate_legal_moves():
        b.push(m)
        eval = minMax(b, depth - 1)
        b.pop()
        bestScore = max(eval, bestScore)
    return bestScore


def evaluationGameOver(b: chess.Board) -> int:
    if b.result() == "1-0":
        return 500
    elif b.result() == "0-1":
        return -500
    else:
        return 0


def maxMovement(b: chess.Board, depth: int = 3) -> chess.Move:
    bestScoreMove = None
    bestScore = -inf
    for m in b.generate_legal_moves():
        b.push(m)
        evl = minMax(b, depth - 1)
        b.pop()
        if (evl > bestScore) or (bestScoreMove is None):
            bestScore = evl
            bestScoreMove = m
    return bestScoreMove


def minMovement(b: chess.Board, depth: int = 3) -> chess.Move:
    worstScoreMove = None
    worstScoreVal = inf
    for m in b.generate_legal_moves():
        b.push(m)
        evl = maxMin(b, depth - 1)
        b.pop()
        if (evl < worstScoreVal) or (worstScoreMove is None):
            worstScoreVal = evl
            worstScoreMove = m
    return worstScoreMove


def playGame(b: chess.Board, depthAmi: int = 1, depthEnnemi: int = 1) -> str:
    while True:
        b.push(maxMovement(b, depthAmi))
        # print(b)
        if b.is_game_over():
            return b.result()
        # print("--------------------")
        b.push(minMovement(b, depthEnnemi))
        # print(b)
        # print("--------------------")
        if b.is_game_over():
            return b.result()


def playGameTest(b: chess.Board):
    amiUserDepth = int(input("AMI depth : "))
    ennUserDepth = int(input("ENNEMI depth : "))
    s = time.time()
    res = playGame(b, amiUserDepth, ennUserDepth)
    e = time.time()
    print(f"* AMI depth = {amiUserDepth}, ENNUMI depth = {ennUserDepth}")
    displayTime(s, e, "Max - Min")
    print("*** ", "AMI WIN" if res == "1-0" else "ENNEMI WIN" if res == "0-1" else "EGA", " ***")


'''********************************************************************************'''

'''************************** L’alpha et l’oméga de α − β *************************'''


# alpha = -inf
def maxValue(b: chess.Board, alpha: float, omega: float, depth: int = 3) -> float:
    if depth == 0:
        return evaluation(b)
    if b.is_game_over():
        return evaluationGameOver(b)
    for m in b.generate_legal_moves():
        b.push(m)
        alpha = max(alpha, minValue(b, alpha, omega, depth - 1))
        b.pop()
        if alpha >= omega:
            return omega
    return alpha


def minValue(b: chess.Board, alpha: float, omega: float, depth: int = 3) -> float:
    if depth == 0:
        return evaluation(b)
    if b.is_game_over():
        return evaluationGameOver(b)
    for m in b.generate_legal_moves():
        b.push(m)
        omega = min(omega, maxValue(b, alpha, omega, depth - 1))
        b.pop()
        if alpha >= omega:
            return alpha
    return omega


def maxAOMovement(b: chess.Board, depth: int = 3) -> chess.Move:
    bestScoreMove = None
    bestScore = -inf
    for m in b.generate_legal_moves():
        b.push(m)
        evl = minValue(b, -inf, inf, depth - 1)
        b.pop()
        if (evl > bestScore) or (bestScoreMove is None):
            bestScoreMove = m
            bestScore = evl
    return bestScoreMove


def minAOMovement(b: chess.Board, depth: int = 3) -> chess.Move:
    worstScoreMove = None
    worstScoreVal = inf
    for m in b.generate_legal_moves():
        b.push(m)
        evl = maxValue(b, -inf, inf, depth - 1)
        b.pop()
        if (evl < worstScoreVal) or (worstScoreMove is None):
            worstScoreVal = evl
            worstScoreMove = m
    return worstScoreMove


def playGameOnAO(b: chess.Board, depthAmi: int = 1, depthEnnemi: int = 1) -> str:
    while True:
        b.push(maxAOMovement(b, depthAmi))
        # print(b)
        if b.is_game_over():
            return b.result()
        # print("--------------------")
        b.push(minAOMovement(b, depthEnnemi))
        # print(b)
        # print("--------------------")
        if b.is_game_over():
            return b.result()


def playGameOnAOTest(b: chess.Board):
    amiUserDepth = int(input("AMI depth : "))
    ennUserDepth = int(input("ENNEMI depth : "))
    s = time.time()
    res = playGameOnAO(b, amiUserDepth, ennUserDepth)
    e = time.time()
    print(f"* AMI depth = {amiUserDepth}, ENNUMI depth = {ennUserDepth}")
    displayTime(s, e, "Alfa - Omega")
    print("*** ", "AMI WIN" if res == "1-0" else "ENNEMI WIN" if res == "0-1" else "EGA", " ***")


'''********************************************************************************'''


def main():
    board = chess.Board()
    # deroulementRandom(board)
    ## EXO 1 test:
    # possibleGamesTest(board)
    # EXO 2 test :
    playGameTest(board)
    board.reset()
    ## EXO 3
    playGameOnAOTest(board)


main()
