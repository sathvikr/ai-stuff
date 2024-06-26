from othello.othello_modelling.othello_imports import possible_moves
from random import choice
import sys

board = sys.argv[1]
player = sys.argv[2]
print(choice(possible_moves(board, player)))