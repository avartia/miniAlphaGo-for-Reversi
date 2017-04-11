# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/8
from datetime import *
from random import choice
from Logic.logic import *
from math import log, sqrt


class MonteCarloTreeSearch(object):
    """
    Monte Carlo Tree Search
    """
    def __init__(self, board, **kwargs):
        """
        :param board: GUI.Board
        :param kwargs
        time_limit: 每一步的时间限制，默认为10s。
        max_moves: 最多步数，默认60
        Cp: parameter for MCTS
        """
        self.board = board
        self.time_limit = timedelta(seconds=kwargs.get("time_limit", 10))
        self.states = []
        self.max_moves = kwargs.get('max_moves', 60)
        self.wins = {}
        self.plays = {}
        self.max_depth = 0
        self.Cp = kwargs.get('Cp', 1.414)

    def update(self, board):
        """
        append board to history
        :param board: GUI.Board
        :return:
        """
        self.board = board
        self.states.append(board.array)
        self.wins = {}
        self.plays = {}
        self.max_depth = 0

    def play(self):
        """
        calculate the best move. Keep simulation until time out.
        :return: a move [x, y] maximizing winning percentage
        """
        # tree depth
        self.max_depth = 0
        state = self.states[-1]
        cur_player = self.board.player
        valid_moves = get_valid_moves(state, cur_player)

        # special case
        if len(valid_moves) == 0:
            return
        if len(valid_moves) == 1:
            return valid_moves[0]

        # count of simulation
        count = 0

        start_time = datetime.utcnow()
        while datetime.utcnow() - start_time < self.time_limit:
            self.simulation()
            count += 1

        moves_states = [(p, move(state, cur_player, p[0], p[1])) for p in valid_moves]

        print("Num of Simulations: {} \n Time played:{}".format(count, datetime.utcnow() - start_time))

        # choose the move with max win percent
        percent_win, win_move = max(
            (
                self.wins.get((cur_player, str(s)), 0) / self.plays.get((cur_player, str(s)), 1), p
            )
            for p, s in moves_states
        )
        print("Maximum depth searched: {} \n Max percent of winning:{}".format(self.max_depth, percent_win))

        return win_move

    def simulation(self):
        """
        play randomly from the current position and then updates the statistics tables
        :return:
        """
        plays, wins = self.plays, self.wins

        visited_states = set()
        copy_states = self.states[:]
        copy_board = self.board
        state = copy_states[-1]
        cur_player = copy_board.player
        winner = 0

        expand = True
        for t in range(1, self.max_moves + 1):
            valid_moves = get_valid_moves(state, cur_player)
            moves_states = [(p, move(state, cur_player, p[0], p[1])) for p in valid_moves]

            # 如果所有的valid move信息已经在 plays 字典中
            # fully expanded => return the best child
            if all(plays.get((cur_player, str(s))) for p, s in moves_states):
                log_total = log(sum(plays[(cur_player, str(s))] for p, s in moves_states))
                value, chosen_move, state = max(
                    ((wins[(cur_player, str(s))] / plays[(cur_player, str(s))] +
                      self.Cp * sqrt(log_total / plays[(cur_player, str(s))]), p, s)
                     for p, s in moves_states
                     )
                )
            else:
                # select randomly from valid moves
                chosen_move, state = choice(moves_states)

            copy_states.append(state)
            # if state is not fully expanded
            if expand and (cur_player, str(state)) not in plays:
                expand = False
                wins[(cur_player, str(state))] = 0
                plays[(cur_player, str(state))] = 0
                if t > self.max_depth:
                    self.max_depth += 1
                # 简单比较
                winner = (dumb_score(state, 1) > 0)

            visited_states.add((cur_player, str(state)))
            # 0 player 1 AI

            cur_player = 1 - cur_player
            if not expand:
                break

        # backup
        for player, state in visited_states:
            s = str(state)
            if (player, s) not in self.plays:
                continue
            self.plays[(player, s)] += 1
            if player == winner:
                self.wins[(player, s)] += 1
