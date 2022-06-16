import timeit,os
import random
from board2 import *
cnodos=0
def min_conflicts(state, n, lim=1000000):
    global cnodos
    def random_pos(li, filt):
        return random.choice([i for i in range(n) if filt(li[i])])

    for k in range(lim):
        confs = find_conflicts(state, n)
        if sum(confs) == 0:
            #print('Nodos expandidos:    ', k)
            cnodos=k
            return state
        col = random_pos(confs, lambda elt: elt > 0)
        vconfs = [hits(state, n, col, row) for row in range(n)]
        state[col] = random_pos(vconfs, lambda elt: elt == min(vconfs))# se elige aleatoriamente una configuracion del tablero
    raise Exception("Limite alcanzado, solucion incompleta")


def find_conflicts(soln, n):
    return [hits(soln, n, col, soln[col]) for col in range(n)]


def hits(soln, n, col, row):#calcula los conflictos en el tablero
    total = 0
    for i in range(n):
        if i == col:
            continue
        if soln[i] == row or abs(i - col) == abs(soln[i] - row):
            total += 1
    return total

def minc(n):
    start = timeit.default_timer()
    q=min_conflicts(list(range(n)), n)
    print(q)
    #os.system('pause')
    elapsed = timeit.default_timer() - start  # en segundos
    print('Tiempo de ejecucion: ', elapsed, 'segundos')
    print('Tiempo de ejecucion: ', elapsed / 60, 'minutos')
    print('Nodos expandidos:    ', cnodos)
    draw_board(q)
#minc(4)
