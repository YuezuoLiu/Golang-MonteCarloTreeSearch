import sys
from pathlib import Path
base_dir = str(Path(__file__).resolve().parent)
sys.path.append(base_dir)
from game.game import Golang
from policy.bot import select_bot_move
from args.args import *
from utils.utils import save_move_positions


GAME_NUM = 1
PLAYER = 'black'  #black or white
assert PLAYER in {'black', 'white'}

player_idx = 1 if PLAYER == 'black' else -1
bot_idx = - player_idx

for games in range(GAME_NUM):
    new_game = Golang(need_render=True)
    step = 0
    move_positions = []
    save_dir = './results/player_vs_bot/({}*{})-{}win-game{}.txt'
    if new_game.need_render == True:
        new_game.render()
    while True:
        if new_game.next_turn == player_idx:
            while True:
                pos_str = input('choose your next move (x, y), for example: 0 0  :').split()
                move = (int(pos_str[1]), int(pos_str[0]))   #command line input pos is (col, row)
                if 0 <= move[0] < BOARD_LEN and 0 <= move[1] < BOARD_LEN\
                        and new_game.board_matrix[move[0]][move[1]] == 0: 
                    move_positions.append((move[0], move[1], new_game.next_turn))
                    end, winner = new_game.make_move(move)
                    break
                else: print('invlid position!')
        
        else:
            move = select_bot_move(new_game.board_matrix, True, player=bot_idx, coeff=0)
            move_positions.append((move[0], move[1], new_game.next_turn))
            end, winner = new_game.make_move(move)

        if new_game.need_render == True:
            new_game.render()
        
        if end:
            winner_str = 'black' if winner == 1 else 'white'
            # new_game.render(stay_time=10)
            print('winner: {}, total_step: {}'.format(winner_str, step))
            print(new_game.board_matrix)
            save_move_positions(move_positions, save_dir)
            break

        step += 1

