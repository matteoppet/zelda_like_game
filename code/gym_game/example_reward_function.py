import numpy as np

last_distance = 100

def reward_function(
        agent_position,
        target_position,
        reached_redius=70,
        completion_reward=2000
):
    distance_from_target = np.linalg.norm(np.array(agent_position) - np.array(target_position))
    distance_from_target = distance_from_target - reached_redius

    if distance_from_target == 0:
        reward = completion_reward
    else:
        if distance_from_target < last_distance:
            reward = 1
        else:
            reward = -1.5

    print(f"Agent_position: {agent_position}")
    print(f"Target_position: {target_position}")
    print(f"Distance_from_target: {distance_from_target:.2f}")
    print(f"Reward: {reward:.2f}")

    return reward

agent_position = (200, 400)
target_position = (1500, 400)
reward = reward_function(agent_position, target_position)
print(f"Reward: {reward}")