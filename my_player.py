import sys
import random
import timeit
import math
import argparse
from collections import Counter
from copy import deepcopy

size = 5                              # size of the game board 5x5
komi_rule = 2.5                       # storing the Komi rule: n / 2
max_steps = 24                        # max steps allowed in a 5x5 game: n * n - 1


class game:
    def __init__(self):
        self.captured = []                              # stores captured pieces
        self.B_player = True                            # set to True when the player with black pieces plays
        self.steps = 0                                  # counts the number of steps so far
        self.prev_board = []                            # stores previous go board
        self.game_board = []                            # stores current go board

    # Referenced set_board function from host.py
    def check_game(self, curr_piece, prev_board, current_board):
        if curr_piece == 1:                              # if the player with black piece plays, set it to true
            self.B_player = True
        else:
            self.B_player = False                        # else it is the player with white pieces
        for i in range(5):
            for j in range(5): # check every point of the board to see if a piece has been captured since the last round
                if current_board[i][j] == curr_piece and prev_board[i][j] != curr_piece:
                    self.captured.append((i, j))

        self.game_board = curr_board
        self.prev_board = prev_board
    # Referenced set_board function from host.py


    # # Referenced set_board function from host.py
    # def detect_neighbor(self, x, y):
    #     current_board = self.game_board
    # # Referenced set_board function from host.py
    #
    #
    # # Referenced set_board function from host.py
    # def detect_neighbor_ally(self, i, j):
    # # Referenced set_board function from host.py


# Referenced readInput function from read.py
def get_board(file='input.txt'):  # method for my player to read the input provided by host
    lines = open(file, 'r')  # Gets the lines from the input.txt file
    curr_player = lines.readline().rstrip('\n')  # Gets the player in play from the first line of input
    next_lines = lines.readlines()  # read the next lines
    prev_board = [[int(x) for x in i.rstrip()] for i in next_lines[0: 5]]  # constructs previous board from lines 2-6
    curr_board = [[int(x) for x in i.rstrip()] for i in next_lines[5: 10]]  # constructs current board from lines 7-11

    return int(curr_player), prev_board, curr_board
    # Referenced readInput function from read.py


    # Referenced writeOutput function from write.py
def write(coordinates, file='output.txt'):  # method for my player to write the location to play for the host
    output = open(file, 'w')  # opens a file output.txt to write
    if coordinates == "PASS":  # if the player passes, we write pass
        output.write("PASS")
    else:
        output.write(str(coordinates[0]) + ',' + str(coordinates[1]))  # else we write the coordinates to play
    # Referenced writeOutput function from write.py


def legal_move(i , j, player):
    if i > 4 or i < 0 or j > 4 or j < 0:
        return False


def get_score(player, board):                             #TIME CAN BE IMPROVED????
    b_points = 0
    w_points = 0

    for i in range(5):
        for j in range(5):
            if board[i][j] == 1 and player:
                b_points += 1
            if board[i][j] == 2 and not player:
                w_points += 1

    if player:
        return b_points
    else:
        return w_points

class AlphaBeta:

    def minimax_decision(self, board, depth, alpha, beta, max_player):
        if depth == 0:    # or terminal(board):
            return get_score(max_player, board)
        if max_player:
            val = -math.inf
            for i in range(0, 5):
                for j in range(0, 5):
                    if legal_move(i, j, max_player):            #QUESTION: DO WE MAKE A COPY OF BOARD
                        board[i][j] = 1
                        val = max(val, self.minimax_decision(board, depth - 1, alpha, beta, False))
                        if val >= beta:
                            break
                        alpha = max(alpha, val)
            return val
        else:
            val = math.inf
            for i in range(0, 5):
                for j in range(0, 5):
                    if legal_move(i, j, False):            #QUESTION: DO WE MAKE A COPY OF BOARD
                        board[i][j] = 2
                        val = min(val, self.minimax_decision(board, depth - 1, alpha, beta, True))
                        if val <= alpha:
                            break
                        beta = min(beta, val)
            return val


if __name__ == "__main__":
    piece, prev_board, curr_board = get_board()
    go = game
    go.check_game(piece, prev_board, curr_board)
    player = AlphaBeta()
    action = player.get_input(go, piece)
    write(action)
