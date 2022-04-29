import numpy as np
import sys
from pathlib import Path
base_dir = str(Path(__file__).resolve().parent.parent)
sys.path.append(base_dir)
from args.args import *


# parameters           1  2   3   4   5   6    7    8    9   10  11   12    13    14    15    16    17    18    19    20    
coeffs = [np.array([[-12, 0,-35,-15,-34,-25,-1000,-45,-1000,-30,-30,-1000,-9500,-9500,-9500,-9500,-9500,-9500,-9500,-90000],
                    [ 10, 3, 30, 15, 29, 12,  190, 55, 180,  20, 20, 4000,  140,  135,  130, 130,  200,  135,  135, 90000]]),
          
          np.array([[-15, 0,-35,-15,-34,-25,-1000,-40,-1000,-30,-30,-1000,-9500,-9500,-9500,-9500,-9500,-9500,-9500,-30000],
                    [ 10,10, 30, 15, 29, 12,  195, 50, 180,  20, 20, 4000,  140,  135,  130, 130,  200,  135,  135, 40000]])]


def select_bot_move(board_matrix, is_first_step, player, coeff):
    '''compute bot's move
    :param board_matrix: real-time situation
    :param is_first_step: if it's first step True, else False
    :param player: black = 1, white = -1
    '''
    #0:player-player, 1:PC-player, 2:player-PC, 3:PC-PC
    #global numsall
    max_score = -np.inf
    ymax = 1; xmax = 1
    # Calculate the scores at each point
    for y in range(BOARD_LEN):
        for x in range(BOARD_LEN):
            if board_matrix[y][x] == 0:
                cd = abs(y-BOARD_LEN/2+0.5) + abs(x-BOARD_LEN/2+0.5)
                if (is_first_step and cd>3)\
                     or (not is_first_step and not np.any(board_matrix[max(y-2,0):min(y+3,BOARD_LEN),max(x-2,0):min(x+3,BOARD_LEN)])):
                    score = -np.inf
                    #print("     ",end='')
                else:
                    board_matrix[y][x] = player
                    scores = score_calc(board_matrix, coeffs[coeff], player)
                    score = scores[0] - cd + np.random.randint(-6,5)    # my score in this move
                    score_opp = scores[1]    # the opponent's score in this move
                    board_matrix[y][x] = -player
                    score2 = score_calc(board_matrix, coeffs[coeff], player)[0]       # my score if the opponent take this move
                    # Treatment of 33, 34 and 44
                    if coeffs[coeff][0][12]*3<score_opp<coeffs[coeff][0][6]*0.5+coeffs[coeff][0][12]:
                        score -= coeffs[coeff][0][6]
                    if 1.5<score2/coeffs[coeff][0][6]<2.5:
                        score -= coeffs[coeff][0][6]*0.25
                    elif 1.9<score2/coeffs[coeff][0][12]<2.1 or 0.5<(score2-coeffs[coeff][0][12])/coeffs[coeff][0][6]<1.5:
                        score -= coeffs[coeff][0][6]*0.5
                    elif 0.5<score2/coeffs[coeff][0][19]<3.5:
                        score -= coeffs[coeff][0][12]
                    #print('%5d' % score,end='')
                    if max_score < score:
                        max_score = score; ymax = y; xmax = x
                    board_matrix[y][x] = 0   # recover to original board_matrix
            else: pass
                #print('  ['+'%s'%chr(21*board[y][x]+45)+']',end='')
        #print("")
    #print("B:",end='')
    #for j in range(len(numsall[0])): print('%2d'%int(numsall[0][j]),end=' ')
    #print("\nW:",end='')
    #for j in range(len(numsall[0])): print('%2d'%int(numsall[1][j]),end=' ')
    #print("")
    return ymax, xmax


def score_calc(board_matrix, coeff, player):
    '''calculate total score
    :param player: black = 1, white = -1
    '''
    assert player in (-1, 1)
    nums = np.zeros((2,len(coeffs[0][0])))  
    def one_calc(a):
        '''calculate each list'''
        l = len(a)
        a = a.tolist()
        for i in range(l-2):
            if a[i:i+3]==[0,1,0]: nums[0][0]+=1
            elif a[i:i+3]==[2,1,0] or a[i:i+3]==[0,1,2]: nums[0][1]+=1
                
            elif a[i:i+3]==[0,2,0]: nums[1][0]+=1
            elif a[i:i+3]==[1,2,0] or a[i:i+3]==[0,2,1]: nums[1][1]+=1
        for i in range(l-3):
            if a[i:i+4]==[0,1,1,0]: nums[0][2]+=1
            elif a[i:i+4]==[2,1,1,0] or a[i:i+4]==[0,1,1,2]: nums[0][3]+=1
                
            elif a[i:i+4]==[0,2,2,0]: nums[1][2]+=1
            elif a[i:i+4]==[1,2,2,0] or a[i:i+4]==[0,2,2,1]: nums[1][3]+=1
        for i in range(l-4):
            if a[i:i+5]==[0,1,0,1,0]: nums[0][4]+=1
            elif a[i:i+5]==[0,1,0,1,2] or a[i:i+5]==[2,1,0,1,0]: nums[0][5]+=1
            elif a[i:i+5]==[0,1,1,1,0]: nums[0][6]+=1
            elif a[i:i+5]==[0,1,1,1,2] or a[i:i+5]==[2,1,1,1,0]: nums[0][7]+=1
            elif a[i:i+5]==[1,1,1,1,1]: nums[0][-1]+=1
                
            elif a[i:i+5]==[0,2,0,2,0]: nums[1][4]+=1
            elif a[i:i+5]==[0,2,0,2,1] or a[i:i+5]==[1,2,0,2,0]: nums[1][5]+=1
            elif a[i:i+5]==[0,2,2,2,0]: nums[1][6]+=1
            elif a[i:i+5]==[0,2,2,2,1] or a[i:i+5]==[1,2,2,2,0]: nums[1][7]+=1
            elif a[i:i+5]==[2,2,2,2,2]: nums[1][-1]+=1
            
        if l>=6:
            for i in range(l-5):
                if a[i:i+6]==[0,1,0,1,1,0] or a[i:i+6]==[0,1,1,0,1,0]: nums[0][8]+=1
                elif a[i:i+6]==[2,1,0,1,1,0] or a[i:i+6]==[0,1,1,0,1,2]: nums[0][9]+=1
                elif a[i:i+6]==[2,1,1,0,1,0] or a[i:i+6]==[0,1,0,1,1,2]: nums[0][10]+=1
                elif a[i:i+6]==[0,1,1,1,1,0]: nums[0][11]+=1
                elif a[i:i+6]==[2,1,1,1,1,0] or a[i:i+6]==[0,1,1,1,1,2]: nums[0][12]+=1
                elif a[i:i+6]==[1,1,1,0,1,1] or a[i:i+6]==[1,1,0,1,1,1]: nums[0][13]+=1
                    
                elif a[i:i+6]==[0,2,0,2,2,0] or a[i:i+6]==[0,2,2,0,2,0]: nums[1][8]+=1
                elif a[i:i+6]==[1,2,0,2,2,0] or a[i:i+6]==[0,2,2,0,2,1]: nums[1][9]+=1
                elif a[i:i+6]==[0,2,2,0,2,1] or a[i:i+6]==[0,2,0,2,2,1]: nums[1][10]+=1
                elif a[i:i+6]==[0,2,2,2,2,0]: nums[1][11]+=1
                elif a[i:i+6]==[1,2,2,2,2,0] or a[i:i+6]==[0,2,2,2,2,1]: nums[1][12]+=1
                elif a[i:i+6]==[2,2,2,0,2,2] or a[i:i+6]==[2,2,0,2,2,2]: nums[1][13]+=1
                
        if l>=7:
            for i in range(l-6):
                if a[i:i+7]==[0,1,1,1,0,1,0] or a[i:i+7]==[0,1,0,1,1,1,0]: nums[0][16]+=1
                elif a[i:i+7]==[2,1,1,0,1,1,2] or a[i:i+7]==[2,1,0,1,1,1,2] or a[i:i+7]==[2,1,1,1,0,1,2]: nums[0][13]+=1
                elif a[i:i+7]==[2,1,1,0,1,1,0] or a[i:i+7]==[0,1,1,0,1,1,2]: nums[0][14]+=1
                elif a[i:i+7]==[0,1,1,0,1,1,0] or a[i:i+7]==[0,1,1,1,0,1,2] or a[i:i+7]==[2,1,0,1,1,1,0]: nums[0][15]+=1
                elif a[i:i+7]==[0,1,0,1,1,1,2] or a[i:i+7]==[2,1,1,1,0,1,0]: nums[0][17]+=1
                
                elif a[i:i+7]==[0,2,2,2,0,2,0] or a[i:i+7]==[0,2,0,2,2,2,0]: nums[1][16]+=1
                elif a[i:i+7]==[1,2,2,0,2,2,1] or a[i:i+7]==[1,2,0,2,2,2,1] or a[i:i+7]==[1,2,2,2,0,2,1]: nums[1][13]+=1
                elif a[i:i+7]==[1,2,2,0,2,2,0] or a[i:i+7]==[0,2,2,0,2,2,1]: nums[1][14]+=1
                elif a[i:i+7]==[0,2,2,0,2,2,0] or a[i:i+7]==[0,2,2,2,0,2,1] or a[i:i+7]==[1,2,0,2,2,2,0]: nums[1][15]+=1
                elif a[i:i+7]==[0,2,0,2,2,2,1] or a[i:i+7]==[1,2,2,2,0,2,0]: nums[1][17]+=1
        
    for i in range(BOARD_LEN):
        # Calculate row and column
        one_calc(board_matrix[i])
        one_calc(board_matrix[:,i])
    for i in range(-BOARD_LEN+5, BOARD_LEN-4):
        # Calculate the main and sub diagonals
        one_calc(np.diag(board_matrix,i))
        one_calc(np.diag(np.flip(board_matrix,axis=0),i))
        
    nums[:,0] -= nums[:,4]*2 + nums[:,8]+nums[:,10]+nums[:,16]+nums[:,17]
    nums[:,1] -= nums[:,5] + nums[:,9]
    nums[:,2] -= nums[:,8] + nums[:,9]+nums[:,14]+nums[:,15]
    nums[:,3] -= nums[:,10] + nums[:,14]
    nums[:,6] -= nums[:,15] + nums[:,16]
    nums[:,7] -= nums[:,17]
    
    #global numsall
    #numsall = nums
    if player == -1: 
        return np.sum(nums*coeff), np.sum(nums*np.flip(coeff,axis=0))
    else:
        return np.sum(nums*np.flip(coeff,axis=0)), np.sum(nums*coeff)




