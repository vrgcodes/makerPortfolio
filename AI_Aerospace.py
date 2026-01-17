import gymnasium as gym
import numpy as np
from stable_baselines3 import PPO
import matplotlib.pyplot as plt

class FlightControlEnv(gym.Env):
    def __init__(self):
        super().__init__()
        self.action_space = gym.spaces.Discrete(3)

        self.observation_space = gym.spaces.Box(
            low=np.array([-180.0, -50.0], dtype=np.float32),
            high=np.array([180.0, 50.0], dtype=np.float32),
        )

        self.angle = 0.0
        self.rate = 0.0
        self.target_angle = 0.0

        self.max_steps = 1000
        self.steps = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.angle = np.random.uniform(-15, 15)
        self.rate = 0.0
        self.steps = 0
        return np.array([self.angle, self.rate], dtype=np.float32), {}

    def step(self, action):
        self.steps += 1

        disturbance = np.random.normal(0, 1.0)
        self.rate += disturbance

        if action == 1:
            self.rate -= 2.0
        elif action == 2:
            self.rate += 2.0

        self.rate *= 0.9

        dt = 0.1
        self.angle += dt * self.rate

        error = self.angle - self.target_angle

        reward = -abs(error) - 0.01 * abs(self.rate)

        terminated = abs(error) < 0.1
        truncated = self.steps >= self.max_steps

        obs = np.array([self.angle, self.rate], dtype=np.float32)
        return obs, reward, terminated, truncated, {}

env = FlightControlEnv()
model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=50_000)

obs, _ = env.reset()
angles = []

for _ in range(300):
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = env.step(action)
    angles.append(obs[0])
    if terminated or truncated:
        break

plt.plot(angles)
plt.axhline(0, linestyle="--", label="Target Angle")
plt.xlabel("Time steps")
plt.ylabel("Angle (degrees)")
plt.legend()
plt.grid(True)
plt.show()
