# import all of the necessary libraries
import pygame, sys
from pygame.locals import *

# import helper libraries
import ConnectFourGraphics
import ConnectFourBoard



class ConnectFour:


    # The `__init__` method is called to initialise the `ConnectFour` game.
    def __init__(self,
            height = 9, width = 9,
            rewards = None,
            red_player = None,
            blue_player = None,
            ai_delay = 60,
            winscore = 1000
            ):

        self.field_state = [[0, 0, 0, 0, 0, 0],
        [1, 2, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [2, 1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0]]
        self.col_heights = [0, 4, 1, 2, 1, 0, 0]



        ## initialise pygame
        pygame.init()
        pygame.font.init()

        ## board
        self.board = ConnectFourBoard.EmptyBoard(height, width, rewards, winscore)

        ## interface
        self.selected_index = -1
        self.display = \
            ConnectFourGraphics.setup_display(self.board)

        ### PLAYER SETTINGS ###
        self.red_player = red_player
        self.blue_player = blue_player
        self.ai_delay = ai_delay

        ## state of the game (scoreboard, who's turn it is, etc.)
        self.score_red = 0
        self.score_blue = 0
        self.winner = 0
        self.score_win = 1000
        self.game_running = True
        self.red_turn = True

        ## draw initial board
        self.draw()


    def human_turn(self):
        if self.red_turn and self.red_player is None:
            # It's red's turn and red's human
            return True
        elif (not self.red_turn) and self.blue_player is None:
            # It's red's turn and red's human
            return True
        else:
            return False

    def draw(self):
        # A wrapper around the `ConnectFourGraphics.draw_board` function that
        # picks all the right components of `self`.
        ConnectFourGraphics.draw_board(self.display, self.board,
                self.score_red, self.score_blue,
                self.selected_index, self.game_running,
                self.human_turn(), self.red_turn, self.winner)

    def turn_token(self):
        if self.red_turn:
            return ConnectFourBoard.RED
        else:
            return ConnectFourBoard.BLUE

    # current player attempts to insert into a column
    def attempt_insert(self, col):
        token = self.turn_token()
        success = self.board.attempt_insert(col, token)
        if success:
            (self.score_red, self.score_blue) = self.board.score()
            if self.win_check():
                self.set_winner()
            self.red_turn = not(self.red_turn)
        # else do nothing: this forces the player to choose again



    def game_loop(self):
        while self.game_running:
            # Let the AI play if it's its turn
            if not self.human_turn():
                start_ai_time = pygame.time.get_ticks()
                token = self.turn_token()
                if token == ConnectFourBoard.RED:
                    move = self.red_player(self.board, token)
                elif token == ConnectFourBoard.BLUE:
                    move = self.blue_player(self, token)
                self.attempt_insert(move)
                stop_ai_time = pygame.time.get_ticks()
                ai_time_span = stop_ai_time - start_ai_time
                if ai_time_span < self.ai_delay:
                    pygame.time.delay(self.ai_delay - ai_time_span)

            # Process all events, especially mouse events.
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == MOUSEMOTION:
                    self.selected_index = \
                        ConnectFourGraphics.hovered_col(self.board)
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if self.human_turn():
                        self.attempt_insert(self.selected_index)


            # Refresh the display and loop back
            self.draw()
            pygame.time.wait(40)

        # Once the game is finish, simply wait for the `QUIT` event
        while True:
            event = pygame.event.wait()
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            pygame.time.wait(60)

    def refresh_scores(self):
        (red, blue) = self.board.score()
        self.score_red = red
        self.score_blue = blue


    # is the game finished?
    # return True if that is the case otherwise return False
    def win_check(self):
        self.red_win = self.score_red >= self.score_win
        self.blue_win = self.score_blue >= self.score_win
        self.full_board = all([self.board.col_height(col) == self.board.height for col in range(self.board.width)])
        return self.red_win or self.blue_win or self.full_board

    def set_winner(self):
        self.game_running = False
        if self.score_red > self.score_blue:
            self.winner = ConnectFourBoard.RED
        elif self.score_red < self.score_blue:
            self.winner = ConnectFourBoard.BLUE
        else:
            self.winner = 0
