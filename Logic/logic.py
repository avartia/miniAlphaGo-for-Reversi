# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/7
from copy import deepcopy

from Logic import valid


def exec_move(passed_array, player, x, y, copy=True):
    """
    FUNCTION: Returns a board after making a exec_move according to Othello rules
    Assumes the exec_move is valid
    :param passed_array: 8x8 matrix
    :param player: player now
    :param x: index of the last exec_move
    :param y: index of the last exec_move
    :param copy: pass by copy or not.
    :return: 8x8 matrix
    """
    # Must copy the passedArray so we don't alter the original
    if copy:
        array = deepcopy(passed_array)
    else:
        array = passed_array
    return valid.move(array, player, x, y)