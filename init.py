# -*- coding: utf-8 -*-
# created by avartialu@gmail.com on 2017/4/8
from tkinter import *

# Tkinter setup
Root = Tk()
screen = Canvas(Root, width=500, height=600, background="#222", highlightthickness=0)
screen.pack()

# Variable setup for minimax
nodes = 0
# max tree depth
# depth = 5
# total moves
moves = 0

# Variable setup for monte carlo
valid_table = {}
# Variables for distributed monte carlo
k = 1
m = 1
