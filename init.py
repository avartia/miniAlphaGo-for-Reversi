# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/8
from tkinter import *

# Tkinter setup
root = Tk()
screen = Canvas(root, width=500, height=600, background="#222", highlightthickness=0)
screen.pack()

# Variable setup for minimax
nodes = 0
# max tree depth
depth = 6
# total moves
moves = 0
