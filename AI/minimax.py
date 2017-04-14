# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/8
from Logic.logic import *


def minimax(board, node, dep, maximizing):
    """
    This contains the minimax algorithm
    http://en.wikipedia.org/wiki/Minimax
    :param board: GUI.Board
    :param node: 8x8 matrix
    :param dep: depth
    :param maximizing: to maximize or not
    :return: [best value, best board]
    """
    global nodes
    nodes += 1
    boards = []
    choices = []

    for x in range(8):
        for y in range(8):
            # append possible moves
            if valid(board.array, board.player, x, y):
                test = board.move(node, x, y)
                boards.append(test)
                choices.append([x, y])

    if dep == 0 or len(choices) == 0:
        return [decent_heuristic(node, 1-maximizing), node]

    if maximizing:
        best_value = -float("inf")
        best_board = []
        for b in boards:
            val = minimax(board, b, dep - 1, 0)[0]
            if val > best_value:
                best_value = val
                best_board = b
        return [best_value, best_board]

    else:
        best_value = float("inf")
        best_board = []
        for b in boards:
            val = minimax(board, b, dep - 1, 1)[0]
            if val < best_value:
                best_value = val
                best_board = b
        return [best_value, best_board]


def alpha_beta(board, node, dep, alpha, beta, maximizing):
    """
    alpha_beta pruning on the minimax tree
    http://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning
    :param board: GUI.Board
    :param node: 8x8 matrix
    :param dep: depth of tree
    :param alpha: parameter in alpha_beta pruning
    :param beta: parameter in alpha_beta pruning
    :param maximizing: to maximize or not
    :return: [value, best result board, best exec_move]
    """
    global nodes
    nodes += 1
    boards = []
    choices = []

    for x in range(8):
        for y in range(8):
            if valid(board.array, board.player, x, y):
                test = board.move(node, x, y)
                boards.append(test)
                choices.append([x, y])

    if dep == 0 or len(choices) == 0:
        return [final_heuristic(node,maximizing), node]

    if maximizing:
        v = -float("inf")
        best_board = []
        best_choice = []
        for b in boards:
            board_value = alpha_beta(board, b, dep - 1, alpha, beta, 0)[0]
            if board_value > v:
                v = board_value
                best_board = b
                best_choice = choices[boards.index(b)]
            alpha = max(alpha, v)
            if beta <= alpha:
                break
        return [v, best_board, best_choice]
    else:
        v = float("inf")
        best_board = []
        best_choice = []
        for b in boards:
            board_value = alpha_beta(board, b, dep - 1, alpha, beta, 1)[0]
            if board_value < v:
                v = board_value
                best_board = b
                best_choice = choices[boards.index(b)]
            beta = min(beta, v)
            if beta <= alpha:
                break
        return [v, best_board, best_choice]

