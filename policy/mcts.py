import numpy as np
import sys
import math
import copy
from pathlib import Path
base_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_dir)
from args.args import *
from game.game import Golang
from policy.bot import select_bot_move
from utils.utils import render_board_matrix, judge


class Tree_node:
    def __init__(self, branch_num, board_matrix, next_player, pos, parent=None):
        # next_turn: black=1, white=-1, starting from this situation, which player makes next move
        self.next_player = next_player
        self.row = pos[0]      # pos = (row_idx, col_idx)
        self.col = pos[1]
        self.board_matrix = copy.deepcopy(board_matrix)
        self.visit_count = 0  # 这些统计量的更新放进backup的时候去了
        self.total_win = 0    # value = total_win / C
        self.childs = [None for _ in range(branch_num)]
        self.parent = parent
        

class Monte_carlo_tree():
    def __init__(self, start_board_matrix, next_player, C, start_pos):
        self.root_next_player = next_player
        self.C = C
        self.epsilon = 0.01
        self.simulate_num = 0
        self.root = Tree_node(BOARD_LEN * BOARD_LEN, start_board_matrix, next_player, start_pos)
    
    def uct(self, vi, ni, np):
        return vi + self.C * math.sqrt(math.log(np) / (ni + self.epsilon))
    
    def branch_idx_to_board_idx(self, branch_index):
        return (branch_index // BOARD_LEN, branch_index % BOARD_LEN)

    def find_unvisited_child(self, start_node):
        for idx in range(BOARD_LEN * BOARD_LEN):
            row, col = self.branch_idx_to_board_idx(idx)
            if start_node.childs[idx] == None and\
                    start_node.board_matrix[row][col] == 0:  # empty position
                return idx
        return None

    def select_next_node_in_tree(self, start_node):
        #如果当前节点已经是terminal,不用再分枝了,返回原来的start_node, 此时rollout时能直接判断结束
        #之所以加一个这步骤，因为judge的判断依赖于最后落子位置，如果在这里分枝，后续rollout judge胜负可能有误
        end, winner = judge(start_node.board_matrix, (start_node.row, start_node.col))
        if end: return True, start_node

        # if unvisited(None) childs exists, select them first, and expand the tree
        unvisited_child_idx = self.find_unvisited_child(start_node)
        if unvisited_child_idx is not None:
            traverse_end = True
            new_node = self.expand(start_node, unvisited_child_idx)
            start_node.childs[unvisited_child_idx] = new_node
            return traverse_end, new_node

        traverse_end = False
        max_uct_idx = None          
        max_uct_value = -100000      

        for idx in range(BOARD_LEN * BOARD_LEN):
            row, col = self.branch_idx_to_board_idx(idx)
            if start_node.board_matrix[row][col] == 0:   # empty position
                vi = float(start_node.childs[idx].total_win) / float(start_node.childs[idx].visit_count)
                ni = start_node.childs[idx].visit_count
                np = start_node.visit_count
                uct_value = self.uct(vi, ni, np)
                if uct_value > max_uct_value:
                    max_uct_value = uct_value
                    max_uct_idx = idx

        return traverse_end, start_node.childs[max_uct_idx]


    def expand(self, parent_node, branch_idx):
        pos = self.branch_idx_to_board_idx(branch_idx)
        new_node = Tree_node(BOARD_LEN*BOARD_LEN, parent_node.board_matrix,
             -parent_node.next_player, pos, parent_node)
        new_node.board_matrix[pos[0]][pos[1]] = parent_node.next_player
        return new_node

    def traverse_in_tree(self):
        current = self.root
        while True:
            end, current = self.select_next_node_in_tree(current)
            if end == True: return current

    def rollout(self, start_node):
        """simulates a game from the leaf node using bot policy for both players"""
        rollout_game = Golang(start_node.board_matrix, start_node.next_player, need_render=False)

        end, winner = rollout_game.judge(rollout_game.board_matrix, (start_node.row, start_node.col))
        if end: return winner

        bot_move = select_bot_move(rollout_game.board_matrix, True,\
                player=rollout_game.next_turn, coeff=0)
        step = 0
        while True:
            end, winner = rollout_game.make_move(bot_move)
            if end:
                if winner == 1: winner_str = 'black'
                elif winner == -1: winner_str = 'white'
                else: winner_str = 'draw'    
                self.simulate_num += 1
                print('MCTS rollout {} ended, winner: {}, total_step: {}'\
                    .format(self.simulate_num, winner_str, step))
                return winner
            step += 1
            bot_move = select_bot_move(rollout_game.board_matrix, False, player=rollout_game.next_turn, coeff=0)
    
    def backup(self, leaf_node, winner):
        is_win = 1 if winner == self.root_next_player else 0
        while leaf_node != None:
            if -leaf_node.next_player == winner: #-nextplayer才是当前节点代表的玩家（的动作)
                leaf_node.total_win += 1          #双方都取uct最大动作。赢得玩家节点+1,输的+0
                # print('updated node next_player: {}, pos=({},{})'\
                #     .format(leaf_node.next_player, leaf_node.row, leaf_node.col))
            # else:
            #     print('notupdated node next_player: {}'.format(leaf_node.next_player))
            leaf_node.visit_count += 1
            leaf_node = leaf_node.parent

    def tree_search_once(self):
        leaf_node = self.traverse_in_tree()
        winner = self.rollout(leaf_node)
        self.backup(leaf_node, winner)
    
    def monte_carlo_tree_search(self, total_simulate_num):
        self.simulate_num = 0
        for simulate in range(total_simulate_num):
            self.tree_search_once()
        max_visit_count = -1
        for idx in range(BOARD_LEN*BOARD_LEN):
            if self.root.childs[idx] is not None and\
                     self.root.childs[idx].visit_count > max_visit_count:
                max_visit_count = self.root.childs[idx].visit_count
                max_visit_count_idx = idx
        move_pos = self.branch_idx_to_board_idx(max_visit_count_idx)
        return move_pos
    
    
    def show_node_child_visit(self, node):
        visits = np.zeros((BOARD_LEN, BOARD_LEN), np.int32)
        for idx in range(BOARD_LEN * BOARD_LEN):
            row = idx // BOARD_LEN
            col = idx % BOARD_LEN
            if node.childs[idx] is not None:
                visits[row][col] = node.childs[idx].visit_count
        print('child_visit_count:')
        print(visits)
    
    def show_node_child_win_rate(self, node):
        visits = np.zeros((BOARD_LEN, BOARD_LEN), np.float16)
        for idx in range(BOARD_LEN * BOARD_LEN):
            row = idx // BOARD_LEN
            col = idx % BOARD_LEN
            if node.childs[idx] is not None:
                visits[row][col] = node.childs[idx].total_win / node.childs[idx].visit_count
        print('child_win_rate:')
        print(visits)

    def init_first_layer_using_bot_knowledge(self, bot_choose_num):
        # using bot knowledge to reduce searching directions
        for i in range(bot_choose_num):
            bot_choise = select_bot_move(self.root.board_matrix, False, self.root.next_player, coeff=0)
            branch_idx = bot_choise[0] * BOARD_LEN + bot_choise[1]
            if self.root.childs[branch_idx] == None:
                self.root.childs[branch_idx] =  self.expand(self.root, branch_idx)
            self.root.childs[branch_idx].visit_count += 1
            self.root.childs[branch_idx].total_win += 1


if __name__ == '__main__':
    assert BOARD_LEN == 7
    assert WIN_N == 4
    start_board = np.zeros((BOARD_LEN, BOARD_LEN), np.int8)
    start_board[3][3] = 1
    start_board[4][3] = -1
    test_board = np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0,-1, 0, 0],
                           [0, 0, 0, 1, 0, 0, 0],
                           [0, 0, 1,-1,-1, 0, 0],
                           [0, 1, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]], dtype=np.int8)

    mct = Monte_carlo_tree(test_board, next_player=1, C=COEFFICIENT, start_pos=(1,4))
    move_pos = mct.monte_carlo_tree_search(300)
    print('selected move: ', move_pos)
    mct.show_node_child_visit(mct.root)
    mct.show_node_child_win_rate(mct.root)





    
    

        





