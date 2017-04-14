# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/14
from init import *
weight_table = ([8, 2, 1, 1, 1, 1, 2, 8],
              [2, 1, 1, 1, 1, 1, 1, 2],
              [1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1, 1],
              [2, 1, 1, 1, 1, 1, 1, 2],
              [8, 2, 1, 1, 1, 1, 2, 8])


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


def get_definite_count(array, player):
    """
    获得确定子的数目。
    :param array: 8*8 matrix
    :param player: 0 for player, 1 for computer
    :return: count
    """
    count = 0
    x11 = 0
    traced = ([False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False],
              [False, False, False, False, False, False, False, False])
    last = 8  # last player step
    while last > 0 and x11 < 8:
        for y in range(last):
            if array[x11][y] == player:
                if not traced[x11][y]:
                    count += weight_table[x11][y]
                    traced[x11][y] = True

            else:
                last = y
                traced[x11][y] = True
                break
        x11 += 1

    # reverse direction
    last = -1
    x12 = 0
    while last < 7 and x12 < 8:
        for y in range(7, last, -1):
            if array[x12][y] == player:
                if not traced[x12][y]:
                    count += weight_table[x12][y]
                    traced[x12][y] = True
            else:
                last = y
                traced[x12][y] = True
                break
        x12 += 1
    # from down
    x21 = 7
    last = 8
    while last > 0 and x21 >= 0:
        for y in range(last):
            if array[x21][y] == player:
                if not traced[x21][y]:
                    count += weight_table[x21][y]
                    traced[x21][y] = True
            else:
                last = y
                traced[x21][y] = True
                break
        x21 -= 1

    x22 = 7
    last = -1
    while last < 7 and x22 >= 0:
        for y in range(7, last, -1):
            if array[x22][y] == player:
                if not traced[x22][y]:
                    count += weight_table[x22][y]
                    traced[x22][y] = True
            else:
                last = y
                traced[x22][y] = True
                break
        x22 -= 1
    return count
