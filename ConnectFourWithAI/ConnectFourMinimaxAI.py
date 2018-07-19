import copy

import ConnectFourBoard

def other(token):
    if token == ConnectFourBoard.RED:
        return ConnectFourBoard.BLUE
    elif token == ConnectFourBoard.BLUE:
        return ConnectFourBoard.RED
    else:
        return None


# estimate of a field quality
def state_score(field, token):
    (score_red, score_blue) = field.score()
    if token == ConnectFourBoard.RED:
        return score_red - score_blue
    else:
        return score_blue - score_red

def max_play(game, field, fieldheights):
    moves = []
    for n in range(0, game.board.width):
        if(fieldheights[n] < game.board.height):
            newfield = copy.deepcopy(field)
            newheights = copy.deepcopy(fieldheights)
            token = 1 if game.red_turn else 2
            newfield.field[n][fieldheights[n]] = token
            newheights[n] += 1
            value = state_score(newfield, token)
            moves.append((n,value))
    best_move = max(moves, key = lambda x: x[1])
    return best_move

def AIcheck(game, token):
    # Modify to set a different search depth
    fieldheights = []
    for i in range(game.board.width):
        fieldheights.append(game.board.col_height(i))
    ply_remaining = 3
    (move, value) = max_play(game, game.board, fieldheights)
    return move
