import sys
from pathlib import Path
base_dir = str(Path(__file__).resolve().parent)
sys.path.append(base_dir)
from game.game import Golang
from policy.bot import select_bot_move
from policy.mcts import Monte_carlo_tree
from args.args import *


for game in range(50):
    new_game = Golang(need_render=True)
    bot_move = select_bot_move(new_game.board_matrix, True, player=new_game.next_turn, coeff=0)
    end, winner = new_game.make_move(bot_move) #bot black 1, mcts white -1
    mct = Monte_carlo_tree(new_game.board_matrix, new_game.next_turn, C=COEFFICIENT,\
         start_pos=bot_move)
    step = 0
    if new_game.need_render == True: new_game.render()
    while True:
        if new_game.next_turn == -1:
            mct.init_first_layer_using_bot_knowledge(BOT_INIT_TREE)
            mcts_move = mct.monte_carlo_tree_search(SIMULATE_NUM)
            print('MCTS chosen move position: ({},{})'.format(mcts_move[0], mcts_move[1]))
            mct.show_node_child_visit(mct.root)
            mct.show_node_child_win_rate(mct.root)
            end, winner = new_game.make_move(mcts_move)
            if not end:
                branch_idx = mcts_move[0] * BOARD_LEN + mcts_move[1] # inherits sub-tree
                mct.root = mct.root.childs[branch_idx]
        else:
            bot_move = select_bot_move(new_game.board_matrix, False, player=new_game.next_turn, coeff=0)
            end, winner = new_game.make_move(bot_move)
            if not end:
                branch_idx = bot_move[0] * BOARD_LEN + bot_move[1]   # inherits sub-tree
                if mct.root.childs[branch_idx] is not None:
                    mct.root = mct.root.childs[branch_idx]
                else:                                                # create a new tree
                    mct = Monte_carlo_tree(new_game.board_matrix, new_game.next_turn,\
                         C=COEFFICIENT, start_pos=bot_move)
        # print('step {}'.format(i))
        
        if new_game.need_render == True: new_game.render()
        
        if end:
            winner_str = 'black' if winner == 1 else 'white'
            new_game.render(stay_time=10)
            print('winner: {}, total_step: {}'.format(winner_str, step))
            print(new_game.board_matrix)

            # write game results to a file
            with open('./results/mcts_vs_bot-({}*{})-{}win-game-{}.txt'\
                    .format(BOARD_LEN, BOARD_LEN, WIN_N, game), 'w') as file:
                print('winner: {}, total_step: {}'.format(winner_str, step))
                print(new_game.board_matrix, file=file)
            break
        step += 1
