from agentes import othello
import timeit



black=othello.minimax_searcher(3, othello.score)
white=othello.alphabeta_searcher(3, othello.score)


startt = timeit.default_timer()
# black, white = get_players()
board, score = othello.play(black, white)
elapsed = timeit.default_timer() - startt  # en segundos
cl = elapsed
print('Tiempo de ejecucion: ', elapsed, 'segundos')
print('Tiempo de ejecucion: ', elapsed / 60, 'minutos')