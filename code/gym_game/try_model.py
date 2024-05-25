from stable_baselines3 import PPO
from envs.sprites_movements.avoid_obstacles_movements import Animal_environment

if __name__ == "__main__":
    env = Animal_environment(render_mode="human")

    path_model = "trained_agent/models/PPO_MODELS/PPO_MODEL.zip"
    MODEL = PPO.load(path_model)

    obs, _info = env.reset()
    for i in range(10000):
        action, _states = MODEL.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            obs, _info = env.reset()