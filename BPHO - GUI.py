from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
import os, sys
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def restart_program():
    root.destroy()
    subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:]) 
    

root = tk.Tk()
root.title("Our Solar System")
root.geometry('1980x1080')

canvas = Canvas(root, width=1920, height=1080, bd=0, highlightthickness=0)
canvas.pack()


background_image = ImageTk.PhotoImage(Image.open("ezgif.com-webp-to-jpg.jpg"))
canvas.create_image(500,500,image=background_image)
title = Label(root, text="British Physics Olympiad - Computational Project", font = ('Comfortaa', 30, 'bold'), bg = "#000000", fg="#FFFFFF")
title.place(x=300, y=10)


KeplerThird = Image.open("Task1.jpg")
KeplerThird_Zoomed = ImageTk.PhotoImage(KeplerThird)

Inner2d = Image.open("Task2_I.jpg")
Inner2d_Zoomed = ImageTk.PhotoImage(Inner2d)

Outer2d = Image.open("Task2_II.jpg")
Outer2d_Zoomed = ImageTk.PhotoImage(Outer2d)

OrbitvAngle = Image.open("Task5.png")
OrbitvAngle_Zoomed = ImageTk.PhotoImage(OrbitvAngle)

InnerRelativePlot2D = Image.open("Task7.png")
InnerRelativePlot2D_Zoomed = ImageTk.PhotoImage(InnerRelativePlot2D)

OuterRelativePlot2D = Image.open("Task7i.png")
OuterRelativePlot2D_Zoomed = ImageTk.PhotoImage(OuterRelativePlot2D)

Return_Icon = Image.open("Return - Copy.png")
Return_Zoom = Return_Icon.resize((79, 53), Image.Resampling.LANCZOS)
Return_Zoomed = ImageTk.PhotoImage(Return_Zoom)

def remove_all():
    FirstTask.place_forget()
    SecondTaskP1.place_forget()
    SecondTaskP2.place_forget()
    FifthTask.place_forget()
    SeventhTaskP1.place_forget()
    SeventhTaskP2.place_forget()
    Extension1.place_forget()
    Extension2.place_forget()
    SeventhTaskP3.place_forget()
    SeventhTaskP4.place_forget()

def remove_all2():
    mass_StarL.place_forget()
    mass_Star.place_forget()
    mass_A.place_forget()
    mass_B.place_forget()
    massA.place_forget()
    massB.place_forget()
    xposA.place_forget()
    xposB.place_forget()
    x_posA.place_forget()
    x_posB.place_forget()
    yvelA.place_forget()
    y_velB.place_forget()
    yvelB.place_forget()
    y_velA.place_forget()
    inclinationA.place_forget()
    inclinationA_E.place_forget()
    inclinationB.place_forget()
    inclinationB_E.place_forget()
    orbital_PeriodA.place_forget()
    orbital_PeriodB.place_forget()
    orbitalPeriodA.place_forget()
    orbitalPeriodB.place_forget()
    button1.place_forget()

def revive():
    restart_program()

def Task1():
    remove_all()
    canvas.create_image(500, 400, image=KeplerThird_Zoomed)
    text_box = canvas.create_text(1100, 400, text="To execute this task we calculated the gradients between two points in the array, and repeated the same for another two points. If Kepler's Third Law is correct, the difference between the two gradients should amount to 0, as the gradient is constant for a straight line. We used a while loop that would only plot the graph if the difference was less than 1 (to account for any accuracy issues during the calculations). We end up getting a straight line graph.", 
                   font=("Helvetica", 18), justify="left", width=500, fill="#FFFFFF")
                   
    x0, y0, x1, y1 = canvas.bbox(text_box)
    bbox = x0-5, y0-5, x1+5, y1+5
    canvas.create_rectangle(bbox, outline="white", width=5)

    Restart = Button(root, image=Return_Zoomed, command=revive, bg="#cd53aa")
    Restart.place(x = 800, y = 700)

def Task2():
    remove_all()
    canvas.create_image(500, 400, image=Inner2d_Zoomed)
    text_box = canvas.create_text(1100, 400, text="Used Newton's Laws of Gravitation and Newton's Second Law of Motion, together with equations of motion, to calculate the x-component and y-component of the position of the planet, which was then stored in an array, and later plotted to provide us with the graph we see here.", 
                   font=("Helvetica", 18), justify="left", width=500, fill="#FFFFFF")
                   
    x0, y0, x1, y1 = canvas.bbox(text_box)
    bbox = x0-5, y0-5, x1+5, y1+5
    canvas.create_rectangle(bbox, outline="white", width=5)

    Restart = Button(root, image=Return_Zoomed, command=revive, bg="#cd53aa")
    Restart.place(x = 800, y = 700)

def Task2ii():
    remove_all()
    canvas.create_image(500, 400, image=Outer2d_Zoomed)
    text_box = canvas.create_text(1100, 400, text="Used Newton's Laws of Gravitation and Newton's Second Law of Motion, together with equations of motion, to calculate the x-component and y-component of the position of the planet, which was then stored in an array, and later plotted to provide us with the graph we see here.", 
                   font=("Helvetica", 18), justify="left", width=500, fill="#FFFFFF")
                   
    x0, y0, x1, y1 = canvas.bbox(text_box)
    bbox = x0-5, y0-5, x1+5, y1+5
    canvas.create_rectangle(bbox, outline="white", width=5)

    Restart = Button(root, image=Return_Zoomed, command=revive, bg="#cd53aa")
    Restart.place(x = 800, y = 700)

def Task5():
    remove_all()
    canvas.create_image(500, 400, image=OrbitvAngle_Zoomed)
    text_box = canvas.create_text(1100, 400, text="Used Simpson's Numerical Integral Model, processing the integral as a sum, allowing us to use the even and odd iterations to accurately calculate the sum for each orbital angle value. This was then plotted against a planet with a circular orbit instead of Pluto's eliptical orbit.", 
                   font=("Helvetica", 18), justify="left", width=500, fill="#FFFFFF")
                   
    x0, y0, x1, y1 = canvas.bbox(text_box)
    bbox = x0-5, y0-5, x1+5, y1+5
    canvas.create_rectangle(bbox, outline="white", width=5)

    Restart = Button(root, image=Return_Zoomed, command=revive, bg="#cd53aa")
    Restart.place(x = 800, y = 700)

def Task7():
    remove_all()
    canvas.create_image(500, 400, image=InnerRelativePlot2D_Zoomed)
    text_box = canvas.create_text(1100, 400, text="We used the x and y coordinates from the arrays formed in other tasks, and calculated the difference in position between the Earth and that planet, for each value in that array, which formed a new array of x and y positions, that were plotted to achieve this.", 
                   font=("Helvetica", 18), justify="left", width=500, fill="#FFFFFF")
                   
    x0, y0, x1, y1 = canvas.bbox(text_box)
    bbox = x0-5, y0-5, x1+5, y1+5
    canvas.create_rectangle(bbox, outline="white", width=5)

    Restart = Button(root, image=Return_Zoomed, command=revive, bg="#cd53aa")
    Restart.place(x = 800, y = 700)

def Task7i():
    remove_all()
    canvas.create_image(500, 400, image=OuterRelativePlot2D_Zoomed)
    text_box = canvas.create_text(1100, 400, text="We used the x and y coordinates from the arrays formed in other tasks, and calculated the difference in position between the Saturn and that planet, for each value in that array, which formed a new array of x and y positions, that were plotted to achieve this.", 
                   font=("Helvetica", 18), justify="left", width=500, fill="#FFFFFF")
                   
    x0, y0, x1, y1 = canvas.bbox(text_box)
    bbox = x0-5, y0-5, x1+5, y1+5
    canvas.create_rectangle(bbox, outline="white", width=5)

    Restart = Button(root, image=Return_Zoomed, command=revive, bg="#cd53aa")
    Restart.place(x = 800, y = 700)

def Task7ii():
    remove_all()
    x_final_3dMer = []
    y_final_3dMer = []
    z_final_3dMer = []

    x_final_3dSun = []
    y_final_3dSun = []
    z_final_3dSun = []

    x_final_3dV = []
    y_final_3dV = []
    z_final_3dV = []

    x_final_3dM = []
    y_final_3dM = []
    z_final_3dM = []

    fig5 = plt.figure(figsize=(7,7))
    ax5 = plt.axes(projection='3d')
    ax5.axis("auto")

    axis_size = 0.3

    ax5.set_xlim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)
    ax5.set_ylim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)
    ax5.set_zlim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)

    x_rotated_mer = np.load("Earth_Coordinates_X.npy")
    y_rotated_mer = np.load("Earth_Coordinates_Y.npy")
    z_rotated_mer = np.load("Earth_Coordinates_Z.npy")
    x_rotated_ven = np.load("Venus_Coordinates_X.npy")
    y_rotated_ven = np.load("Venus_Coordinates_Y.npy")
    z_rotated_ven = np.load("Venus_Coordinates_Z.npy")
    x_rotated_earth = np.load("Earth_Coordinates_X.npy")
    y_rotated_earth = np.load("Earth_Coordinates_Y.npy")
    z_rotated_earth = np.load("Earth_Coordinates_Z.npy")
    x_rotated_m = np.load("Mars_Coordinates_X.npy")
    y_rotated_m = np.load("Mars_Coordinates_Y.npy")
    z_rotated_m = np.load("Mars_Coordinates_Z.npy")



    for i in range(len(x_rotated_mer)):
        plotxMer = x_rotated_earth[i] - x_rotated_mer[i]
        plotxVen = x_rotated_earth[i] - x_rotated_ven[i]
        plotXMars = x_rotated_m[i] - x_rotated_earth[i]
        plotyMer = y_rotated_earth[i] - y_rotated_mer[i]
        plotyVen = y_rotated_earth[i] - y_rotated_ven[i]
        plotyMars = y_rotated_m[i] - y_rotated_earth[i]
        plotzMer = z_rotated_earth[i] - z_rotated_mer[i]
        plotzVen = z_rotated_earth[i] - z_rotated_ven[i]
        plotzMars = z_rotated_m[i] - z_rotated_earth[i]
        plotxSun = x_rotated_earth[i]-0
        plotySun = y_rotated_earth[i]-0
        plotzSun = z_rotated_earth[i]-0
        x_final_3dMer.append(plotxMer)
        x_final_3dV.append(plotxVen)
        x_final_3dM.append(plotXMars)
        y_final_3dMer.append(plotyMer)
        y_final_3dV.append(plotyVen)
        y_final_3dM.append(plotyMars)
        x_final_3dSun.append(plotxSun)
        y_final_3dSun.append(plotySun)
        z_final_3dSun.append(plotzSun)
        z_final_3dMer.append(plotzMer)
        z_final_3dM.append(plotzMars)
        z_final_3dV.append(plotzVen)


    ax5.plot(x_final_3dMer, y_final_3dMer, z_final_3dMer, label = "Mercury")
    ax5.plot(x_final_3dV, y_final_3dV, z_final_3dV, label = "Venus")
    ax5.plot(x_final_3dM, y_final_3dM, z_final_3dM, label = "Mars")
    ax5.plot(x_final_3dSun, y_final_3dSun, z_final_3dSun, label = "Sun")
    ax5.set_xlabel("x / m")
    ax5.set_ylabel("y / m")
    ax5.set_zlabel("z / m")
    ax5.scatter(0, 0, 0, color='blue', marker='o', s=30, label = "Earth")
    ax5.legend()
    canvas = FigureCanvasTkAgg(fig5, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=100, y=100)  # Adjust the placement coordinates
    Restart = Button(root, image=Return_Zoomed, command=revive, bg="#cd53aa")
    Restart.place(x = 900, y = 700)
    Info_Exo = Label(root, text = """
    Converted the 2D Plot to a 
    3D Plot through the use of rotated 
    coordinated used for creating the 3D 
    animation.
                     """, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 20, 'bold'), compound = 'center', border = 0)
    Info_Exo.place(x=860, y=300)

def Task7iii():
    remove_all()
    x_final_3dJ = []
    y_final_3dJ = []
    z_final_3dJ = []

    x_final_3dU = []
    y_final_3dU = []
    z_final_3dU = []

    x_final_3dN = []
    y_final_3dN = []
    z_final_3dN = []

    x_final_3dS = []
    y_final_3dS = []
    z_final_3dS = []

    x_final_3dP = []
    y_final_3dP = []
    z_final_3dP = []

    fig2 = plt.figure(figsize=(7,7))
    ax2 = plt.axes(projection='3d')
    ax2.axis("auto")

    axis_size = 5

    ax2.set_xlim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)
    ax2.set_ylim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)
    ax2.set_zlim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)

    x_rotated_sat = np.load("Saturn_Coordinates_X.npy")
    y_rotated_sat = np.load("Saturn_Coordinates_Y.npy")
    z_rotated_sat = np.load("Saturn_Coordinates_Z.npy")
    x_rotated_j = np.load("Jupiter_Coordinates_X.npy")
    y_rotated_j = np.load("Jupiter_Coordinates_Y.npy")
    z_rotated_j = np.load("Jupiter_Coordinates_Z.npy")
    x_rotated_u = np.load("Uranus_Coordinates_X.npy")
    y_rotated_u = np.load("Uranus_Coordinates_Y.npy")
    z_rotated_u = np.load("Uranus_Coordinates_Z.npy")
    x_rotated_nep = np.load("Neptune_Coordinates_X.npy")
    y_rotated_nep = np.load("Neptune_Coordinates_Y.npy")
    z_rotated_nep = np.load("Neptune_Coordinates_Z.npy")
    x_rotated_p = np.load("Pluto_Coordinates_X.npy")
    y_rotated_p = np.load("Pluto_Coordinates_Y.npy")
    z_rotated_p = np.load("Pluto_Coordinates_Z.npy")

    for i in range(len(x_rotated_nep)):
        plotxJup = x_rotated_sat[i] - x_rotated_j[i]
        plotxUra = x_rotated_u[i] - x_rotated_sat[i]
        plotXNep = x_rotated_nep[i] - x_rotated_sat[i]
        plotyJup = y_rotated_sat[i] - y_rotated_j[i]
        plotyUra = y_rotated_u[i] - y_rotated_sat[i]
        plotyNep = y_rotated_nep[i] - y_rotated_sat[i]
        plotxPluto = x_rotated_p[i] - x_rotated_sat[i]
        plotyPluto = y_rotated_p[i] - y_rotated_sat[i]
        plotzJup = z_rotated_sat[i] - z_rotated_j[i]
        plotzUra = z_rotated_u[i] - z_rotated_sat[i]
        plotzNep = z_rotated_nep[i] - z_rotated_sat[i]
        plotzPluto = z_rotated_p[i] - z_rotated_sat[i]
        plotxSun = x_rotated_sat[i]-0
        plotySun = y_rotated_sat[i]-0
        plotzSun = z_rotated_sat[i]-0
        x_final_3dJ.append(plotxJup)
        x_final_3dU.append(plotxUra)
        x_final_3dN.append(plotXNep)
        y_final_3dJ.append(plotyJup)
        y_final_3dU.append(plotyUra)
        y_final_3dN.append(plotyNep)
        x_final_3dS.append(plotxSun)
        y_final_3dS.append(plotySun)
        x_final_3dP.append(plotxPluto)
        y_final_3dP.append(plotyPluto)
        z_final_3dJ.append(plotzJup)
        z_final_3dU.append(plotzUra)
        z_final_3dN.append(plotzNep)
        z_final_3dP.append(plotzPluto)
        z_final_3dS.append(plotzSun)


    ax2.plot(x_final_3dJ, y_final_3dJ, z_final_3dJ, label = "Jupiter")
    ax2.plot(x_final_3dU, y_final_3dU, z_final_3dU, label = "Uranus")
    ax2.plot(x_final_3dN, y_final_3dN, z_final_3dN, label = "Neptune")
    ax2.plot(x_final_3dS, y_final_3dS, z_final_3dS, label = "Sun")
    ax2.plot(x_final_3dP, y_final_3dP, z_final_3dP, label = "Pluto")
    ax2.set_xlabel("x / m")
    ax2.set_ylabel("y / m")
    ax2.set_zlabel("z / m")
    ax2.scatter(0, 0, 0, color='orange', marker='o', s=30, label = "Saturn")
    ax2.legend()
    canvas = FigureCanvasTkAgg(fig2, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=100, y=100)  # Adjust the placement coordinates
    Restart = Button(root, image=Return_Zoomed, command=revive, bg="#cd53aa")
    Restart.place(x = 900, y = 700)
    Info_Exo = Label(root, text = """
    Converted the 2D Plot to a 
    3D Plot through the use of rotated 
    coordinated used for creating the 3D 
    animation.
                     """, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 20, 'bold'), compound = 'center', border = 0)
    Info_Exo.place(x=860, y=300)


gravity_constant = 6.67430e-11
astronomical_unit = 149597870.7 *1000

def Gravitation(gravity, mass1, mass2, distancex1, distancey1, distancex2, distancey2):
    xdistance = distancex1-distancex2
    ydistance = distancey1 - distancey2
    final_distance = ((xdistance**2)+(ydistance**2))**(3/2)
    force_x = -(gravity*mass1*mass2*xdistance)/final_distance
    force_y = -(gravity*mass1*mass2*ydistance)/final_distance
    return force_x, force_y   

def ExoPlanet():
   remove_all()
   def radial_Coords(a, e, theta):
     r = (a*(1-(e**2)))/(1+(e*np.cos(theta)))
     x_val = r*(np.cos(theta))
     y_val = r*(np.sin(theta))
     return x_val, y_val


   solar_mass = 2e30
   earth_mass = 5.9722e+24
   jovian_mass = 1.898e+27

   mass_star = 0.346*solar_mass

   mass_d = 7.55*earth_mass
   semi_majorD = 0.021838*astronomical_unit
   orbital_periodD = 1.937793/365.25
   eccentricityD = 0.057
   inclinationD = np.radians(53.06)
   xpos_list_D = []
   ypos_list_D = []
   zpos_list_D = []

   mass_c = 0.8357*jovian_mass
   semi_majorC = 0.136044*astronomical_unit
   orbital_periodC = 30.0972/365.25
   eccentricityC = 0.2571
   inclinationC = np.radians(53.06)
   xpos_list_C = []
   ypos_list_C = []
   zpos_list_C = []

   mass_b = 	2.660*jovian_mass
   semi_majorB = 0.218627*astronomical_unit
   orbital_periodB = 61.1057/360
   eccentricityB = 0.0325
   inclinationB = np.radians(53.06)
   xpos_list_B = []
   ypos_list_B = []
   zpos_list_B = []

   mass_e = 15.8*earth_mass
   semi_majorE = 0.3501*astronomical_unit
   orbital_periodE = 123.83/360
   eccentricityE = 0.03
   inclinationE = np.radians(53.06)
   xpos_list_E = []
   ypos_list_E = []
   zpos_list_E = []


   angle_array = []

   for i in range(0,361):
      angle_array.append(np.radians(i))

   counter = 0

   while counter<len(angle_array):
      x_valD, y_valD = radial_Coords(semi_majorD, eccentricityD, angle_array[counter])
      xpos_list_D.append(x_valD)
      ypos_list_D.append(y_valD)
      zpos_list_D.append(0)

      x_valC, y_valC = radial_Coords(semi_majorC, eccentricityC ,angle_array[counter])
      xpos_list_C.append(x_valC)
      ypos_list_C.append(y_valC)
      zpos_list_C.append(0)

      x_valB, y_valB = radial_Coords(semi_majorB, eccentricityB,angle_array[counter])
      xpos_list_B.append(x_valB)
      ypos_list_B.append(y_valB)
      zpos_list_B.append(0)

      x_valE, y_valE = radial_Coords(semi_majorE, eccentricityE,angle_array[counter])
      xpos_list_E.append(x_valE)
      ypos_list_E.append(y_valE)
      zpos_list_E.append(0)
      counter+=1

   rotationalMatrixD= np.array([
      [1, 0 , 0],
      [0, np.cos(inclinationD), -(np.sin(inclinationD))],
      [0, (np.sin(inclinationD)), np.cos(inclinationD)]
   ])

   rotationalMatrixC= np.array([
      [1, 0 , 0],
      [0, np.cos(inclinationC), -(np.sin(inclinationC))],
      [0, (np.sin(inclinationC)), np.cos(inclinationC)]
   ])

   rotationalMatrixB= np.array([
      [1, 0 , 0],
      [0, np.cos(inclinationB), -(np.sin(inclinationB))],
      [0, (np.sin(inclinationB)), np.cos(inclinationB)]
   ])

   rotationalMatrixE= np.array([
      [1, 0 , 0],
      [0, np.cos(inclinationE), -(np.sin(inclinationE))],
      [0, (np.sin(inclinationE)), np.cos(inclinationE)]
   ])

   orbit_coords_D = np.vstack((xpos_list_D, ypos_list_D, zpos_list_D))
   rotated_coords_D = np.dot(rotationalMatrixD, orbit_coords_D)

   x_rotated_D, y_rotated_D, z_rotated_D = rotated_coords_D

   orbit_coords_C = np.vstack((xpos_list_C, ypos_list_C, zpos_list_C))
   rotated_coords_C = np.dot(rotationalMatrixC, orbit_coords_C)

   x_rotated_C, y_rotated_C, z_rotated_C = rotated_coords_C

   orbit_coords_B = np.vstack((xpos_list_B, ypos_list_B, zpos_list_B))
   rotated_coords_B = np.dot(rotationalMatrixB, orbit_coords_B)

   x_rotated_B, y_rotated_B, z_rotated_B = rotated_coords_B

   orbit_coords_E = np.vstack((xpos_list_E, ypos_list_E, zpos_list_E))
   rotated_coords_E = np.dot(rotationalMatrixE, orbit_coords_E)

   x_rotated_E, y_rotated_E, z_rotated_E = rotated_coords_E


   fig4 = plt.figure(figsize=(7,7))
   ax4 = plt.axes(projection='3d')
   ax4.axis("auto")

   axis_size4 = 0.4
   ax4.set_xlim(-axis_size4*astronomical_unit,axis_size4*astronomical_unit)
   ax4.set_ylim(-axis_size4*astronomical_unit,axis_size4*astronomical_unit)
   ax4.set_zlim(-axis_size4*astronomical_unit,axis_size4*astronomical_unit)

   ax4.plot(x_rotated_D, y_rotated_D, z_rotated_D, label = "Gl 876 d")
   ax4.plot(x_rotated_C, y_rotated_C, z_rotated_C, label = "Gl 876 c")
   ax4.plot(x_rotated_B, y_rotated_B, z_rotated_B, label = "Gl 876 b")
   ax4.plot(x_rotated_E, y_rotated_E, z_rotated_E, label = "Gl 876 e")
   ax4.scatter(0, 0, 0, color='orange', marker='o', s=30)
   ax4.legend()
   canvas = FigureCanvasTkAgg(fig4, master=root)
   canvas.draw()
   canvas.get_tk_widget().place(x=100, y=100)  # Adjust the placement coordinates
   Restart = Button(root, image=Return_Zoomed, command=revive, bg="#cd53aa")
   Restart.place(x = 900, y = 700)
   Info_Exo = Label(root, text = """
    Used information available on 
    the internet 
    and calculation methods 
    as used for other plots above to 
    successfully and accurately plot 
    the orbit of exoplanets in the 
    Gliese 876 Planetary System.""", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 20, 'bold'), compound = 'center', border = 0)
   Info_Exo.place(x=860, y=300)


def OwnPlot(mass_Star, xpos_star, ypos_star, massA, xposA, yposA, xvelocityA, yvelocityA, orbitalA , inclinationA , massB, xposB, yposB, xvelocityB, yvelocityB, orbitalB, inclinationB):
    remove_all()
    remove_all2()
    # ... (rest of the OwnPlot function code)
    
    dt = 24*60*60
    t=0
    t1=0
    xpos_listA = []
    ypos_listA = []
    zpos_listA = []

    xpos_listB = []
    ypos_listB = []
    zpos_listB = []
    while t<dt*orbitalA*2:
        #G Force on Earth
        fx_A, fy_A = Gravitation(gravity_constant, mass_Star, massA, xposA, yposA, xpos_star, ypos_star)

        ax_A = fx_A/massA
        ay_A = fy_A/massA

        xvelocityA += ax_A*dt
        yvelocityA += ay_A*dt

        xposA += xvelocityA*dt
        yposA += yvelocityA*dt

        xpos_listA.append(xposA)
        ypos_listA.append(yposA)
        zpos_listA.append(0)
        t+=dt

    while t1<dt*orbitalB*2:
        fx_B, fy_B = Gravitation(gravity_constant, mass_Star, massB, xposB, yposB, xpos_star, ypos_star)

        ax_B = fx_B/massB
        ay_B = fy_B/massB

        xvelocityB += ax_B*dt
        yvelocityB += ay_B*dt

        xposB += xvelocityB*dt
        yposB += yvelocityB*dt

        xpos_listB.append(xposB)
        ypos_listB.append(yposB)
        zpos_listB.append(0)
        t1+=dt

    rotationalMatrixA= np.array([
      [1, 0 , 0],
      [0, np.cos(np.radians(inclinationA)), -(np.sin(np.radians(inclinationA)))],
      [0, (np.sin(np.radians(inclinationA))), np.cos(np.radians(inclinationA))]
    ])

    rotationalMatrixB= np.array([
      [1, 0 , 0],
      [0, np.cos(np.radians(inclinationB)), -(np.sin(np.radians(inclinationB)))],
      [0, (np.sin(np.radians(inclinationB))), np.cos(np.radians(inclinationB))]
    ])


    orbit_coords_A = np.vstack((xpos_listA, ypos_listA, zpos_listA))
    rotated_coords_A = np.dot(rotationalMatrixA, orbit_coords_A)

    x_rotated_A, y_rotated_A, z_rotated_A = rotated_coords_A

    orbit_coords_B = np.vstack((xpos_listB, ypos_listB, zpos_listB))
    rotated_coords_B = np.dot(rotationalMatrixB, orbit_coords_B)

    x_rotated_B, y_rotated_B, z_rotated_B = rotated_coords_B

    fig4 = plt.figure(figsize=(7,7))
    ax4 = plt.axes(projection='3d')
    ax4.axis("auto")

    axis_size4 = 1
    ax4.set_xlim(-axis_size4*astronomical_unit,axis_size4*astronomical_unit)
    ax4.set_ylim(-axis_size4*astronomical_unit,axis_size4*astronomical_unit)
    ax4.set_zlim(-axis_size4*astronomical_unit,axis_size4*astronomical_unit)

    ax4.plot(x_rotated_A, y_rotated_A, z_rotated_A, label = "Planet A")
    ax4.plot(x_rotated_B, y_rotated_B, z_rotated_B, label = "Planet B")
    ax4.scatter(0, 0, 0, color='orange', marker='o', s=30)
    ax4.legend()
    canvas = FigureCanvasTkAgg(fig4, master=root)
    canvas.draw()
    canvas.get_tk_widget().place(x=100, y=100)
    Restart = Button(root, image=Return_Zoomed, command=revive, bg="#cd53aa")
    Restart.place(x = 800, y = 700)

def OwnPlotPre():
    global mass_StarL, mass_Star, mass_A, mass_B, massA, massB, xposA, xposB, x_posA, x_posB, yvelA, y_velB, yvelB, y_velA, inclinationA, inclinationA_E, inclinationB, inclinationB_E, orbital_PeriodA, orbital_PeriodB, orbitalPeriodA, orbitalPeriodB, button1
    remove_all()
    mass_StarL = Label(canvas, text = "Please enter the mass of the star: ", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12, 'bold'), compound = 'center', border = 0)
    mass_StarL.place(x = 500, y = 100)
    mass_Star = Entry(canvas, width = 55, borderwidth= 5, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12))
    mass_Star.place(x=510, y = 130)
    massA = Label(canvas, text = "Please enter the mass of planet A: ", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12, 'bold'), compound = 'center', border = 0)
    massA.place(x = 500, y = 160)
    mass_A = Entry(canvas, width = 55, borderwidth= 5, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12))
    mass_A.place(x=510, y = 190)
    xposA = Label(canvas, text = "Please enter the x-position of planet A (at Aphelion if possible or Semi-Major Axis): ", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12, 'bold'), compound = 'center', border = 0)
    xposA.place(x = 500, y = 220)
    x_posA = Entry(canvas, width = 55, borderwidth= 5, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12))
    x_posA.place(x=510, y = 250)
    yvelA = Label(canvas, text = "Please enter the y-velocity of planet A (Minimum Speed if Aphelion Value is entered above): ", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12, 'bold'), compound = 'center', border = 0)
    yvelA.place(x = 500, y = 280)
    y_velA = Entry(canvas, width = 55, borderwidth= 5, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12))
    y_velA.place(x=510, y = 310)
    inclinationA = Label(canvas, text = "Please enter the inclination of planet A: ", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12, 'bold'), compound = 'center', border = 0)
    inclinationA.place(x = 500, y = 340)
    inclinationA_E = Entry(canvas, width = 55, borderwidth= 5, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12))
    inclinationA_E.place(x=510, y = 370)
    orbitalPeriodA = Label(canvas, text = "Please enter the orbital period of planet A: ", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12, 'bold'), compound = 'center', border = 0)
    orbitalPeriodA.place(x = 500, y = 400)
    orbital_PeriodA = Entry(canvas, width = 55, borderwidth= 5, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12))
    orbital_PeriodA.place(x=510, y = 430)
    massB = Label(canvas, text = "Please enter the mass of planet B: ", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12, 'bold'), compound = 'center', border = 0)
    massB.place(x = 500, y = 460)
    mass_B = Entry(canvas, width = 55, borderwidth= 5, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12))
    mass_B.place(x=510, y = 490)
    xposB = Label(canvas, text = "Please enter the x-position of planet B (at Aphelion if possible or Semi-Major Axis): ", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12, 'bold'), compound = 'center', border = 0)
    xposB.place(x = 500, y = 520)
    x_posB = Entry(canvas, width = 55, borderwidth= 5, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12))
    x_posB.place(x=510, y = 550)
    yvelB = Label(canvas, text = "Please enter the y-velocity of planet B (Minimum Speed if Aphelion Value is entered above): ", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12, 'bold'), compound = 'center', border = 0)
    yvelB.place(x = 500, y = 580)
    y_velB = Entry(canvas, width = 55, borderwidth= 5, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12))
    y_velB.place(x=510, y = 610)
    inclinationB = Label(canvas, text = "Please enter the inclination of planet B: ", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12, 'bold'), compound = 'center', border = 0)
    inclinationB.place(x = 500, y = 640)
    inclinationB_E = Entry(canvas, width = 55, borderwidth= 5, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12))
    inclinationB_E.place(x=510, y = 670)
    orbitalPeriodB = Label(canvas, text = "Please enter the orbital period of planet B: ", bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12, 'bold'), compound = 'center', border = 0)
    orbitalPeriodB.place(x = 500, y = 700)
    orbital_PeriodB = Entry(canvas, width = 55, borderwidth= 5, bg = "#6c1408", fg = "#FFFFFF", font = ('Comfortaa', 12))
    orbital_PeriodB.place(x=510, y = 730)
    button1 = tk.Button(root, text="Enter", command=lambda: OwnPlot(float(mass_Star.get()), 0,0,float(mass_A.get()), float(x_posA.get()), 0, 0, float(y_velA.get()), float(orbital_PeriodA.get()), float(inclinationA_E.get()), float(mass_B.get()), float(x_posB.get()), 0, 0, float(y_velB.get()), float(orbital_PeriodB.get()), float(inclinationB_E.get())), bg= "#6c1408", fg = "#FFFFFF", activebackground = "#6c1408", activeforeground = "#FFFFFF", font = ('Comfortaa', 20, 'bold'),  cursor = "hand2", compound= 'center', border = 0)
    button1.place(x=700, y = 770)
    


FirstTask = Button(root, command=Task1, text="Proving Kepler's Third Law",border=10, bg="#cd53aa", cursor="hand2", font = ('Comfortaa', 20))
FirstTask.place(x=150, y= 200)

SecondTaskP1 = Button(root, command=Task2, text="2D Plots of the Inner Planets",border=10, bg="#cd53aa", cursor="hand2", font = ('Comfortaa', 20))
SecondTaskP1.place(x=550, y= 200)

SecondTaskP2 = Button(root, command=Task2ii, text="2D Plots of the Outer Planets",border=10, bg="#cd53aa", cursor="hand2", font = ('Comfortaa', 20))
SecondTaskP2.place(x=980, y= 200)

FifthTask = Button(root, command=Task5, text="Pluto's Orbit Time vs Polar Angle",border=10, bg="#cd53aa", cursor="hand2", font = ('Comfortaa', 20))
FifthTask.place(x=10, y= 350)

SeventhTaskP1 = Button(root, command=Task7, text="2D Plots of the Inner Planets (Ptolemy)",border=10, bg="#cd53aa", cursor="hand2", font = ('Comfortaa', 20))
SeventhTaskP1.place(x=470, y= 350)

SeventhTaskP2 = Button(root, command=Task7i, text="2D Plots of the Outer Planets (Ptolemy)",border=10, bg="#cd53aa", cursor="hand2", font = ('Comfortaa', 20))
SeventhTaskP2.place(x=1000, y= 350)

SeventhTaskP3 = Button(root, command=Task7ii, text="3D Plots of the Inner Planets (Ptolemy)",border=10, bg="#cd53aa", cursor="hand2", font = ('Comfortaa', 20))
SeventhTaskP3.place(x=50, y= 500)

SeventhTaskP4 = Button(root, command=Task7iii, text="3D Plots of the Outer Planets (Ptolemy)",border=10, bg="#cd53aa", cursor="hand2", font = ('Comfortaa', 20))
SeventhTaskP4.place(x=600, y= 500)

Extension1 = Button(root, command=ExoPlanet, text="Multiplanetary System",border=10, bg="#cd53aa", cursor="hand2", font = ('Comfortaa', 20))
Extension1.place(x=1150, y= 500)

Extension2 = Button(root, command=OwnPlotPre, text="Plot your own orbit!",border=10, bg="#cd53aa", cursor="hand2", font = ('Comfortaa', 20))
Extension2.place(x=600, y= 650)

root.mainloop()
