from game_code import tetris
import copy
import numpy as np



def column_height(field): # from top to bottom
    h = []
    for j in range(10):
        column = [field[i][j] for i in range(20)]
        height = 0
        while height < 20 and column[height] == 0:
            height += 1
        h.append(20 - height)
    return h


def maximum_height(field):
    return(max(column_height(field)))

def column_difference(field):# absolute difference between adjacent columns
    df=[]
    h=column_height(field)
    for j in range(9):
        df.append(abs(h[j+1]-h[j]))
    return(df)

def holes(field):
    L=0
    h=column_height(field)
    for j in range(10):
        for i in range(20-h[j],20):
            if field[i][j]==0:
                L+=1
    return(L)

def evaluate(W, field): 
    #W=[w1, ..., w21] vector of parameters to tune 
    h=column_height(field)
    dh=column_difference(field)
    L=holes(field)
    H=maximum_height(field)
    S1,S2,S3,S4 = 0,0,0,0
    for k in range (len(h)):
        S1+=h[k]*W[k]
    for k in range (len(dh)):
        S2+=dh[k]*W[10+k]
    S3=W[19]*L
    S4=W[20]*H
    return(S1+S2+S3+S4)

def evaluate_best_move(W, field, type, color):
    L = []
    score = []

    initial_field = [row[:] for row in field]  # Sauvegarde de l'état initial de la grille

    for k in range(4):
        for col in range(-5, 10):
            game_copy = tetris.Tetris(20, 10)
            game_copy.field = [row[:] for row in initial_field]  # Restauration de l'état initial de la grille
            game_copy.new_figure()
            
            for _ in range(k):
                game_copy.rotate() 

            game_copy.go_side(col)

            if not game_copy.intersects():
                game_copy.go_space()
                score.append(evaluate(W, game_copy.field))
                L.append([col, k])

    if len(L) > 0:
        best_move = score.index(min(score))
        return L[best_move]
    else:
        return [0, 0]

    
def simulation(W):
    game = tetris.Tetris(20, 10)
    while game.state!="gameover":

        fig=np.random.randint(0,6)
        color=1

        game.new_figure()

        old_rotation = game.figure.rotation
        col, rot = evaluate_best_move(W,game.field,fig,color)
        game.rotate()
        if game.intersects():
            game.figure.rotation = old_rotation  # Restaure la rotation précédente
        game.go_side(col)

        if game.intersects():
            game.state="gameover"
        
        else:
            game.go_space()

    return(game.score)

