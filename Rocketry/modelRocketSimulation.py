import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy import interpolate
from scipy.optimize import minimize
import math
import matplotlib.image as mpimg
import matplotlib.animation as animation


dryMass = 0.906
burnTime = 3.4
totalImpulse = 49.6
propellant1Mass = 0.064
propellant2Mass = 0.064
totalMass = dryMass+propellant1Mass+propellant2Mass
dragCoeff = 0.75
diameter = 0.09
rho = 1.225
g = 9.81

timePoints = [0,0.2,0.4,0.43,0.6,0.8,1,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3,3.2,3.4]
thrustPoints = [0,11,24,25.3,19,16.5,15.5, 15, 14.8, 14.7,14.4,14,13.8,13.5,13,13,13,12.8,0]

thrust_curve = interpolate.interp1d(timePoints, thrustPoints, kind='linear', fill_value="extrapolate")
# time_fine = np.linspace(0, 3.5, 1000)  # 1000 points between 0 and 6 seconds
# thrust_fine = thrust_curve(time_fine)
# # Plot the original thrust curve with data points
# plt.plot(timePoints, thrustPoints, 'o', label='Original Data', color='red')

# # Plot the interpolated thrust curve
# plt.plot(time_fine, thrust_fine, label='Interpolated Curve', color='blue')
# plt.xlabel('Time (s)')
# plt.ylabel('Thrust (N)')
# plt.title('Thrust vs Time (Interpolated)')
# plt.grid(True)
# plt.legend()

# # Show the plot
# plt.show()

area = np.pi*0.25*(diameter)**2
print(area)
massFlowRate = propellant1Mass/burnTime
time = np.linspace(0,burnTime,10000)
dragF = []
drafT =[]


def rocketDynamic(state, t, fireTime):
    v, h= state
    if t<burnTime:
        currentMass = totalMass-(massFlowRate*t)
        F_thrust = thrust_curve(t)
    elif t<fireTime:
        currentMass = (totalMass-propellant1Mass)
        F_thrust = 0
    elif t<fireTime+burnTime:
        currentMass = (totalMass-propellant1Mass)-(massFlowRate*(t-fireTime))
        F_thrust = thrust_curve(t-fireTime)
    else:
        currentMass = dryMass
        F_thrust=0
    
    dragForce = 0.5 * rho * dragCoeff * area * v**2
    dragF.append(dragForce)
    drafT.append(t)
    dv_dt = (F_thrust - dragForce) / currentMass - g
    
    dh_dt = v
    return [dv_dt, dh_dt]

def animate_rocket():
    v0 = 0
    h0 = 0
    time = np.linspace(0, 10, 1000) 

    fireTime1 = 6.35  # First firing time

    solution = odeint(rocketDynamic, [v0, h0], time, args=(fireTime1,))

    velocity = solution[:, 0]
    height = solution[:, 1]

    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(time, velocity, label='Velocity (m/s)', color='b')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.grid(True)
    plt.legend()

    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(drafT, dragF, label='Velocity (m/s)', color='b')
    plt.xlabel('Time (s)')
    plt.ylabel('Velocity (m/s)')
    plt.grid(True)
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(time, height, label='Height (m)', color='g')
    plt.xlabel('Time (s)')
    plt.ylabel('Height (m)')
    plt.grid(True)
    plt.legend()

    plt.show()
    rocket_img = mpimg.imread('rocket_image.jpg')

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim((0, 10))  
    ax.set_ylim((0, max(height) + 10))  
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Height (m)')
    ax.grid(True)

    rocket = ax.imshow(rocket_img, extent=[-0.5, 0.5, -5, 5], aspect='auto', zorder=10)
    time_text = ax.text(0.8, 0.95, '', transform=ax.transAxes)
    
    trajectory_line, = ax.plot([], [], 'o-', lw=2, label='Trajectory')

    x_traj = []
    y_traj = [] 

    def update(i):
        x_position = time[i]  
        y_position = height[i] 

        rocket_width = 1  
        rocket_height = 5 
        rocket.set_extent([
            x_position - rocket_width / 2,
            x_position + rocket_width / 2, 
            y_position - rocket_height / 2, 
            y_position + rocket_height / 2, 
        ])

        x_traj.append(x_position)
        y_traj.append(y_position)

        trajectory_line.set_data(x_traj, y_traj)

        time_text.set_text(f'Time: {time[i]:.2f}s')
        return rocket, trajectory_line, time_text
    ani = animation.FuncAnimation(fig, update, frames=len(time), interval=50, blit=True)

    plt.legend()
    plt.show()

animate_rocket()
