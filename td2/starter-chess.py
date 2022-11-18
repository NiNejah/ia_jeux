# -*- coding: utf-8 -*-
import math
import time
import chess
from random import randint, choice

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

def possibleGamesAux(b ,depth,games,nodes):
    if b.is_game_over() or depth == 0:
        # eval(b)
        games.append(1)
    else:
        for m in b.generate_legal_moves():
            b.push(m)
            nodes.append(1)
            possibleGamesAux(b,depth -1 ,games,nodes)
            b.pop()
def possibleGames(b , depth = 3):
    game=[]
    nodes=[]
    possibleGamesAux(b,depth,game,nodes)
    return len(game),len(nodes)


def evalue( board , turn = "AMI"):
    value = {
        'K':200,
        'Q':9,
        'R': 5,
        'B': 3 ,
        'N':3 ,
        'P':1,
        '.':0
    }
    scour , posfac = 0 , .2
    for k,p in board.piece_map().items():
        l = p.symbol()
        u = l.upper()
        pos = k // 8
        # upper AMI ;
        if(l==u): scour += value[l] + (pos * posfac)
        # lower ENNEMI :
        else: scour -= value[u] - ((1-pos ) * posfac)
    return scour

##### ENNEMI :
def minMax(b : chess.Board , depth = 3):
    if depth == 0:
     return evalue(b)
    if b.is_game_over():
        return evalueGameOver(b)
    pire = math.inf
    for m in b.generate_legal_moves():
        b.push(m)
        eval = maxMin(b,depth-1)
        b.pop()
        pire = min(eval,pire)
    return pire

def maxMin(b : chess.Board , depth = 3 ):
    if depth == 0:
     return evalue(b)
    if b.is_game_over():
        return evalueGameOver(b)
    meilleur = - math.inf
    for m in b.generate_legal_moves():
        b.push(m)
        eval = minMax(b,depth-1)
        b.pop()
        meilleur = max (meilleur ,eval)
    return meilleur

def evalueGameOver(b : chess.Board):
    if b.result() == "1-0":
        return 500
    elif b.result() == "0-1":
        return -500
    else:
        return 0

def amiMove(b : chess.Board , depth = 3):
    meilleurMove = None
    meilleur = 0
    for m in b.generate_legal_moves():
        b.push(m)
        evl = maxMin(b,depth)
        b.pop()
        if ( evl > meilleur) or (meilleurMove == None):
            meilleur = evl
            meilleurMove = m
    return meilleurMove
def ennemiMove(b : chess.Board , depth = 3):
    pireMove = None
    pire = 0
    for m in b.generate_legal_moves():
        b.push(m)
        evl = minMax(b,depth)
        b.pop()
        if ( evl < pire) or (pireMove == None):
            pire = evl
            pireMove = m
    return pireMove

def playGame(b : chess.Board):
    while(not b.is_game_over()):
        b.push(amiMove(b,1))
        print(b)
        print("------------------------")
        b.push(ennemiMove(b,3))
        print(b)
        print("------------------------")

def possibleGalmesTest(b):
    for depth in range(1,10):
        start = time.time()
        g,n = possibleGames(b ,depth)
        end = time.time()
        print(f"for depth = {depth} we have {g} games and {n} nodes \ntime of execution {(end -start)} s");
        print("--------------------------")

def main():
    board = chess.Board()
    # deroulementRandom(board)
    playGame(board)

main()
