import sys
from pathlib import Path
base_dir = str(Path(__file__).resolve().parent)
sys.path.append(base_dir)
from game.game import Golang
from policy.bot import select_bot_move
from args.args import *
from utils.utils import save_board_matrix, save_move_positions



for game in range(10):
    new_game = Golang(need_render=True)
    bot_move = select_bot_move(new_game.board_matrix, True, player=new_game.next_turn, coeff=0)
    step = 0
    move_positions = []
    save_dir = './results/bot_vs_bot/({}*{})-{}win-game{}.txt'\
            .format(BOARD_LEN, BOARD_LEN, WIN_N, game)
    #save_board_matrix(new_game.board_matrix, save_dir)

    while True:
        # print('step {}'.format(i))
        move_positions.append((bot_move[0], bot_move[1], new_game.next_turn))
        end, winner = new_game.make_move(bot_move)
        if new_game.need_render == True:
            new_game.render()
        #save_board_matrix(new_game.board_matrix, save_dir)
        if end:
            winner_str = 'black' if winner == 1 else 'white'
            new_game.render(stay_time=10)
            print('winner: {}, total_step: {}'.format(winner_str, step))
            print(new_game.board_matrix)
            save_move_positions(move_positions, save_dir)
            break

        bot_move = select_bot_move(new_game.board_matrix, False, player=new_game.next_turn, coeff=0)
        step += 1
