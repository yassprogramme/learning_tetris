import tetris
import numpy as np

figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],
        [[4, 5, 9, 10], [2, 6, 5, 9]],
        [[6, 7, 9, 10], [1, 5, 6, 10]],
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],
        [[1, 2, 5, 6]],
    ]


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
    L = 0
    h  =column_height(field)
    for j in range(10):
        for i in range(20-h[j],20):
            if field[i][j] == 0:
                L+=1
    return(L)

def evaluate(W, field): 
    #W=[w1, ..., w21] vector of parameters to tune 
    h=column_height(field)
    dh=column_difference(field)
    L=holes(field)
    H=maximum_height(field)
    S = 0
    for k in range (len(h)):
        S += h[k] * W[k]
    for k in range (len(dh)):
        S += dh[k] * W[10+k]
    S += W[19] * L
    S += W[20] * H
    return(S)


def evaluate_best_move(W,field,type):
    L=[]
    score=[]
    n_rot = len(figures[type])
    
    for k in range (n_rot):
        for col in range (-5,10):
            game_copy = tetris.Tetris(20,10)
            
            game_copy.field = [[cell for cell in row] for row in field]

            game_copy.new_figure(type)
            game_copy.rotate(k)
            game_copy.go_side(col) 
            

            if not game_copy.intersects():
                game_copy.go_space()
                score.append(evaluate(W,game_copy.field))
                L.append((col,k))
    if len(L)>0:
        best_move = score.index(min(score))
        return(L[best_move])
    else : 
        return((0,0))




def simulation(W):
    
    game = tetris.Tetris(20, 10)
    while game.state != "gameover":

        type = np.random.randint(0,6)
        game.new_figure(type)

        col, rot = evaluate_best_move(W,game.field,type)
        game.rotate(rot)
        game.go_side(col)
        game.go_space()

    return(game.score)