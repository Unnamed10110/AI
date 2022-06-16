file=open('cnds.txt', 'w')
file2=open('cnds2.txt', 'w')
cnodos=0
cnodos2=0
EMPTY, BLACK, WHITE, OUTER = '.', '#', 'O', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}


UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

def squares():
    # lista de celdas validas en el tablero
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board():
    # se inicializa el tablero con las cuatro primeras priezas repectivas del juego, por cada jugador
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # se ubican las 4 piezas iniciales
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board):
    #representacion del tablero como string
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep



def is_valid(move):
    #validar movimiento
    return isinstance(move, int) and move in squares()

def opponent(player):
    #obtener pieza del oponente
    return BLACK if player is WHITE else WHITE

def find_bracket(square, player, board, direction):
    # encuentra una celda que forme un grupo con 'square' para un 'player' en una direccion dada.

    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move, player, board):
    #movimiento legal para el player
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(map(hasbracket, DIRECTIONS))


def make_move(move, player, board):
    #actualizar el tablero dado un movimiento del player
    board[move] = player
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move, player, board, direction):
    # invertir las piezas dado el movimiento del player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction



class IllegalMoveError(Exception):
    def __init__(self, player, move, board):
        self.player = player
        self.move = move
        self.board = board

    def __str__(self):
        return '%s no puede mover a %d' % (PLAYERS[self.player], self.move)

def legal_moves(player, board):
    #lista de movimientos validos para player
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player, board):
    #verifica si el player puede realizar algun movimiento
    return any(is_legal(sq, player, board) for sq in squares())


def play(black_strategy, white_strategy):
    # ejecuta el juego y retorna el tablero final y las puntuaciones
    board = initial_board()
    player = BLACK
    strategy = lambda who: black_strategy if who == BLACK else white_strategy
    while player is not None:
        move = get_move(strategy(player), player, board)
        make_move(move, player, board)
        player = next_player(board, player)
    return board, score(BLACK, board)

def next_player(board, prev_player):
    opp = opponent(prev_player)
    if any_legal_move(opp, board):
        return opp
    elif any_legal_move(prev_player, board):
        return prev_player
    return None

def get_move(strategy, player, board):
    # obtiene un movimiento para el jugador en el tablero dada una estrategia
    copy = list(board) # duplicado del tablero para validar
    move = strategy(player, copy)
    if not is_valid(move) or not is_legal(move, player, board):
        raise IllegalMoveError(player, move, copy)
    return move

def score(player, board):

    mine, theirs = 0, 0
    opp = opponent(player)
    for sq in squares():
        piece = board[sq]
        if piece == player: mine += 1
        elif piece == opp: theirs += 1
    return mine - theirs



import random

def random_strategy(player, board):
    # estrategia aleatoria para puebas
    return random.choice(legal_moves(player, board))


def maximizer(evaluate):

    def strategy(player, board):
        def score_move(move):
            return evaluate(player, make_move(move, player, list(board)))
        return max(legal_moves(player, board), key=score_move)
    return strategy


SQUARE_WEIGHTS = [
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
    0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
    0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
    0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
    0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
]


def weighted_score(player, board):
    opp = opponent(player)
    total = 0
    for sq in squares():
        if board[sq] == player:
            total += SQUARE_WEIGHTS[sq]
        elif board[sq] == opp:
            total -= SQUARE_WEIGHTS[sq]
    return total



def minimax(player, board, depth, evaluate):

    def value(board):
        global cnodos
        cnodos=cnodos+1
        #print(cnodos)
        #print(cnodos, '---------------------------')
        global file
        #file.seek(0)
        #file.truncate()
        file.write('%d\n' % cnodos)
        return -minimax(opponent(player), board, depth-1, evaluate)[0]

    if depth == 0:

        return evaluate(player, board), None

    moves = legal_moves(player, board)

    if not moves:
        if not any_legal_move(opponent(player), board):
            #print(cnodos, '---------------------------')
            return final_value(player, board), None
            #print("Nodos expandidos (Minimax) %d" % cnodos)
        #print("Nodos expandidos (Minimax) %d"%cnodos)
        return value(board), None

    return max((value(make_move(m, player, list(board))), m) for m in moves)



MAX_VALUE = sum(map(abs, SQUARE_WEIGHTS))
MIN_VALUE = -MAX_VALUE

def final_value(player, board):

    diff = score(player, board)
    if diff < 0:
        return MIN_VALUE
    elif diff > 0:
        return MAX_VALUE
    return diff

def minimax_searcher(depth, evaluate):

    def strategy(player, board):
        return minimax(player, board, depth, evaluate)[1]
    return strategy


def alphabeta(player, board, alpha, beta, depth, evaluate):
    if depth == 0:
        return evaluate(player, board), None

    def value(board, alpha, beta):
        global cnodos2
        cnodos2 = cnodos2 + 1
        global file2
        file2.write('%d\n' % cnodos2)
        return -alphabeta(opponent(player), board, -beta, -alpha, depth-1, evaluate)[0]

    moves = legal_moves(player, board)
    if not moves:
        if not any_legal_move(opponent(player), board):
            return final_value(player, board), None
        #print("Nodos expandidos (alpha-beta) %d" % cnodos2)
        return value(board, alpha, beta), None

    best_move = moves[0]
    for move in moves:
        if alpha >= beta:
            break
        val = value(make_move(move, player, list(board)), alpha, beta)
        if val > alpha:
            alpha = val
            best_move = move
    return alpha, best_move

def alphabeta_searcher(depth, evaluate):
    def strategy(player, board):
        return alphabeta(player, board, MIN_VALUE, MAX_VALUE, depth, evaluate)[1]
    return strategy


#####################3
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame, os
from multiprocessing import Process, Queue

def draw_board(q):
    """ Draw a chess board with queens, as determined by the the_board. """
    n=8

    q2=[]
    for a in range(0,100):
        if q[a]== '#'or q[a]== 'O':
            q2.append(q[a])
    #print(q2)
    #os.system('pause')

    pygame.init()
    colors = [(255, 250, 250), (0, 0, 0), (250, 0, 0)]
    surfaceSz = 640          # Proposed physical surface size.
    sq_sz = surfaceSz // n    # sq_sz is length of a square.
    surfaceSz = n * sq_sz     # Adjust to exact multiple of sq_sz

    # Create the surface of (width, height), and its window.
    pygame.display.set_caption("Simulador")
    surface = pygame.display.set_mode((surfaceSz, surfaceSz))


    ball = pygame.image.load("black2.png")
    if ball.get_width() > sq_sz:
       ball = pygame.transform.scale(ball, (sq_sz - 10, sq_sz - 10))
    ball2 = pygame.image.load("white2.png")
    if ball2.get_width() > sq_sz:
        ball2 = pygame.transform.scale(ball2, (sq_sz - 10, sq_sz - 10))

    # Use an extra offset to centre the ball in its square.
    # If the square is too small, offset becomes negative,
    # but it will still be centered :-)
    ball_offset = (sq_sz-ball.get_rect()[2]) // 2


    while True:

        # look for an event from keyboard, mouse, etc.
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:
            break;

        #if not q.empty():
        #    e = q.get()
        #    the_board = e["board"]
        #    solution = e["solution"]

        # Draw a fresh background (a blank chess board)
        cc=0
        for row in range(n):  # Draw each row of the board.
            #c_indx = row % 2  # Alternate starting color
            for col in range(n):  # Run through cols drawing squares
                if q2[cc]=='#':
                    colora=(0, 0, 0)
                    #colora = (255, 250, 250)
                else:
                    #colora=(255, 250, 250)
                    colora = (0, 0, 0)
                the_square = (col * sq_sz, row * sq_sz, sq_sz, sq_sz)
                surface.fill(colora, the_square)
                if q2[cc] == '#':
                    surface.blit(ball,(col * sq_sz + ball_offset, row * sq_sz + ball_offset))
                else:
                    surface.blit(ball2, (col * sq_sz + ball_offset, row * sq_sz + ball_offset))
                # now flip the color index for the next square
                #c_indx = (c_indx + 1) % 2
                cc=cc+1
                if cc>100: break
                #pygame.display
                #os.system('pause')
        pygame.display

        pygame.time.delay(50)
        # Now that squares are drawn, draw the queens.
        '''for (col, row) in enumerate(the_board):
            if row != -1:
                surface.blit(ball,
                    (col*sq_sz+ball_offset,row*sq_sz+ball_offset))

        '''
        '''if solution:
            pygame.display.flip()
            pygame.time.delay(1000)
            #print(the_board,'-----')
        else:
            pygame.time.delay(200)
        if q.empty():
            break
        '''


    pygame.quit()