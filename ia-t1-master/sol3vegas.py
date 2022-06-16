import os,timeit
import random
from multiprocessing import Queue
from board2 import *


def restringir(tab, n):

    restringidos = list()
    for pos in range(n):#inicializa la lista
        lista = list()
        restringidos.insert(pos, lista)
    for col in range(n):#restricciones en el tablero
        if tab[col] != -1:  #columna libre
            for fil in range(n):
                if fil not in restringidos[col]:
                    restringidos[col].append(fil)  # se restringe la fila actual
            for k in range(n):
                reina = tab[col]
                if not reina in restringidos[k]:
                    restringidos[k].append(reina)  # se restringe la columna actual

            # diagonales
            reina = tab[col]
            for col2 in range(n):
                for fil2 in range(n):
                    if reina - col == fil2 - col2 or reina + col == fil2 + col2 or col - col2 == reina - fil2 or col - col2 == fil2 - reina:
                        if not fil2 in restringidos[col2]:
                            restringidos[col2].append(fil2)
    return restringidos



def liberar(restringidos, n):

    libres = list()

    for pos in range(n):
        lista = list()
        libres.insert(pos, lista)

    for col in range(n):

        for fil in range(n):

            if not fil in restringidos[col] and not fil in libres[col]:
                libres[col].append(fil)
    return libres


def vegas(n):

    tab = list()

    for i in range(n):
        tab.insert(i, -1)

    restringidos = list()
    for i in range(n):
        lista = list()
        restringidos.insert(i, lista)

    libres = list()
    cnodos = 0
    column = 0
    start = timeit.default_timer()

    while column < n:

        restringidos= restringir(tab, n)

        libres = liberar(restringidos, n)

        if len(libres[column]) != 0:
            fila = random.choice(libres[column])

            tab[column] = fila
            column += 1
        else:
            tab[column] = -1
            if column > 0:
                column -= 1

        cnodos += 1

    print(tab)
    #os.system('pause')
    elapsed = timeit.default_timer() - start  # en segundos
    print('Tiempo de ejecucion: ', elapsed, 'segundos')
    print('Tiempo de ejecucion: ', elapsed / 60, 'minutos')
    print('Nodos expandidos:    ', cnodos)
    draw_board(tab)
#vegas(4)