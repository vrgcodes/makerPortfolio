import math
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp
import numpy as np
#Simulating the motion of a projectile under gravity in a vacuum

gravity = 9.81
initial_velocity = float(input("Enter the velocity of the object: "))
angle = float(input("Enter the angle to the horizontal : "))
angle_rad = math.radians(angle)


def projectile_motion(vel, theta):
    vel_X = vel*math.cos(theta)
    vel_y = vel*math.sin(theta)
    time_of_flight = (2*vel*math.sin(theta))/gravity
    time_to_maximum_height = (vel*math.sin(theta))/gravity
    time_values = np.linspace(0,time_of_flight)
    displacement_x_arr = []
    displacement_y_arr = []
    for time in time_values:
        displacement_x = vel_X*time
        displacement_y = (vel_y*time) - (0.5*gravity*(time**2))
        displacement_x_arr.append(displacement_x)
        displacement_y_arr.append(displacement_y)
    return displacement_x_arr, displacement_y_arr, time_of_flight, time_to_maximum_height

s_x = np.array(projectile_motion(initial_velocity, angle_rad)[0])
s_y = np.array(projectile_motion(initial_velocity, angle_rad)[1])

print("Time of flight = {:.2f} s".format(projectile_motion(initial_velocity, angle_rad)[2]))
print("Time to Maximum Height = {:.2f} s".format(projectile_motion(initial_velocity, angle_rad)[3]))
print("Range to Impact Zone = {:.2f} m".format(s_x[-1]))
print("Maximum Height = {:.2f}".format(max(s_y)))

def animate(frame):
    x_data = s_x[:frame+1]
    y_data = s_y[:frame+1]

    line.set_data(x_data, y_data)

    if frame == len(s_x)-1:
        animation.event_source.stop()

    return line,

fig, ax = plt.subplots()
ax.set_xlim(0,max(s_x)+(max(s_x)))
ax.set_ylim(0,max(s_x)+(max(s_y)))

line, = ax.plot([], [], label="Trajectory")

ax.legend()

animation = FuncAnimation(fig, animate, frames=len(s_x),interval=25,blit=True)
plt.show()

#Simulating the motion of a projectile under gravity considering the effects of air resistance (using https://scipython.com/book2/chapter-8-scipy/examples/a-projectile-with-air-resistance/)

gravity = 9.81
drag_coefficient = 0.47
density = 1.225
radius = 0.09
k = -0.5*drag_coefficient*density*math.pi*(radius**2)
mass = 17.60

initial_vel = float(input("Enter the initial velocity: "))
angle_2 = float(input("Enter the angle to the horizontal: "))
angle_2_rad = math.radians(angle_2)

def differential(time, u):
    x, vel_x2, z, vel_z2 = u
    speed = ((vel_x2**2)+(vel_z2**2))**0.5
    acceleration_x = (k*speed*vel_x2)/mass
    acceleration_z = ((k*speed*vel_z2)-(mass*gravity))/mass
    return vel_x2, acceleration_x, vel_z2, acceleration_z

u0 = 0, initial_vel*(math.cos(angle_2_rad)), 0, initial_vel*(math.sin(angle_2_rad))
t0, tf = 0, 50

def hit_target(t, u):
    return u[2]

hit_target.terminal = True
hit_target.direction = -1

def max_height(t, u):
    return u[3]

solution = solve_ivp(differential, (t0,tf), u0, dense_output=True, events=(hit_target,max_height)) 

time = np.linspace(0, solution.t_events[0][0], 100)

sol = solution.sol(time)

x, z = sol[0], sol[2]

print("Time of flight = {:.2f} s".format(solution.t_events[0][0]))
print("Time to Maximum Height = {:.2f} s".format(solution.t_events[1][0]))
print("Range to Impact Zone = {:.2f} m".format(x[-1]))
print("Maximum Height = {:.2f} m".format(max(z)))

s_x2 = np.array(x)
s_z2 = np.array(z)

def animate2(frame):
    x_data = s_x2[:frame+1]
    y_data = s_z2[:frame+1]

    line.set_data(x_data, y_data)

    if frame == len(s_x2)-1:
        animation2.event_source.stop()

    return line,

fig2, ax2 = plt.subplots()
ax2.set_xlim(0,max(s_x2)+(max(s_x2)))
ax2.set_ylim(0,max(s_z2)+(max(s_z2)))

line, = ax2.plot([], [], label="Trajectory")

ax2.legend()

animation2 = FuncAnimation(fig2, animate2, frames=len(s_x2),interval=25,blit=True)
plt.show()