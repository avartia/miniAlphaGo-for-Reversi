# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/8
from datetime import *
from math import log, sqrt
from multiprocessing.dummy import Pool as ThreadPool
from random import choice
from Strategy.strategy import *
from Logic.logic import *


class Node(object):
    """
    A node of tree.
    """
    def __init__(self, state, player, depth, parent=None, pre_move=None):
        """
        :param state: 8x8 matrix
        :param player: current player
        :param depth: depth in the tree
        :param parent: parent
        :param pre_move: last_move
        """
        self.player = player
        self.state = state
        self.parent = parent
        self.children = []
        self.depth = depth
        self.pre_move = pre_move
        self.remain_valid_moves = valid.get_valid_moves(self.state, self.player)
        self.N = 0
        self.Q = 0
        self.start_time = None

    def add_child(self, choose_move):
        """
        add a child.
        :param choose_move: 8x8 matrix
        :return:
        """
        self.remain_valid_moves.remove(choose_move)
        child = Node(exec_move(self.state, self.player, choose_move[0], choose_move[1]),
                     1 - self.player, self.depth + 1, self, choose_move)
        self.children.append(child)

    def fully_expandable(self):
        """
        whether fully expandable
        :return:
        """
        return len(self.remain_valid_moves) == 0

    def terminal(self):
        """
        whether in terminal state
        :return: True or False
        """
        return len(self.remain_valid_moves) == 0 and len(self.children) == 0

    def __str__(self):
        return "state:{}\n depth:{}".format(self.state, self.depth)


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
        self.max_moves = kwargs.get('max_moves', 60)
        self.max_depth = 0
        self.Cp = kwargs.get('Cp', 1.414)
        self.root = None
        self.default_time = timedelta(seconds=0)
        self.start_time = None
        self.definite_count = [0, 0]

    def update(self, board):
        """
        append board to history
        :param board: GUI.Board
        :return:
        """
        self.board = board
        self.root = Node(board.array, board.player, 0)
        self.max_depth = 0
        self.default_time = timedelta(seconds=0)
        self.definite_count = [get_definite_count(self.board.array, p) for p in [0, 1]]

    def tree_policy(self, node):
        """
        TREEPOLICY
        :param node: Node
        :return:
        """
        while not node.terminal():
            if node.fully_expandable():
                value, node = self.best_child(node, self.Cp)
            else:
                return self.expand(node)
        return node

    def best_child(self, node, c):
        """
        return the best child.
        :param node: Node
        :param c: constant
        :return: [value, child]
        """
        child_value = [1 - child.Q / child.N + c*sqrt(log(node.N) / child.N) for child in node.children]
        value = max(child_value)
        idx = child_value.index(value)
        return value, node.children[idx]

    def expand(self, node):
        """
        expand node
        :param node: Node
        :return: expanded node
        """
        chosen_move = choice(node.remain_valid_moves)
        node.add_child(chosen_move)
        if node.children[-1].depth > self.max_depth:
            self.max_depth = node.children[-1].depth
        return node.children[-1]

    def default_policy(self, node):
        """
        randomly choose child until terminate
        :param node: Node
        :return: reward
        """
        cur_player = node.player
        state = deepcopy(node.state)

        num_moves = 0
        while num_moves < 60:
            valid_moves = valid.get_valid_moves(state, cur_player)
            if len(valid_moves) == 0:
                cur_player = 1 - cur_player
                valid_moves = valid.get_valid_moves(state, cur_player)
                if len(valid_moves) == 0:
                    # terminal
                    break
            chosen_move = choice(valid_moves)
            state = valid.move(state, cur_player, chosen_move[0], chosen_move[1])
            cur_player = 1 - cur_player
            num_moves += 1
            count = get_definite_count(state, self.board.player)
            if count > self.definite_count[self.board.player]:
                return count - self.definite_count[self.board.player]
            count = get_definite_count(state, 1-self.board.player)
            if count > self.definite_count[1 - self.board.player]:
                return self.definite_count[1 - self.board.player] - count
        if dumb_score(state, self.board.player) > 0:
            return 1
        return -1

    def back_up(self, node, reward):
        """
        back up.
        :param node: Node
        :param reward: reward
        :return:
        """
        while node is not None:
            node.N += abs(reward)
            if node.player == self.board.player and reward > 0:
                node.Q += reward
            elif node.player == 1 - self.board.player and reward < 0:
                node.Q -= reward
            node = node.parent

    def uct_search(self):
        """
        uct search.
        :return: a exec_move [x, y] maximizing winning percentage
        """
        # tree depth
        self.max_depth = 0

        # count of simulation
        self.start_time = datetime.utcnow()
        count = self.mul_simulation(self.root)
        print("Num of Simulations: {} \nTime played:{}\nDefault Policy Played:{}\n".
              format(count, datetime.utcnow() - self.start_time, self.default_time))

        max_win_percent, chosen_child = self.best_child(self.root, 0)
        print("Maximum depth searched: {} \nMax percent of winning:{}".format(self.max_depth, max_win_percent))
        # print("Size of table: {}".format(len(valid_table)))
        print("{}/{}".format(self.root.Q, self.root.N))
        for child in self.root.children:
            print("{}/{}".format(child.Q, child.N))
        return chosen_child.pre_move

    def mul_simulation(self, node):
        """
        multiprocessing simulation.
        :param node: root node
        :return: count
        """
        count = 0
        while datetime.utcnow() - self.start_time < self.time_limit:
            v = self.tree_policy(node)
            reward = self.default_policy(v)
            self.back_up(v, reward)
            count += 1
            if node.fully_expandable():
                break
        pool = ThreadPool(len(node.children))
        counts = pool.map(self.simulation, node.children)
        count += sum(counts)
        return count

    def simulation(self, node):
        """
        :param node: root node
        :return: count
        """
        count = 0
        while datetime.utcnow() - self.start_time < self.time_limit:
            v = self.tree_policy(node)
            reward = self.default_policy(v)
            self.back_up(v, reward)
            count += 1
        return count

