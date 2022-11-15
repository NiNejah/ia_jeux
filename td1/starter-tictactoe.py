# -*- coding: utf-8 -*-

import time
import Tictactoe 
from random import randint,choice

def RandomMove(b):
    """Renvoie un mouvement au hasard sur la liste des mouvements possibles"""
    return choice(b.legal_moves())

def deroulementRandom(b):
    """Effectue un déroulement aléatoire du jeu de morpion."""
    print("----------")
    print(b)
    if b.is_game_over():
        res = getresult(b)
        if res == 1:
            print("Victoire de X")
        elif res == -1:
            print("Victoire de O")
        else:
            print("Egalité")
        return
    b.push(RandomMove(b))
    deroulementRandom(b)
    b.pop()


def getresult(b):
    """Fonction qui évalue la victoire (ou non) en tant que X. Renvoie 1 pour victoire, 0 pour
       égalité et -1 pour défaite. """
    if b.result() == b._X:
        return 1
    elif b.result() == b._O:
        return -1
    else:
        return 0



"""
1. En utilisant les méthodes legal_moves() et is_game_over(), proposer une méthode permettant
d’explorer toutes les parties possibles au Morpion (lorsque X commence). Combien y-a-t-il de parties ?
Combien votre arbre de recherche a-t-il de noeuds ? Combien de temps faut-il pour tout explorer ?
"""
def possibleGamesAux(b ,games,nodes):
    if b.is_game_over():
        # eval(b)
        games.append(1)
    else:
        for m in b.legal_moves():
            b.push(m)
            nodes.append(1)
            possibleGamesAux(b,games,nodes)
            b.pop()
def possibleGames(b):
    game=[]
    nodes=[]
    possibleGamesAux(b,game,nodes)
    return len(game),len(nodes)

def existWinningStrategyAux(b : Tictactoe.Board, winningGames = None):
    if b.is_game_over() and getresult(b) == 1 :
        if(winningGames == None):
            return True
        else:
            winningGames.append(1)
    else:
        for m in b.legal_moves():
            b.push(m)
            if existWinningStrategyAux(b,winningGames):
                return True
            b.pop()
        return False
def existWinningStrategy(b : Tictactoe.Board ):
    return existWinningStrategyAux(b)

def main ():
    board = Tictactoe.Board()
    # print(board)
    # ### Deroulement d'une partie aléatoire
    # deroulementRandom(board)
    # print("Apres le match, chaque coup est défait (grâce aux pop()): on retrouve le plateau de départ :")
    # print(board)
    start = time.time()
    isThere = existWinningStrategy(board)
    # g,n = possibleGames(board)
    end = time.time()
    print("there is", " not " if not isThere else " ")
    print(f"time : {(end -start)} s")
    # print(f"we have {g} games and {n} nodes \ntime of execution {(end -start)} s");
main()



