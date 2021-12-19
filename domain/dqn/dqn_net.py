from domain.dqn.dqn import DQN
from game.game_settings import MAP_WIDTH_IN_TILES, MAP_HEIGHT_IN_TILES

dqn_params = {
    "width": MAP_WIDTH_IN_TILES,
    "height": MAP_HEIGHT_IN_TILES,
    "num_training": 10000,  # Training cycles. Just for statistics
    # Model backups
    'load_file': None,#'saves/model-pacman_1_14906_9000'
    'save_file': 'pacman_1',
    'save_interval': 1000,

    # Training parameters
    'train_start': 30,    # Episodes before training starts
    'batch_size': 32,       # Replay memory batch size
    'mem_size': 100000,     # Replay memory size

    'discount': 0.95,       # Discount rate (gamma value)
    'lr': .0002,            # Learning reate
    # 'rms_decay': 0.99,      # RMS Prop decay (switched to adam)
    # 'rms_eps': 1e-6,        # RMS Prop epsilon (switched to adam)

    # Epsilon value (epsilon-greedy)
    'eps': 1.0,             # Epsilon start value
    'eps_final': 0.1,       # Epsilon end value
    'eps_step': 10000       # Epsilon steps between start and end (linear)
}

dqn_net = DQN(dqn_params)