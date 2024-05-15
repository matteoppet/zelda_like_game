import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pygame

from ....__init__ import SIZE_WINDOW
from ....helpers.sprites.animals import sensors_data


class BaseEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}
    window_size = SIZE_WINDOW

    def __init__(self, render_mode=None):
        super().__init__()

        self.action_space = spaces.Discrete(5)

        low = np.array([])
        high = np.array([])
        shape = (0,)
        self.observation_space = spaces.Box(low=low, high=high,
                                            shape=shape, dtype=np.float32)

        self.render_mode = render_mode
        self.window = None
        self.clock = None

        self.AGENT = self.AGENT_TO_TRAIN
        self.step_counter = 0
        self.max_step = 700

        self.last_position = None


    def _get_obs(self):
        obs = [
            self._agent_location[0],
            self._agent_location[1],
        ]

        for index in range(len(sensors_data)):
            obs.append(sensors_data[index+1]["distance_collision"])

        return np.array(obs)
    

    def random_target_point(self):
        x = np.random.randint(self.window_size[0])
        y = np.random.randint(self.window_size[1])

        # TODO: adjust to not spawn in a obstacle
        return (x,y)


    def step(self, action):
        self.step_counter += 1

        self.last_position = self._agent_location
        self.AGENT.actions(action)
        self._agent_location = self.AGENT.rect.center
        
        self.AGENT.sensors_position_update()
        self.AGENT.check_collision_sensors(self.borders_obstacles_group) # group sprites

        terminated = False
        truncated = False
        agent_crashed = self.AGENT.collisions_in_gym(self.borders_obstacles_group)
        target_reached = self.AGENT.target_reached(self._target_location)

        distance_from_target = np.linalg.norm(np.array([*self._agent_location]) - np.array([*self._target_location]))

        if agent_crashed:
            terminated = True

        if self.step_counter == self.max_step:
            truncated = True

        reward = self.get_reward(distance_from_target, target_reached, agent_crashed)

        observation = self._get_obs()
        info = {
            'new_state': self._agent_location,  # Example: provide the new state to the agent
            'distance_from_target': distance_from_target,
            'reward_details': {
                'raw_reward': reward  # Example: provide the raw reward value
            }
        }

        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, truncated, info


    def _render_frame(self):
        ...


    def close(self):
        ...



class Animal_environment(BaseEnv):
    def __init__(self, render_mode=None, obstacles=False):
        super().__init__()

        self.render_mode = render_mode

        if obstacles:
            self.create_world()

        self.borders_obstacles_group = pygame.sprite.Group()
        self.window_borders_obstacles()
    

    def window_borders_obstacles(self):

        info_obstacles = [
            (0, -50, self.window_size[0], 50), # up
            (0, self.window_size[1], self.window_size[0], 50), # down
            (-50, 0, -50, self.window_size[1]), # left
            (self.window_size[0], 0, 50, self.window_size[1]) # right
        ]

        for obstacle in info_obstacles:
            rect_sprite = pygame.Rect(*obstacle)

            self.borders_obstacles_group.add(rect_sprite)

    
    def get_reward(self, distance_target_point, target_reached, agent_crashed):
        reward = -distance_target_point

        if target_reached:
            reward = 4000

        if agent_crashed:
            reward = -5000

        return reward
    

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self._agent_location = self.AGENT.random_position_spawn()
        self._target_location = self.random_target_point()

        self.AGENT.sensors_position_update()
        self.AGENT.check_collision_sensors(self.borders_obstacles_group)

        self.step_counter = 0

        observation = self._get_obs()
        info = {
            'initial_state': self._agent_location
        }

        if self.render_mode == "human":
            self.render()

        return observation, info