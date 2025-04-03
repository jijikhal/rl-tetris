import gymnasium as gym
from stable_baselines3 import SAC, PPO, A2C, DQN
import os
import tetris_env
import datetime
from stable_baselines3.common.callbacks import EvalCallback, CheckpointCallback
from sb3_contrib import QRDQN
from stable_baselines3.common.monitor import Monitor
from gymnasium.wrappers import FlattenObservation
import math

def exp_schedule(initial_value: float):
    def func(progress_remaining: float) -> float:
        return math.exp(-2*(1-progress_remaining))*initial_value*0.6

    return func

def train():
    log_dir = "logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    best_model_path = os.path.join(log_dir, "best_model")
    last_model_path = os.path.join(log_dir, "last_model")

    # Create training environment
    train_env = gym.make('tetris-v1')
    train_env = FlattenObservation(train_env)  # Flatten observations if needed
    train_env = Monitor(train_env)  # Ensures logging and episode tracking

    # Create a separate evaluation environment
    eval_env = gym.make('tetris-v1')
    eval_env = FlattenObservation(eval_env)
    eval_env = Monitor(eval_env)  # Monitor ensures proper evaluation tracking

    model = PPO('MlpPolicy', train_env, verbose=True, tensorboard_log=log_dir, device='cuda', learning_rate=exp_schedule(2.5e-4))

    eval_callback = EvalCallback(
        eval_env,
        best_model_save_path=best_model_path,
        log_path=log_dir,
        eval_freq=10000,  # Evaluate every 10000 steps
        deterministic=True,
        render=False,
        n_eval_episodes=20,
        verbose=1
    )

    checkpoint_callback = CheckpointCallback(
        save_freq=10_000,
        save_path=last_model_path
    )

    model.learn(total_timesteps=10_000_000, callback=[eval_callback, checkpoint_callback])

if __name__ == '__main__':
    train()