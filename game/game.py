import numpy as np
from matplotlib import pyplot as plt
import sys
import time
import copy
from pathlib import Path
base_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_dir)
from args.args import *
from utils.utils import check_column, check_row, check_principal_diagonal, check_sub_diagonal
from utils.utils import check_empty_position


class Golang():

    def __init__(self, initial_board=None, next_turn=1, need_render=False):
        """create a new game starting from a inital situation
        :param initial_board: situation which the new game starts from
        :param next_turn: 1 denotes black, -1 denotes white
        :param need_render: if need_render == False, store selected positions.
        """
        assert next_turn in (1, -1)
        self.next_turn = next_turn
        if initial_board is not None:
            self.board_matrix = copy.deepcopy(initial_board)
        else:
            self.board_matrix = np.zeros((BOARD_LEN, BOARD_LEN), dtype=np.int8)
        self.step = 0
        self.need_render = need_render
        self.end = False
        if need_render:
            self.black_moves_row = []
            self.black_moves_col = []
            self.white_moves_row = []
            self.white_moves_col = []
            plt.ion
            self.fig, self.ax = plt.subplots(1, 1)


    def make_move(self, pos):
        assert self.board_matrix[pos[0]][pos[1]] == 0
        self.board_matrix[pos[0]][pos[1]] = 1 if self.next_turn == 1 else -1
        if self.need_render:
            if self.next_turn == 1:
                self.black_moves_row.append(pos[0])
                self.black_moves_col.append(pos[1])
            else:
                self.white_moves_row.append(pos[0])
                self.white_moves_col.append(pos[1])
        self.next_turn = -self.next_turn
        self.step += 1
        self.end, winner = self.judge(self.board_matrix, pos)
        return self.end, winner
        
    def judge(self, board_matrix, pos):
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



    def render(self, stay_time=1):
        assert self.need_render == True
        vlines = np.linspace(0, BOARD_LEN-1, BOARD_LEN)
        hlines = np.linspace(0, BOARD_LEN-1, BOARD_LEN)
        self.ax.hlines(hlines, min(vlines), max(vlines), colors='.25', linewidth=.75)
        self.ax.vlines(vlines, min(hlines), max(hlines), colors='.25', linewidth=.75)
        if len(self.black_moves_col) > 0:
            self.ax.scatter(self.black_moves_col, self.black_moves_row,
                c='k', s=200*12/(BOARD_LEN-1), linewidths=1, edgecolors='k', zorder=128)
        if len(self.white_moves_col) > 0:
            self.ax.scatter(self.white_moves_col, self.white_moves_row,
                c='w', s=200*12/(BOARD_LEN-1), linewidths=1, edgecolors='k', zorder=128)
        time.sleep(stay_time)
        plt.pause(0.1)
        if self.end: plt.close()
    
    


    

    








