from sol1backtrack import *
from sol2minconflict import *
from sol3vegas import *
import easygui as eg

respuesta=''
while respuesta!='Salir':
    num=0
    respuesta = eg.buttonbox(msg='Electiva 3 - Inteligencia Artificial',
                             title='I.A.  :  N Reinas',
                             choices=('Backtracking', 'Minimmun Conflicts', 'Las Vegas', 'Salir'),
                             image='q.png')
    if respuesta=='Backtracking':
        num = eg.integerbox(msg='Ingresar tamano del tablero:',
                            title='I.A.  :  N Reinas',
                            lowerbound=0,
                            upperbound=1000000,
                            image='q.png')
        if num!= None:
            r0= eg.buttonbox(msg='Electiva 3 - Inteligencia Artificial',
                             title='I.A.  :  N Reinas',
                             choices=('Una solucion', 'Todas las soluciones'),
                             image='q.png')
            if r0=='Una solucion':
                backtrack(num,num)
            if r0 == 'Todas las soluciones':
                backtrack(num, 0)

    if respuesta=='Minimmun Conflicts':
        num = eg.integerbox(msg='Ingresar tamano del tablero:',
                            title='I.A.  :  N Reinas',
                            lowerbound=0,
                            upperbound=1000000,
                            image='q.png')
        if num != None and num>0:
            minc(num)

    if respuesta=='Las Vegas':
        num = eg.integerbox(msg='Ingresar tamano del tablero:',
                            title='I.A.  :  N Reinas',
                            lowerbound=0,
                            upperbound=1000000,
                            image='q.png')
        if num != None and num > 0:
            vegas(num)

