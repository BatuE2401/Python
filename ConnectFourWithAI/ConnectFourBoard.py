import copy

# Board tokens
RED = 1
BLUE = 2

# A few helper functions to manage board initialisation
def new_empty_board(height, width):
    return [([0] * height) for k in range(width)]

class InvalidBoard(Exception):
    pass

def valid_board(board):
    # Checks that the board is a rectangle. If it isn't, this function raises
    # an exception which interupts the program.
    if len(board) == 0:
        raise InvalidBoard('The board has no space')
    else:
        l = len(board[0])
        if any(len(col) != l for col in board):
            raise InvalidBoard('Not all columns have the same heights')
        elif l == 0:
            raise InvalidBoard('The board has no space')




class Board():

    def __init__(self, board=None, rewards=None, winscore=1000):
        if board == None:
            # If no board is passed explicitely, just create one
            board = new_empty_board(8, 9)
        self.field = board
        # This next line will crash the program if the provided board is wrong
        valid_board(self.field)
        self.width = len(self.field)
        self.height = len(self.field[0])
        if rewards == None:
            # The default rewards: [0, 1, 2, 4, 8, 16, 32, etc. ]
            rewards = [0] + [ 2 ** (n - 1) for n in range(1, max(self.width, self.height)) ]
        self.rewards = rewards
        self.winscore = winscore


    def copy(self):
        # Creates a new board using the same underlying field of play
        return Board(
             board=copy.deepcopy(self.field),
             rewards=self.rewards,
             winscore=self.winscore
        )

    def col_height(self, col):
        # Finds out the height of a given column
        # This is useful for inserting tokens and for detecting if the board
        # is full.
        l = 0
        for space in self.field[col]:
            if space != 0:
                l += 1
        return l

    def not_full_columns(self):
        # This method collects all the columns that are not full. This gives a
        # list of playable columns. It is useful for AIs.
        cs = []
        for col in range(self.width):
            if self.col_height(col) < self.height:
                cs.append(col)
        return cs

    def attempt_insert(self, col, token):
        # is it possible to insert into this column?
        if self.col_height(col) < self.height:

            # add a token in the selected column
            self.field[col][self.col_height(col)] = token
            # return True for success
            return True

        else:
            # return False for Failure
            return False

    def update_sequence(self, token, sequence, scores):
        if token == sequence['colour']:
            sequence['length'] += 1
        else:
            if sequence['length'] > 0:
                points = self.rewards[sequence['length'] - 1]
            else:
                points = 0
            if sequence['colour'] == 1:
                scores['red'] += points
            elif sequence['colour'] == 2:
                scores['blue'] += points
            if token == 0:
                sequence['colour'] = 0
                sequence['length'] = 0
            else:
                sequence['colour'] = token
                sequence['length'] = 1

    def score_vertical(self):
        scores = { 'red': 0, 'blue': 0 }
        for col in range(0, self.width):
            sequence = { 'length': 0, 'colour':0  }
            for row in range(0, self.height):
                token = self.field[col][row]
                self.update_sequence(token, sequence, scores)
            self.update_sequence(0, sequence, scores)
        return scores

    def score_horizontal(self):
        scores = {'red': 0, 'blue': 0}
        for row in range(0, self.height):
            sequence = {'length': 0, 'colour': 0}
            for col in range(0, self.width):
                token = self.field[col][row]
                self.update_sequence(token, sequence, scores)
            self.update_sequence(0, sequence, scores)
        return scores

    def score_upright(self, field):
        scores = {'red': 0, 'blue': 0}
        for col in range(self.width):
            sequence = {'length': 0, 'colour': 0}
            for row in range(self.height):
                if col+row < self.width:
                    token = field[col+row][row]
                    self.update_sequence(token, sequence, scores)
                else:
                    self.update_sequence(0, sequence, scores)
            self.update_sequence(0, sequence, scores)

        for row in range(1, self.height):
            sequence = {'length': 0, 'colour': 0}
            for col in range(self.width):
                if col+row < self.height:
                    token = field[col][row+col]
                    self.update_sequence(token, sequence, scores)
                else:
                    self.update_sequence(0, sequence, scores)
            self.update_sequence(0, sequence, scores)
        return scores

    def score_upleft(self):
        return self.score_upright(list(reversed(self.field)))


    def score(self):
        v_scores = self.score_vertical()
        h_scores = self.score_horizontal()
        ur_scores = self.score_upright(self.field)
        ul_scores = self.score_upleft()
        red = v_scores['red'] + h_scores['red'] \
        + ur_scores['red'] + ul_scores['red']
        blue = v_scores['blue'] + h_scores['blue'] + \
        ur_scores['blue'] + ul_scores['blue']
        return (red, blue)

    def is_full(self):
        # TODO: You need to implement this method
        return False




# This additional class simply creates an empty board of a given size.
# Note the `Board` between brackets (`(` and `)`). This means that the methods
# from the class `Board` are available in the class `EmptyBoard`. In other
# words, `EmptyBoard` is just a special case of the general case `Board`.
class EmptyBoard(Board):

    # Function to set up the objects of this class
    def __init__(self, height=8, width=9, rewards=None, winscore=100):
        # Create a simple empty board with the right height and width
        fresh_board = new_empty_board(height, width)
        # Then, proceed to set-up as in `Board`. The `super()` part refers to
        # the class `Board`.
        Board.__init__(self, fresh_board, rewards, winscore)
