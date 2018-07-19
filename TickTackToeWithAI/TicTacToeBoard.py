import copy

## Constants: tokens, board

CROSS = 'X'
NOUGHT = 'O'

# None is empty, X is cross, O is nought
EMPTY_BOARD = [
    None, None, None,
    None, None, None,
    None, None, None,
]

# NOTE: because lists are 0-indexed, the board looks like:
# 0 1 2
# 3 4 5
# 6 7 8




## Conversion functions between different type of addressing

def coordinates_of_index(index):
    coordinates = [
        (0,0), (0,1), (0,2),
        (1,0), (1,1), (1,2),
        (2,0), (2,1), (2,2),
    ]
    return coordinates[index]

def index_of_coordicates(row, col):
    indices = [
        [0,1,2],
        [3,4,5],
        [6,7,8],
    ]
    return indices[row][col]

ROWS_COLS_DIAGONALS = [
    (0,1,2), (3,4,5), (6,7,8),
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
]



## Board class: managing a board, checking its status, modifying it

class Board():
    def __init__(self, board=None):
        if board == None:
            board = copy.deepcopy(EMPTY_BOARD)
        self.board = board

    def copy(self):
        copied_board = copy.deepcopy(self.board)
        return Board(copied_board)

    def is_free(self, index):
        return self.board[index] == None

    def free_spaces(self):
        return [ index for index in range(0, 9) if self.is_free(index) ]

    def input_move(self, index, token):
        self.board[index] = token

    def win(self, token):
        for (a,b,c) in ROWS_COLS_DIAGONALS:
            if self.board[a] == token \
                and self.board[b] == token \
                and self.board[c] == token:
                    return True
        return False

    def full(self):
        return all(self.board)

    def game_over(self):
        return self.full() or self.win(NOUGHT) or self.win(CROSS)
