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

def displayTime(start: float, end: float, functionName: str):
    ''' Fonction auxiliaire utilisée pour afficher le temps '''
    print(f" {functionName} function ", end=" ")
    m = 0
    s = end - start
    if s > 60.0:
        m = s // 60
        s %= 60.0
    print("take {} Minutes {:.2} Seconds as a run time".format(int(m), s))

''' Variable globale pour compter le nombre de noeuds à l'issue de MinMax '''
nb_nodes = 0

def possibleGamesAux(b: chess.Board, depth: int, cpt):
    ''' Fonction récursive auxiliare de la fonction possibleGames. Cette fonction va parcourir et compter le nombre de noeuds qu'elle va parcourir en les
    ajoutant à la liste nodes qui lui est fournie par la fonction possibleGames. Si la fonction tombe sur un jeu terminée ou qu'il ne peut pas allez plus
    profondément dans l'arbre, alors il ajoute l'élément à la liste games.'''
    cpt["nodes"] += 1
    if b.is_game_over() or depth == 0:
        cpt["games"] += 1
    else:
        for m in b.generate_legal_moves():
            b.push(m)
            possibleGamesAux(b, depth - 1, cpt)
            b.pop()

def possibleGames(b: chess.Board, depth: int = 3):
    ''' Fonction qui permet de calculer et de retourner le nombre de feuilles/jeux terminés ainsi que le nombre de noeuds parcourus à une certaine profondeur
    dans l'arbre des possibilités en appelant la fonction récursive possibleGamesAux. '''
    cpt = {
        "games": 0,
        "nodes": 0
    }
    possibleGamesAux(b, depth, cpt)
    return cpt["games"], cpt["nodes"]


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
    ''' Fonction qui permet de calculer et de retourner la distance euclidienne entre 2 pièces du plateau. '''
    x1 = pos1 % 8
    y1 = pos1 // 8
    x2 = pos2 % 8
    y2 = pos2 // 8
    return sqrt((pow(x1 - x2, 2)) + (pow(y1 - y2, 2)))



def findPos(b: chess.Board, piece: str) -> int:
    ''' Fonction qui permet de renvoyer la position sur le plateau d'une pièce passée en paramètre.'''
    for k, p in b.piece_map().items():
        if p.symbol() == piece:
            return k
    return -1

def evaluation(b: chess.Board) -> float:
    ''' Fonction qui évalue le score de la partie actuelle en donnant un score aux pièces. Les pièces ennemies (noires/minuscules) retirent 
    leur valeur au score total tandis que les pièces amies (blanches/majuscules) ajoutent leur valeur au score total.
    Les valeurs des deux types de pièces sont augmentées ou réduites en fonction de leur position sur le plateau de jeu et de leur distance par
    rapport au roi.'''
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



def evaluationGameOver(b: chess.Board) -> int:
    ''' Fonction utilisée à la fin de chaque jeu. Ajoute des points au score total en fonction de qui gagne la partie.
    Permet d'inciter l'IA à faire des coups lui permettant de gagner.'''
    if b.result() == "1-0":
        return 500
    elif b.result() == "0-1":
        return -500
    else:
        return 0


def MaxMin(b: chess.Board, saveMovement, depth: int = 3, originalDepth: int = 3, maximizer: bool = True) -> float:
    ''' Fonction qui lance l'algorithme MaxMin ou MinMax en fonction 
    de la valeur de la variable maximizer.'''
    global nb_nodes
    nb_nodes += 1
    if depth == 0:
        return evaluation(b)
    if b.is_game_over():
        return evaluationGameOver(b)
    if maximizer:
        bestScore = - inf
        for m in b.generate_legal_moves():
            b.push(m)
            eval = MaxMin(b, saveMovement, depth - 1, originalDepth, False)
            b.pop()
            if eval > bestScore:
                bestScore = eval
                if depth == originalDepth:
                    saveMovement["best"] = m
        return bestScore
    else:
        worstScore = inf
        for m in b.generate_legal_moves():
            b.push(m)
            eval = MaxMin(b, saveMovement, depth - 1, originalDepth, True)
            b.pop()
            if eval < worstScore:
                worstScore = eval
                if depth == originalDepth:
                    saveMovement["worst"] = m
        return worstScore


def getMovementFromMinMax(b: chess.Board, depth: int = 3, maximizer: bool = True) -> chess.Move:
    ''' Fonction qui renvoie le pire ou le meilleur mouvement en fonction de la valeur de la
    variable maximizer en utilisant la fonction MaxMin '''
    move = {
        "best": None,
        "worst": None
    }
    MaxMin(b, move, depth, depth, maximizer)
    return move["best"] if maximizer else move["worst"]


'''********************************************************************************'''

'''************************** EXO3 : L’alpha et l’oméga de α − β *************************'''

# globals variables used to count the number
nb_nodes_AO = 0
# Iterative Deepening
timeAlphaOmegaStart = 0.
TIMEOUT = 10
timeout = False


# fonction Alpha-Beta
def alphaOmega(b: chess.Board, alpha: float, omega: float, saveMovement, depth: int = 3, originalDepth: int = 3,
               maximizer: bool = True, isDeepening: bool = False) -> float:
    ''' Fonction qui permet de lancer l'algorithme Alpha-Oméga en version normale ou bien
    Iterative Deepening en fonction de la valeur isDeepening. La variable maximizer
    permet, en fonction de sa valeur, d'aller chercher la meilleure ou la pire valeur dans l'arbre à la profondeur depth.'''
    global nb_nodes_AO
    nb_nodes_AO += 1
    global timeout
    if depth == 0:
        return evaluation(b)
    if b.is_game_over():
        return evaluationGameOver(b)
    # for IterativeDeepening functionality 
    if isDeepening and time.time() - timeAlphaOmegaStart > TIMEOUT:
        timeout = True
        return alpha if maximizer else omega
    if maximizer:
        for m in b.generate_legal_moves():
            b.push(m)
            eval = alphaOmega(b, alpha, omega, saveMovement, depth - 1, originalDepth, False, isDeepening)
            b.pop()
            if eval > alpha:
                alpha = eval
                if depth == originalDepth:
                    saveMovement["best"] = m
            if alpha >= omega:
                return omega
        return alpha
    else:
        for m in b.generate_legal_moves():
            b.push(m)
            eval = alphaOmega(b, alpha, omega, saveMovement, depth - 1, originalDepth, True, isDeepening)
            b.pop()
            if eval < omega:
                omega = eval
                if depth == originalDepth:
                    saveMovement["worst"] = m
            if alpha >= omega:
                return alpha
        return omega



def getMovementFromAlphaOmega(b: chess.Board, depth: int = 3, maximizer: bool = True) -> chess.Move:
    ''' Fonction qui renvoie le pire ou le meilleur mouvement en fonction de la valeur de la
    variable maximizer en utilisant alphaOmega  '''
    move = {
        "best": None,
        "worst": None
    }
    alphaOmega(b, -inf, inf, move, depth, depth, maximizer)
    return move["best"] if maximizer else move["worst"]



def getMovementIterativeDeepening(b: chess.Board, depth: int = 3, maximizer: bool = True) -> chess.Move:
    ''' Fonction permettant de faire un iterative deepening sur Alpha-Omega et qui retourne le meilleur ou le pire mouvement en
    fonction de la valeur de la variable maximizer. Si la profondeur passée en paramètre est trop élevée pour le temps
    de recherche stocké dans TIMEOUT alors la fonction renvoie un randomMove().'''
    global timeout
    global timeAlphaOmegaStart
    globalMovement: chess.Move = None
    moves = {
        "best": None,
        "worst": None,
    }
    timeout = False
    timeAlphaOmegaStart = time.time()
    d = 0
    while True:
        if d > 0:
            globalMovement = moves["best"] if maximizer else moves["worst"]
        d += 1
        alphaOmega(b, -inf, inf, moves, depth + d, depth + d, maximizer, True)
        if timeout:
            if globalMovement is not None:
                print("---- change the movement to", globalMovement.from_square, "->", globalMovement.to_square,
                      ":in depth = ",
                      depth + d - 1)
                return globalMovement
            else:
                print("Rand depth = ", depth + d)
                return randomMove(b)


def playGameWithTimer(b: chess.Board, movementMethodAmi, movementMethodEnnemi, amiUserDepth: int, ennUserDepth: int,
                      description: str):
    '''Fonction permettant de lancer la fonction playGame() et d'initialiser les compteurs 
    de noeuds nb_nodes et nb_nodes_AO à 0. Quand playGame() se termine, affiche la durée de
    la partie venant d'être jouée.'''
    global nb_nodes
    global nb_nodes_AO
    nb_nodes = 0
    nb_nodes_AO = 0
    s = time.time()
    res = playGame(b, movementMethodAmi, movementMethodEnnemi, amiUserDepth, ennUserDepth)
    e = time.time()
    print(f"* AMI depth = {amiUserDepth}, ENNEMI depth = {ennUserDepth}")
    displayTime(s, e, description)
    print("*** ", "AMI WIN" if res == "1-0" else "ENNEMI WIN" if res == "0-1" else "EGALITE", " ***")


def playGame(b: chess.Board, movementMethodAmi, movementMethodEnnemi, depthAmi: int = 1, depthEnnemi: int = 1):
    '''Fonction permettant à deux IA de jouer aux échecs. La première est représentée
    par la variable movementMethodAmi et pourra regarder jusqu'à la profondeur depthAmi
    pour choisir le meilleur coup.
    La seconde est représentée par la variable movementMethodEnnemi et pourra regarder
    jusqu'à la profondeur depthEnnemi pour choisir le pire coup.'''
    while True:
        b.push(movementMethodAmi(b, depthAmi, True))
        # print(b)
        if b.is_game_over():
            print("nodes AO :", nb_nodes_AO)
            print("nodes MinMax :", nb_nodes)
            return b.result()
        # print("--------------------")
        b.push(movementMethodEnnemi(b, depthEnnemi, False))
        # print(b)
        # print("--------------------")
        if b.is_game_over():
            print("nodes AO :", nb_nodes_AO)
            print("nodes MinMax :", nb_nodes)
            return b.result()


# user function : possible
def displayPossibleMovement(b: chess.Board):
    '''Fonction permettant d'afficher en ligne de commande
    l'ensemble des coups possibles.'''
    print("All possible movements : ")
    print("{ ", end="")
    for m in b.generate_legal_moves():
        print(m.uci(), end=", ")
    print("}")


def checkMovementValidation(b: chess.Board, move: str):
    '''Fonction qui permet de vérifier que le coup sélectionné par l'utilisateur
    est valide.'''
    for m in b.generate_legal_moves():
        if move == m.uci():
            return True
    return False


def getMovementFromTheUser(b: chess.Board):
    '''Fonction permettant à l'utilisateur de jouer un coup.'''
    while True:
        displayPossibleMovement(b)
        strM = input("Your movement : ")
        if checkMovementValidation(b, strM):
            userMovement = b.parse_uci(strM)
            return userMovement
        else:
            print("This is not a valid movement ! ")
            continue


def playGameWithUser(b: chess.Board, iAMovementMethod, depthIa: int = 1):
    '''Fonction permettant à l'utilisateur de jouer contre une IA. iAMovementMethod
    représente l'IA contre laquelle l'utilisateur souhaite jouer.'''
    print(b)
    while True:
        b.push(getMovementFromTheUser(b))
        print("<<<< User move >>>> ")
        print(b)
        if b.is_game_over():
            return b.result()
        print("--------------------")
        print("<<<< IA move >>>>")
        b.push(iAMovementMethod(b, depthIa, False))
        print(b)
        print("--------------------")
        if b.is_game_over():
            return b.result()


'''********************************************************************************'''


# Méthodes pour l'interface
def numberError():
    print("That's not a valid number")


# fonction pour que l'utilisateur choisit les profondeurs de recherche Ami et Ennemi
def depthChoice():
    amiDepth = int(input("Enter the depth for AMI : "))
    ennemiDepth = int(input("Enter the depth for ENNEMI : "))
    return amiDepth, ennemiDepth


def mainMenu():
    print(" 1 - Using MinMax algorithm.")
    print(" 2 - Using Alpha Omega algorithm.")
    print(" 3 - Using Alpha Omega Iterative Deepening algorithm.")
    print(" 4 - Comparing the two algorithms.")


def compareMenu(b: chess.Board, amiDepth: int, ennemiDepth: int):
    print(" 1 - MinMax (AMI) VS Alpha-Oméga (ENNEMI)")
    print(" 2 - Alpha-Oméga (AMI) VS MinMax (ENNEMI)")
    chosenNumber = int(input("Enter the number corresponding to your choice : "))
    if chosenNumber == 1:
        playGameWithTimer(b, getMovementFromMinMax, getMovementFromAlphaOmega, amiDepth, ennemiDepth,
                          " Ami est MaxMin , Ennemi Alpha-Omega")
    elif chosenNumber == 2:
        playGameWithTimer(b, getMovementFromAlphaOmega, getMovementFromMinMax, amiDepth, ennemiDepth,
                          " Ami est AlphaOmega , Ennemi MinMax ")
    else:
        numberError()



def askUser(b: chess.Board):
    '''Fonction utilisée pour communiquer avec l'utilisateur.'''
    while True:
        b.reset()
        global nb_nodes
        nb_nodes = 0
        global nb_nodes_AO
        nb_nodes_AO = 0
        mainMenu()
        chosenNumber = int(input("Enter the number corresponding to your choice : "))
        amiDepth, ennemiDepth = depthChoice()
        if chosenNumber == 1:
            playGameWithTimer(b, getMovementFromMinMax, getMovementFromMinMax, amiDepth, ennemiDepth,
                              " MaxMin VS MaxMin " )
        elif chosenNumber == 2:
            playGameWithTimer(b, getMovementFromAlphaOmega, getMovementFromAlphaOmega, amiDepth, ennemiDepth,
                              " Alpha - Omega VS Alpha - Omega ")
        elif chosenNumber == 3:
            playGameWithTimer(b,getMovementIterativeDeepening,getMovementIterativeDeepening,amiDepth,ennemiDepth,
                              " Alpha - Omega Iterative Deepening ")
        elif chosenNumber == 4:
            compareMenu(b, amiDepth, ennemiDepth)
        else:
            numberError()


if __name__ == '__main__':
    board = chess.Board()
    askUser(board)