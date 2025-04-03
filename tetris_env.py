import gymnasium as gym
from tetris import Tetris
import numpy as np
from numpy.typing import NDArray
from typing import Optional
from gymnasium.envs.registration import register
from stable_baselines3.common.env_checker import check_env
from gymnasium.wrappers import FlattenObservation

register(
    id='tetris-v1',
    entry_point='tetris_env:TetrisEnv'
)

class TetrisEnv(gym.Env):
    def __init__(self) -> None:
        super().__init__()
        self.tetris = Tetris()

        self.action_space = gym.spaces.Discrete(5)
        self.observation_space = gym.spaces.MultiDiscrete(np.array([[3]*10]*20))

    def reset(self, seed: Optional[int] = None, options = None):
        super().reset(seed=seed)
        self.tetris.reset(seed)
        return self.tetris.get_observation(), {}
    
    def step(self, action):
        reward, terminated = self.tetris.step(action)
        return self.tetris.get_observation(), reward+0.01, terminated, False, {}
    
    def render(self):
        self.tetris.draw()
    
if __name__ == "__main__":
    env = gym.make('tetris-v1')
    env = FlattenObservation(env)
    check_env(env)

    obs = env.reset(seed=1)[0]

    for i in range(1000):
        rand_action = env.action_space.sample()
        print(rand_action)
        obs, reward, terminated, _, _ = env.step(rand_action)
        print(reward, terminated)
        env.render()
        if (terminated):
            break


