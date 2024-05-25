import gymnasium as gym
import numpy as np
from gymnasium import spaces
import pygame

from project.code.helpers.sprites.animals import sensors_data
from project.code.helpers.sprites.animals import Base_animal

############### USEFULL CLASS
class Obstacles_sprites(pygame.sprite.Sprite):
    def __init__(self, size, pos):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface(size)
        self.image.fill("blue")
        self.rect = self.image.get_rect(topleft=pos)


class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.Surface((150, 150))
        self.image.fill("lightblue")
        self.rect = self.image.get_rect(center=(0,0))

    def regenerate_position(self):
        x = np.random.randint(0, 1600)
        y = np.random.randint(0, 960)

        self.rect.center = (x, y)

###################################


class BaseEnv(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 60}
    window_size = (1600, 960)

    def __init__(self, render_mode=None):
        super().__init__()

        self.action_space = spaces.Discrete(5)

        low = np.array([0 for _ in range(13)])
        high = np.array([self.window_size[0], self.window_size[1], self.window_size[0], self.window_size[1], 3000, 9999,9999,9999,9999,9999,9999,9999,9999])
        shape = (len(high),)
        self.observation_space = spaces.Box(low=low, high=high,
                                            shape=shape, dtype=np.float32)

        self.render_mode = render_mode
        self.window = None
        self.clock = None

        self.AGENT = self.AGENT_TO_TRAIN
        self.step_counter = 0
        self.max_step = 3000

        self.TARGET = Target()

        self.last_distance = 0


    def _get_obs(self):
        obs = [
            self._agent_location[0],
            self._agent_location[1],
            self._target_location[0],
            self._target_location[1],
            self._distance_from_target,
        ]

        for index in range(len(sensors_data)):
            obs.append(sensors_data[str(index+1)]["distance_collision"])

        return np.array(obs)

    def step(self, action):
        self.step_counter += 1

        self.AGENT.actions(action)
        self._agent_location = self.AGENT.rect.center
        
        self.AGENT.sensors_position_update()
        self.AGENT.check_collision_sensors(self.borders_obstacles_group) # group sprites

        self._distance_from_target = np.linalg.norm(np.array([*self._agent_location]) - np.array([*self._target_location]))
        self._distance_from_target = self._distance_from_target - self.TARGET.rect.width/2

        terminated = False
        truncated = False
        agent_crashed = self.AGENT.collisions_in_gym(self.borders_obstacles_group)
        target_reached = self.AGENT.target_reached(self.TARGET.rect)

        if agent_crashed:
            terminated = True

        if self.step_counter == self.max_step:
            truncated = True

        if target_reached:
            terminated = True

        reward = self.get_reward(target_reached, agent_crashed)

        observation = self._get_obs()
        info = {
            'new_state': self._agent_location,  # Example: provide the new state to the agent
            'distance_from_target': self._distance_from_target,
            'target_location': self._target_location,
            'reward_details': {
                'raw_reward': reward  # Example: provide the raw reward value
            }
        }

        if self.render_mode == "human":
            self._render_frame()

        return observation, reward, terminated, truncated, info


    def _render_frame(self):
        if self.window is None and self.render_mode == "human":
            pygame.init()
            pygame.display.init()
            pygame.display.set_caption("Training environment")

            self.window = pygame.display.set_mode(self.window_size)
            self.background = pygame.Surface(self.window_size)
            self.font = pygame.font.SysFont("calibri", 20)
        
        if self.clock is None and self.render_mode == "human":
            self.clock = pygame.time.Clock()

        if self.render_mode == "human":
            self.window.fill("#17181a")

            self.borders_obstacles_group.draw(self.window, self.background)

            self.AGENT.draw_sensors(self.window)
            self.window.blit(self.AGENT.image, self.AGENT.rect)

            for sensor in sensors_data:
                if sensors_data[sensor]["point_of_collision"] != None:
                    pygame.draw.circle(self.window, "red", sensors_data[sensor]["point_of_collision"], 3)

            self.window.blit(self.TARGET.image, self.TARGET.rect)

            pygame.draw.line(self.window, "white", self._agent_location, self._target_location, 2)

            pygame.event.pump()
            pygame.display.update()

            self.clock.tick(self.metadata["render_fps"])


    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()


class Animal_environment(BaseEnv):
    AGENT_TO_TRAIN = Base_animal()

    def __init__(self, render_mode=None, obstacles=False):
        super().__init__()

        self.render_mode = render_mode

        if obstacles:
            self.create_world()

        self.borders_obstacles_group = pygame.sprite.Group()
        self.window_borders_obstacles()
        self.last_distance = 0
    

    def window_borders_obstacles(self):
        info_obstacles = [
            (0, -50, self.window_size[0], 50), # up
            (0, self.window_size[1], self.window_size[0], 50), # down
            (-50, 0, 50, self.window_size[1]), # left
            (self.window_size[0], 0, 50, self.window_size[1]) # right
        ]

        for obstacle in info_obstacles:
            size = (obstacle[2], obstacle[3])
            pos = (obstacle[0], obstacle[1])
            sprite = Obstacles_sprites(size, pos)

            self.borders_obstacles_group.add(sprite)

    
    def get_reward(self, target_reached, agent_crashed):   
        completion_reward = 5000
        crash_penalty = -4000

        if self._distance_from_target <= 0:
            reward = completion_reward
        else:
            if self._distance_from_target < self.last_distance:
                reward = 1
            else:
                reward = -1

        if agent_crashed:
            reward = crash_penalty

        self.last_distance = self._distance_from_target

        return reward


    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        pos_start = self.AGENT.random_position_spawn(self.window_size)

        self.AGENT.rect.centerx = pos_start[0]
        self.AGENT.rect.centery = pos_start[1]
        
        self._agent_location = pos_start
        self.TARGET.regenerate_position()
        self._target_location = self.TARGET.rect.center

        self.AGENT.sensors_position_update()
        self.AGENT.check_collision_sensors(self.borders_obstacles_group)

        self._distance_from_target = np.linalg.norm(np.array([*self._agent_location]) - np.array([*self._target_location]))
        self._distance_from_target = self._distance_from_target - self.TARGET.rect.width/2

        self.step_counter = 0

        observation = self._get_obs()
        info = {
            'initial_state': self._agent_location,
            'initial_target_location': self._target_location,
        }

        if self.render_mode == "human":
            self._render_frame()

        return observation, info