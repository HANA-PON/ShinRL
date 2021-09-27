"""
Author: Toshinori Kitamura
Affiliation: NAIST
"""
from functools import cached_property
from typing import Any, Optional, Tuple

import gym
import jax.numpy as jnp
import numpy as np
from chex import Array
from matplotlib.axes import Axes

from shinrl import ShinEnv

from .core import calc, plot
from .core.config import MountainCarConfig


class MountainCar(ShinEnv):
    """Dynamics and reward are based on OpenAI gym's implementation of MountainCar-v0"""

    DefaultConfig = MountainCarConfig

    @property
    def config(self) -> MountainCarConfig:
        return self._config

    @property
    def dS(self) -> int:
        return self.config.pos_res * self.config.vel_res

    @property
    def dA(self) -> int:
        return self.config.dA

    @cached_property
    def init_probs(self) -> Array:
        pos_step = (self.config.pos_max - self.config.pos_min) / (
            self.config.pos_res - 1
        )
        ini_pos = np.arange(-0.6, -0.4, pos_step)
        idxs = []
        for pos in ini_pos:
            idxs.append(calc.pos_vel_to_state(self.config, pos, 0.0))
        idxs = np.unique(np.array(idxs))
        probs = np.ones_like(idxs, dtype=float) / len(idxs)
        init_probs = np.zeros(self.dS)
        np.put(init_probs, idxs, probs)
        return jnp.array(init_probs)

    @cached_property
    def observation_space(self) -> gym.spaces.Space:
        if self.config.obs_mode == MountainCarConfig.OBS_MODE.tuple:
            space = gym.spaces.Box(
                low=np.array([self.config.pos_min, self.config.vel_min]),
                high=np.array([self.config.pos_max, self.config.vel_max]),
                dtype=float,
            )
        elif self.config.obs_mode == MountainCarConfig.OBS_MODE.image:
            space = gym.spaces.Box(
                low=np.zeros((28, 28, 1)),
                high=np.ones((28, 28, 1)),
                dtype=float,
            )
        return space

    @cached_property
    def action_space(self) -> gym.spaces.Space:
        if self.config.act_mode == MountainCarConfig.ACT_MODE.discrete:
            space = gym.spaces.Discrete(self.config.dA)
        elif self.config.act_mode == MountainCarConfig.ACT_MODE.continuous:
            space = gym.spaces.Box(
                low=np.array(-self.config.force_max),
                high=np.array(self.config.force_max),
                dtype=float,
            )
        return space

    def transition(self, state: int, action: int) -> Tuple[Array, Array]:
        return calc.transition(self.config, state, action)

    def reward(self, state: int, action: int) -> float:
        return calc.reward(self.config, state, action)

    def observation(self, state: int) -> Array:
        if self.config.obs_mode == MountainCarConfig.OBS_MODE.tuple:
            return calc.observation_tuple(self.config, state)
        elif self.config.obs_mode == MountainCarConfig.OBS_MODE.image:
            return calc.observation_image(self.config, state)

    def plot_S(
        self,
        tb: Array,
        title: Optional[str] = None,
        ax: Optional[Axes] = None,
        cbar_ax: Optional[Axes] = None,
        vmin: Optional[float] = None,
        vmax: Optional[float] = None,
        fontsize: Optional[int] = 10,
        **kwargs: Any,
    ) -> None:
        plot.plot_S(tb, self.config, title, ax, cbar_ax, vmin, vmax, fontsize, **kwargs)
