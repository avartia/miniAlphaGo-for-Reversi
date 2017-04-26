# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/7
from time import *

from AI.monte_carlo import *


class Board:
    """
    A chess board class that handles GUI.
    """
    def __init__(self, AIplayer=1):
        """
        (0 is white and player, 1 is black and computer)
        :param player: 0 or 1
        """
        self.player = 1
        self.AIPlayer = AIplayer
        self.passed = False
        self.over = False
        # Initializing an empty board
        self.array = []
        for x in range(8):
            self.array.append([])
            for y in range(8):
                self.array[x].append(None)
        # time
        self.AI_single_time = timedelta(seconds=0)
        self.AI_total_time = timedelta(seconds=0)
        self.player_single_time = timedelta(seconds=0)
        self.player_total_time = timedelta(seconds=0)
        self.end_time = datetime.utcnow()
        # Initializing center values
        self.array[3][3] = 0
        self.array[3][4] = 1
        self.array[4][3] = 1
        self.array[4][4] = 0
        self.array = tuple(self.array)

        # Initializing old values
        self.old_array = self.array

        self.last_array = self.array

        # MCTS
        self.MCTS = MonteCarloTreeSearch(self)
        self.MCTS.update(board=self)
        # update
        self.update()

    def update(self):
        """
        Updating the board to the screen
        :return:
        """
        screen.delete("highlight")
        screen.delete("tile")
        for x in range(8):
            for y in range(8):
                # Could replace the circles with images later, if I want
                if self.old_array[x][y] == 0:
                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#aaa", outline="#aaa")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#fff", outline="#fff")

                elif self.old_array[x][y] == 1:
                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#000", outline="#000")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#111", outline="#111")
        # Animation of new tiles
        screen.update()
        for x in range(8):
            for y in range(8):
                # could replace the circles with images later
                if self.array[x][y] != self.old_array[x][y] and self.array[x][y] == 0:
                    screen.delete("{0}-{1}".format(x, y))
                    # 42 is width of tile so 21 is half of that
                    # Shrinking 收缩效果
                    for i in range(21):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                           tags="tile animated", fill="#000", outline="#000")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                           tags="tile animated", fill="#111", outline="#111")
                        if i % 3 == 0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    # Growing 放大效果
                    for i in reversed(range(21)):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                           tags="tile animated", fill="#aaa", outline="#aaa")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                           tags="tile animated", fill="#fff", outline="#fff")
                        if i % 3 == 0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, tags="tile", fill="#aaa",
                                       outline="#aaa")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, tags="tile", fill="#fff",
                                       outline="#fff")
                    screen.update()

                elif self.array[x][y] != self.old_array[x][y] and self.array[x][y] == 1:
                    screen.delete("{0}-{1}".format(x, y))
                    # 42 is width of tile so 21 is half of that
                    # Shrinking
                    for i in range(21):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                           tags="tile animated", fill="#aaa", outline="#aaa")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                           tags="tile animated", fill="#fff", outline="#fff")
                        if i % 3 == 0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")
                    # Growing
                    for i in reversed(range(21)):
                        screen.create_oval(54 + i + 50 * x, 54 + i + 50 * y, 96 - i + 50 * x, 96 - i + 50 * y,
                                           tags="tile animated", fill="#000", outline="#000")
                        screen.create_oval(54 + i + 50 * x, 52 + i + 50 * y, 96 - i + 50 * x, 94 - i + 50 * y,
                                           tags="tile animated", fill="#111", outline="#111")
                        if i % 3 == 0:
                            sleep(0.01)
                        screen.update()
                        screen.delete("animated")

                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y, tags="tile", fill="#000",
                                       outline="#000")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y, tags="tile", fill="#111",
                                       outline="#111")
                    screen.update()

        # Drawing of highlight circles
        # 提示效果
        for x in range(8):
            for y in range(8):
                if self.player == 1 - self.AIPlayer:
                    if valid.valid(self.array, self.player, x, y):
                        screen.create_oval(68 + 50 * x, 68 + 50 * y, 32 + 50 * (x + 1), 32 + 50 * (y + 1),
                                           tags="highlight", fill="#008000", outline="#008000")

        if not (len(valid.get_valid_moves(self.array, self.player)) == 0 and
                        len(valid.get_valid_moves(self.array, 1 - self.player)) == 0):
            # Draw the scoreboard and update the screen
            screen.update()
            self.draw_score_board()
            # If the computer is AI, make a exec_move
            if self.player == self.AIPlayer:
                # update time
                self.player_single_time = datetime.utcnow() - self.end_time
                self.player_total_time = self.player_total_time + self.player_single_time
                self.draw_score_board()
                start_time = datetime.utcnow()
                mcts_move = self.MCTS.uct_search()
                if mcts_move is not None:
                    self.board_move(mcts_move[0], mcts_move[1])
                delta_time = datetime.utcnow() - start_time
                self.AI_single_time = delta_time
                self.AI_total_time = self.AI_total_time + self.AI_single_time
                print("Time used for this step: {} ".format(delta_time))
                self.draw_score_board()
                self.end_time = datetime.utcnow()
        else:
            black_cnt = 0
            white_cnt = 0
            for i in self.array:
                for j in i:
                    if j == self.AIPlayer:
                        black_cnt += 1
                    if j == 1-self.AIPlayer:
                        white_cnt += 1
            self.draw_score_board()
            if white_cnt > black_cnt:
                screen.create_text(250, 550, anchor="c", font=("Consolas", 15), text="You Win!")
            elif white_cnt == black_cnt:
                screen.create_text(250, 550, anchor="c", font=("Consolas", 15), text="Tie!")
            else:
                screen.create_text(250, 550, anchor="c", font=("Consolas", 15), text="You Lose!")
            if black_cnt + white_cnt == 64 or (len(valid.get_valid_moves(self.array, 0)) == 0 and len(valid.get_valid_moves(self.array, 1))):
                self.over = True

    def recover_last_move(self):
        """
        recover last move
        """
        self.array = self.last_array
        # update MCTS
        self.MCTS.update(self)

        # Check if ai must pass
        self.pass_test()
        self.update()

    # Moves to position
    def board_move(self, x, y):
        """
        perform a board exec_move.
        :param x: index of exec_move
        :param y: index of exec_move
        :return:
        """
        if self.player == 1-self.AIPlayer:
            self.last_array = deepcopy(self.array)
        # Move and update screen
        self.old_array = deepcopy(self.array)
        self.array = exec_move(self.array, self.player, x, y)
        self.old_array[x][y] = self.array[x][y]

        # Switch Player
        self.player = 1 - self.player
        # update MCTS
        self.MCTS.update(self)

        # Check if ai must pass
        self.pass_test()
        self.update()

    def draw_score_board(self):
        """
        METHOD: Draws scoreboard to screen
        :return:
        """
        # Deleting prior score elements
        screen.delete("score")

        # Scoring based on number of tiles
        player_score = 0
        computer_score = 0
        for x in range(8):
            for y in range(8):
                if self.array[x][y] == 0:
                    player_score += 1
                elif self.array[x][y] == 1:
                    computer_score += 1

        screen.create_oval(5, 540, 25, 560, fill="white", outline="white")
        screen.create_oval(420, 540, 440, 560, fill="black", outline="black")

        # Pushing text to screen
        screen.create_text(30, 550, anchor="w", tags="score", font=("Consolas", 30), fill="white", text=player_score)
        single_time_white = self.player_single_time
        total_time_white = self.player_total_time
        single_time_black = self.AI_single_time
        total_time_black = self.AI_total_time
        if self.AIPlayer == 0:
            single_time_white = self.AI_single_time
            total_time_white = self.AI_total_time
            single_time_black = self.player_single_time
            total_time_black = self.player_total_time
        screen.create_text(80, 550, anchor="w", tags="score", font=("Consolas", 20), fill="white", text=str(single_time_white.seconds // 60) + ':' + str(single_time_white.seconds % 60) + '/')
        screen.create_text(160, 550, anchor="w", tags="score", font=("Consolas", 20), fill="white",
                           text=str(total_time_white.seconds // 60) + ':' + str(total_time_white.seconds % 60))
        screen.create_text(275, 550, anchor="w", tags="score", font=("Consolas", 20), fill="black",
                           text=str(single_time_black.seconds // 60) + ':' + str(
                               single_time_black.seconds % 60) + '/')
        screen.create_text(350, 550, anchor="w", tags="score", font=("Consolas", 20), fill="black",
                           text=str(total_time_black.seconds // 60) + ':' + str(total_time_black.seconds % 60))
        screen.create_text(450, 550, anchor="w", tags="score", font=("Consolas", 30), fill="black", text=computer_score)


    def pass_test(self):
        """
        METHOD: Test if player must pass: if they do, switch the player
        :return:
        """
        must_pass = True
        for x in range(8):
            for y in range(8):
                if valid.valid(self.array, self.player, x, y):
                    must_pass = False
        if must_pass:
            self.player = 1 - self.player
            if self.passed is True:
                self.over = True
            else:
                self.passed = True
            self.update()
        else:
            self.passed = False
