from envs.sprites_movements.avoid_obstacles_movements import Animal_environment
from stable_baselines3.common.vec_env import DummyVecEnv


def make_env():
    return Animal_environment(render_mode=None, obstacles=False)

n_cpu = 6
env = DummyVecEnv([make_env for _ in range(n_cpu)])


from stable_baselines3 import DQN, PPO 
import os


path_model = "trained_agent/models/" + "PPO_MODELS" + "/PPO_MODEL"

model = PPO.load(
    path=path_model,
    env=env,
    device="cpu",
)


MODELS_DIR = f"trained_agent/models/PPO_MODELS"
LOGS_DIR = f"trained_agent/logs/PPO_MODELS"

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)
    print("> Models dir created")

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)
    print("> Logs dir created")


TIMESTEPS = 20000000
try:
    model.learn(
        total_timesteps=TIMESTEPS,
        tb_log_name="PPO",
        reset_num_timesteps=False
    )
except KeyboardInterrupt:
    print("Model stopped and save and the current TIMESTEP where it was.")

model.save(f"{MODELS_DIR}/PPO_MODEL")
