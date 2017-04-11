# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/7
from time import *
import numpy as np
from AI.monte_carlo import *


class Board:
    """
    A chess board class that handles GUI.
    """
    def __init__(self, player=0):
        """
        (0 is white and player, 1 is black and computer)
        :param player: 0 or 1
        """
        self.player = player
        self.passed = False
        self.over = False
        # Initializing an empty board
        self.array = []
        for x in range(8):
            self.array.append([])
            for y in range(8):
                self.array[x].append(None)

        # Initializing center values
        self.array[3][3] = "w"
        self.array[3][4] = "b"
        self.array[4][3] = "b"
        self.array[4][4] = "w"
        self.array = tuple(self.array)

        # Initializing old values
        self.old_array = self.array

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
                if self.old_array[x][y] == "w":
                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#aaa", outline="#aaa")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#fff", outline="#fff")

                elif self.old_array[x][y] == "b":
                    screen.create_oval(54 + 50 * x, 54 + 50 * y, 96 + 50 * x, 96 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#000", outline="#000")
                    screen.create_oval(54 + 50 * x, 52 + 50 * y, 96 + 50 * x, 94 + 50 * y,
                                       tags="tile {0}-{1}".format(x, y), fill="#111", outline="#111")
        # Animation of new tiles
        screen.update()
        for x in range(8):
            for y in range(8):
                # could replace the circles with images later
                if self.array[x][y] != self.old_array[x][y] and self.array[x][y] == "w":
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

                elif self.array[x][y] != self.old_array[x][y] and self.array[x][y] == "b":
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
                if self.player == 0:
                    if valid(self.array, self.player, x, y):
                        screen.create_oval(68 + 50 * x, 68 + 50 * y, 32 + 50 * (x + 1), 32 + 50 * (y + 1),
                                           tags="highlight", fill="#008000", outline="#008000")

        if not self.over:
            # Draw the scoreboard and update the screen
            self.draw_score_board()
            screen.update()
            # If the computer is AI, make a move
            if self.player == 1:
                start_time = datetime.utcnow()
                mcts_move = self.MCTS.play()
                self.board_move(mcts_move[0], mcts_move[1])
                delta_time = datetime.utcnow() - start_time
                print("Time used for this step: {} ".format(delta_time))
        else:
            black_cnt = 0
            white_cnt = 0
            for i in self.array:
                for j in i:
                    if j == 'b':
                        black_cnt += 1
                    if j == 'w':
                        white_cnt += 1
            if white_cnt > black_cnt:
                screen.create_text(250, 550, anchor="c", font=("Consolas", 15), text="You Win!")
            elif white_cnt == black_cnt:
                screen.create_text(250, 550, anchor="c", font=("Consolas", 15), text="Tie!")
            else:
                screen.create_text(250, 550, anchor="c", font=("Consolas", 15), text="You Lose!")

    # Moves to position
    def board_move(self, x, y):
        """
        perform a board move.
        :param x: index of move
        :param y: index of move
        :return:
        """
        global nodes
        # Move and update screen
        self.old_array = self.array
        self.old_array[x][y] = "w"
        self.array = move(self.array, self.player, x, y)
        self.MCTS.update(self)

        # Switch Player
        self.player = 1 - self.player
        self.update()

        # Check if ai must pass
        self.pass_test()
        self.update()

    def draw_score_board(self):
        """
        METHOD: Draws scoreboard to screen
        :return:
        """
        global moves
        # Deleting prior score elements
        screen.delete("score")

        # Scoring based on number of tiles
        player_score = 0
        computer_score = 0
        for x in range(8):
            for y in range(8):
                if self.array[x][y] == "w":
                    player_score += 1
                elif self.array[x][y] == "b":
                    computer_score += 1

        if self.player == 0:
            player_color = "green"
            computer_color = "gray"
        else:
            player_color = "gray"
            computer_color = "green"

        screen.create_oval(5, 540, 25, 560, fill=player_color, outline=player_color)
        screen.create_oval(380, 540, 400, 560, fill=computer_color, outline=computer_color)

        # Pushing text to screen
        screen.create_text(30, 550, anchor="w", tags="score", font=("Consolas", 50), fill="white", text=player_score)
        screen.create_text(400, 550, anchor="w", tags="score", font=("Consolas", 50), fill="black", text=computer_score)

        moves = player_score + computer_score

    def pass_test(self):
        """
        METHOD: Test if player must pass: if they do, switch the player
        :return:
        """
        must_pass = True
        for x in range(8):
            for y in range(8):
                if valid(self.array, self.player, x, y):
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