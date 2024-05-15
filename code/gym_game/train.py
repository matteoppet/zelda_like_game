from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

import os

from envs.sprites_movements.avoid_obstacles_movements import Animal_environment

### HYPER PARAMETERS
TIMESTEPS = 1000000
N_CPU = 6
RENDER = None

def make_env():
    return Animal_environment(render_mode=None, obstacles=False)


env = DummyVecEnv([make_env for _ in range(N_CPU)])


MODELS_DIR = "trained_agent/models/PPO_MODELS"
LOGS_DIR = "trained_agent/logs/PPO_LOGS"

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)
    print("> Models dir created")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print("> Logs dir created")


model = PPO(
    "MlpPolicy",
    env,
    verbose=1,
    batch_size=4200,
    tensorboard_log=LOGS_DIR,
    device="cpu",
    n_steps=700
)

try:
    model.learn(
        total_timesteps=TIMESTEPS,
        tb_log_name="PPO",
        reset_num_timesteps=True
    )
except KeyboardInterrupt:
    print("Model training interrupted, model saved in the current timesteps")

model.save(f"{MODELS_DIR}/PPO_MODEL_{TIMESTEPS}")