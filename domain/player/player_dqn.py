import os
import random
import sys
import time
from collections import deque
from typing import List

import numpy as np
import tensorflow as tf

from domain.direction_enum import Direction
from domain.dqn.dqn_net import dqn_net, dqn_params
from domain.game_state import GameState
from domain.map import MapTile, Map
from domain.player.player import Player
from domain.position import Position
from domain.score import Score

tf = tf.compat.v1


class PlayerDQN(Player):
    def __init__(self, map: Map, initial_x, initial_y):
        super().__init__(map, initial_x, initial_y)

        # Start Tensorflow session
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=0.1)
        self.sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options))
        self.qnet = dqn_net
        self.params = self.qnet.params

        # time started
        self.general_record_time = time.strftime("%a_%d_%b_%Y_%H_%M_%S", time.localtime())
        # Q and cost
        self.Q_global = []
        self.cost_disp = 0

        # Stats
        self.cnt = self.qnet.sess.run(self.qnet.global_step)
        self.local_cnt = 0

        self.numeps = 0
        self.last_score = 0
        self.s = time.time()
        self.last_reward = 0.
        self.last_action = None

        self.replay_mem = deque()
        self.last_scores = deque()

        self.current_state = None
        self.terminal = False

        self.ep_rew = 0
        self.frame = 0
        self.won = False

        self.force_observe_counter = 0

    def move_to_next_position(
            self,
            enemy_positions: List[Position],
            score: Score
    ) -> None:
        next_position = self.get_next_position()
        print(self.direction)
        self.set_position(next_position)
        self.direction = self.get_next_direction(enemy_positions, Score(score.available_points, score.score))

        game_state = GameState(self.map, Score(score.available_points, score.score), Position(self.x, self.y), Direction.RIGHT, enemy_positions)
        self.observation_step(game_state)

    def get_next_direction(
            self,
            enemy_positions: List[Position],
            score: Score
    ) -> Direction:
        if self.current_state is None:
            game_state = GameState(self.map, score, Position(self.x, self.y), Direction.RIGHT, enemy_positions)
            self.current_state = self.get_state_matrices(game_state)

        # Exploit / Explore
        rand = np.random.rand()
        if rand > self.params['eps']:
            # Exploit action
            self.Q_pred = self.qnet.sess.run(
                self.qnet.y,
                feed_dict={
                    self.qnet.x: np.reshape(self.current_state, (1, self.params['width'], self.params['height'], 4)),
                    self.qnet.q_t: np.zeros(1),
                    self.qnet.actions: np.zeros((1, 4)),
                    self.qnet.terminals: np.zeros(1),
                    self.qnet.rewards: np.zeros(1)
                }
            )[0]

            self.Q_global.append(max(self.Q_pred))
            a_winner = np.argwhere(self.Q_pred == np.amax(self.Q_pred))

            # print(self.Q_pred, a_winner, self.current_state, self.params['eps'])

            if len(a_winner) > 1:
                direction = self.map_value_to_direction(a_winner[np.random.randint(0, len(a_winner))][0])
            else:
                direction = self.map_value_to_direction(a_winner[0][0])
        else:
            # Random:
            direction = self.map.get_random_opened_direction(self.x, self.y)

        # Save last_action
        self.last_action = direction

        # game_state = GameState(self.map, score, self.get_next_position(), Direction.RIGHT, enemy_positions)

        return direction

    @staticmethod
    def map_direction_to_value(direction: Direction):
        if direction == Direction.UP:
            return 0.
        elif direction == Direction.RIGHT:
            return 1.
        elif direction == Direction.DOWN:
            return 2.
        else:
            return 3.

    @staticmethod
    def map_value_to_direction(value) -> Direction:
        if value == 0.:
            return Direction.UP
        elif value == 1.:
            return Direction.RIGHT
        elif value == 2.:
            return Direction.DOWN
        else:
            return Direction.LEFT

    def observation_step(self, state, is_final=False):
        if self.last_action is not None:
            # Process current experience state
            self.last_state = np.copy(self.current_state)
            self.current_state = self.get_state_matrices(state)

            # Process current experience reward
            self.current_score = state.score.score
            reward = self.current_score - self.last_score
            self.last_score = self.current_score

            # if reward >= 10:
            #     self.last_reward = 50.
            # elif reward <= -10:
            #     self.last_reward = -500.
            # elif reward < 0:
            #     self.last_reward = -1.

            self.ep_rew += reward

            # Store last experience into memory
            experience = (self.last_state, float(reward), self.last_action, self.current_state, self.terminal)
            self.replay_mem.append(experience)
            if len(self.replay_mem) > self.params['mem_size']:
                self.replay_mem.popleft()

            # Save model
            if self.qnet.params['save_file']:
                if self.local_cnt > self.params['train_start'] and self.local_cnt % self.params['save_interval'] == 0:
                    self.qnet.save_ckpt('saves/model-' + self.qnet.params['save_file'] + "_" + str(self.cnt) + '_' + str(self.numeps))
                    print('Model saved')

            # Train
            self.train()

        # Next
        self.local_cnt += 1
        self.frame += 1
        self.params['eps'] = max(self.params['eps_final'],
                                 1.00 - float(self.cnt) / float(self.params['eps_step']))

    def finalize(self, state):
        # Next
        self.ep_rew += self.last_reward

        # Do observation
        self.terminal = True
        self.observation_step(state, True)

        # Print stats
        log_file_location = '../logs/'+str(self.general_record_time)+'-l-'+str(self.params['width'])+'-m-'+str(self.params['height'])+'-x-'+str(self.params['num_training'])+'.log'
        if not os.path.exists(log_file_location):
            open(log_file_location, 'w').close()
        log_file = open(log_file_location, 'a')
        log_file.write(f"# {self.numeps} | steps: {self.local_cnt} | steps_t: {self.cnt} | t: {time.time()-self.s} | r: {self.ep_rew} | e: {self.params['eps']}" )
        Q = max(self.Q_global, default=float('nan'))
        log_file.write(f"| Q: {Q} \n")
        sys.stdout.write(f"# {self.numeps} | steps: {self.local_cnt} | steps_t: {self.cnt} | t: {time.time()-self.s} | r: {self.ep_rew} | e: {self.params['eps']} ")
        Q = max(self.Q_global, default=float('nan'))
        sys.stdout.write(f"| Q: {Q} \n")
        sys.stdout.flush()

    def train(self):
        # Train
        if self.local_cnt > self.params['train_start'] and len(self.replay_mem) >= self.params['batch_size']:
            batch = random.sample(self.replay_mem, self.params['batch_size'])
            batch_s = []  # States (s)
            batch_r = []  # Rewards (r)
            batch_a = []  # Actions (a)
            batch_n = []  # Next states (s')
            batch_t = []  # Terminal state (t)

            for i in batch:
                batch_s.append(i[0])
                batch_r.append(i[1])
                batch_a.append(i[2])
                batch_n.append(i[3])
                batch_t.append(i[4])
            batch_s = np.array(batch_s)
            batch_r = np.array(batch_r)
            batch_a = self.get_onehot(np.array(batch_a))
            batch_n = np.array(batch_n)
            batch_t = np.array(batch_t)

            self.cnt, self.cost_disp = self.qnet.train(batch_s, batch_a, batch_t, batch_n, batch_r)

    # Actions here are directions
    def get_onehot(self, actions):
        """ Create list of vectors with 1 values at index of action in list """
        actions_onehot = np.zeros((self.params['batch_size'], 4))
        for i in range(len(actions)):
            actions_onehot[i][int(actions[i])] = 1
        return actions_onehot

    def get_state_matrices(self, state: GameState):
        width, height = self.params['width'], self.params['height']

        def get_wall_matrix():
            """ Return matrix with wall coordinates set to 1 """
            map = state.map
            matrix = np.zeros((height, width), dtype=np.int8)
            for i in range(height):
                for j in range(width):
                    # Put cell vertically reversed in matrix
                    tile = map.get_tile(i, j)
                    cell = 1 if tile == MapTile.WALL else 0
                    matrix[-1-i][j] = cell
            return matrix

        def get_pacman_matrix():
            """ Return matrix with pacman coordinates set to 1 """
            matrix = np.zeros((height, width), dtype=np.int8)

            position = state.player_position
            matrix[-1-position.y][position.x] = 1

            return matrix

        def get_enemy_matrix():
            """ Return matrix with ghost coordinates set to 1 """
            matrix = np.zeros((height, width), dtype=np.int8)

            for enemy_position in state.enemy_positions:
                matrix[-1-enemy_position.y][enemy_position.x] = 1

            return matrix

        def get_food_matrix():
            """ Return matrix with food coordinates set to 1 """
            matrix = np.zeros((height, width), dtype=np.int8)

            for i in range(height):
                for j in range(width):
                    # Put cell vertically reversed in matrix
                    matrix[-1-i][j] = 1 if state.score.has_point(Position(j, i)) else 0

            return matrix

        # Create observation matrix as a combination of
        # wall, pacman, enemy, food matrices
        observation = np.zeros((4, height, width))

        observation[0] = get_wall_matrix()
        observation[1] = get_pacman_matrix()
        observation[2] = get_enemy_matrix()
        observation[3] = get_food_matrix()

        observation = np.swapaxes(observation, 0, 2)

        return observation

    def reset(self, initial_score: Score, initial_enemy_positions: List[Position]):
        # Reset reward
        self.last_score = 0
        self.current_score = 0
        self.last_reward = 0.
        self.ep_rew = 0

        # Reset state
        self.last_state = None
        game_state = GameState(self.map, initial_score, Position(self.initial_x, self.initial_y), Direction.RIGHT, initial_enemy_positions)
        self.current_state = self.get_state_matrices(game_state)

        # Reset actions
        self.last_action = None

        # Reset vars
        self.terminal = None
        self.Q_global = []
        self.delay = 0

        # Next
        self.frame = 0
        self.numeps += 1

        self.force_observe_counter = 0

        self.params = dqn_params

        self.terminal = False

