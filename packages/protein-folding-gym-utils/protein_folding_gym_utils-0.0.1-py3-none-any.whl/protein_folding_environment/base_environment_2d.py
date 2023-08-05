from collections import OrderedDict
from gym import (spaces)

from protein_folding_environment.base_environment import ProteinFoldingBaseEnv
from utils.plotting_utils import plot_2D_folded_protein


class ProteinFolding2DEnv(ProteinFoldingBaseEnv):
    def __init__(self, seq):
        """
        Initializes an instance of the `ProteinFolding2DEnv` class with a protein sequence `seq`.

        Args:
        - seq (str): the protein sequence to be folded.

        Calls the `__init__` method of the base class `ProteinFoldingBaseEnv` and sets the following instance variables:
        - self.actions (list): a list of actions taken so far.
        - self.state (OrderedDict): an ordered dictionary representing the current state of the protein chain.
        """
        super().__init__(seq)
        self.reset()

    def reset(self):
        """
        Resets the environment to its initial state.

        Returns:
        - obs (numpy array): the current observation of the environment.

        Sets the following instance variables:
        - self.actions (list): an empty list of actions taken so far.
        - self.state (OrderedDict): an ordered dictionary representing the current state of the protein chain.
        - self.done (bool): a flag indicating whether the episode is over.
        - obs (numpy array): the current observation of the environment.
        """
        self.actions = []
        self.state = OrderedDict(
            {
                (0, 0): self.seq[0],
                (1, 0): self.seq[1],
            }
        )
        self.done = len(self.seq) == 2
        obs = self.observe()
        return obs

    def render(self, mode='human'):
        """
        Renders the current state of the protein chain.

        Args:
        - mode (str): the rendering mode to use.

        If `mode` is "human", calls `plot_2D_folded_protein` to render the current state of the protein chain.
        """
        if mode == "human":
            plot_2D_folded_protein(
                list(self.state.items()),
            )
