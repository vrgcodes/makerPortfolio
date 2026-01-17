import numpy as np
from scipy.optimize import differential_evolution

import matplotlib.pyplot as plt

class PID:
    def __init__(self, kP, kI, kD):
        self.kP = kP
        self.kI = kI
        self.kD = kD
        self.prevError = 0
        self.integral = 0

    def compute(self, setPoint, currentVal, dt):
        error = setPoint - currentVal

        P = self.kP * error
        self.integral += error * dt
        I = self.kI * self.integral
        D = self.kD * (error - self.prevError) / dt if dt > 0 else 0
        
        self.prevError = error
        correction = P+I+D

        return correction

def simulatePID(kp, ki, kd, target, current, time, dt):
    pid = PID(kP=kp, kI=ki, kD=kd)
    angles = []
    for t in time:
        disturbance = np.random.normal(0, 1)
        correct = pid.compute(target, current, dt)
        current += correct
        angles.append(current)
    return np.array(angles)


def costFunction(params, target, initial, time, dt):
    kp, ki, kd = params
    angles = simulatePID(kp, ki, kd, target, initial, time, dt)
    error = np.sum((angles - target)**2) / len(angles)  
    return error

targetAngle = 0
initialAngle = 60
dt = 0.05
totalTime = 10
time = np.arange(0, totalTime, dt)

initial_guess = [0.5, 10, 0.01]


result = differential_evolution(costFunction, bounds=[(0, 10), (0, 100), (0.01, 1)], args=(targetAngle, initialAngle, time, dt))

optimized_kp, optimized_ki, optimized_kd = result.x

optimized_angles = simulatePID(optimized_kp, optimized_ki, optimized_kd, targetAngle, initialAngle, time, dt)

plt.plot(time, optimized_angles, label="Optimized Rocket Angle (degrees)")
plt.axhline(targetAngle, color='r', linestyle='--', label="Target Angle")
plt.xlabel("Time (seconds)")
plt.ylabel("Angle (degrees)")
plt.legend()
plt.grid(True)
plt.show()

print(f"Optimized PID parameters: Kp = {optimized_kp:.2f}, Ki = {optimized_ki:.2f}, Kd = {optimized_kd:.2f}")
