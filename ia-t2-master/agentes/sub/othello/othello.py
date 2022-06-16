import timeit,os

import easygui as eg
from agentes import othello



def check(move, player, board):
    return othello.is_valid(move) and othello.is_legal(move, player, board)

def human(player, board):
    print(othello.print_board(board))
    print('Su movimiento:')
    while True:
        #move = raw_input('> ')
        move= input(">>_")
        f = int(move[0])
        c = int(move[2])
        move=f*10+c
        #import os; os.system('pause')
        if move and check(int(move), player, board):
            return int(move)
        elif move:
            print('Movimiento invalido.')

def get_choice(prompt, options):
    print(prompt)
    print('Opciones:', options.keys())
    while True:
        choice = raw_input('> ')
        if choice in options:
            return options[choice]
        elif choice:
            print('Opcion invalida.')


def main():
    respuesta = ''
    while respuesta != 'Salir':
        num = 0
        #os.system('cls')
        respuesta = eg.buttonbox(msg='Electiva 3 - Inteligencia Artificial',
                                 title='I.A.  :  Othello',
                                 choices=('Comparar Estrategias','Salir'),
                                 image='unnamed.png')
        if respuesta == 'Salir':
            return

        if respuesta=='Comparar Estrategias':
            r1= eg.buttonbox(msg='Electiva 3 - Inteligencia Artificial \nEstrategia para jugador A - Negras',
                                     title='            Estrategia para jugador A - Negras',
                                     choices=('Minimax','Minimax-Ponderado', 'Alpha-Beta','Alpha-Beta-Ponderado', 'Humano','Aleatorio','Salir'),
                                     image='unnamed.png')

        if r1=='Minimax':
            num = eg.integerbox(msg='Ingresar la profundidad de busqueda:',
                                title='I.A.  :  Othello',
                                lowerbound=1,
                                upperbound=8,
                                image='unnamed.png')
            black=othello.minimax_searcher(num, othello.score)
            #black = othello.minimax_searcher(num, othello.weighted_score)
        if r1 == 'Minimax-Ponderado':
            num = eg.integerbox(msg='Ingresar la profundidad de busqueda:',
                                title='I.A.  :  Othello',
                                lowerbound=1,
                                upperbound=8,
                                image='unnamed.png')
            black = othello.minimax_searcher(num, othello.weighted_score)
        if r1=='Alpha-Beta':
            num = eg.integerbox(msg='Ingresar la profundidad de busqueda:',
                                title='I.A.  :  Othello',
                                lowerbound=1,
                                upperbound=8,
                                image='unnamed.png')
            black=othello.alphabeta_searcher(num, othello.score)
            #black = othello.alphabeta_searcher(num, othello.weighted_score)
        if r1 == 'Alpha-Beta-Ponderado':
            num = eg.integerbox(msg='Ingresar la profundidad de busqueda:',
                                title='I.A.  :  Othello',
                                lowerbound=1,
                                upperbound=8,
                                image='unnamed.png')
            black = othello.alphabeta_searcher(num, othello.weighted_score)
        if r1 == 'Humano':
            black = human
        if r1 == 'Aleatorio':
            black = othello.random_strategy

        if respuesta == 'Comparar Estrategias':
            r2 = eg.buttonbox(msg='Electiva 3 - Inteligencia Artificial\nEstrategia para jugador B - Blancas',
                              title='           Estrategia para jugador B - Blancas',
                              choices=('Minimax','Minimax-Ponderado', 'Alpha-Beta','Alpha-Beta-Ponderado', 'Humano','Aleatorio','Salir'),
                              image='unnamed.png')
        if r2 == 'Minimax':
            num = eg.integerbox(msg='Ingresar la profundidad de busqueda:',
                                title='I.A.  :  Othello',
                                lowerbound=1,
                                upperbound=8,
                                image='unnamed.png')
            white= othello.minimax_searcher(num, othello.score)
            #white = othello.minimax_searcher(num, othello.weighted_score)
        if r2 == 'Minimax-Ponderado':
            num = eg.integerbox(msg='Ingresar la profundidad de busqueda:',
                                title='I.A.  :  Othello',
                                lowerbound=1,
                                upperbound=8,
                                image='unnamed.png')
            white = othello.minimax_searcher(num, othello.weighted_score)
        if r2 == 'Alpha-Beta':
            num = eg.integerbox(msg='Ingresar la profundidad de busqueda:',
                                title='I.A.  :  Othello',
                                lowerbound=1,
                                upperbound=8,
                                image='unnamed.png')
            white= othello.alphabeta_searcher(num, othello.score)
            #white = othello.alphabeta_searcher(nunm, othello.weighted_score)
        if r2 == 'Alpha-Beta-Ponderado':
            num = eg.integerbox(msg='Ingresar la profundidad de busqueda:',
                                title='I.A.  :  Othello',
                                lowerbound=1,
                                upperbound=8,
                                image='unnamed.png')
            white= othello.alphabeta_searcher(num, othello.weighted_score)
        if r2 == 'Humano':
            white = human
        if r2 == 'Aleatorio':
            white = othello.random_strategy
        if r2=='Salir':
            return
        cl=0
        try:
            startt = timeit.default_timer()
            #black, white = get_players()
            board, score = othello.play(black, white)
            elapsed = timeit.default_timer() - startt  # en segundos
            cl=elapsed
            print('Tiempo de ejecucion: ', elapsed, 'segundos')
            print('Tiempo de ejecucion: ', elapsed / 60, 'minutos')
        except othello.IllegalMoveError as e:
            print(e)
            return
        except EOFError as e:
            print('Salir.')
            return
        print('Puntuacion(Black-White):  %d' % score)
        print('::::::   %s Gana!' % ('Black' if score > 0 else 'White'))
        print(othello.print_board(board))
        eg.msgbox(msg='Puntuacion(Black-White):  %d\n' % score+'::::::   %s Gana!' % ('Black' if score > 0 else 'White')+ '\nTiempo de ejecucion:%f segundos' %cl,
                  title='Resultados de Ejecucion', ok_button='Mostrar Tablero',
                  image='unnamed.png')
        try:
            othello.draw_board(board)
        except:
            print('Fuera de rango')
        #os.system('pause')
        #global cnodos
        #print(cnodos)
