import gymnasium as gym
import numpy as np
from gymnasium import spaces

from ....__init__ import SIZE_WINDOW


class Custom(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}


    def __init__(self, render_mode=None):
        super().__init__()

        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=..., high=...,
                                            shape=..., dtype=np.int64)

        self.render_mode = render_mode


    def step(self):
        ...
        return observation, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        ...
        return observation, info

    def _render_frame(self):
        ...

    def close(self):
        ...

