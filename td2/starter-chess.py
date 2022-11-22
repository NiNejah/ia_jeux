# -*- coding: utf-8 -*-
import math
import time
import chess
from random import randint, choice
from math import sqrt , inf ,pow


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

def dist(pos1,pos2):
    x1 = pos1%8
    y1 = pos1//8 
    x2 = pos2%8
    y2 = pos2//8
    return sqrt ((pow(x1-x2,2))+(pow(y1-y2,2)))


def findBlackKingPos(board):
    for k,p in board.piece_map().items():
        s = p.symbol()
        if s == 'k' :
            return k
    return -1 

def findWhiteKingPos(board):
    for k,p in board.piece_map().items():
        s = p.symbol()
        if s == 'K' :
            return k
    return -1 

def evalue( board ):
    value = {
        'K':200,
        'Q':9,
        'R': 5,
        'B': 3 ,
        'N':3 ,
        'P':1,
        '.':0
    }
    score , posfac = 0 , .2
    for k,p in board.piece_map().items():
        l = p.symbol()
        u = l.upper()
        pos = k // 8
        # upper AMI ;
        if( l == u ) :
            score += value[l]  
            score += (pos * posfac)
            if l != 'K' :
                kingPos = findBlackKingPos(board)
                if(kingPos != -1):
                    score -= dist(k,kingPos) * .3
        # lower ENNEMI :
        else : 
            score -= value[u]
            score += ((1-pos ) * posfac)
            if(l != 'k'):
                kingPos = findWhiteKingPos(board)
                if(kingPos != -1):
                    score += dist(k,kingPos) * .3

    return score

def minMax(b : chess.Board , depth = 3):
    if depth == 0:
     return evalue(b)
    if b.is_game_over():
        return evalueGameOver(b)
    pire = inf
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
    meilleur = - inf
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
    meilleur = -inf
    for m in b.generate_legal_moves():
        b.push(m)
        # minMax
        evl = minMax(b,depth-1)
        b.pop()
        if ( evl > meilleur) or (meilleurMove == None):
            meilleur = evl
            meilleurMove = m
    return meilleurMove

def ennemiMove(b : chess.Board , depth = 3):
    pireMove = None
    pireval =  inf
    for m in b.generate_legal_moves():
        b.push(m)
        # maxMin
        evl = maxMin(b,depth-1)
        b.pop()
        if ( evl < pireval) or (pireMove == None):
            pireval = evl
            pireMove = m
    return pireMove

def playGame(b : chess.Board):
    amiUser = int(input("AMI prof : "))
    ennUser = int(input("ENNEMI prof : "))
    while(True):
        b.push(amiMove(b,amiUser))
        print(b)
        if b.is_game_over() : 
            return b.result() ; 
        print("--------------------")
        b.push(ennemiMove(b,ennUser))
        print(b)
        print("--------------------")
        if b.is_game_over() : 
            return b.result() ;  


def possibleGamesTest(b):
    for depth in range(1,10):
        start = time.time()
        g,n = possibleGames(b ,depth)
        end = time.time()
        print(f"for depth = {depth} we have {g} games and {n} nodes \ntime of execution {(end -start)} s");
        print("-----------------------")

def main():
    board = chess.Board()
    # deroulementRandom(board)
    res = playGame(board)
    print( "*** ", " AMI WIN" if res == "1-0" else "ENNEMI WIN" if res == "0-1" else " EGA " , "***") 

main()
