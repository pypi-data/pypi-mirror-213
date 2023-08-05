from collections import OrderedDict

import gym
from gym import (spaces, utils, logger)
import numpy as np


class ProteinFoldingBaseEnv(gym.Env):
    def __init__(self, seq):
        """
        Initializes an instance of the `ProteinFoldingBaseEnv` class with a protein sequence `seq`.

        Args:
        - seq (str): the protein sequence to be folded.

        Initializes instance variables:
        - self.seq (str): the protein sequence to be folded.
        - self.is_trapped (bool): a flag indicating whether the protein chain is trapped in a local minimum.
        - self.done (bool): a flag indicating whether the episode is over.
        """
        self.seq = seq.upper()
        self.is_trapped = False
        self.done = False
        if len(self.seq) <= 2:
            return

    def observe(self):
        """
        Returns a numpy array representation of the current chain of amino acids in the protein sequence.

        Returns:
        - native_obs (numpy array): an array representing the current chain of amino acids in the protein sequence.
        """
        action_chain = self.actions
        native_obs = np.zeros(shape=(len(self.seq) - 2,), dtype=int)
        for i, item in enumerate(action_chain):
            native_obs[i] = item
        return native_obs

    def _compute_reward(self):
        """
        Computes the reward for the current state of the environment.

        Returns:
        - reward (float): the reward value for the current state of the environment.

        Computes `curr_reward` by calling `_compute_free_energy(self.state)` and returns the following based on the state of the protein chain:
        - -0.01 if `self.is_trapped` is True.
        - `curr_reward` if `self.done` is True.
        - 0 otherwise.
        """
        curr_reward = self._compute_free_energy(self.state)
        if self.is_trapped:
            return -0.01
        elif self.done:
            return curr_reward
        else:
            return 0

    def _compute_free_energy(self, chain):
        """
        Computes the free energy of the protein chain represented by `chain`.

        Args:
        - chain (OrderedDict): the protein chain to calculate free energy for.

        Returns:
        - total_energy (float): the free energy of the protein chain.

        Computes `total_energy` as the sum of pairwise interactions between all pairs of hydrophobic residues that are separated by at least two other residues.
        """
        path = list(chain.items())
        total_energy = 0
        for index in range(0, len(path)):
            for jndex in range(index, len(path)):
                if abs(index - jndex) >= 2:
                    current_amino_acid_i = path[index][1]
                    current_amino_acid_j = path[jndex][1]
                    current_place_i = path[index][0]
                    current_place_j = path[jndex][0]
                    x_i = current_place_i[0]
                    y_i = current_place_i[1]
                    x_j = current_place_j[0]
                    y_j = current_place_j[1]
                    if current_amino_acid_i == 'H' and current_amino_acid_j == 'H' and (
                            abs(x_i - x_j) + abs(y_i - y_j) == 1):
                        total_energy += 1
        return total_energy


    def get_observation_info(self, next_state):
        """
        Returns the current observation, reward, done flag, and info dictionary based on the current state of the environment and the proposed next state.

        Args:
        - next_state (OrderedDict): the proposed next state of the protein chain.

        Returns:
        - obs (numpy array): the current observation of the environment.
        - reward (float): the reward value for the current state of the environment.
        - done (bool): a flag indicating whether the episode is over.
        - False (bool): a flag indicating whether the environment has successfully reset.
        - info (dict): a dictionary containing information about the current state of the environment.

        Calls `self.observe()` to get the current observation of the environment and sets the following based on the current state of the protein chain and the proposed next state:
        - is_trapped (bool): a flag indicating whether the protein chain is trapped in a local minimum.
        - self.is_trapped (bool): updates the value of `self.is_trapped`.
        - self.done (bool): updates the value of `self.done`.
        - reward (float): computes the reward for the current state by calling `_compute_reward()` and updates the value of `self.done`.
        - info (dict): a dictionary containing the current chain length, sequence length, actions taken so far, whether the chain is trapped, and the current state of the protein chain.
        """
        is_trapped = False
        if len(self.state) < len(self.seq):
            if set(self._get_adjacent_coords(next_state).values()).issubset(self.state.keys()):
                is_trapped = True
        obs = self.observe()
        self.is_trapped = is_trapped
        self.done = len(self.state) == len(self.seq) or is_trapped
        reward = self._compute_reward()
        info = {
            'chain_length': len(self.state),
            'seq_length': len(self.seq),
            'actions': [str(i) for i in self.actions],
            'is_trapped': is_trapped,
            'state_chain': self.state,
        }
        return obs, reward, self.done, False, info


    def seed(self, seed=None):
        """
        Seeds the environment's random number generator and the action space's random number generator with a given seed value or with a randomly generated seed value if none is provided.

        Args:
        - seed (int, optional): the seed value to use for the random number generator.

        Returns:
        - [seed] (list): a list containing the generated seed value.
        """
        self.np_random, seed = utils.seeding.np_random(seed)
        self.action_space.seed(seed)
        np.random.seed(seed)

        return [seed]