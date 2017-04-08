# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/7
from copy import deepcopy
from time import *
from AI.minimax import *


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

        # Initializing old values
        self.old_array = self.array

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
                start_time = time()
                self.old_array = self.array
                alpha_beta_result = alpha_beta(self, self.array, depth, -float("inf"), float("inf"), 1)
                self.array = alpha_beta_result[1]

                if len(alpha_beta_result) == 3:
                    position = alpha_beta_result[2]
                    self.old_array[position[0]][position[1]] = "b"

                self.player = 1 - self.player
                delta_time = round((time() - start_time) * 100) / 100
                print(delta_time)
                # reset the nodes
                nodes = 0
                # Player must pass?
                self.pass_test()
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

    def move(self, passed_array, x, y):
        """
        FUNCTION: Returns a board after making a move according to Othello rules
        Assumes the move is valid
        :param passed_array: 8x8 matrix
        :param x: index of the last move
        :param y: index of the last move
        :return: 8x8 matrix
        """
        # Must copy the passedArray so we don't alter the original
        array = deepcopy(passed_array)
        # Set color and set the moved location to be that color
        if self.player == 0:
            color = "w"
        else:
            color = "b"
        array[x][y] = color

        # Determining the neighbours to the square
        neighbours = []
        for i in range(max(0, x - 1), min(x + 2, 8)):
            for j in range(max(0, y - 1), min(y + 2, 8)):
                if array[i][j] is not None:
                    neighbours.append([i, j])

        # Which tiles to convert
        convert = []

        # For all the generated neighbours, determine if they form a line
        # If a line is formed, we will add it to the convert array
        for neighbour in neighbours:
            neigh_x = neighbour[0]
            neigh_y = neighbour[1]
            # Check if the neighbour is of a different color - it must be to form a line
            if array[neigh_x][neigh_y] != color:
                # The path of each individual line
                path = []

                # Determining direction to move
                delta_x = neigh_x - x
                delta_y = neigh_y - y

                temp_x = neigh_x
                temp_y = neigh_y

                # While we are in the bounds of the board
                while 0 <= temp_x <= 7 and 0 <= temp_y <= 7:
                    path.append([temp_x, temp_y])
                    value = array[temp_x][temp_y]
                    # If we reach a blank tile, we're done and there's no line
                    if value is None:
                        break
                    # If we reach a tile of the player's color, a line is formed
                    if value == color:
                        # Append all of our path nodes to the convert array
                        for node in path:
                            convert.append(node)
                        break
                    # Move the tile
                    temp_x += delta_x
                    temp_y += delta_y

        # Convert all the appropriate tiles
        for node in convert:
            array[node[0]][node[1]] = color

        return array

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
        self.array = self.move(self.array, x, y)

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

