import gymnasium as gym
from stable_baselines3 import SAC, PPO, A2C, DQN
import os
import tetris_env
import datetime
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from sb3_contrib import QRDQN
from stable_baselines3.common.monitor import Monitor
from gymnasium.wrappers import FlattenObservation

def evaluate():
    model_path = r"C:\Users\Jindra\Documents\rl-tetris\logs\20250403-233003\best_model\best_model.zip"

    # Create training environment
    eval_env = gym.make('tetris-v1')
    eval_env = FlattenObservation(eval_env)  # Flatten observations if needed

    model = PPO.load(model_path, eval_env)

    terminated = False
    obs = eval_env.reset()[0]
    total_rew = 0
    while not terminated:
        action = model.predict(obs, deterministic=True)[0]
        #print(action)
        obs, r, terminated, _, _ = eval_env.step(action)
        total_rew += r
        eval_env.render()

    print(total_rew)



if __name__ == "__main__":
    evaluate()