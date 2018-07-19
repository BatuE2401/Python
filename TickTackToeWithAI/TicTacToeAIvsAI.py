# Python libraries
import sys
import pygame
from pygame.locals import *
from time import *

# Board management library
import TicTacToeBoard

# AIs
#import GoodAI
import BruteForceAI
#import GuessingAI
#import RandomAI

### Values for players

# The computer opponent, change the lines to change the computer opponent
#computer_AI = BruteForceAI.computer_AI
#computer_AI = GuessingAI.computer_AI
ai_1_picker = BruteForceAI.computer_AI
ai_2_picker = BruteForceAI.computer_AI

# Player is X (crosses), Computer is O (noughts)
ai_1 = TicTacToeBoard.CROSS
ai_2 = TicTacToeBoard.NOUGHT

score = []


### Values for drawing graphics

black = (  0,   0,   0)
white = (250, 250, 250)
red   = (250,   0,   0)
blue  = (  0,   0, 250)

width_0 = 0
# The width of one square
width_1 = 200
width_2 = 400
# The width of the whole board
width_3 = 600

# Size and thickness of noughts and crosses
figure_radius = 70
figure_thickness = 15

grid_thickness = 5
text_size = 24



### Setting up and drawing

def initialise_surface(display_window):
    ## Set up the background surface
    draw_surface = pygame.Surface(display_window.get_size())
    draw_surface = draw_surface.convert()
    draw_surface.fill(white)

    ## Draw the grid lines:
    pygame.draw.line(draw_surface, black, (width_1, width_0), (width_1, width_3), grid_thickness)
    pygame.draw.line(draw_surface, black, (width_2, width_0), (width_2, width_3), grid_thickness)
    pygame.draw.line(draw_surface, black, (width_0, width_1), (width_3, width_1), grid_thickness)
    pygame.draw.line(draw_surface, black, (width_0, width_2), (width_3, width_2), grid_thickness)

    return draw_surface


def show_board(display_window, draw_surface):
    display_window.blit(draw_surface, (width_0, width_0))
    pygame.display.flip()

def draw_move(draw_surface, index, token):
    (row, col) = TicTacToeBoard.coordinates_of_index(index)
    if token == TicTacToeBoard.NOUGHT:
        draw_nought(draw_surface, row, col)
    else:
        draw_cross(draw_surface, row, col)

def draw_nought(draw_surface, row, col):
    center_X = int( (col * width_1) + (width_1 / 2) )
    center_Y = int( (row * width_1) + (width_1 / 2) )
    pygame.draw.circle(draw_surface, red, (center_X, center_Y), figure_radius, figure_thickness)

def draw_cross(draw_surface, row, col):
    center_X = int( (col * width_1) + (width_1 / 2) )
    center_Y = int( (row * width_1) + (width_1 / 2) )
    left = center_X - figure_radius
    right = center_X + figure_radius
    bottom = center_Y - figure_radius
    top = center_Y + figure_radius
    pygame.draw.line(draw_surface, blue, (left, bottom), (right, top), figure_thickness)
    pygame.draw.line(draw_surface, blue, (left, top), (right, bottom), figure_thickness)

def show_text(draw_surface, font, message):
    text = font.render(message, 1, black)
    draw_surface.fill(white, (0, width_3, width_3, 50))
    draw_surface.blit(text, (10, width_3))

### Handling clicks

def index_of_click_position(mouse_X, mouse_Y):
    # determine the row the user clicked
    if mouse_Y < width_1:
        row = 0
    elif mouse_Y < width_2:
        row = 1
    else:
        row = 2
    # determine the column the user clicked
    if mouse_X < width_1:
        col = 0
    elif mouse_X < width_2:
        col = 1
    else:
        col = 2

    index = TicTacToeBoard.index_of_coordicates(row, col)
    return index

def index_of_click(board, draw_surface):

    (mouse_X, mouse_Y) = pygame.mouse.get_pos()
    index = index_of_click_position(mouse_X, mouse_Y)

    # make sure this space is not in use
    if board.is_free(index):
        return index
    else:
        return None


### Helpers for running the game

def next_to_play(playing):
    if playing == ai_1:
        return ai_2
    else:
        return ai_1

def game_won(board):
    if board.win(ai_1):
        print(ai_1)
        return "AI1 has won"
    elif board.win(ai_2):
        print(ai_2)
        return "AI2 has won"
    elif board.full():
        print('=')
        return "This game is a tie."
    else:
        return None


### Running the game

while True:

    # Set-up the graphics
    pygame.init()
    display_window = pygame.display.set_mode((width_3, width_3 + 1 + text_size))
    pygame.display.set_caption('Tic-Tac-Toe')
    draw_surface = initialise_surface(display_window)
    font = pygame.font.Font(None, text_size)
    show_text(draw_surface, font, "Welcome to a Game of TicTacToe! Click to play!")


    # Initialise the state (board and player)
    board = TicTacToeBoard.Board()
    playing = ai_1
    game_playing = True


    # Main event loop
    while game_playing:
        sleep(1)
        event = pygame.event.poll()

        # Handle the player quiting
        if event.type is QUIT:
            game_playing = False
            pygame.quit()
            sys.exit(0)

        elif playing == ai_1 and game_playing:
            index = ai_1_picker(board)
            if index is not None:
                board.input_move(index, ai_1)
                draw_move(draw_surface, index, ai_1)
                winning = game_won(board)
                if winning is not None:
                    show_text(draw_surface, font, winning)
                    game_playing = False
                playing = next_to_play(playing)

        elif playing == ai_2 and game_playing:
            index = ai_2_picker(board)
            if index is not None:
                board.input_move(index, ai_2)
                draw_move(draw_surface, index, ai_2)
                winning = game_won(board)
                if winning is not None:
                    show_text(draw_surface, font, winning)
                    game_playing = False
                playing = next_to_play(playing)

        show_board(display_window, draw_surface)

    pygame.quit()
    sys.exit(0)
