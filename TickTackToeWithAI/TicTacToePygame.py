# Python libraries
import sys
import pygame
from pygame.locals import *

# Board management and display modules
import TicTacToeBoard
import TicTacToeGraphics

# AIs
# import GoodAI
import BruteForceAI
# import GuessingAI
import RandomAI
### Values for players

# Player is X (crosses), Computer is O (noughts)
HUMAN = BruteForceAI.HUMAN
COMPUTER = BruteForceAI.COMPUTER

# The computer opponent, change the lines to change the computer opponent
#computer_AI = BruteForceAI.computer_AI
#computer_AI = GuessingAI.computer_AI
computer_AI = BruteForceAI.computer_AI
#computer_AI = RandomAI.computer_AI



### Helpers for running the game

def next_to_play(playing):
    if playing == HUMAN:
        return COMPUTER
    else:
        return HUMAN

def game_won(board):
    if board.win(HUMAN):
        return ("You have won")
    elif board.win(COMPUTER):
        return ("You have lost")
    elif board.full():
        return ("Its a draw!")
        sys.exit(0)
    else:
        return None


### Running the game

while True:
    # Initialise underlying library
    pygame.init()

    # Initialise graphics
    display = TicTacToeGraphics.Display()

    # Initialise the state (board and player)
    board = TicTacToeBoard.Board()
    playing = HUMAN
    game_playing = True


    # Main event loop
    while game_playing:
        event = pygame.event.poll()

        # Handle the player quiting
        if event.type is QUIT:
            game_playing = False
            pygame.quit()
            sys.exit(0)

        # Handle the player's click if it's their turn
        elif event.type is MOUSEBUTTONDOWN and playing == HUMAN:
            # Find the selected square and check it's an available spot
            (row, col) = display.position_of_click()
            index = TicTacToeBoard.index_of_coordicates(row, col)
            if board.is_free(index):

                # Add a token
                board.input_move(index, HUMAN)
                (row, col) = TicTacToeBoard.coordinates_of_index(index)
                display.draw_move(row, col, HUMAN)

                # Check victory and, if so, act on it
                winning = game_won(board)
                if winning is not None:
                    display.show_text(winning)
                    game_playing = False
                # Yield
                playing = next_to_play(playing)

        # Handle the computer's choice if it's its turn
        elif playing == COMPUTER and game_playing:
            index = computer_AI(board)
            if index is not None:
                board.input_move(index, COMPUTER)
                (row, col) = TicTacToeBoard.coordinates_of_index(index)
                display.draw_move(row, col, COMPUTER)
                # Check victory and, if so, act on it
                winning = game_won(board)
                if winning is not None:
                    display.show_text(winning)
                    game_playing = False
                playing = next_to_play(playing)

        display.refresh()


    # After the main loop is over, wait two seconds and quit
    pygame.time.delay(2000)
    pygame.quit()
    sys.exit(0)
