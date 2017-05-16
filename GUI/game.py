# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/8
from GUI import Board
from init import *
from Logic import valid


def draw_grid_background(outline=True):
    """
    Method for drawing the grid lines
    :param outline: whether to draw the outlines
    :return:
    """
    # If we want an outline on the board then draw one
    if outline:
        screen.create_rectangle(50, 50, 450, 450, fill="yellow", outline="#111")

    # Drawing the intermediate lines
    for i in range(7):
        line_shift = 50 + 50 * (i + 1)

        # Horizontal line
        screen.create_line(50, line_shift, 450, line_shift, fill="#111")

        # Vertical line
        screen.create_line(line_shift, 50, line_shift, 450, fill="#111")

    screen.update()


def click_handle(event):
    """
    When the user clicks, if it's a valid exec_move, make the exec_move
    :param event: mouse event
    :return:
    """
    global depth
    x_mouse = event.x
    y_mouse = event.y
    if running:
        if x_mouse >= 450 and y_mouse <= 50:
            Root.destroy()
        elif x_mouse <= 50 and y_mouse <= 50:
            init_game()
        else:
            # Is it the player's turn?
            if board.player == 1 - board.AIPlayer:
                # Delete the highlights
                x = int((event.x - 50) / 50)
                y = int((event.y - 50) / 50)
                # Determine the grid index for where the mouse was clicked

                # If the click is inside the bounds and the exec_move is valid, exec_move to that location
                if 0 <= x <= 7 and 0 <= y <= 7:
                    if valid.valid(board.array, board.player, x, y):
                        board.board_move(x, y)
    else:
        # Player of AI choose
        if 300 <= y_mouse <= 350:
            # player
            if 55 <= x_mouse <= 235:
                play_game(0)
            elif 285 <= x_mouse <= 475:
                play_game(1)


def key_handle(event):
    """
    short cuts.
    :param event: key event
    :return:
    """
    symbol = event.keysym
    # restart game
    if symbol.lower() == "r":
        init_game()
    # quit game
    elif symbol.lower() == "q":
        Root.destroy()
    # recover
    elif symbol.lower() == "z":
        board.recover_last_move()


def create_buttons():
    """
    create buttons.
    :return:
    """
    # Restart button
    # Background/shadow
    screen.create_rectangle(0, 5, 50, 55, fill="#003300", outline="#000033")
    screen.create_rectangle(0, 0, 50, 50, fill="#008800", outline="#000088")

    # Arrow
    screen.create_arc(5, 5, 45, 45, fill="#000111", width="4", style="arc", outline="white", extent=300)
    screen.create_polygon(33, 38, 36, 45, 40, 39, fill="white", outline="white")

    # Quit button
    # Background/shadow
    screen.create_rectangle(450, 5, 500, 55, fill="#003300", outline="#330000")
    screen.create_rectangle(450, 0, 500, 50, fill="#008800", outline="#880000")
    # "X"
    screen.create_line(455, 5, 495, 45, fill="white", width="4")
    screen.create_line(495, 5, 455, 45, fill="white", width="4")


def init_game():
    """
    Init game
    :return:
    """
    global running
    running = False
    screen.delete(ALL)
    # Title and shadow
    screen.create_text(250, 203, anchor="c", text="Mini AlphaGo", font=("Consolas", 50), fill="#aaa")
    screen.create_text(250, 200, anchor="c", text="Mini AlphaGo", font=("Consolas", 50), fill="#fff")

    # choose player first or computer first
    screen.create_rectangle(55, 310, 235, 355, fill="#000", outline="#000")
    screen.create_rectangle(55, 300, 235, 350, fill="#111", outline="#111")
    screen.create_text(155, 326, anchor="c", text="Player First", font=("Consolas", 14),
                               fill="#b29600")
    screen.create_text(155, 327, anchor="c", text="Player First", font=("Consolas", 14),
                               fill="#b29600")

    screen.create_rectangle(285, 310, 475, 355, fill="#000", outline="#000")
    screen.create_rectangle(285, 300, 475, 350, fill="#111", outline="#111")
    screen.create_text(375, 326, anchor="c", text="AI First", font=("Consolas", 14),
                       fill="#b29600")
    screen.create_text(375, 327, anchor="c", text="AI First", font=("Consolas", 14),
                       fill="#b29600")

    screen.update()


def play_game(player=0):
    """
    play game.
    :return:
    """
    global board, running
    running = True
    screen.delete(ALL)
    create_buttons()
    board = 0

    # Draw the background
    draw_grid_background()

    # Create the board and update it
    board = Board.Board(player)
    board.update()
