import random

def AIcheck(board, token):  # randomly select a column
    available_moves = board.not_full_columns()
    return random.choice(available_moves)
