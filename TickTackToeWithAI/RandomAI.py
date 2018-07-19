import random
def computer_AI(board):
    possible_moves = []
    for i in [0,1,2,3,4,5,6,7,8]:
        if board.is_free(i):
            possible_moves.append(i)
    return random.choice(possible_moves)
