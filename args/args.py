# SCREEN SETUP
BOARD_LEN = 9    # grid num in game, stantard golang: 15
WIN_N = 5        # victory condition: 5 same color in a row

EXPAND_THRESHOLD = 5  # visit count num a node can expand (add child nodes to the tree)
SIMULATE_NUM = 300 # MCTS simulation times per decison
COEFFICIENT = 1   # coeffient C in UCT
BOT_INIT_TREE = 0  # init the search tree using bot knowledge to reduce searching directions

