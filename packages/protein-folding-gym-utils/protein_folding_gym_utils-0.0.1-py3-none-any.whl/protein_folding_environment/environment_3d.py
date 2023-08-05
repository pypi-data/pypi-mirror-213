from collections import OrderedDict
import gym
from gym import (spaces,logger)
import numpy as np

from protein_folding_environment.base_environment import ProteinFoldingBaseEnv
from utils.movement_utils import move_to_new_state_3d
from utils.plotting_utils import plot_3D_foleded_protein

class ProteinFolding3DEnv(ProteinFoldingBaseEnv):
    def __init__(self, seq):
        """
        Initializes a new instance of the `ProteinFolding3DEnv` class.

        Parameters:
        -----------
        seq : str
            The protein sequence to be folded.

        Returns:
        --------
        None
        """
        super().__init__(seq)
        self.reset()
        self.action_space = spaces.Discrete(start=1, n=6)
        self.observation_space = spaces.Box(low=0, high=5,
                                            shape=(len(self.seq) - 2,),
                                            dtype=int)

    def step(self, action):
        """
        Performs one step of the protein folding simulation.

        Parameters:
        -----------
        action : int
            The action to be taken by the agent.

        Returns:
        --------
        tuple
            The new observation, the reward, whether the episode is done, and additional information.
        """
        if not self.action_space.contains(action):
            raise ValueError("%r (%s) invalid" % (action, type(action)))

        self.last_action = action

        previous = list(self.state.keys())[-1]
        previous2 = list(self.state.keys())[-1]
        next_state = move_to_new_state_3d(
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

    def reset(self):
        """
        Resets the environment to the initial state.

        Returns:
        --------
        numpy.ndarray
            The initial observation of the environment.
        """
        self.actions = []
        self.state = OrderedDict(
            {
                (0, 0, 0): self.seq[0],
                (1, 0, 0): self.seq[1],
            }
        )
        self.done = len(self.seq) == 2
        obs = self.observe()
        return obs

    def render(self, mode='human', display_mode="draw",
               pause_t=0.0, save_fig=False, save_path="",
               score=2022, optima_idx=0):
        """
        Renders the current state of the environment.

        Parameters:
        -----------
        mode : str, optional
            The rendering mode. 'human' for displaying in the console, 'rgb_array' for returning an RGB array.
        display_mode : str, optional
            The display mode. 'draw' for drawing the environment using ASCII art, 'plot' for plotting the environment
            using Matplotlib.
        pause_t : float, optional
            The amount of time to pause the rendering.
        save_fig : bool, optional
            Whether to save the rendering as a figure.
        save_path : str, optional
            The path to save the rendering as a figure.
        score : int, optional
            The current score of the environment.
        optima_idx : int, optional
            The index of the optimal score.

        Returns:
        --------
        None
        """
        if mode == "human":
            plot_3D_foleded_protein(
                list(self.state.items()),
            )

    def _get_adjacent_coords(self, coords):
        """
        Returns a dictionary containing adjacent coordinates for a given set of coordinates.

        Parameters:
        -----------
        coords: tuple
            The coordinates (x, y, z) for which adjacent coordinates are to be found.

        Returns:
        --------
        dict
            A dictionary containing adjacent coordinates as values and their respective directions as keys.

        """
        x, y, z = coords
        adjacent_coords = {
            0: (x - 1, y, z),
            1: (x, y - 1, z),
            2: (x, y + 1, z),
            3: (x + 1, y, z),
            4: (x, y, z - 1),
            5: (x, y, z + 1)
        }
        return adjacent_coords

    def _compute_free_energy(self, chain):
        """
        Computes the free energy of a given chain.

        Parameters:
        -----------
        chain: OrderedDict
            An ordered dictionary containing the coordinates and corresponding amino acids in a chain.

        Returns:
        --------
        int
            The total free energy of the chain.

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
                    z_i = current_place_i[2]
                    x_j = current_place_j[0]
                    y_j = current_place_j[1]
                    z_j = current_place_j[2]
                    if current_amino_acid_i == 'H' and current_amino_acid_j == 'H' and (
                            abs(x_i - x_j) + abs(y_i - y_j) + abs(z_i - z_j) == 1):
                        total_energy += 1
        return total_energy


