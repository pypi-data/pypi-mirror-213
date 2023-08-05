from gym.envs.registration import register
from .base_environment import ProteinFoldingBaseEnv
from .base_environment_2d import ProteinFolding2DEnv
from .environement_triunghiular import ProteinFoldingTriangularEnv
from .environment_2d import ProteinFoldingSquareEnv
from .environment_3d import ProteinFolding3DEnv
from .environment_LRF import ProteinFoldingLRF2DEnv

#register all custom environments
register(
    id='ProteinFoldingSquareEnv',
    entry_point='protein_folding_environment.environment_2d:ProteinFoldingSquareEnv',
    max_episode_steps=100000,
)

register(
    id='ProteinFolding3DEnv',
    entry_point='protein_folding_environment.environment_3d:ProteinFolding3DEnv',
    max_episode_steps=100000,
)

register(
    id='ProteinFoldingLRF2DEnv',
    entry_point='protein_folding_environment.environment_LRF:ProteinFoldingLRF2DEnv',
    max_episode_steps=100000,
)

register(
    id='ProteinFoldingTriangularEnv',
    entry_point='protein_folding_environment.environement_triunghiular:ProteinFoldingTriangularEnv',
    max_episode_steps=100000,
)
