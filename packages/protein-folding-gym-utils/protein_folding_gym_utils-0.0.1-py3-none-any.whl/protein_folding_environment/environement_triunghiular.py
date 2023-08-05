from collections import OrderedDict

import gym
from gym import (spaces, logger)
import numpy as np

from protein_folding_environment.base_environment_2d import ProteinFolding2DEnv
from utils.movement_utils import move_to_new_state_triangular


class ProteinFoldingTriangularEnv(ProteinFolding2DEnv):
    def __init__(self, seq):
        """
        Initializes an instance of the `ProteinFoldingTriangularEnv` class with a protein sequence `seq`.

        Args:
        - seq (str): the protein sequence to be folded.

        Calls the `__init__` method of the base class `ProteinFolding2DEnv` and sets the following instance variables:
        - self.action_space (Discrete): a discrete action space representing the six possible moves in a triangular lattice.
        - self.observation_space (Box): a box observation space representing the current chain of amino acids in the protein sequence.
        """
        super().__init__(seq)
        self.action_space = spaces.Discrete(start=1, n=6)
        self.observation_space = spaces.Box(low=0, high=5,
                                            shape=(len(self.seq) - 2,),
                                            dtype=int)

    def step(self, action):
        """
        Advances the environment by one step given an action.

        Args:
        - action (int): the action to take.

        Returns:
        - obs (numpy array): the current observation of the environment.
        - reward (float): the reward value for the current state of the environment.
        - done (bool): a flag indicating whether the episode is over.
        - False (bool): a flag indicating whether the environment has successfully reset.
        - info (dict): a dictionary containing information about the current state of the environment.

        If `action` is not a valid action, raises a `ValueError`.
        Calculates the next state of the protein chain using `move_to_new_state_triangular()` based on the current state and the proposed action and updates the environment's state with the next state.
        If `next_state` is None or already in the state dictionary, returns `(None, None, False, False, {})`.
        Appends `action` to the list of actions taken so far and calls `self.get_observation_info(next_state)` to get the current observation, reward, done flag, and info dictionary based on the current state of the environment and the proposed next state.
        """
        if not self.action_space.contains(action):
            raise ValueError("%r (%s) invalid" % (action, type(action)))

        previous = list(self.state.keys())[-1]
        previous2 = list(self.state.keys())[-2]
        next_state = move_to_new_state_triangular(
            previous,
            previous2,
            action
        )
        idx = len(self.state)
        if next_state is None or next_state in self.state:
            return (None, None, False, False, {})
        self.actions.append(action)
        try:
            self.state.update({next_state: self.seq[idx]})
        except IndexError:
            logger.error('All molecules have been placed! Nothing can be added to the protein chain.')
            raise

        return self.get_observation_info(next_state)

    def _get_adjacent_coords(self, coords):
        """
        Returns a dictionary containing the adjacent coordinates of a given set of coordinates in a triangular lattice.

        Args:
        - coords (tuple): the coordinates to get adjacent coordinates for.

        Returns:
        - adjacent_coords (dict): a dictionary containing the adjacent coordinates of `coords`.

        Calculates the adjacent coordinates of `coords` in a triangular lattice and returns them as a dictionary.
        """
        x, y = coords
        adjacent_coords = {
            0: (x - 1, y),
            1: (x, y - 1),
            2: (x, y + 1),
            3: (x + 1, y),
            4: (x + 1, y + 1),
            5: (x - 1, y - 1),
        }
        return adjacent_coords

