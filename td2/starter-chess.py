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


# EXO1 :
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


# fin EXO1
def dist(pos1: int, pos2: int):
    x1 = pos1 % 8
    y1 = pos1 // 8
    x2 = pos2 % 8
    y2 = pos2 // 8
    return sqrt((pow(x1 - x2, 2)) + (pow(y1 - y2, 2)))


def findPos(b: chess.Board, piece: str):
    for k, p in b.piece_map().items():
        s = p.symbol()
        if s == piece:
            return k
    return -1


def evalue(b: chess.Board):
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
        if (l == u):
            score += value[l]
            if l != 'K':
                score += (pos * posfac)
                kingPos = findPos(b, 'k')
                if (kingPos != -1):
                    score -= dist(k, kingPos) * .3
        # lower ENNEMI :
        else:
            score -= value[u]
            if (l != 'k'):
                score += ((1 - pos) * posfac)
                kingPos = findPos(b, 'K')
                if (kingPos != -1):
                    score += dist(k, kingPos) * .3
    return score


def minMax(b: chess.Board, depth: int = 3) -> int:
    if depth == 0:
        return evalue(b)
    if b.is_game_over():
        return evalueGameOver(b)
    pire = inf
    for m in b.generate_legal_moves():
        b.push(m)
        eval = maxMin(b, depth - 1)
        b.pop()
        pire = min(eval, pire)
    return pire


def maxMin(b: chess.Board, depth: int = 3) -> int:
    if depth == 0:
        return evalue(b)
    if b.is_game_over():
        return evalueGameOver(b)
    meilleur = - inf
    for m in b.generate_legal_moves():
        b.push(m)
        eval = minMax(b, depth - 1)
        b.pop()
        meilleur = max(meilleur, eval)
    return meilleur


def evalueGameOver(b: chess.Board)-> int:
    if b.result() == "1-0":
        return 500
    elif b.result() == "0-1":
        return -500
    else:
        return 0


def amiMove(b: chess.Board, depth: int = 3) -> chess.Move:
    meilleurMove = None
    meilleur = -inf
    for m in b.generate_legal_moves():
        b.push(m)
        evl = minMax(b, depth - 1)
        b.pop()
        if (evl > meilleur) or (meilleurMove is None):
            meilleur = evl
            meilleurMove = m
    return meilleurMove


def ennemiMove(b: chess.Board, depth: int = 3) -> chess.Move:
    pireMove = None
    pireval = inf
    for m in b.generate_legal_moves():
        b.push(m)
        evl = maxMin(b, depth - 1)
        b.pop()
        if (evl < pireval) or (pireMove is None):
            pireval = evl
            pireMove = m
    return pireMove


def playGame(b: chess.Board, depthAmi: int = 1, depthEnnemi: int = 1) -> str:
    while (True):
        b.push(amiMove(b, depthAmi))
        print(b)
        if b.is_game_over():
            return b.result()
        print("--------------------")
        b.push(ennemiMove(b, depthEnnemi))
        print(b)
        print("--------------------")
        if b.is_game_over():
            return b.result()


def main():
    board = chess.Board()
    # deroulementRandom(board)
    amiUser = int(input("AMI depth : "))
    ennUser = int(input("ENNEMI depth : "))
    res = playGame(board, amiUser, ennUser)
    print("*** ", "AMI WIN" if res == "1-0" else "ENNEMI WIN" if res == "0-1" else "EGA", " ***")


main()
