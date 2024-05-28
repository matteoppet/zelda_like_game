from stable_baselines3 import PPO, A2C, SAC, DQN
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.callbacks import EvalCallback
from stable_baselines3.common.env_util import make_vec_env

import os

from envs.avoid_obstacles_movements import Animal_environment

### HYPER PARAMETERS
TIMESTEPS = 20000000
N_CPU = 6
RENDER = None
MODEL_USED = "PPO"

# def make_env():
#     return Animal_environment(render_mode=None, obstacles=False)

# env = DummyVecEnv([make_env for _ in range(N_CPU)])
# eval_env = DummyVecEnv([make_env for _ in range(N_CPU)])

env = make_vec_env(Animal_environment, n_envs=N_CPU)
MODELS_DIR = f"trained_agent/models/{MODEL_USED}_MODELS"
LOGS_DIR = f"trained_agent/logs/{MODEL_USED}_LOGS"

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)
    print("> Models dir created")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

    print("> Logs dir created")


# eval_callback = EvalCallback(eval_env, best_model_save_path='trained_agent/models/BEST_MODELS',
#     log_path='trained_agent/logs/A2C_LOGS', eval_freq=10000,
#     deterministic=True, render=False)


model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    tensorboard_log=LOGS_DIR,
    device="cpu",
)


try:
    model.learn(
        total_timesteps=TIMESTEPS,
        tb_log_name=MODEL_USED,
        reset_num_timesteps=True
    )
except KeyboardInterrupt:
    print("Model training interrupted, model saved in the current timesteps")

model.save(f"{MODELS_DIR}/{MODEL_USED}_MODEL")