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
        m = s // 60
        s %= 60
    print("take {} Minutes {:.2} Seconds as a run time".format(int(m), s))


'''************************************* EXO 1.1 *************************************'''
'''Le facteur de branchement de cet arbre est 3.
Il n'est pas nécessaire que toutes les branches de l'arbre soit de même hauteur car toutes les parties n'ont pas la même durée'''

'''************************************* EXO 1.2 *************************************'''
'''Le meilleur plateau pour Ami est celui où on obtient 8. Pour ennemi, le meilleur plateau est -4. Si deux noeuds de l'arbre ont un unique fils alors c'est une
mauvaise chose pour l'ami car il est alors obligé de jouer le coup ennemi remonté.'''

'''************************************* EXO 1.3 *************************************'''
'''On peut remplacer ?? par toute valeur inférieure ou égale à 3.'''

'''************************************* EXO2.1 *************************************'''
# global variable to count the number of node in minmax
nb_nodes = 0


def possibleGamesAux(b: chess.Board, depth: int, games: list, nodes: list):
    nodes.append(1)
    if b.is_game_over() or depth == 0:
        games.append(1)
    else:
        for m in b.generate_legal_moves():
            b.push(m)
            possibleGamesAux(b, depth - 1, games, nodes)
            b.pop()


def possibleGames(b: chess.Board, depth: int = 3):
    game = []
    nodes = []
    possibleGamesAux(b, depth, game, nodes)
    return len(game), len(nodes)


def possibleGamesTest(b: chess.Board):
    for depth in range(1, 5):
        start = time.time()
        g, n = possibleGames(b, depth)
        end = time.time()
        print(f"for depth = {depth} we have {g} games and {n} nodes \ntime of execution {(end - start)} s");
        print("-----------------------")


'''********************************************************************************'''

'''************************************* EXO2 (1-2-3) *************************************'''


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
    global nb_nodes
    nb_nodes += 1
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
    global nb_nodes
    nb_nodes += 1
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
    global nb_nodes
    nb_nodes += 1
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
    global nb_nodes
    nb_nodes += 1
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


def playGameTest(b: chess.Board, amiUserDepth: int, ennUserDepth: int):
    s = time.time()
    res = playGame(b, amiUserDepth, ennUserDepth)
    e = time.time()
    print(f"* AMI depth = {amiUserDepth}, ENNEMI depth = {ennUserDepth}")
    displayTime(s, e, "Max - Min")
    print("*** ", "AMI WIN" if res == "1-0" else "ENNEMI WIN" if res == "0-1" else "EGALITE", " ***")


'''********************************************************************************'''

'''************************** EXO3 : L’alpha et l’oméga de α − β *************************'''

'''Comparaison des temps de recherche et du nombre de noeuds parcourus'''

'''Nombre de noeuds parcourus et durée pour MinMax :'''
'''Profondeur (1,1) : 1626 noeuds parcourus en 0.77 secondes'''
'''Profondeur (2,2) : 62370 noeuds parcourus en 43 secondes'''
'''Profondeur (3,3) : 1999189 noeuds parcourus en 16 minutes'''

'''Nombre de noeuds parcourus et durée pour Alpha-Oméga :'''
'''Profondeur (1,1) : 1626 noeuds parcourus en 0.77 secondes'''
'''Profondeur (2,2) : 62370 noeuds parcourus en 0.77 secondes'''
'''Profondeur (3,3) : 713023 noeuds parcourus en 0.77 secondes'''

# globals variables used to count the number
nb_nodes_AO = 0
bestScoreMove = None
saveBestMove = None
worstScoreMove = None
saveWorstMove = None
# Iterative Deepening
timeAlphaOmegaStart = 0.
TIMEOUT = 2
timeout = False


# alpha = -inf
def maxMinAlphaOmega(b: chess.Board, alpha: float, omega: float, depth: int = 3, originalDepth: int = 3,
                     maximizer: bool = True) -> float:
    global bestScoreMove
    global worstScoreMove

    global timeAlphaOmegaStart
    global timeout

    global nb_nodes_AO
    nb_nodes_AO += 1

    if depth == 0:
        return evaluation(b)
    if b.is_game_over():
        return evaluationGameOver(b)
    if maximizer:
        if time.time() - timeAlphaOmegaStart > TIMEOUT:
            timeout = True
            return alpha
        # bestScore = -inf
        for m in b.generate_legal_moves():
            b.push(m)
            eval = maxMinAlphaOmega(b, alpha, omega, depth - 1, originalDepth, False)
            b.pop()
            # bestScore = min(eval, bestScore)
            if bestScoreMove is None:
                bestScoreMove = m
            if eval > alpha:
                alpha = eval
                if depth == originalDepth:
                    bestScoreMove = m
            if alpha >= omega:
                return omega
        return alpha
    else:
        if time.time() - timeAlphaOmegaStart > TIMEOUT:
            timeout = True
            return alpha
        # worstScore = inf
        for m in b.generate_legal_moves():
            b.push(m)
            eval = maxMinAlphaOmega(b, alpha, omega, depth - 1, originalDepth, True)
            b.pop()
            # worstScore = min(eval, worstScore)
            if worstScoreMove is None:
                worstScoreMove = m
            if eval < omega:
                omega = eval
                if depth == originalDepth:
                    worstScoreMove = m
            if alpha >= omega:
                return alpha
        return omega


def maxAOMovement(b: chess.Board, depth: int = 3) -> chess.Move:
    global bestScoreMove
    maxMinAlphaOmega(b, -inf, inf, depth, depth, True)
    return bestScoreMove


def minAOMovement(b: chess.Board, depth: int = 3) -> chess.Move:
    global worstScoreMove
    maxMinAlphaOmega(b, -inf, inf, depth, depth, False)
    return worstScoreMove


def maxAOMovementIterativeDeepening(b: chess.Board, depth: int = 3) -> chess.Move:
    global bestScoreMove
    global timeout
    global timeAlphaOmegaStart
    global saveBestMove
    timeout = False
    timeAlphaOmegaStart = time.time()
    d = 0
    while True:
        if d > 0:
            saveBestMove = bestScoreMove
            # print(" I change the move ment to", saveBestMove.from_square, "->", saveBestMove.to_square, ":in depth = ",
            #       depth + d - 1)
            # print("start at", timeAlphaOmegaStart, "/ now it is = ", time.time(), "the diferant is ",
            #       time.time() - timeAlphaOmegaStart)
        maxMinAlphaOmega(b, -inf, inf, depth + d, depth + d, True)
        d += 1
        if timeout:
            return saveBestMove if saveBestMove is not None else bestScoreMove


def minAOMovementIterativeDeepening(b: chess.Board, depth: int = 3) -> chess.Move:
    global worstScoreMove
    global timeout
    global timeAlphaOmegaStart
    global saveWorstMove
    timeout = False
    timeAlphaOmegaStart = time.time()
    d = 0
    # depth = 1 -> 2 -> 3 -> 4
    while True:
        if d > 0:
            saveWorstMove = worstScoreMove
            # on fait pas ça : depth += d
        maxMinAlphaOmega(b, -inf, inf, depth + d, depth + d, False)
        d += 1
        if timeout:
            # print("change the move ment to", saveWorstMove.from_square, "->", saveWorstMove.to_square, ":in depth = ",
            #       depth + d - 1)
            return saveWorstMove if saveWorstMove is not None else worstScoreMove


def playGameOnAO(b: chess.Board, depthAmi: int = 1, depthEnnemi: int = 1) -> str:
    while True:
        b.push(maxAOMovementIterativeDeepening(b, depthAmi))
        # print(b)
        if b.is_game_over():
            return b.result()
        # print("--------------------")
        b.push(minAOMovementIterativeDeepening(b, depthEnnemi))
        # print(b)
        # print("--------------------")
        if b.is_game_over():
            return b.result()


def playGameOnAOTest(b: chess.Board, amiUserDepth: int, ennUserDepth: int):
    s = time.time()
    res = playGameOnAO(b, amiUserDepth, ennUserDepth)
    e = time.time()
    print(f"* AMI depth = {amiUserDepth}, ENNEMI depth = {ennUserDepth}")
    displayTime(s, e, "Alpha - Omega")
    print("*** ", "AMI WIN" if res == "1-0" else "ENNEMI WIN" if res == "0-1" else "EGALITE", " ***")


'''********************************************************************************'''


def numberError():
    print("That's not a valid number")


def mainMenu():
    print(" 1 - Using MinMax algo.")
    print(" 2 - Using Alpha Omega algo.")
    print(" 3 - Comparing the two algo.")


def depthMenu():
    print(" 1 - Depth (AMI = 1, ENNEMI = 1)")
    print(" 2 - Depth (AMI = 2, ENNEMI = 2)")
    print(" 3 - Depth (AMI = 3, ENNEMI = 3)")
    print(" 4 - Depth (AMI = 3, ENNEMI = 1)")
    print(" 5 - Depth (AMI = 1, ENNEMI = 3)")


def compareMenu(b: chess.Board):
    print(" 1 - MinMax (AMI = 1, ENNEMI = 1) VS Alpha-Oméga (AMI = 1, ENNEMI = 1)")
    print(" 2 - MinMax (AMI = 2, ENNEMI = 2) VS Alpha-Oméga (AMI = 2, ENNEMI = 2)")
    print(" 3 - MinMax (AMI = 3, ENNEMI = 3) VS Alpha-Oméga (AMI = 3, ENNEMI = 3)")


def minMaxChoiceMenu(b: chess.Board):
    depthMenu()
    chosenNumber = int(input("Enter the number corresponding to your choice : "))
    if (chosenNumber == 1):
        playGameTest(b, 1, 1)
    elif (chosenNumber == 2):
        playGameTest(b, 2, 2)
    elif (chosenNumber == 3):
        playGameTest(b, 3, 3)
    elif (chosenNumber == 4):
        playGameTest(b, 3, 1)
    elif (chosenNumber == 5):
        playGameTest(b, 1, 3)
    else:
        numberError()


def aoChoiceMenu(b: chess.Board):
    depthMenu()
    chosenNumber = int(input("Enter the number corresponding to your choice : "))
    if (chosenNumber == 1):
        playGameOnAOTest(b, 1, 1)
    elif (chosenNumber == 2):
        playGameOnAOTest(b, 2, 2)
    elif (chosenNumber == 3):
        playGameOnAOTest(b, 3, 3)
    elif (chosenNumber == 4):
        playGameOnAOTest(b, 3, 1)
    elif (chosenNumber == 5):
        playGameOnAOTest(b, 1, 3)
    else:
        numberError()


def askUser(b: chess.Board):
    while True:
        b.reset()
        mainMenu()
        chosenNumber = int(input("Enter the number corresponding to your choice : "))
        if (chosenNumber == 1):
            minMaxChoiceMenu(b)
        elif (chosenNumber == 2):
            aoChoiceMenu(b)
        elif (chosenNumber == 3):
            compareMenu(b)
        else:
            numberError()
        pass


if __name__ == '__main__':
    board = chess.Board()
    # askUser(board)
    # deroulementRandom(board)
    ## EXO 1 test:
    # possibleGamesTest(board)
    # EXO 2 test :
    # playGameTest(board)
    # print("nb_nodes =", nb_nodes)
    # board.reset()
    ## EXO 3
    # playGameOnAOTest(board)
    # print("nb_nodesAO =", nb_nodes_AO)

    ##my Test
    playGameOnAOTest(board, 3, 3)
