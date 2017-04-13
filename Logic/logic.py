# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/7
from copy import deepcopy

from Logic import valid
from init import *


def move(passed_array, player, x, y, copy=True):
    """
    FUNCTION: Returns a board after making a move according to Othello rules
    Assumes the move is valid
    :param passed_array: 8x8 matrix
    :param player: player now
    :param x: index of the last move
    :param y: index of the last move
    :param copy: pass by copy or not.
    :return: 8x8 matrix
    """
    # Must copy the passedArray so we don't alter the original
    if copy:
        array = deepcopy(passed_array)
    else:
        array = passed_array
    return valid.move(array, player, x, y)


def create_buttons():
    """
    create buttons.
    :return:
    """
    # Restart button
    # Background/shadow
    screen.create_rectangle(0, 5, 50, 55, fill="#000033", outline="#000033")
    screen.create_rectangle(0, 0, 50, 50, fill="#000088", outline="#000088")

    # Arrow
    screen.create_arc(5, 5, 45, 45, fill="#000088", width="2", style="arc", outline="white", extent=300)
    screen.create_polygon(33, 38, 36, 45, 40, 39, fill="white", outline="white")

    # Quit button
    # Background/shadow
    screen.create_rectangle(450, 5, 500, 55, fill="#330000", outline="#330000")
    screen.create_rectangle(450, 0, 500, 50, fill="#880000", outline="#880000")
    # "X"
    screen.create_line(455, 5, 495, 45, fill="white", width="3")
    screen.create_line(495, 5, 455, 45, fill="white", width="3")


def dumb_score(array, player):
    """
    Simple heuristic. Compares number of each tile.
    :param array: 8x8 matrix
    :param player: 0(player) or 1(computer)
    :return: player - opponent
    """
    score = 0
    # Set player and opponent colors
    color = player
    opponent = 1 - player

    # +1 if it's player color, -1 if it's opponent color
    for x in range(8):
        for y in range(8):
            if array[x][y] == color:
                score += 1
            elif array[x][y] == opponent:
                score -= 1
    return score


def slightly_less_dumb_score(array, player):
    """
    Less simple but still simple heuristic. Weights corners and edges as more
    :param array: 8x8 matrix
    :param player: 0(player) or 1(computer)
    :return: player - opponent
    """
    score = 0
    # Set player and opponent colors
    color = player
    opponent = 1 - player
    # Go through all the tiles
    for x in range(8):
        for y in range(8):
            # Normal tiles worth 1
            weight = 1
            # Edge tiles worth 3
            if (x == 0 and 1 < y < 6) or (x == 7 and 1 < y < 6) or (y == 0 and 1 < x < 6) or (y == 7 and 1 < x < 6):
                weight = 3
            # Corner tiles worth 5
            elif (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7):
                weight = 5
            # Add or subtract the value of the tile corresponding to the color
            if array[x][y] == color:
                score += weight
            elif array[x][y] == opponent:
                score -= weight
    return score


def decent_heuristic(array, player):
    """
    Heuristic that weights corner tiles and edge tiles as positive,
    adjacent to corners, (if the corner is not yours) as negative
    Weights other tiles as one point
    :param array: 8x8 matrix
    :param player: 0 for player and 1 for computer
    :return: score
    """
    score = 0
    corner_val = 25
    adjacent_val = 5
    side_val = 5
    # Set player and opponent colors
    color = player
    opponent = 1 - player
    # Go through all the tiles
    for x in range(8):
        for y in range(8):
            # Normal tiles worth 1
            add = 1

            # Adjacent to corners are worth -3
            if (x == 0 and y == 1) or (x == 1 and 0 <= y <= 1):
                if array[0][0] == color:
                    add = side_val
                else:
                    add = -adjacent_val

            elif (x == 0 and y == 6) or (x == 1 and 6 <= y <= 7):
                if array[7][0] == color:
                    add = side_val
                else:
                    add = -adjacent_val

            elif (x == 7 and y == 1) or (x == 6 and 0 <= y <= 1):
                if array[0][7] == color:
                    add = side_val
                else:
                    add = -adjacent_val

            elif (x == 7 and y == 6) or (x == 6 and 6 <= y <= 7):
                if array[7][7] == color:
                    add = side_val
                else:
                    add = -adjacent_val

            # Edge tiles worth 3
            elif (x == 0 and 1 < y < 6) or (x == 7 and 1 < y < 6) or (y == 0 and 1 < x < 6) or (y == 7 and 1 < x < 6):
                add = side_val
            # Corner tiles worth 15
            elif (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7):
                add = corner_val
            # Add or subtract the value of the tile corresponding to the color
            if array[x][y] == color:
                score += add
            elif array[x][y] == opponent:
                score -= add
    return score


def final_heuristic(array, player):
    """
    separate the use of heuristics for early/mid/late game.
    :param array: 8x8 matrix
    :param player:
    :return: score
    """
    if moves <= 8:
        num_moves = 0
        for x in range(8):
            for y in range(8):
                if valid.valid(array, player, x, y):
                    num_moves += 1
        return num_moves + decent_heuristic(array, player)
    elif moves <= 52:
        return decent_heuristic(array, player)
    elif moves <= 58:
        return slightly_less_dumb_score(array, player)
    else:
        return dumb_score(array, player)
