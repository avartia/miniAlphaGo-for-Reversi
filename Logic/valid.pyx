from random import *


def valid(tuple array, int player, int x, int y):
    '''
    Check valid exec_move.
    '''
    cdef int color = player
    if array[x][y] is not None:
        return False
    else:
        # according to 6 directions
        # right direct
        if x < 6 and array[x+1][y] == 1 - color:
            for i in range(x+2, 8):
                if array[i][y] == color:
                    return True
                if array[i][y] is None:
                    break
        # left direct
        if x > 1 and array[x-1][y] == 1 - color:
            for i in range(x - 2, -1, -1):
                if array[i][y] == color:
                    return True
                if array[i][y] is None:
                    break
        # up direct
        if y < 6 and array[x][y+1] == 1 - color:
            for i in range(y+2, 8):
                if array[x][i] == color:
                    return True
                if array[x][i] is None:
                    break
        # down direct
        if y > 1 and array[x][y-1] == 1 - color:
            for i in range(y - 2, -1, -1):
                if array[x][i] == color:
                    return True
                if array[x][i] is None:
                    break
        # up right direct
        if x < 6 and y < 6 and array[x+1][y+1] == 1 - color:
            for i in range(2, min(8-x, 8-y)):
                if array[x+i][y+i] == color:
                    return True
                if array[x+i][y+i] is None:
                    break
        # up left
        if x > 1 and y < 6 and array[x-1][y+1] == 1 - color:
            for i in range(2, min(x+1, 8-y)):
                if array[x-i][y+i] == color:
                    return True
                if array[x-i][y+i] is None:
                    break
        # down right
        if x < 6 and y > 1 and array[x+1][y-1] == 1 - color:
            for i in range(2, min(8-x, y+1)):
                if array[x+i][y-i] == color:
                    return True
                if array[x+i][y-i] is None:
                    break
        # down left
        if x > 1 and y > 1 and array[x-1][y-1] == 1 - color:
            for i in range(2, min(x+1, y+1)):
                if array[x-i][y-i] == color:
                    return True
                if array[x-i][y-i] is None:
                    break

        return False

def get_valid_moves(tuple array, int player=1):
    """
    get all valid moves.
    :param array: 8x8 matrix
    :param player: 默认为计算机
    :return:
    """
    cdef list valid_moves = []
    for x in range(8):
        for y in range(8):
            if valid(array, player, x, y):
                valid_moves.append((x, y))
    return valid_moves

def get_priority_valid_moves(tuple array, list priority_table, int player=1):
    """
    get the valid moves of the same priority.
    :param array: 8x8 matrix
    :param priority_table: 优先表
    :param player: 默认为计算机
    :return: valid list
    """
    cdef list valid_moves = []
    for priority in priority_table:
        for (x, y) in priority:
            if valid(array, player, x, y):
                valid_moves.append((x, y))
        if len(valid_moves) > 0:
            break
    return valid_moves

def move(tuple array, int player, int x, int y):
    """
    FUNCTION: Returns a board after making a exec_move according to Othello rules
    Assumes the exec_move is valid
    :param array: 8x8 matrix
    :param player: player now
    :param x: index of the last exec_move
    :param y: index of the last exec_move
    :param copy: pass by copy or not.
    :return: 8x8 matrix
    """

    cdef int color = player
    array[x][y] = color

    # according to 6 directions
    # right direct
    if x < 6 and array[x + 1][y] == 1 - color:
        for i in range(x + 2, 8):
            if array[i][y] == color:
                for j in range(x+1, i):
                    array[j][y] = color
                break
            if array[i][y] is None:
                break
    # left direct
    if x > 1 and array[x - 1][y] == 1 - color:
        for i in range(x - 1, -1, -1):
            if array[i][y] == color:
                for j in range(x - 1, i, -1):
                    array[j][y] = color
                break
            if array[i][y] is None:
                break
    # up direct
    if y < 6 and array[x][y + 1] == 1 - color:
        for i in range(y + 1, 8):
            if array[x][i] == color:
                for j in range(y+1, i):
                    array[x][j] = color
                break
            if array[x][i] is None:
                break
    # down direct
    if y > 1 and array[x][y - 1] == 1 - color:
        for i in range(y - 2, -1, -1):
            if array[x][i] == color:
                for j in range(y-1, i, -1):
                    array[x][j] = color
                break
            if array[x][i] is None:
                break
    # up right direct
    if x < 6 and y < 6 and array[x + 1][y + 1] == 1 - color:
        for i in range(2, min(8 - x, 8 - y)):
            if array[x + i][y + i] == color:
                for j in range(1, i):
                    array[x+j][y+j] = color
                break
            if array[x + i][y + i] is None:
                break
    # up left
    if x > 1 and y < 6 and array[x - 1][y + 1] == 1 - color:
        for i in range(2, min(x + 1, 8 - y)):
            if array[x - i][y + i] == color:
                for j in range(1, i):
                    array[x - j][y + j] = color
                break
            if array[x - i][y + i] is None:
                break
    # down right
    if x < 6 and y > 1 and array[x + 1][y - 1] == 1 - color:
        for i in range(2, min(8 - x, y + 1)):
            if array[x + i][y - i] == color:
                for j in range(1, i):
                    array[x+j][y-j] = color
                break
            if array[x + i][y - i] is None:
                break
    # down left
    if x > 1 and y > 1 and array[x - 1][y - 1] == 1 - color:
        for i in range(2, min(x + 1, y + 1)):
            if array[x - i][y - i] == color:
                for j in range(1, i):
                    array[x-j][y-j] = color
                break
            if array[x - i][y - i] is None:
                break
    return array


def parity(tuple array, int player, int x, int y):
    """
    whether (x, y) is even or odd
    :param array: 8x8 matrix
    :param player: 1 for ai
    :param x:
    :param y:
    :return: False even, True odd
    """
    cdef int count = 0
    cdef int has_opposite = False
    for i in range(8):
        if array[x][i] is None:
            count += 1
        elif array[x][i] == 1 - player:
            has_opposite = True
    if count > 0 and count % 2 == 0 and has_opposite:
        return False
    count = 0
    has_opposite = False
    for i in range(8):
        if array[i][y] is None:
            count += 1
        elif array[i][y] == 1 - player:
            has_opposite = True
    return count > 0 and count % 2 == 0 and has_opposite


