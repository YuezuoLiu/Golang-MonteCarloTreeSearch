import numpy as np
import sys
from pathlib import Path
from matplotlib import pyplot as plt
import time
base_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_dir)
from args.args import *



def check_column(board_matrix, pos):
    count = i = 0
    row, col = pos
    while i < BOARD_LEN - 1 and count < WIN_N - 1:
        if board_matrix[row][i] != 0 and board_matrix[row][i] == board_matrix[row][i+1]:
            count += 1
        else: count = 0
        i += 1
    if count == WIN_N - 1: return True
    else: return False

def check_row(board_matrix, pos):
    count = i = 0
    row, col = pos
    while i < BOARD_LEN - 1 and count < WIN_N - 1:
        if board_matrix[i][col] != 0 and board_matrix[i][col] == board_matrix[i+1][col]:
            count += 1
        else: count = 0
        i += 1
    if count == WIN_N - 1: return True
    else: return False

def check_principal_diagonal(board_matrix, pos):
    count = i = 0
    row, col = pos
    row_ = row - min(row, col)
    col_ = col - min(row, col)
    while i+row_ < BOARD_LEN-1 and i+col_ < BOARD_LEN-1 and count < WIN_N-1:
        if board_matrix[i+row_][i+col_] != 0 and\
                board_matrix[i+row_+1][i+col_+1] == board_matrix[i+row_][i+col_]:
            count += 1
        else: count = 0
        i += 1
    if count == WIN_N - 1: return True
    else: return False

def check_sub_diagonal(board_matrix, pos):
    count = i = 0
    row, col = pos
    while col > 0 and row < BOARD_LEN - 1: # 沿对角线移动到坐下角,再斜着统计
        row += 1
        col -= 1
    while row-i-1 > 0 and i+col+1 < BOARD_LEN and count < WIN_N - 1:
        if board_matrix[row-i][i+col] != 0 and\
                board_matrix[row-i-1][col+i+1] == board_matrix[-i+row][i+col]:
            count += 1
        else: count = 0
        i += 1
    if count == WIN_N - 1: return True
    else: return False

def check_empty_position(board_matrix):
    for i in range(BOARD_LEN):
        for j in range(BOARD_LEN):
            if board_matrix[i][j] == 0:
                return True
    return False


def judge(board_matrix, pos):
    """judge if a player wins by taking a move at pos
    param board_matrix: a board_matrix denoting the real-time game situation
    param pos: position of the last move
    return: returns the judge result and the winner in [-1 or 1, or 0] where 0 denotes a draw
    """
    if check_column(board_matrix, pos) or check_row(board_matrix, pos)\
            or check_principal_diagonal(board_matrix, pos) or check_sub_diagonal(board_matrix, pos):
        return True, board_matrix[pos[0]][pos[1]]
    elif check_empty_position(board_matrix) == False:     # no empty position left, ends in a draw.
        return True, 0
    else:
        return False, None



def draw_lines_and_pieces(ax, board_len, bmr, bmc, wmr, wmc):
    vlines = np.linspace(0, board_len-1, board_len)
    hlines = np.linspace(0, board_len-1, board_len)
    ax.hlines(hlines, min(vlines), max(vlines), colors='.25', linewidth=.75)
    ax.vlines(vlines, min(hlines), max(hlines), colors='.25', linewidth=.75)
    if len(bmc) > 0:
        ax.scatter(bmc, bmr,
            c='k', s=200*12/(board_len-1), linewidths=1, edgecolors='k', zorder=128)
    if len(wmr) > 0:
        ax.scatter(wmc, wmr,
            c='w', s=200*12/(board_len-1), linewidths=1, edgecolors='k', zorder=128)


def render_board_matrix(board_matrix, stay_time):
        plt.ion
        fig, ax = plt.subplots(1, 1)
        black_moves_row = []
        black_moves_col = []
        white_moves_row = []
        white_moves_col = []
        for i in range(board_matrix.shape[0]):
            for j in range(board_matrix.shape[1]):
                if board_matrix[i][j] == 1:
                    black_moves_row.append(i); black_moves_col.append(j)
                elif board_matrix[i][j] == -1:
                    white_moves_row.append(i); white_moves_col.append(j)
        draw_lines_and_pieces(ax, black_moves_row, black_moves_col, white_moves_row, white_moves_col)
        time.sleep(1)
        plt.pause(stay_time)
        plt.close()


def save_move_positions(move_positions, file_name):
    f = open(file_name, 'a')
    line = []
    for move_position in move_positions:
        line.append(str(move_position[0]) + ' ' + str(move_position[1]) + ' ' + str(move_position[2]))
    line = ','.join(line) + '\n'
    f.write(line)
    f.close()


def show_saved_game(file_name, board_len=BOARD_LEN, stay_time=1):
    file = open(file_name, 'r')
    move_positions = file.readline().split(',')
    plt.ion
    fig, ax = plt.subplots(1, 1)
    black_moves_row = []
    black_moves_col = []
    white_moves_row = []
    white_moves_col = []
    for move in move_positions:
        move = move.split(' ')
        if move[2] == '1':
            black_moves_row.append(int(move[0]))
            black_moves_col.append(int(move[1]))
        else:
            white_moves_row.append(int(move[0]))
            white_moves_col.append(int(move[1]))
        draw_lines_and_pieces(ax, board_len, black_moves_row, black_moves_col, white_moves_row, white_moves_col)

        time.sleep(1)
        plt.pause(stay_time)
    plt.close()


def save_board_matrix(board_matrix, file_name):
    file = open(file_name, 'a')
    line = ''
    for i in range(board_matrix.shape[0]):
        row = []
        for j in range(board_matrix.shape[1]):
            row.append(str(board_matrix[i][j]))
        row = ' '.join(row) + 'j'
        line += row
    line += '\n'
    file.write(line)
    file.close()



if __name__ == '__main__':
    board = np.array([[-1,  0,  0, -1, -1,  0,  0,  0],
                        [ 0, -1,  1,  1,  1, -1,  0,  0],
                        [ 0,  0, -1, -1,  1,  1,  0,  0],
                        [ 0,  0,  1, -1, -1, -1,  1,  0],
                        [ 0,  1,  1,  1, -1, -1,  1,  0],
                        [ 0, -1,  1, -1,  1,  0,  1,  0],
                        [ 0,  1,  1,  1, -1, -1,  1,  0],
                        [ 0,  0, -1,  0, -1,  0,  0,  0]], np.int8)

    render_board_matrix(board, stay_time=100)
    








