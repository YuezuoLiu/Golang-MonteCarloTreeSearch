# COLOR = (RED, GREEN, BULE)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BG_COLOR = (100, 180, 250)

# SCREEN SETUP
BOARD_LEN = 8
DIST_TO_BOUNDARY = 20
CHESS_SQUARE_LEN = 20
WIN_N = 5   # victory condition: 5 same color in a row

SIMULATE_NUM = 300 # MCTS simulation times per decison
COEFFICIENT = 0.2   # coeffient C in UCT
BOT_INIT_TREE = 20  # init the search tree using bot knowledge to reduce searching directions

