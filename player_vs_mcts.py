import sys
from pathlib import Path
base_dir = str(Path(__file__).resolve().parent)
sys.path.append(base_dir)
from game.game import Golang
from policy.mcts import Monte_carlo_tree
from args.args import *
from utils.utils import save_move_positions

GAME_NUM = 1
PLAYER = 'black'  #black or white
assert PLAYER in {'black', 'white'}

player_idx = 1 if PLAYER == 'black' else -1
mcts_idx = - player_idx

for game in range(GAME_NUM):
    new_game = Golang(need_render=True)
    if new_game.need_render == True: new_game.render()
    step = 0
    move_positions = []
    save_dir = './results/player_vs_mcts/({}*{})-{}win-game{}.txt'\
            .format(BOARD_LEN, BOARD_LEN, WIN_N, game)

    #蒙特卡洛树搜索构建树提供了一个上一步落子的参数，虽然不是必须的，如果mcts后手，需要先让player获取一个输入
    if player_idx == 1:
        while True:
            pos_str = input('choose your next move (x, y), for example: 0 0  :').split()
            player_move = (int(pos_str[1]), int(pos_str[0])) #input pos is (col, row)
            if 0 <= player_move[0] < BOARD_LEN and 0 <= player_move[1] < BOARD_LEN\
                    and new_game.board_matrix[player_move[0]][player_move[1]] == 0:
                move_positions.append((player_move[0], player_move[1], new_game.next_turn))
                end, winner = new_game.make_move(player_move)
                break
            else: print('invlid position!')
        if new_game.need_render == True: new_game.render()

    mct = Monte_carlo_tree(new_game.board_matrix, new_game.next_turn, C=COEFFICIENT,start_pos=(0,0))

    while True:
        if new_game.next_turn == mcts_idx:
            mct.init_first_layer_using_bot_knowledge(BOT_INIT_TREE)
            mcts_move = mct.monte_carlo_tree_search(SIMULATE_NUM)
            print('MCTS chosen move position: ({},{})'.format(mcts_move[0], mcts_move[1]))
            mct.show_node_child_visit(mct.root)
            mct.show_node_child_win_rate(mct.root)
            move_positions.append((mcts_move[0], mcts_move[1], new_game.next_turn))
            end, winner = new_game.make_move(mcts_move)
            if not end:
                branch_idx = mcts_move[0] * BOARD_LEN + mcts_move[1] # inherits sub-tree
                mct.root = mct.root.childs[branch_idx]
        else:
            while True:  # get player move position
                pos_str = input('chose your next move (x, y), for example: 0 0  :').split()
                player_move = (int(pos_str[1]), int(pos_str[0]))  #input pos is (col, row)
                if 0 <= player_move[0] < BOARD_LEN and 0 <= player_move[1] < BOARD_LEN\
                        and new_game.board_matrix[player_move[0]][player_move[1]] == 0:
                    move_positions.append((player_move[0], player_move[1], new_game.next_turn))
                    end, winner = new_game.make_move(player_move)
                    break
                else: print('invlid position!')
                
            if not end:
                branch_idx = player_move[0] * BOARD_LEN + player_move[1]   # inherits sub-tree
                if mct.root.childs[branch_idx] is not None:
                    mct.root = mct.root.childs[branch_idx]
                else:                                                # create a new tree
                    mct = Monte_carlo_tree(new_game.board_matrix, new_game.next_turn,\
                         C=COEFFICIENT, start_pos=player_move)
        # print('step {}'.format(i))
        
        if new_game.need_render == True: new_game.render()
        
        if end:
            winner_str = 'black' if winner == 1 else 'white'
            print('winner: {}, total_step: {}'.format(winner_str, step))
            print(new_game.board_matrix)

            # write game results to a file
            save_move_positions(move_positions, save_dir)
            break
        step += 1
        