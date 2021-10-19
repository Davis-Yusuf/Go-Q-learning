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


# Referenced readInput function from read.py
def get_board(file='input.txt'):  # method for my player to read the input provided by host
    lines = open(file, 'r')  # Gets the lines from the input.txt file
    curr_player = lines.readline().rstrip('\n')  # Gets the player in play from the first line of input
    next_lines = lines.readlines()  # read the next lines
    previous_board = [[int(x) for x in i.rstrip()] for i in next_lines[0: 5]]  # constructs previous board from lines 2-6
    current_board = [[int(x) for x in i.rstrip()] for i in next_lines[5: 10]]  # constructs current board from lines 7-11

    return int(curr_player), previous_board, current_board
    # Referenced readInput function from read.py


    # Referenced writeOutput function from write.py
def write(coordinates, file='output.txt'):  # method for my player to write the location to play for the host
    output = open(file, 'w')  # opens a file output.txt to write
    if coordinates == "PASS":  # if the player passes, we write pass
        output.write("PASS")
    else:
        output.write(str(coordinates[0]) + ',' + str(coordinates[1]))  # else we write the coordinates to play
    # Referenced writeOutput function from write.py


    # Referenced writeOutput function from write.py
def compare(board):  # method for my player to write the location to play for the host
    for i in range(5):
        for j in range(5):
            if prev_board[i][j] != board[i][j]:
                return False
    return True
    # Referenced writeOutput function from write.py


    # Referenced detect_neighbor_ally function from host.py
def get_adjacent_pieces(i, j):
    adjacent = []
    if i <= 3:
        adjacent.append((i + 1, j))
    if j <= 3:
        adjacent.append((i, j + 1))
    if i >= 1:
        adjacent.append((i - 1, j))
    if j >= 1:
        adjacent.append((i, j - 1))

    return adjacent
    # Referenced detect_neighbor_ally function from host.py


    # Referenced detect_neighbor_ally function from host.py
def get_connected_pieces(board, i, j):
    connected_pieces = []
    adjacent = get_adjacent_pieces(i, j)
    for curr_piece in adjacent:
        if board[i][j] == board[curr_piece[0]][curr_piece[1]]:
            connected_pieces.append(curr_piece)
    return connected_pieces
    # Referenced detect_neighbor_ally function from host.py


def has_liberty(board, i, j):
    all_connected_pieces = []
    search = [(i, j)]
    while search:
        curr_player = search.pop()
        all_connected_pieces.append(curr_player)
        adjacent_pieces = get_connected_pieces(board, curr_player[0], curr_player[1])
        for curr_piece in adjacent_pieces:
            if curr_piece not in all_connected_pieces and curr_piece not in search:
                search.append(curr_piece)

    for curr_piece in all_connected_pieces:
        neighbors = get_adjacent_pieces(curr_piece[0], curr_piece[1])
        for neighbor in neighbors:
            if board[neighbor[0]][neighbor[1]] == 0:
                return True

    return False


def get_new_board(board, opp_player):
    bad_pieces = []
    for i in range(5):
        for j in range(5):
            if board[i][j] == opp_player:
                if not has_liberty(i, j):
                    bad_pieces.append((i, j))

    if not bad_pieces:
        return board, True
    for curr_piece in bad_pieces:
        board[curr_piece[0]][curr_piece[1]] = 0
    return board, False


def legal_move(board, i, j, player):
    if player:
        curr_player = 1
    else:
        curr_player = 2

    if i > 4 or i < 0 or j > 4 or j < 0:
        return False

    if board[i][j] == 1 or board[i][j] == 2:
        return False

    board[i][j] = curr_player

    if has_liberty(board, i, j):
        return True

    new_board, flag = get_new_board(board, 3 - curr_player)

    if not has_liberty(new_board, i, j):
        return False
    else:
        if flag is False and compare(new_board):
            return False
    return True


def get_score(player, board):                             #TIME CAN BE IMPROVED without the ????
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
                    if legal_move(board, i, j, max_player):
                        board[i][j] = 1
                        val = max(val, self.minimax_decision(board, depth - 1, alpha, beta, False))
                        board[i][j] = 0
                        if val >= beta:
                            break
                        alpha = max(alpha, val)
            return val
        else:
            val = math.inf
            for i in range(0, 5):
                for j in range(0, 5):
                    if legal_move(board, i, j, False):
                        board[i][j] = 2
                        val = min(val, self.minimax_decision(board, depth - 1, alpha, beta, True))
                        board[i][j] = 0
                        if val <= alpha:
                            break
                        beta = min(beta, val)
            return val


if __name__ == "__main__":
    piece, prev_board, curr_board = get_board()
    go = game
    go.check_game(piece, prev_board, curr_board)
    # write(action)
