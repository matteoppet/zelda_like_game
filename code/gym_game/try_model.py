from stable_baselines3 import PPO, A2C
from project.code.gym_game.envs.avoid_obstacles_movements import Animal_environment

if __name__ == "__main__":
    env = Animal_environment(render_mode="human")

    path_model = "trained_agent/models/A2C_MODELS/A2C_MODEL.zip"
    MODEL = A2C.load(path_model)

    obs, _info = env.reset()
    for i in range(10000):
        action, _states = MODEL.predict(obs)
        obs, reward, terminated, truncated, info = env.step(action)

        if terminated or truncated:
            obs, _info = env.reset()