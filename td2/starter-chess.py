# -*- coding: utf-8 -*-
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
        # TODO : fix - (pos * posfac)
        else: scour -= value[u] - (pos * posfac)
    return scour

def main():
    board = chess.Board()
    # deroulementRandom(board)
    for depth in range(1,10):
        start = time.time()
        g,n = possibleGames(board ,depth)
        end = time.time()
        print(f"for depth = {depth} we have {g} games and {n} nodes \ntime of execution {(end -start)} s");
        print("--------------------------")

main()
