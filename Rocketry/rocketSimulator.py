import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import customtkinter as ctk
from PIL import Image, ImageTk
import mysql.connector as mysql
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from scipy import interpolate
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


HOST = "localhost"
DATABASE = "rocketmotors"
USER = "root"
PASSWORD = "T79N7g&$n"

dry_mass = ""
drag_coefficient = "0.75"
diameter = ""
no_of_motors = ""
motor_1 = ""
motor_2 = ""
pitch_over = "No"
pitch_over_height = ""
fireTime = ""
rho = 1.225
g = 9.81

conn = mysql.connect(host = HOST, database = DATABASE, user = USER, password = PASSWORD)
cursor = conn.cursor(buffered=True)

sqlMotorSelect = "SELECT idavailableMotors FROM availablemotors"
cursor.execute(sqlMotorSelect)
motors = cursor.fetchall()
availMotors = []
for motor in motors:
    availMotors.append(motor[0])


root = ctk.CTk()
root.title("Rocket Simulator")
root.geometry('1980x1080')

canvas = ctk.CTkCanvas(root, width=1920, height=1080, bd=0, highlightthickness=0)
canvas.pack(fill="both", expand=True)


background_image = ImageTk.PhotoImage(Image.open("image 53.jpg"))
canvas.create_image(-15, 0, image=background_image, anchor="nw")

canvas.create_rectangle(0, 0, 1920, 90, fill="#000000", outline="")

title = ctk.CTkLabel(
    root,
    text="Welcome to the Rocket Simulator!",
    font=('Comfortaa', 30, 'bold'),
    bg_color="#000000",
)
canvas.create_window(980, 50, window=title, anchor="center")  

# Create a frame within the canvas for scrolling
scrollable_frame_container = ctk.CTkFrame(root, fg_color="#2c2c2c", width=1200, height=800)
scrollable_frame_container.place(x=360, y=150)

scrollable_canvas = ctk.CTkCanvas(
    scrollable_frame_container,
    bg="#2c2c2c",
    width=1180,
    height=780,
    bd=0,
    highlightthickness=0
)
scrollable_canvas.pack(side="left", fill="both", expand=True)

# Add a vertical scrollbar
scrollbar = Scrollbar(scrollable_frame_container, orient="vertical", command=scrollable_canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configure canvas scrolling
scrollable_canvas.configure(yscrollcommand=scrollbar.set)
scrollable_canvas.bind(
    "<Configure>",
    lambda e: scrollable_canvas.configure(scrollregion=scrollable_canvas.bbox("all")),
)

# Create an inner frame to hold widgets
inner_frame = ctk.CTkFrame(scrollable_canvas, fg_color="#2c2c2c", width=1180, height=780)
scrollable_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Function to create input fields inside the scrollable frame
def create_input_field(frame, label_text, entry_variable, y_position):
    label = ctk.CTkLabel(
        frame,
        text=label_text,
        text_color="#FFFFFF",
        font=('Comfortaa', 16, 'bold'),
        padx=10,
        pady=10,
    )
    entry = ctk.CTkEntry(
        frame,
        textvariable=entry_variable,
        width=350,
        height=40,
        border_width=5,
        text_color="#FFFFFF",
        font=('Comfortaa', 16),
    )
    label.grid(row=y_position, column=0, padx=20, pady=10, sticky="w")
    entry.grid(row=y_position, column=1, padx=20, pady=10)
    return entry

# Add input fields to the inner frame
dryMassVar = StringVar()
dryMassVar.set("")
dryMassEntry = create_input_field(inner_frame, "Enter the dry mass: ", dryMassVar, 0)

dragCoeffVar = StringVar()
dragCoeffVar.set("0.75")
dragCoeffEntry = create_input_field(inner_frame, "Enter the drag coefficient (assumed to be 0.75): ", dragCoeffVar, 1)

diameterVar = StringVar()
diameterVar.set("")
diameterEntry = create_input_field(inner_frame, "Enter the diameter: ", diameterVar, 2)

noOfMotorsVar = StringVar()
noOfMotorsVar.set("")
noOfMotorsEntry = create_input_field(inner_frame, "Enter the number of motors used: ", noOfMotorsVar, 3)

def resize_image(image, width, height):
    return image.resize((width, height), Image.ANTIALIAS)

def rocketOneStageNP(thrustPoints, timePoints, dryMass, area, burnTime, propellantMass, totalMass, dragCoeff):

    
    thrust_curve = interpolate.interp1d(timePoints, thrustPoints, kind='linear', fill_value="extrapolate")

    resultantForces = []
    resForceTime = []

    thrustXVals = []
    dt = 0.1

    massFlowRate = propellantMass/burnTime
    tolerance = 2

    def rocketDynamics(state, t):
        currentFlightPathAngle, currentAngularVelocity, currentVerticalVelocity, currentHorizontalVelocity, vy, currentHeight, hx, hy = state
        currentFlightPathAngle = np.radians(currentFlightPathAngle)

        
        if t<burnTime:
            currentMass = totalMass-(massFlowRate*t)
            F_thrust = thrust_curve(t)
        else:
            currentMass = dryMass
            F_thrust=0


        thrustZ = F_thrust*np.cos(currentFlightPathAngle)
        thrustX = F_thrust*np.sin(currentFlightPathAngle)
        
        

        v = (currentVerticalVelocity**2+currentHorizontalVelocity**2)**0.5

        dragForce = 0.5 * rho * dragCoeff * area * v**2
        dragForceZ = dragForce*np.cos(currentFlightPathAngle)
        dragForceX = dragForce*np.sin(currentFlightPathAngle)

        dFlightPath_dt = 0
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
    initial_state = [initialFlightPath, initialAngularVel, vz0, vx0, vy0, hz0, hx0, hy0]

    solution = odeint(rocketDynamics, initial_state, time)

    flightPath = solution[:, 0]
    angularVel = solution[:, 1]
    velZ = solution[:, 2]
    velX = solution[:, 3]
    velY = solution[:, 4]
    distanceZ = solution[:, 5]
    distanceX = solution[:, 6]
    distanceY = solution[:, 7]

    plt.figure()
    plt.plot(time, velZ, label="Vertical Velocity (m/s)", color="g")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velZ_plot.png")

    plt.figure()
    plt.plot(time, flightPath, label="Flight Path", color="b")
    plt.xlabel("Time (s)")
    plt.ylabel("Flight Path (degrees)")
    plt.legend()
    plt.grid(True)
    plt.savefig("flightPath_plot.png")

    plt.figure()
    plt.plot(time, angularVel, label="Angular Velocity (rad/s)", color="r")
    plt.xlabel("Time (s)")
    plt.ylabel("Angular Velocity (rad/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("angularVel_plot.png")

    plt.figure()
    plt.plot(time, velX, label="Horizontal Velocity (m/s)", color="c")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velX_plot.png")

    plt.figure()
    plt.plot(time, velY, label="Velocity in Y Direction (m/s)", color="m")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velY_plot.png")

    plt.figure()
    plt.plot(time, distanceZ, label="Distance in Z (m)", color="y")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceZ_plot.png")

    plt.figure()
    plt.plot(time, distanceX, label="Distance in X (m)", color="orange")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceX_plot.png")

    plt.figure()
    plt.plot(time, distanceY, label="Distance in Y (m)", color="purple")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceY_plot.png")

    plotImage = ImageTk.PhotoImage(resize_image(Image.open("flightPath_plot.png"), 400, 300))
    canvas.create_image(50, 200, image=plotImage, anchor="nw")
    canvas.plotImage = plotImage

    plotImage1 = ImageTk.PhotoImage(resize_image(Image.open("angularVel_plot.png"), 400, 300))
    canvas.create_image(550, 200, image=plotImage1, anchor="nw")
    canvas.plotImage1 = plotImage1

    plotImage2 = ImageTk.PhotoImage(resize_image(Image.open("velX_plot.png"), 400, 300))
    canvas.create_image(1000, 200, image=plotImage2, anchor="nw")
    canvas.plotImage2 = plotImage2

    plotImage3 = ImageTk.PhotoImage(resize_image(Image.open("velY_plot.png"), 400, 300))
    canvas.create_image(1450, 200, image=plotImage3, anchor="nw")
    canvas.plotImage3 = plotImage3

    plotImage4 = ImageTk.PhotoImage(resize_image(Image.open("velZ_plot.png"), 400, 300))
    canvas.create_image(50, 550, image=plotImage4, anchor="nw")
    canvas.plotImage4 = plotImage4

    plotImage5 = ImageTk.PhotoImage(resize_image(Image.open("distanceY_plot.png"), 400, 300))
    canvas.create_image(550, 550, image=plotImage5, anchor="nw")
    canvas.plotImage5 = plotImage5

    plotImage6 = ImageTk.PhotoImage(resize_image(Image.open("distanceX_plot.png"), 400, 300))
    canvas.create_image(1000, 550, image=plotImage6, anchor="nw")
    canvas.plotImage6 = plotImage6

    plotImage7 = ImageTk.PhotoImage(resize_image(Image.open("distanceZ_plot.png"), 400, 300))
    canvas.create_image(1450, 550, image=plotImage7, anchor="nw")
    canvas.plotImage7 = plotImage7


def rocketOneStageP(thrustPoints, timePoints, dryMass, area, burnTime, propellantMass, totalMass, dragCoeff, pitchOverHeight):

    global pitchOverInitiated, angularVelUpdate
    thrust_curve = interpolate.interp1d(timePoints, thrustPoints, kind='linear', fill_value="extrapolate")

    resultantForces = []
    resForceTime = []

    thrustXVals = []
    dt = 0.1
    angularVelUpdate = 0

    tolerance = 2
    pitchOverInitiated = False

    massFlowRate = propellantMass/burnTime

    def rocketDynamics(state, t):
        global angularVelUpdate, pitchOverInitiated
        currentFlightPathAngle, currentAngularVelocity, currentVerticalVelocity, currentHorizontalVelocity, vy, currentHeight, hx, hy = state
        currentFlightPathAngle = np.radians(currentFlightPathAngle)

        
        if t<burnTime:
            currentMass = totalMass-(massFlowRate*t)
            F_thrust = thrust_curve(t)
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
    initial_state = [initialFlightPath, initialAngularVel, vz0, vx0, vy0, hz0, hx0, hy0]

    solution = odeint(rocketDynamics, initial_state, time)

    flightPath = solution[:, 0]
    angularVel = solution[:, 1]
    velZ = solution[:, 2]
    velX = solution[:, 3]
    velY = solution[:, 4]
    distanceZ = solution[:, 5]
    distanceX = solution[:, 6]
    distanceY = solution[:, 7]


    plt.figure()
    plt.plot(time, velZ, label="Vertical Velocity (m/s)", color="g")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velZ_plot.png")


    plt.figure()
    plt.plot(time, flightPath, label="Flight Path", color="b")
    plt.xlabel("Time (s)")
    plt.ylabel("Flight Path (degrees)")
    plt.legend()
    plt.grid(True)
    plt.savefig("flightPath_plot.png")

    plt.figure()
    plt.plot(time, angularVel, label="Angular Velocity (rad/s)", color="r")
    plt.xlabel("Time (s)")
    plt.ylabel("Angular Velocity (rad/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("angularVel_plot.png")

    plt.figure()
    plt.plot(time, velX, label="Horizontal Velocity (m/s)", color="c")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velX_plot.png")

    plt.figure()
    plt.plot(time, velY, label="Velocity in Y Direction (m/s)", color="m")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velY_plot.png")

    plt.figure()
    plt.plot(time, distanceZ, label="Distance in Z (m)", color="y")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceZ_plot.png")

    plt.figure()
    plt.plot(time, distanceX, label="Distance in X (m)", color="orange")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceX_plot.png")

    plt.figure()
    plt.plot(time, distanceY, label="Distance in Y (m)", color="purple")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceY_plot.png")

    plotImage = ImageTk.PhotoImage(resize_image(Image.open("flightPath_plot.png"), 400, 300))
    canvas.create_image(50, 200, image=plotImage, anchor="nw")
    canvas.plotImage = plotImage

    plotImage1 = ImageTk.PhotoImage(resize_image(Image.open("angularVel_plot.png"), 400, 300))
    canvas.create_image(550, 200, image=plotImage1, anchor="nw")
    canvas.plotImage1 = plotImage1

    plotImage2 = ImageTk.PhotoImage(resize_image(Image.open("velX_plot.png"), 400, 300))
    canvas.create_image(1000, 200, image=plotImage2, anchor="nw")
    canvas.plotImage2 = plotImage2

    plotImage3 = ImageTk.PhotoImage(resize_image(Image.open("velY_plot.png"), 400, 300))
    canvas.create_image(1450, 200, image=plotImage3, anchor="nw")
    canvas.plotImage3 = plotImage3

    plotImage4 = ImageTk.PhotoImage(resize_image(Image.open("velZ_plot.png"), 400, 300))
    canvas.create_image(50, 550, image=plotImage4, anchor="nw")
    canvas.plotImage4 = plotImage4

    plotImage5 = ImageTk.PhotoImage(resize_image(Image.open("distanceY_plot.png"), 400, 300))
    canvas.create_image(550, 550, image=plotImage5, anchor="nw")
    canvas.plotImage5 = plotImage5

    plotImage6 = ImageTk.PhotoImage(resize_image(Image.open("distanceX_plot.png"), 400, 300))
    canvas.create_image(1000, 550, image=plotImage6, anchor="nw")
    canvas.plotImage6 = plotImage6

    plotImage7 = ImageTk.PhotoImage(resize_image(Image.open("distanceZ_plot.png"), 400, 300))
    canvas.create_image(1450, 550, image=plotImage7, anchor="nw")
    canvas.plotImage7 = plotImage7

def rocketTwoStageNP(thrustPoints, timePoints, dryMass, area, burnTime1, propellantMass1, burnTime2, propellantMass2, totalMass, dragCoeff, fireTime):



    thrust_curve = interpolate.interp1d(timePoints, thrustPoints, kind='linear', fill_value="extrapolate")

    resultantForces = []
    resForceTime = []

    thrustXVals = []
    dt = 0.1

    massFlowRate1 = propellantMass1/burnTime1
    massFlowRate2 = propellantMass2/burnTime2
    tolerance = 2

    def rocketDynamics(state, t):
        currentFlightPathAngle, currentAngularVelocity, currentVerticalVelocity, currentHorizontalVelocity, vy, currentHeight, hx, hy = state
        currentFlightPathAngle = np.radians(currentFlightPathAngle)

        
        if t<burnTime1:
            currentMass = totalMass-(massFlowRate1*t)
            F_thrust = thrust_curve(t)
        elif t<fireTime:
            currentMass = (totalMass-propellantMass1)
            F_thrust = 0
        elif t<fireTime+burnTime2:
            currentMass = (totalMass-propellantMass1)-(massFlowRate2*(t-fireTime))
            F_thrust = thrust_curve(t-fireTime)
        else:
            currentMass = dryMass
            F_thrust=0

        thrustZ = F_thrust*np.cos(currentFlightPathAngle)
        thrustX = F_thrust*np.sin(currentFlightPathAngle)

        v = (currentVerticalVelocity**2+currentHorizontalVelocity**2)**0.5

        dragForce = 0.5 * rho * dragCoeff * area * v**2
        dragForceZ = dragForce*np.cos(currentFlightPathAngle)
        dragForceX = dragForce*np.sin(currentFlightPathAngle)

        dFlightPath_dt = 0
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
    initial_state = [initialFlightPath, initialAngularVel, vz0, vx0, vy0, hz0, hx0, hy0]

    solution = odeint(rocketDynamics, initial_state, time)

    flightPath = solution[:, 0]
    angularVel = solution[:, 1]
    velZ = solution[:, 2]
    velX = solution[:, 3]
    velY = solution[:, 4]
    distanceZ = solution[:, 5]
    distanceX = solution[:, 6]
    distanceY = solution[:, 7]

    plt.figure()
    plt.plot(time, velZ, label="Vertical Velocity (m/s)", color="g")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velZ_plot.png")

    plt.figure()
    plt.plot(time, flightPath, label="Flight Path", color="b")
    plt.xlabel("Time (s)")
    plt.ylabel("Flight Path (degrees)")
    plt.legend()
    plt.grid(True)
    plt.savefig("flightPath_plot.png")

    plt.figure()
    plt.plot(time, angularVel, label="Angular Velocity (rad/s)", color="r")
    plt.xlabel("Time (s)")
    plt.ylabel("Angular Velocity (rad/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("angularVel_plot.png")

    plt.figure()
    plt.plot(time, velX, label="Horizontal Velocity (m/s)", color="c")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velX_plot.png")

    plt.figure()
    plt.plot(time, velY, label="Velocity in Y Direction (m/s)", color="m")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velY_plot.png")

    plt.figure()
    plt.plot(time, distanceZ, label="Distance in Z (m)", color="y")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceZ_plot.png")

    plt.figure()
    plt.plot(time, distanceX, label="Distance in X (m)", color="orange")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceX_plot.png")

    plt.figure()
    plt.plot(time, distanceY, label="Distance in Y (m)", color="purple")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceY_plot.png")

    plotImage = ImageTk.PhotoImage(resize_image(Image.open("flightPath_plot.png"), 400, 300))
    canvas.create_image(50, 200, image=plotImage, anchor="nw")
    canvas.plotImage = plotImage

    plotImage1 = ImageTk.PhotoImage(resize_image(Image.open("angularVel_plot.png"), 400, 300))
    canvas.create_image(550, 200, image=plotImage1, anchor="nw")
    canvas.plotImage1 = plotImage1

    plotImage2 = ImageTk.PhotoImage(resize_image(Image.open("velX_plot.png"), 400, 300))
    canvas.create_image(1000, 200, image=plotImage2, anchor="nw")
    canvas.plotImage2 = plotImage2

    plotImage3 = ImageTk.PhotoImage(resize_image(Image.open("velY_plot.png"), 400, 300))
    canvas.create_image(1450, 200, image=plotImage3, anchor="nw")
    canvas.plotImage3 = plotImage3

    plotImage4 = ImageTk.PhotoImage(resize_image(Image.open("velZ_plot.png"), 400, 300))
    canvas.create_image(50, 550, image=plotImage4, anchor="nw")
    canvas.plotImage4 = plotImage4

    plotImage5 = ImageTk.PhotoImage(resize_image(Image.open("distanceY_plot.png"), 400, 300))
    canvas.create_image(550, 550, image=plotImage5, anchor="nw")
    canvas.plotImage5 = plotImage5

    plotImage6 = ImageTk.PhotoImage(resize_image(Image.open("distanceX_plot.png"), 400, 300))
    canvas.create_image(1000, 550, image=plotImage6, anchor="nw")
    canvas.plotImage6 = plotImage6

    plotImage7 = ImageTk.PhotoImage(resize_image(Image.open("distanceZ_plot.png"), 400, 300))
    canvas.create_image(1450, 550, image=plotImage7, anchor="nw")
    canvas.plotImage7 = plotImage7

def rocketTwoStageP(thrustPoints, timePoints, dryMass, area, burnTime1, propellantMass1, burnTime2, propellantMass2, totalMass, dragCoeff, fireTime, pitchOverHeight):
    global pitchOverInitiated, angularVelUpdate
    thrust_curve = interpolate.interp1d(timePoints, thrustPoints, kind='linear', fill_value="extrapolate")

    resultantForces = []
    resForceTime = []

    thrustXVals = []
    dt = 0.1

    massFlowRate1 = propellantMass1/burnTime1
    massFlowRate2 = propellantMass2/burnTime2
    tolerance = 2

    pitchOverInitiated = False
    angularVelUpdate=0

    def rocketDynamics(state, t):
        global pitchOverInitiated, angularVelUpdate
        currentFlightPathAngle, currentAngularVelocity, currentVerticalVelocity, currentHorizontalVelocity, vy, currentHeight, hx, hy = state
        currentFlightPathAngle = np.radians(currentFlightPathAngle)

        
        if t<burnTime1:
            currentMass = totalMass-(massFlowRate1*t)
            F_thrust = thrust_curve(t)
        elif t<fireTime:
            currentMass = (totalMass-propellantMass1)
            F_thrust = 0
        elif t<fireTime+burnTime2:
            currentMass = (totalMass-propellantMass1)-(massFlowRate2*(t-fireTime))
            F_thrust = thrust_curve(t-fireTime)
        else:
            currentMass = dryMass
            F_thrust=0

        if not pitchOverInitiated and abs(currentHeight - pitchOverHeight) <= tolerance:
            pitchOverInitiated = True

        if pitchOverInitiated and t<(burnTime1-0.4):
            targetFlightPathAngle = np.radians(30) 

            angleError = targetFlightPathAngle - currentFlightPathAngle
            kp_angular = 7 
            angularVelUpdate = kp_angular * angleError

            #in real situation, we would instruct the servo motor using pid to achieve the respective angle

        else:
            angularVelUpdate = 0

        if t >= burnTime2+0.85 and t<((burnTime1+burnTime2)):
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
    initial_state = [initialFlightPath, initialAngularVel, vz0, vx0, vy0, hz0, hx0, hy0]

    solution = odeint(rocketDynamics, initial_state, time)

    flightPath = solution[:, 0]
    angularVel = solution[:, 1]
    velZ = solution[:, 2]
    velX = solution[:, 3]
    velY = solution[:, 4]
    distanceZ = solution[:, 5]
    distanceX = solution[:, 6]
    distanceY = solution[:, 7]

    plt.figure()
    plt.plot(time, velZ, label="Vertical Velocity (m/s)", color="g")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velZ_plot.png")

    plt.figure()
    plt.plot(time, flightPath, label="Flight Path", color="b")
    plt.xlabel("Time (s)")
    plt.ylabel("Flight Path (degrees)")
    plt.legend()
    plt.grid(True)
    plt.savefig("flightPath_plot.png")

    plt.figure()
    plt.plot(time, angularVel, label="Angular Velocity (rad/s)", color="r")
    plt.xlabel("Time (s)")
    plt.ylabel("Angular Velocity (rad/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("angularVel_plot.png")

    plt.figure()
    plt.plot(time, velX, label="Horizontal Velocity (m/s)", color="c")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velX_plot.png")

    plt.figure()
    plt.plot(time, velY, label="Velocity in Y Direction (m/s)", color="m")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.legend()
    plt.grid(True)
    plt.savefig("velY_plot.png")

    plt.figure()
    plt.plot(time, distanceZ, label="Distance in Z (m)", color="y")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceZ_plot.png")

    plt.figure()
    plt.plot(time, distanceX, label="Distance in X (m)", color="orange")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceX_plot.png")

    plt.figure()
    plt.plot(time, distanceY, label="Distance in Y (m)", color="purple")
    plt.xlabel("Time (s)")
    plt.ylabel("Distance (m)")
    plt.legend()
    plt.grid(True)
    plt.savefig("distanceY_plot.png")

    plotImage = ImageTk.PhotoImage(resize_image(Image.open("flightPath_plot.png"), 400, 300))
    canvas.create_image(50, 200, image=plotImage, anchor="nw")
    canvas.plotImage = plotImage

    plotImage1 = ImageTk.PhotoImage(resize_image(Image.open("angularVel_plot.png"), 400, 300))
    canvas.create_image(550, 200, image=plotImage1, anchor="nw")
    canvas.plotImage1 = plotImage1

    plotImage2 = ImageTk.PhotoImage(resize_image(Image.open("velX_plot.png"), 400, 300))
    canvas.create_image(1000, 200, image=plotImage2, anchor="nw")
    canvas.plotImage2 = plotImage2

    plotImage3 = ImageTk.PhotoImage(resize_image(Image.open("velY_plot.png"), 400, 300))
    canvas.create_image(1450, 200, image=plotImage3, anchor="nw")
    canvas.plotImage3 = plotImage3

    plotImage4 = ImageTk.PhotoImage(resize_image(Image.open("velZ_plot.png"), 400, 300))
    canvas.create_image(50, 550, image=plotImage4, anchor="nw")
    canvas.plotImage4 = plotImage4

    plotImage5 = ImageTk.PhotoImage(resize_image(Image.open("distanceY_plot.png"), 400, 300))
    canvas.create_image(550, 550, image=plotImage5, anchor="nw")
    canvas.plotImage5 = plotImage5

    plotImage6 = ImageTk.PhotoImage(resize_image(Image.open("distanceX_plot.png"), 400, 300))
    canvas.create_image(1000, 550, image=plotImage6, anchor="nw")
    canvas.plotImage6 = plotImage6

    plotImage7 = ImageTk.PhotoImage(resize_image(Image.open("distanceZ_plot.png"), 400, 300))
    canvas.create_image(1450, 550, image=plotImage7, anchor="nw")
    canvas.plotImage7 = plotImage7

def displayAllValues():
    title.destroy()
    scrollable_frame_container.destroy()
    sqlMotor1Info = "SELECT thrustValues, timeValues, burnTime, mass FROM availablemotors WHERE idavailableMotors=%s"
    cursor.execute(sqlMotor1Info, (motor_1,))
    thrust1Val = [] 
    time1Val = [] 
    burnTime1 = 0
    propellant1Mass = 0
    dryMass = float(dry_mass)
    area = (np.pi)*(float(diameter)/2)**2
    pitchOverHeight = -1
    


    for data in cursor.fetchall():
        thrust1Str = data[0]
        time1Str = data[1]
        burnTime1 = data[2]
        propellant1Mass = data[3]

        thrust1Val = [float(value) for value in thrust1Str.split(',')]
        time1Val = [float(value) for value in time1Str.split(',')]

    totalMass = dryMass+propellant1Mass

    if pitch_over == "Yes":
        pitchOverHeight = float(pitch_over_height)
        rocketOneStageP(thrust1Val, time1Val, dryMass, area, burnTime1, propellant1Mass, totalMass, float(drag_coefficient), pitchOverHeight)
    else:
        rocketOneStageNP(thrust1Val, time1Val, dryMass, area,burnTime1, propellant1Mass, totalMass, float(drag_coefficient))

    if int(no_of_motors) == 2:
        sqlMotor2Info = "SELECT thrustValues, timeValues, burnTime, mass FROM availablemotors WHERE idavailableMotors=%s"
        cursor.execute(sqlMotor2Info, (motor_2,))

        thrust2Val = [] 
        time2Val = []   
        burnTime2 = 0
        propellant2Mass = 0

        for data in cursor.fetchall():
            thrust2Str = data[0]
            time2Str = data[1]
            burnTime2 = data[2]
            propellant2Mass = data[3]

            thrust2Val = [float(value) for value in thrust2Str.split(',')]
            time2Val = [float(value) for value in time2Str.split(',')]

        totalMass = dryMass+propellant1Mass+propellant2Mass

        if pitch_over == "Yes":
            rocketTwoStageP(thrust2Val, time2Val, dryMass, area, float(burnTime1), float(propellant1Mass), float(burnTime2), float(propellant2Mass), totalMass, float(drag_coefficient), float(fireTime), pitchOverHeight)
        else:
            rocketTwoStageNP(thrust2Val, time2Val, dryMass, area, float(burnTime1), float(propellant1Mass), float(burnTime2), float(propellant2Mass), totalMass, float(drag_coefficient), float(fireTime))
    
def pitch_over_info():
    pitchHeightVar = ctk.StringVar()
    pitchHeightVar.set("")

    # Pitch-over Height label
    pitchHeightLabel = ctk.CTkLabel(
        inner_frame, 
        text="Enter the height at which pitch-over maneuver begins:", 
        text_color="#FFFFFF", 
        padx=10,
        pady=10,
        font=('Comfortaa', 16, 'bold')
    )
    pitchHeightLabel.grid(row=9, column=0, padx=20, pady=10, sticky="w")

    # Pitch-over Height entry field
    pitchHeightEntry = ctk.CTkEntry(
        inner_frame, 
        textvariable=pitchHeightVar, 
        width=350, 
        height=40, 
        border_width=5, 
        font=('Comfortaa', 16),
        text_color="#FFFFFF"
    )
    pitchHeightEntry.grid(row=9, column=1, padx=20, pady=10)

    # Define the action for the confirm button
    def get_pitch_over_value():
        confirm_button.destroy()
        global pitch_over_height
        pitch_over_height = pitchHeightVar.get()
        displayAllValues()

    # Confirm button
    confirm_button = ctk.CTkButton(
        inner_frame, 
        text="Confirm Pitch-over Height", 
        command=get_pitch_over_value, 
        text_color="#FFFFFF", 
        font=('Comfortaa', 16, 'bold')
    )
    confirm_button.grid(row=10, column=0, columnspan=2, pady=20)

def motor_selection():
    motorSelectButton.destroy()
    global motor_1, motor_2, no_of_motors, fireTime

    try:
        no_of_motors = int(noOfMotorsVar.get())
    except ValueError:
        ctk.CTkMessagebox.show_error("Error", "Please enter a valid number for motors.")
        return

    motor1Var = ctk.StringVar()
    motor1Var.set(availMotors[0])

    motor1Label = ctk.CTkLabel(
        inner_frame, text="Select motor 1:",
        text_color="#FFFFFF",
        font=('Comfortaa', 16, 'bold'),
        padx=10,
        pady=10
    )
    motor1Menu = ctk.CTkOptionMenu(
        inner_frame, variable=motor1Var,
        values=availMotors,
        dropdown_font=('Comfortaa', 16),
        text_color="#FFFFFF"
    )
    motor1Label.grid(row=5, column=0, padx=20, pady=10, sticky="w")
    motor1Menu.grid(row=5, column=1, padx=20, pady=10)

    if no_of_motors == 2:
        motor2Var = ctk.StringVar()
        motor2Var.set(availMotors[0]) 

        motor2Label = ctk.CTkLabel(
            inner_frame, text="Select motor 2:",
            text_color="#FFFFFF",
            font=('Comfortaa', 16, 'bold'),
            padx=10,
            pady=10
        )
        motor2Menu = ctk.CTkOptionMenu(
            inner_frame, variable=motor2Var,
            values=availMotors,
            dropdown_font=('Comfortaa', 16),
            text_color="#FFFFFF"
        )
        motor2Label.grid(row=6, column=0, padx=20, pady=10, sticky="w")
        motor2Menu.grid(row=6, column=1, padx=20, pady=10)

        secondFireTime = ctk.StringVar()
        secondFireTime.set("")
        secondFireTimeLabel = ctk.CTkLabel(
            inner_frame, text="Enter the ignition time of the second motor:",
            text_color="#FFFFFF",
            font=('Comfortaa', 16, 'bold'),
            padx=10,
            pady=10
        )
        secondFireTimeEntry = ctk.CTkEntry(
            inner_frame, textvariable=secondFireTime,
            width=350,
            height=40,
            border_width=5,
            font=('Comfortaa', 16),
            text_color="#FFFFFF"
        )
        secondFireTimeLabel.grid(row=7, column=0, padx=20, pady=10, sticky="w")
        secondFireTimeEntry.grid(row=7, column=1, padx=20, pady=10)

        def get_motor_values():
            global motor_1, motor_2, dry_mass, drag_coefficient, diameter, fireTime
            confirmButton.destroy()
            fireTime = secondFireTime.get()
            motor_1 = motor1Var.get()
            motor_2 = motor2Var.get()
            dry_mass = dryMassEntry.get()
            drag_coefficient = dragCoeffEntry.get()
            diameter = diameterEntry.get()
            pitch_over_question()

    else:
        def get_motor_values():
            global motor_1, dry_mass, drag_coefficient, diameter
            confirmButton.destroy()
            dry_mass = dryMassEntry.get()
            drag_coefficient = dragCoeffEntry.get()
            diameter = diameterEntry.get()
            motor_1 = motor1Var.get()
            pitch_over_question()

    confirmButton = ctk.CTkButton(
        inner_frame, text="Confirm Motor Selection",
        command=get_motor_values,
        text_color="#FFFFFF",
        font=('Comfortaa', 16, 'bold')
    )
    confirmButton.grid(row=8, column=0, columnspan=2, pady=20)



def motor_info_button():
    motor_selection()

def pitch_over_question():
    global pitch_over
    pitch_over_var = ctk.StringVar()
    pitch_over_var.set("No")  

    # Add label
    pitch_over_label = ctk.CTkLabel(
        inner_frame, 
        text="Does the rocket pitch over? (Yes/No):", 
        text_color="#FFFFFF",
        padx=10,
        pady=10,
        font=('Comfortaa', 16, 'bold')
    )
    pitch_over_label.grid(row=8, column=0, padx=20, pady=10, sticky="w")

    # Add dropdown menu
    pitch_over_menu = ctk.CTkOptionMenu(
        inner_frame, 
        variable=pitch_over_var, 
        values=["Yes", "No"], 
        dropdown_font=('Comfortaa', 16), 
        text_color="#FFFFFF"
    )
    pitch_over_menu.grid(row=8, column=1, padx=20, pady=10)

    # Define the action for the confirm button
    def confirm_pitch_over():
        global pitch_over
        confirm_button.destroy()
        if pitch_over_var.get() == "Yes":
            pitch_over = "Yes"
            pitch_over_info() 
        else:
            displayAllValues()

    # Add confirm button
    confirm_button = ctk.CTkButton(
        inner_frame, 
        text="Confirm Pitch-over Selection", 
        command=confirm_pitch_over, 
        text_color="#FFFFFF", 
        font=('Comfortaa', 16, 'bold')
    )
    confirm_button.grid(row=9, column=0, columnspan=2, pady=20)

motorSelectButton = ctk.CTkButton(
    root, 
    text="Proceed with motor selection", 
    command=motor_info_button, 
    text_color="#FFFFFF",  # Text color
    font=('Comfortaa', 16, 'bold')
)
canvas.create_window(980, 650, window=motorSelectButton)

root.mainloop()
