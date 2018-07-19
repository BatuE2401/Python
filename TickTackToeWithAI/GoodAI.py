import random
import TicTacToeBoard

def choose_move_from_list(board, moves_list):
    possible_moves = []
    for move in moves_list:
        if board.is_free(move):
            possible_moves.append(move)
    if possible_moves:
        return random.choice(possible_moves)
    else:
        return None

def computer_AI(board):
    if board.is_free(4):
        return 4
    corner = choose_move_from_list(board, [0,2,6,8])
    if corner is not None:
        return corner
    side = choose_move_from_list(board, [1,3,5,7])
    if side is not None:
        return side
