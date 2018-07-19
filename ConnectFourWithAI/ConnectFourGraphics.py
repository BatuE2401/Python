import pygame

# This module takes care of the graphical interface: drawing the shapes and
# printing the text that together make the game window.

# display constants (these are not crucial to the game or pygame)
FONTSIZE = 24
CELL_SIZE = 48
OFFSET_CANVAS = 20
TOP_OFFSET = 24
BOTTOM_SPACING = 64

# colour constants
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
BLUE   = (  0,   0, 255)
YELLOW = (250, 240, 190)

def setup_display(board):
    window_width = 2 * OFFSET_CANVAS + board.width * CELL_SIZE
    window_height = 2 * OFFSET_CANVAS + TOP_OFFSET + BOTTOM_SPACING + board.height * CELL_SIZE
    display = pygame.display.set_mode((window_width, window_height), 0, 32)
    pygame.display.set_caption('Connect Four')
    gamefont = pygame.font.Font(None, FONTSIZE)
    return (display, gamefont)

def draw_arrow(display, column):
    top_point = (OFFSET_CANVAS + CELL_SIZE / 2 + CELL_SIZE * column,
                 OFFSET_CANVAS)
    bottom_point = (OFFSET_CANVAS + CELL_SIZE / 2 + CELL_SIZE * column,
                    OFFSET_CANVAS + TOP_OFFSET * 3 / 4)
    left_point = (OFFSET_CANVAS + 3 * CELL_SIZE / 8 + CELL_SIZE * column,
                  OFFSET_CANVAS + TOP_OFFSET / 2)
    right_point = (OFFSET_CANVAS + 5 * CELL_SIZE / 8 + CELL_SIZE * column,
                   OFFSET_CANVAS + TOP_OFFSET / 2)
    pygame.draw.line(display, BLACK, left_point, bottom_point, 3)
    pygame.draw.line(display, BLACK, right_point, bottom_point, 3)
    pygame.draw.line(display, BLACK, top_point, bottom_point, 3)


def draw_board(game_display,
        board, score_red, score_blue,
        selected_index, game_running, player_turn, red_turn, winner):
    (display, gamefont) = game_display
    display.fill(YELLOW)

    # draw border
    pygame.draw.rect(display, BLACK,
            (OFFSET_CANVAS,
             OFFSET_CANVAS + TOP_OFFSET,
             board.width * CELL_SIZE,
             board.height * CELL_SIZE
            ),
            2)

    # draw all tokens and circles
    for j in range(board.height):
        for i in range(board.width):
            xc = OFFSET_CANVAS + CELL_SIZE / 2 + i * CELL_SIZE
            yc = OFFSET_CANVAS + TOP_OFFSET + CELL_SIZE / 2 + (board.height - j - 1) * CELL_SIZE
            if board.field[i][j] == 1:
                pygame.draw.circle(display, RED, (int(xc), int(yc)), int(CELL_SIZE * 2 / 5), 0)
            if board.field[i][j] == 2:
                pygame.draw.circle(display, BLUE, (int(xc), int(yc)), int(CELL_SIZE * 2 / 5), 0)
            pygame.draw.circle(display, BLACK, (int(xc), int(yc)), int(CELL_SIZE * 2 / 5), 1)

    # display players' score
    red_score_surf = gamefont.render('RED: ' + str(score_red), False, RED)
    blue_score_surf = gamefont.render('BLUE: ' + str(score_blue), False, BLUE)
    score_x = OFFSET_CANVAS
    score_y = 2 * OFFSET_CANVAS + TOP_OFFSET + board.height * CELL_SIZE
    display.blit(red_score_surf, (score_x, score_y))
    display.blit(blue_score_surf, (score_x, score_y + FONTSIZE))

    # potentially display arrow
    if selected_index >= 0 and game_running and player_turn:
        draw_arrow(display, selected_index)
    # is it the AI player's turn?
    if game_running:
        if red_turn:
            thinking_surf = gamefont.render("Red playing...", False, RED)
        else:
            thinking_surf = gamefont.render("Blue playing...", False, BLUE)
        display.blit(thinking_surf, (OFFSET_CANVAS + 3 * CELL_SIZE, 2 * OFFSET_CANVAS + TOP_OFFSET + board.height * CELL_SIZE))

    if not(game_running):
        draw_winners(display, gamefont, winner)

    pygame.display.update()

def draw_winners(display, gamefont, winner):
    if winner == 0:
        win_surf = gamefont.render("DRAW!", False, BLACK)
    elif winner == 1:
        win_surf = gamefont.render("RED WINS!", False, RED)
    else:
        win_surf = gamefont.render("BLUE WINS!", False, BLUE)
    display.blit(win_surf, (OFFSET_CANVAS, OFFSET_CANVAS / 2))

# check which column is being hovered
def hovered_col(board):
    (mouse_x, mouse_y) = pygame.mouse.get_pos()
    if (mouse_x >= OFFSET_CANVAS \
       and mouse_x < OFFSET_CANVAS + board.width * CELL_SIZE \
       and mouse_y >= OFFSET_CANVAS + TOP_OFFSET \
       and mouse_y <= OFFSET_CANVAS + TOP_OFFSET + board.height * CELL_SIZE):
        # The player clicked on a column, not outside
        return int((mouse_x - OFFSET_CANVAS) / CELL_SIZE)
    else:
        # `-1` is the indicator that nothing has been selected
        return -1
