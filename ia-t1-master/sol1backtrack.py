import os
from board import *
import timeit
from board import *
cnodos = 0


def conflict(state, x):
    ''' Verifica conflictos, recibe un estado del tablero y la posicion en la que se quiere colocar otra reina'''
    y = len(state)
    for i in range(y):
        # print(state[i])
        # os.system('pause')

        if abs(state[i] - x) in (0, y - i):
            # print("abs(state[i]-X) in (0, Y-i):")
            # print(abs(state[i]-X))
            # os.system('pause')
            return True
    return False


def nqueens(n, sol, state=()):
    ''' Se utiliza generadoes de python para obtenera todos los estados posibles para el tablero,
	recibe el tamano del tablero y su estado, con una solucion parcial'''
    global cnodos
    for x in range(n):
        estado = state + (x,)
        # print(estado)
        # os.system('pause')
        # print(estado,"++")

        while len(estado) != n:
            estado = estado + (-1,)

        cnodos = cnodos + 1
        solucion = {"solution": False, "board": estado}

        sol.put(solucion)

        if not conflict(state, x):
            if len(state) == n - 1:
                yield (x,)
            else:
                for result in nqueens(n, sol, state + (x,)):
                    yield (x,) + result


def backtrack(n, flag):
    global cnodos
    board = [-1 for i in range(n)]
    q = Queue()
    aux = {"board": board, "solution": False}
    q.put(aux)
    # p2 = Process(target=draw_board, args=(q, queen_number))
    # p2.start()
    start = timeit.default_timer()
    for solution in nqueens(n, q):
        solucion = {"solution": True, "board": solution}
        print(solution)
        #draw_board2(solution)
        q.put(solucion)
        if solution and flag:
            break
    elapsed = timeit.default_timer() - start  # en segundos
    print('Tiempo de ejecucion: ', elapsed, 'segundos')
    print('Tiempo de ejecucion: ', elapsed / 60, 'minutos')
    print('Nodos expandidos:    ',cnodos)
    #print(q)
    #os.system('pause')

    draw_board(q, n)


 #backtrack(4, 0)
