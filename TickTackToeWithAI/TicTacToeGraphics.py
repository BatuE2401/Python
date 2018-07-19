import pygame
import TicTacToeBoard


### Values for drawing graphics

BLACK = (  0,   0,   0)
WHITE = (250, 250, 250)
RED   = (250,   0,   0)
BLUE  = (  0,   0, 250)

WIDTH_0 = 0
# The width of one square
WIDTH_1 = 200
WIDTH_2 = 400
# The width of the whole board
WIDTH_3 = 600

# Size and thickness of noughts and crosses
figure_radius = 70
figure_thickness = 15

grid_thickness = 5
text_size = 24


class Display():

    def __init__(self):

        pygame.init()
        pygame.display.set_caption('Tic-Tac-Toe')
        self.display_window = pygame.display.set_mode((WIDTH_3, WIDTH_3 + 1 + text_size))
        self.draw_surface = pygame.Surface(self.display_window.get_size()).convert()
        self.font = pygame.font.Font(None, text_size)


        # Set up the background surface
        self.draw_surface.fill(WHITE)
        # Draw the grid lines:
        pygame.draw.line(self.draw_surface, BLACK, (WIDTH_1, WIDTH_0), (WIDTH_1, WIDTH_3), grid_thickness)
        pygame.draw.line(self.draw_surface, BLACK, (WIDTH_2, WIDTH_0), (WIDTH_2, WIDTH_3), grid_thickness)
        pygame.draw.line(self.draw_surface, BLACK, (WIDTH_0, WIDTH_1), (WIDTH_3, WIDTH_1), grid_thickness)
        pygame.draw.line(self.draw_surface, BLACK, (WIDTH_0, WIDTH_2), (WIDTH_3, WIDTH_2), grid_thickness)

        self.show_text("Welcome to a Game of TicTacToe! Click to play!")


    def refresh(self):
        self.display_window.blit(self.draw_surface, (WIDTH_0, WIDTH_0))
        pygame.display.flip()

    def draw_move(self, row, col, token):
        if token == TicTacToeBoard.NOUGHT:
            self.draw_nought(row, col)
        else:
            self.draw_cross(row, col)

    def draw_nought(self, row, col):
        center_X = int( (col * WIDTH_1) + (WIDTH_1 / 2) )
        center_Y = int( (row * WIDTH_1) + (WIDTH_1 / 2) )
        pygame.draw.circle(self.draw_surface, RED, (center_X, center_Y), figure_radius, figure_thickness)

    def draw_cross(self, row, col):
        center_X = int( (col * WIDTH_1) + (WIDTH_1 / 2) )
        center_Y = int( (row * WIDTH_1) + (WIDTH_1 / 2) )
        left = center_X - figure_radius
        right = center_X + figure_radius
        bottom = center_Y - figure_radius
        top = center_Y + figure_radius
        pygame.draw.line(self.draw_surface, BLUE, (left, bottom), (right, top), figure_thickness)
        pygame.draw.line(self.draw_surface, BLUE, (left, top), (right, bottom), figure_thickness)

    def show_text(self, message):
        text = self.font.render(message, 1, BLACK)
        self.draw_surface.fill(WHITE, (0, WIDTH_3, WIDTH_3, 50))
        self.draw_surface.blit(text, (10, WIDTH_3))


    def position_of_click(self):
        (mouse_X, mouse_Y) = pygame.mouse.get_pos()
        if mouse_Y < WIDTH_1:
            row = 0
        elif mouse_Y < WIDTH_2:
            row = 1
        else:
            row = 2

        if mouse_X < WIDTH_1:
            col = 0
        elif mouse_X < WIDTH_2:
            col = 1
        else:
            col = 2

        return (row, col)

