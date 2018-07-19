import random
import TicTacToeBoard

HUMAN = TicTacToeBoard.CROSS
COMPUTER = TicTacToeBoard.NOUGHT

BRUTEWIN = 1
DRAW = 0
BRUTELOSE = -1

def mock_play(board, index, token):
    second_board = board.copy()
    second_board.input_move(index, token)
    return second_board

def computer_AI(board):
    return brute_force(board)

def brute_force(board):
    best_outcome = -2
    best_move = None
    for move in board.free_spaces():
        possible_board = mock_play(board, move, COMPUTER)
        if possible_board.win(COMPUTER):
            best_outcome = 1
            best_move = move
        else:
            outcome = opponent_play_outcome(possible_board)
            if outcome > best_outcome:
                best_move = move
                best_outcome = outcome
    return best_move

def opponent_play_outcome(board):
    if board.game_over():
        return outcome_of_board(board)
    worst_outcome = 2
    for move in board.free_spaces():
        possible_board = mock_play(board, move, HUMAN)
        outcome = brute_play_outcome(possible_board)
        if outcome < worst_outcome:
            worst_outcome = outcome
    return worst_outcome

def brute_play_outcome(board):
    if board.game_over():
        return outcome_of_board(board)
    best_outcome = -2
    for move in board.free_spaces():
        possible_board = mock_play(board, move, COMPUTER)
        outcome = opponent_play_outcome(possible_board)
        if outcome > best_outcome:
            best_outcome = outcome
    return best_outcome

def outcome_of_board(board):
    if board.win(COMPUTER):
        return BRUTEWIN
    if board.win(HUMAN):
        return BRUTELOSE
    if board.full():
        return DRAW
    return None
