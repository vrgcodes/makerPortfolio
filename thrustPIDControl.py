import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D



# Define the PID class
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
        D = self.kD * (error - self.prevError) / dt
        
        self.prevError = error
        correction = P + I + D

        return correction

dryMass = 0.906
propellant1Mass = 0.064
propellant2Mass = 0.064
g=9.81
totalMass = dryMass+propellant1Mass+propellant2Mass
burnTime = 3.4
I = 2.0  
arm_length = 0.5  
dragCoeff = 0.75
rho = 1.225
diameter = 0.1
area = np.pi * (diameter / 2) ** 2
pitchBackHeight = 10
pitchOverHeight = 20
tolerance = 2
pitchOverInitiated = False
angularVelUpdate = 0 
pidAngle = PID(kP=20, kI = 10, kD = 0.01)
massFlowRate = propellant1Mass/burnTime

timePoints = [0,0.2,0.4,0.43,0.6,0.8,1,1.2,1.4,1.6,1.8,2.0,2.2,2.4,2.6,2.8,3,3.2,3.4]
thrustPoints = [0,11,24,25.3,19,16.5,15.5, 15, 14.8, 14.7,14.4,14,13.8,13.5,13,13,13,12.8,0]

thrust_curve = interpolate.interp1d(timePoints, thrustPoints, kind='linear', fill_value="extrapolate")
dt = 0.1

resultantForces = []
resForceTime = []

thrustXVals = []


def rocketDynamics(state, t, fireTime):
    global pitchOverInitiated, angularVelUpdate
    currentFlightPathAngle, currentAngularVelocity, currentVerticalVelocity, currentHorizontalVelocity, vy, currentHeight, hx, hy = state
    currentFlightPathAngle = np.radians(currentFlightPathAngle)

    
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

    if not pitchOverInitiated and abs(currentHeight - pitchOverHeight) <= tolerance:
        pitchOverInitiated = True

    if pitchOverInitiated and t<3:
        targetFlightPathAngle = np.radians(30) 

        angleError = targetFlightPathAngle - currentFlightPathAngle
        kp_angular = 7 
        angularVelUpdate = kp_angular * angleError

        #in real situation, we would instruct the servo motor using pid to achieve the respective angle

    else:
        angularVelUpdate = 0

    if t >= burnTime+0.85 and t<6:
        correctiveAngle = -currentFlightPathAngle #motor angle
        targetFlightPathAngle = np.radians(0) 

        angleError = targetFlightPathAngle - currentFlightPathAngle
        kp_angular = 6  
        angularVelUpdate = kp_angular * angleError 

    thrustZ = F_thrust*np.cos(currentFlightPathAngle)
    thrustX = F_thrust*np.sin(currentFlightPathAngle)
    
    

    v = (currentVerticalVelocity**2+currentHorizontalVelocity**2)**0.5

    dragForce = 0.5 * rho * dragCoeff * area * v**2
    dragForceZ = dragForce*np.cos(currentFlightPathAngle)
    dragForceX = dragForce*np.sin(currentFlightPathAngle)

    dFlightPath_dt = angularVelUpdate
    dAngularVel_dt = 0
    dVz_dt = (thrustZ-(currentMass*g)-dragForceZ)/currentMass
    resultantForces.append(dVz_dt*currentMass)
    resForceTime.append(t)
    dVx_dt = (thrustX-dragForceX)/currentMass
    thrustXVals.append(dVx_dt)
    dVy_dt = 0
    dHz_dt = currentVerticalVelocity
    dHx_dt = currentHorizontalVelocity
    dHy_dt= 0

    return [np.degrees(dFlightPath_dt), dAngularVel_dt, dVz_dt, dVx_dt, dVy_dt, dHz_dt, dHx_dt, dHy_dt]

time = np.linspace(0, 10, 1000) 
initialFlightPath = 0
initialAngularVel = 0
vz0 = 0
vx0 = 0
vy0 = 0
hz0 = 0
hx0 = 0
hy0 = 0
fireTime = 6.35
initial_state = [initialFlightPath, initialAngularVel, vz0, vx0, vy0, hz0, hx0, hy0]

solution = odeint(rocketDynamics, initial_state, time, args=(fireTime,))

flightPath = solution[:, 0]
angularVel = solution[:, 1]
velZ = solution[:, 2]
velX = solution[:, 3]
velY = solution[:, 4]
distanceZ = solution[:, 5]
distanceX = solution[:, 6]
distanceY = solution[:, 7]

plt.figure(figsize=(12, 12))

# First plot: Resultant Forces
plt.subplot(4, 2, 1)
plt.plot(resForceTime, resultantForces, label="Force", color="g")
plt.xlabel("Time (s)")
plt.ylabel("Force (N)")
plt.legend()
plt.grid(True)

plt.subplot(4, 2, 2)
plt.plot(resForceTime, thrustXVals, label="Force", color="g")
plt.xlabel("Time (s)")
plt.ylabel("Horizontal Force (N)")
plt.legend()
plt.grid(True)

# Third plot: Flight Path
plt.subplot(4, 2, 3)
plt.plot(time, flightPath, label="Flight path (deg)", color="g")
plt.xlabel("Time (s)")
plt.ylabel("Flight path (deg)")
plt.legend()
plt.grid(True)

# Fourth plot: Vertical Velocity
plt.subplot(4, 2, 4)
plt.plot(time, velZ, label="Vertical Velocity (m/s)", color="g")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.grid(True)

# Fifth plot: Horizontal Velocity
plt.subplot(4, 2, 5)
plt.plot(time, velX, label="Horizontal Velocity (m/s)", color="g")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.legend()
plt.grid(True)

# Sixth plot: Vertical Distance
plt.subplot(4, 2, 6)
plt.plot(time, distanceZ, label="Vertical Distance (m)", color="g")
plt.xlabel("Time (s)")
plt.ylabel("Vertical Distance (m)")
plt.legend()
plt.grid(True)

# Seventh plot: Horizontal Distance
plt.subplot(4, 2, 7)
plt.plot(time, distanceX, label="Horizontal Distance (m)", color="g")
plt.xlabel("Time (s)")
plt.ylabel("Horizontal Distance (m)")
plt.legend()
plt.grid(True)

# Adjust layout to prevent overlap
plt.tight_layout()

# Show the combined plot
plt.show()

fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

ax.plot(distanceX, distanceY, distanceZ, label='Rocket Trajectory', color='b', lw=2)

ax.set_xlabel('Distance X (m)')
ax.set_ylabel('Distance Y (m)')
ax.set_zlabel('Distance Z (m)')
ax.set_title('3D Rocket Trajectory')

ax.legend()

plt.show()