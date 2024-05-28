from project.code.gym_game.envs.avoid_obstacles_movements import Animal_environment
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.env_util import make_vec_env


# def make_env():
#     return Animal_environment(render_mode=None, obstacles=False)

n_cpu = 6
env = make_vec_env(Animal_environment, n_envs=n_cpu)


from stable_baselines3 import DQN, PPO, A2C
import os

MODEL_USED = "DQN"
path_model = "trained_agent/models/" + f"{MODEL_USED}_MODELS" + f"/{MODEL_USED}_MODEL"

model = DQN.load(
    path=path_model,
    env=env,
    device="cpu",
)


MODELS_DIR = f"trained_agent/models/{MODEL_USED}_MODELS"
LOGS_DIR = f"trained_agent/logs/{MODEL_USED}_LOGS"

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)
    print("> Models dir created")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print("> Logs dir created")


TIMESTEPS = 10000000
try:
    model.learn(
        total_timesteps=TIMESTEPS,
        tb_log_name=MODEL_USED,
        reset_num_timesteps=True,
        progress_bar=True
    )
except KeyboardInterrupt:
    print("Model stopped and save and the current TIMESTEP where it was.")

model.save(f"{MODELS_DIR}/{MODEL_USED}_MODEL")
