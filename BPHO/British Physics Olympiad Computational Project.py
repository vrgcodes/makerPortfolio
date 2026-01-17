#1. Prove Kepler's Third Law (orbital period squared = distance from the sun cubed)
from matplotlib import pyplot as plt 
import math
import pygame
import numpy as np
from matplotlib.animation import FuncAnimation
import json

orbital_periods = [0.24, 0.62, 1.00, 1.88, 11.86, 29.63, 84.75, 166.34, 248.35]
distance_from_the_sun = [0.387, 0.723, 1, 1.523, 5.20, 9.58, 19.29, 30.25, 39.51]

distance_cubed = []
for distances in distance_from_the_sun:
    distance_cubed.append(distances**3)

orbital_periods_squared = []
for periods in orbital_periods:
    orbital_periods_squared.append(periods**2)

def getSlope(x1, y1, x2, y2):
    gradient = (y2-y1)/(x2-x1)
    return gradient

counter = 0

print(getSlope(distance_cubed[4], orbital_periods_squared[4], distance_cubed[5], orbital_periods_squared[5]) - getSlope(distance_cubed[0], orbital_periods_squared[0], distance_cubed[1], orbital_periods_squared[1]))

while (getSlope(distance_cubed[4], orbital_periods_squared[4], distance_cubed[5], orbital_periods_squared[5]) - getSlope(distance_cubed[0], orbital_periods_squared[0], distance_cubed[1], orbital_periods_squared[1])) < 1 and counter < 1:   
    plt.plot(orbital_periods_squared, distance_cubed)
    plt.xlabel("Distance from the Sun\u00B3 / AU\u00B3")
    plt.ylabel(f"Orbital Period\u00B2 / years\u00B2")
    plt.show()
    counter += 1

#2. Compute and accurately plot elliptical orbits of the five inner planets. Then (using a larger scale), plot the outer planet orbits.

gravity_constant = 6.67430e-11
astronomical_unit = 149597870.7 *1000

mass_sun = 1.989e+30
xvelocity_sun = 0
yvelocity_sun = 0
zvelocity_sun = 0
xpos_sun = 0
ypos_sun = 0
zpos_sun = 0


#Used Aphelion Values Throughout

mass_mercury = 3.3010e+23
xvelocity_mercury = 0
yvelocity_mercury = 38860
zvelocity_mercury = 0
xpos_mercury =  69.818e6*1000
ypos_mercury = 0
zpos_mercury = 0
xpos_list_mer = []
ypos_list_mer = []
zpos_list_mer = []
inclinationRadMer = np.radians(7.004)

mass_venus = 4.8673e+24
xvelocity_venus = 0
yvelocity_venus = 34780
zvelocity_venus = 0
xpos_venus = 108.941e6*1000
ypos_venus = 0
zpos_venus = 0
xpos_list_v = []
ypos_list_v = []
zpos_list_v = []
inclinationRadV = np.radians(3.395)

mass_earth = 5.9722e+24
xvelocity_earth = 0
yvelocity_earth = 29290
zvelocity_earth = 0
xpos_earth = 152.100e6*1000    
ypos_earth = 0
zpos_earth = 0
xpos_list_e = []
ypos_list_e = []
zpos_list_e = []
inclinationRadE = np.radians(0)

mass_mars = 6.4169e+23
xvelocity_mars = 0
yvelocity_mars = 21970
zvelocity_mars = 0
xpos_mars = 249.261e6*1000
ypos_mars = 0
zpos_mars = 0
xpos_list_m = []
ypos_list_m = []
zpos_list_m = []
inclinationRadM = np.radians(1.848)

mass_jupiter = 1.898e+27
xvelocity_jupiter = 0
yvelocity_jupiter = 12440
zvelocity_jupiter = 0
xpos_jupiter = 816.363e6*1000
ypos_jupiter = 0
zpos_jupiter = 0
xpos_list_j = []
ypos_list_j = []
zpos_list_j = []
inclinationRadJ = np.radians(1.304)

mass_saturn = 5.683e+26
xvelocity_saturn = 0
yvelocity_saturn = 9140
zvelocity_saturn = 0
xpos_saturn = 1506.527e6*1000
ypos_saturn = 0
zpos_saturn = 0
xpos_list_sat = []
ypos_list_sat = []
zpos_list_sat = []
inclinationRadS = np.radians(2.486)

mass_neptune = 1.024e+26
xvelocity_neptune = 0
yvelocity_neptune = 5370
zvelocity_neptune = 0
xpos_neptune = 4514.953e6*1000
ypos_neptune = 0
zpos_neptune = 0
xpos_list_nep = []
ypos_list_nep = []
zpos_list_nep = []
inclinationRadNep = np.radians(1.770)

mass_uranus = 8.681e+25
xvelocity_uranus = 0
yvelocity_uranus = 6490
zvelocity_uranus = 0
xpos_uranus = 3001.390e6*1000
ypos_uranus = 0
zpos_uranus = 0
xpos_list_ura = []
ypos_list_ura = []
zpos_list_ura = []
inclinationRadUra = np.radians(0.770)

mass_pluto = 0.01303e+24
xvelocity_pluto = 0
yvelocity_pluto = 3710
zvelocity_pluto = 0
xpos_pluto = 7304.326e6*1000
ypos_pluto = 0
zpos_pluto = 0
xpos_list_p = []
ypos_list_p = []
zpos_list_p = []
inclinationRadPluto = np.radians(17.16)

dt = 24*60*60
t=0
t1 = 0
t2 = 0
t3 = 0

def Gravitation(gravity, mass1, mass2, distancex1, distancey1, distancex2, distancey2):
    xdistance = distancex1-distancex2
    ydistance = distancey1 - distancey2
    final_distance = ((xdistance**2)+(ydistance**2))**(3/2)
    force_x = -(gravity*mass1*mass2*xdistance)/final_distance
    force_y = -(gravity*mass1*mass2*ydistance)/final_distance
    return force_x, force_y

while t<dt*30*365:
    #G Force on Earth
     fx_e, fy_e = Gravitation(gravity_constant, mass_sun, mass_earth, xpos_earth, ypos_earth, xpos_sun, ypos_sun)

     ax_e = fx_e/mass_earth
     ay_e = fy_e/mass_earth

     xvelocity_earth += ax_e*dt
     yvelocity_earth += ay_e*dt

     xpos_earth += xvelocity_earth*dt
     ypos_earth += yvelocity_earth*dt

     xpos_list_e.append(xpos_earth)
     ypos_list_e.append(ypos_earth)
     zpos_list_e.append(0)
     t+=dt

while t1<dt*30*365:
     fx_mer, fy_mer = Gravitation(gravity_constant, mass_sun, mass_mercury, xpos_mercury, ypos_mercury, xpos_sun, ypos_sun)

     ax_mer = fx_mer/mass_mercury
     ay_mer = fy_mer/mass_mercury

     xvelocity_mercury += ax_mer*dt
     yvelocity_mercury += ay_mer*dt

     xpos_mercury += xvelocity_mercury*dt
     ypos_mercury += yvelocity_mercury*dt

     xpos_list_mer.append(xpos_mercury)
     ypos_list_mer.append(ypos_mercury)
     zpos_list_mer.append(0)
     t1+=dt

while t2<dt*30*365:
     fx_ven, fy_ven = Gravitation(gravity_constant, mass_sun, mass_venus, xpos_venus, ypos_venus, xpos_sun, ypos_sun)

     ax_ven = fx_ven/mass_venus
     ay_ven = fy_ven/mass_venus

     xvelocity_venus += ax_ven*dt
     yvelocity_venus += ay_ven*dt

     xpos_venus += xvelocity_venus*dt
     ypos_venus += yvelocity_venus*dt

     xpos_list_v.append(xpos_venus)
     ypos_list_v.append(ypos_venus)
     zpos_list_v.append(0)
     t2+=dt

while t3<dt*30*365:

     fx_m, fy_m = Gravitation(gravity_constant, mass_sun, mass_mars, xpos_mars, ypos_mars, xpos_sun, ypos_sun)

     ax_m = fx_m/mass_mars
     ay_m = fy_m/mass_mars

     xvelocity_mars += ax_m*dt
     yvelocity_mars += ay_m*dt

     xpos_mars += xvelocity_mars*dt
     ypos_mars += yvelocity_mars*dt

     xpos_list_m.append(xpos_mars)
     ypos_list_m.append(ypos_mars)
     zpos_list_m.append(0)

     t3+=dt

plt.plot(xpos_list_mer, ypos_list_mer, "-r", label = "Mercury")
plt.plot(xpos_list_v, ypos_list_v, "-y", label = "Venus")
plt.plot(xpos_list_e, ypos_list_e, "-g", label = "Earth")
plt.plot(xpos_list_m, ypos_list_m, "-b", label = "Mars")
plt.xlabel("x / m")
plt.ylabel("y / m")
plt.scatter(0, 0, color='orange', marker='o', s=30, label = "Sun")
plt.legend()
plt.axis("equal")
plt.show()





t4 = 0
t5 = 0
t6 = 0
t7 = 0

while t4<dt*248*365:

     fx_j, fy_j = Gravitation(gravity_constant, mass_sun, mass_jupiter, xpos_jupiter, ypos_jupiter, xpos_sun, ypos_sun)

     ax_j = fx_j/mass_jupiter
     ay_j = fy_j/mass_jupiter

     xvelocity_jupiter += ax_j*dt
     yvelocity_jupiter += ay_j*dt

     xpos_jupiter += xvelocity_jupiter*dt
     ypos_jupiter += yvelocity_jupiter*dt

     xpos_list_j.append(xpos_jupiter)
     ypos_list_j.append(ypos_jupiter)
     zpos_list_j.append(0)

     t4+=dt

while t5<dt*248*365:

     fx_sat, fy_sat = Gravitation(gravity_constant, mass_sun, mass_saturn, xpos_saturn, ypos_saturn, xpos_sun, ypos_sun)

     ax_sat = fx_sat/mass_saturn
     ay_sat = fy_sat/mass_saturn

     xvelocity_saturn += ax_sat*dt
     yvelocity_saturn += ay_sat*dt

     xpos_saturn += xvelocity_saturn*dt
     ypos_saturn += yvelocity_saturn*dt

     xpos_list_sat.append(xpos_saturn)
     ypos_list_sat.append(ypos_saturn)
     zpos_list_sat.append(0)


     t5+=dt
     
while t6<dt*248*365:

     fx_n, fy_n = Gravitation(gravity_constant, mass_sun, mass_neptune, xpos_neptune, ypos_neptune, xpos_sun, ypos_sun)

     ax_n = fx_n/mass_neptune
     ay_n = fy_n/mass_neptune

     xvelocity_neptune += ax_n*dt
     yvelocity_neptune += ay_n*dt

     xpos_neptune += xvelocity_neptune*dt
     ypos_neptune += yvelocity_neptune*dt

     xpos_list_nep.append(xpos_neptune)
     ypos_list_nep.append(ypos_neptune)
     zpos_list_nep.append(0)

     t6+=dt

while t7<dt*248*365:

     fx_u, fy_u = Gravitation(gravity_constant, mass_sun, mass_uranus, xpos_uranus, ypos_uranus, xpos_sun, ypos_sun)

     ax_u = fx_u/mass_uranus
     ay_u = fy_u/mass_uranus

     xvelocity_uranus += ax_u*dt
     yvelocity_uranus += ay_u*dt

     xpos_uranus += xvelocity_uranus*dt
     ypos_uranus += yvelocity_uranus*dt

     xpos_list_ura.append(xpos_uranus)
     ypos_list_ura.append(ypos_uranus)
     zpos_list_ura.append(0)

     t7+=dt

plt.plot(xpos_list_j, ypos_list_j, "-r", label = "Jupiter")
plt.plot(xpos_list_sat, ypos_list_sat, "-y", label = "Saturn")
plt.plot(xpos_list_ura, ypos_list_ura, "-g", label = "Uranus")
plt.plot(xpos_list_nep, ypos_list_nep, "-b", label = "Neptune")
plt.scatter(0, 0, color='orange', marker='o', s=30, label = "Sun")
plt.xlabel("x / m")
plt.ylabel("y / m")
plt.legend()
plt.axis("equal")
plt.show()

#3. Create a 2D animation of the orbits of the planets.

pygame.init()
WIDTH, HEIGHT = 1080, 1080
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Animation of the First Four Inner Planets of the Solar System")
font = pygame.font.SysFont("Helvetica", 16)
background = r"C:\Users\veerg\Documents\Coding\Algorithms, Programming and Logic\Python\Simulation_BG.jpg"
bg = pygame.image.load(background)

#inititalize all variables
#draw the planet initially
#calculate the gravitational forces
#update the position


class Planet: 
    gravity_constant2 = 6.67430e-11
    astronomical_unit2 = 149597870.7 *1000
    scale = 150/astronomical_unit2 #1AU = 100px
    time_step = 24*60*60
    def __init__(self, xpos, ypos, xvel, yvel, mass, radius, color):
          self.xpos = xpos
          self.ypos = ypos
          self.xvel = xvel
          self.yvel = yvel
          self.mass = mass
          self.radius = radius
          self.Sun = False
          self.distanceToSun = 0
          self.positionVal = []
          self.color = color
    def draw(self, window):
         x = self.xpos*self.scale + (WIDTH/2)
         y = self.ypos*self.scale + (HEIGHT/2)
         if len(self.positionVal) > 2:
              updated_orbit = []
              for position in self.positionVal:
                   x,y = position
                   x = x*self.scale + (WIDTH/2)
                   y = y*self.scale + (HEIGHT/2)
                   updated_orbit.append((x,y))
              pygame.draw.lines(window, self.color, False, updated_orbit, 2)
         if not self.Sun:
              distance_text = font.render(f"{round(self.distanceToSun/1000,1)}km", 1, (255,255,255))
              window.blit(distance_text, (x-(distance_text.get_width()/2), y-(distance_text.get_width()/2)))
         pygame.draw.circle(window, self.color, (x,y), self.radius)

    def Gravitation2(self, other):
        other_x, other_y = other.xpos, other.ypos
        distance_x = other_x - self.xpos
        distance_y = other_y - self.ypos
        distance_final = ((distance_x)**2+(distance_y)**2)**0.5
        if other.Sun:
             self.distanceToSun = distance_final
        force = (self.gravity_constant2*self.mass*other.mass)/(distance_final**2)
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x, force_y
    def update_pos(self, planets):
        totalForceX, totalForceY = 0,0
        for planet in planets:
            if self == planet:
                 continue
            forceX, forceY = self.Gravitation2(planet)
            totalForceX += forceX
            totalForceY += forceY
        self.xvel += (totalForceX/self.mass)*self.time_step
        self.yvel += (totalForceY/self.mass)*self.time_step
        self.xpos += (self.xvel*self.time_step)
        self.ypos += (self.yvel*self.time_step)
        self.positionVal.append((self.xpos, self.ypos))



def Main():
    run = True
    clock = pygame.time.Clock()
    Sun = Planet(0,0,0,0,1.989e+30,30,(253, 184, 19))
    Sun.Sun = True
    Mercury = Planet(69.818e6*1000, 0, 0, -38860, 3.301e+23, 6, (219, 206, 202))
    Venus = Planet(108.941e6*1000, 0, 0, -34780, 4.8673e+24, 16, (139, 125, 130))
    Earth = Planet(-152.100e6*1000, 0, 0, 29290, 5.9722e+24, 18, (100, 149, 237))
    Mars = Planet(-249.261e6*1000, 0, 0, 21970, 6.4169e+23, 9, (173,98,66))
    
    #initialize all planet data
    #while loop to run

    planets = [Sun, Mercury, Venus, Earth, Mars]
    while run:
         clock.tick(60)
         window.fill((0,0,0))
         window.blit(bg, (0,0))
         for event in pygame.event.get():
              if event.type == pygame.QUIT:
                run = False
         for planet in planets:
              planet.update_pos(planets)
              planet.draw(window)
         pygame.display.update()
    pygame.quit()
            
Main()

pygame.init()
WIDTH2, HEIGHT2 = 1080, 1080
window2 = pygame.display.set_mode((WIDTH2, HEIGHT2))
pygame.display.set_caption("2D Animation of the Four Outer Planets of the Solar System")
font2 = pygame.font.SysFont("Helvetica", 16)
background2 = r"C:\Users\veerg\Documents\Coding\Algorithms, Programming and Logic\Python\Simulation_BG.jpg"
bg2 = pygame.image.load(background2)

#inititalize all variables
#draw the planet initially
#calculate the gravitational forces
#update the position

#work on changing the overlaying lines


class Planet2: 
    gravity_constant3 = 6.67430e-11
    astronomical_unit3 = 149597870.7 *1000
    scale2 = 150/(astronomical_unit3*10) #1AU = 100px
    time_step2 = 24*60*60*15
    def __init__(self, xpos, ypos, xvel, yvel, mass, radius, color):
          self.xpos = xpos
          self.ypos = ypos
          self.xvel = xvel
          self.yvel = yvel
          self.mass = mass
          self.radius = radius
          self.Sun = False
          self.distanceToSun = 0
          self.positionVal = []
          self.color = color
    def draw(self, window):
         x = self.xpos*self.scale2 + (WIDTH2/2)
         y = self.ypos*self.scale2 + (HEIGHT2/2)
         if len(self.positionVal) > 2:
              updated_orbit = []
              for position in self.positionVal:
                   x,y = position
                   x = x*self.scale2 + (WIDTH2/2)
                   y = y*self.scale2 + (HEIGHT2/2)
                   updated_orbit.append((x,y))
              pygame.draw.lines(window, self.color, False, updated_orbit, 1)
         if not self.Sun:
              distance_text = font2.render(f"{round(self.distanceToSun/1000,1)}km", 1, (255,255,255))
              window.blit(distance_text, (x-(distance_text.get_width()/2), y-(distance_text.get_width()/2)))
         pygame.draw.circle(window, self.color, (x,y), self.radius)

    def Gravitation2(self, other):
        other_x, other_y = other.xpos, other.ypos
        distance_x = other_x - self.xpos
        distance_y = other_y - self.ypos
        distance_final = ((distance_x)**2+(distance_y)**2)**0.5
        if other.Sun:
             self.distanceToSun = distance_final
        force = (self.gravity_constant3*self.mass*other.mass)/(distance_final**2)
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x, force_y
    def update_pos(self, planets):
        totalForceX, totalForceY = 0,0
        for planet in planets:
            if self == planet:
                 continue
            forceX, forceY = self.Gravitation2(planet)
            totalForceX += forceX
            totalForceY += forceY
        self.xvel += (totalForceX/self.mass)*self.time_step2
        self.yvel += (totalForceY/self.mass)*self.time_step2
        self.xpos += (self.xvel*self.time_step2)
        self.ypos += (self.yvel*self.time_step2)
        self.positionVal.append((self.xpos, self.ypos))



def Main2():
    run = True
    clock = pygame.time.Clock()
    Sun2 = Planet2(0,0,0,0,1.989e+30,30,(253, 184, 19))
    Sun2.Sun = True
    Jupiter = Planet2(816.363e6*1000, 0, 0, -12440, 1898.13e+24, 20, (219, 206, 202))
    Saturn = Planet2(1506.527e6*1000, 0, 0, -9140, 568.32e+24, 15, (139, 125, 130))
    Uranus = Planet2(-3001.390e6*1000, 0, 0, 6490, 86.811e+24, 8, (100, 149, 237))
    Neptune = Planet2(-4558.857e6*1000, 0, 0, 5370, 102.409e+24, 6, (173,98,66))
    
    #initialize all planet data
    #while loop to run

    planets2 = [Sun2, Jupiter, Saturn, Uranus, Neptune]
    while run:
         clock.tick(60)
         window2.fill((0,0,0))
         window2.blit(bg2, (0,0))
         for event in pygame.event.get():
              if event.type == pygame.QUIT:
                run = False
         for planet2 in planets2:
              planet2.update_pos(planets2)
              planet2.draw(window2)
         pygame.display.update()
    pygame.quit()
            
Main2()

#4. Use the inclination angle value and hence plot 3D orbit animations of the planets. Do include the dwarf planet Pluto, as it is off the plane of the ecliptic much more than the other planets.

rotationalMatrixMer= np.array([
     [1, 0 , 0],
     [0, np.cos(inclinationRadMer), -(np.sin(inclinationRadMer))],
     [0, (np.sin(inclinationRadMer)), np.cos(inclinationRadMer)]
])

rotationalMatrixV= np.array([
     [1, 0 , 0],
     [0, np.cos(inclinationRadV), -(np.sin(inclinationRadV))],
     [0, (np.sin(inclinationRadV)), np.cos(inclinationRadV)]
])

rotationalMatrixE= np.array([
     [1, 0 , 0],
     [0, np.cos(inclinationRadE), -(np.sin(inclinationRadE))],
     [0, (np.sin(inclinationRadE)), np.cos(inclinationRadE)]
])

rotationalMatrixM= np.array([
     [1, 0 , 0],
     [0, np.cos(inclinationRadM), -(np.sin(inclinationRadM))],
     [0, (np.sin(inclinationRadM)), np.cos(inclinationRadM)]
])

rotationalMatrixJ= np.array([
     [1, 0 , 0],
     [0, np.cos(inclinationRadJ), -(np.sin(inclinationRadJ))],
     [0, (np.sin(inclinationRadJ)), np.cos(inclinationRadJ)]
])

rotationalMatrixS= np.array([
     [1, 0 , 0],
     [0, np.cos(inclinationRadS), -(np.sin(inclinationRadS))],
     [0, (np.sin(inclinationRadS)), np.cos(inclinationRadS)]
])

rotationalMatrixU= np.array([
     [1, 0 , 0],
     [0, np.cos(inclinationRadUra), -(np.sin(inclinationRadUra))],
     [0, (np.sin(inclinationRadUra)), np.cos(inclinationRadUra)]
])

rotationalMatrixN= np.array([
     [1, 0 , 0],
     [0, np.cos(inclinationRadNep), -(np.sin(inclinationRadNep))],
     [0, (np.sin(inclinationRadNep)), np.cos(inclinationRadNep)]
])

rotationalMatrixP= np.array([
     [1, 0 , 0],
     [0, np.cos(inclinationRadPluto), -(np.sin(inclinationRadPluto))],
     [0, (np.sin(inclinationRadPluto)), np.cos(inclinationRadPluto)]
])


def Gravitation3(gravity, mass1, mass2, distancex1, distancey1, distancez1, distancex2, distancey2, distancez2):
    xdistance = distancex1-distancex2
    ydistance = distancey1 - distancey2
    zdistance = distancez1 - distancez2
    final_distance = ((xdistance**2)+(ydistance**2)+(zdistance)**2)**(3/2)
    force_x = -(gravity*mass1*mass2*xdistance)/final_distance
    force_y = -(gravity*mass1*mass2*ydistance)/final_distance
    force_z = -(gravity*mass1*mass2*zdistance)/final_distance
    return force_x, force_y, force_z

t8 = 0

while t8<dt*248*365:
    #G Force on Pluto
     fx_p, fy_p, fz_p = Gravitation3(gravity_constant, mass_sun, mass_pluto, xpos_pluto, ypos_pluto, zpos_pluto, xpos_sun, ypos_sun, zpos_sun)

     ax_p = fx_p/mass_pluto
     ay_p = fy_p/mass_pluto
     az_p = fz_p/mass_pluto

     xvelocity_pluto += ax_p*dt
     yvelocity_pluto += ay_p*dt
     zvelocity_pluto += az_p*dt

     xpos_pluto += xvelocity_pluto*dt
     ypos_pluto += yvelocity_pluto*dt
     zpos_pluto += zvelocity_pluto*dt

     xpos_list_p.append(xpos_pluto)
     ypos_list_p.append(ypos_pluto)
     zpos_list_p.append(zpos_pluto)
     t8+=dt



orbit_coords_mer = np.vstack((xpos_list_mer, ypos_list_mer, zpos_list_mer))
rotated_coords_mer = np.dot(rotationalMatrixMer, orbit_coords_mer)

x_rotated_mer, y_rotated_mer, z_rotated_mer = rotated_coords_mer

orbit_coords_ven = np.vstack((xpos_list_v, ypos_list_v, zpos_list_v))
rotated_coords_ven = np.dot(rotationalMatrixV, orbit_coords_ven)

x_rotated_ven, y_rotated_ven, z_rotated_ven = rotated_coords_ven

orbit_coords_e = np.vstack((xpos_list_e, ypos_list_e, zpos_list_e))
rotated_coords_e = np.dot(rotationalMatrixE, orbit_coords_e)

x_rotated_earth, y_rotated_earth, z_rotated_earth = rotated_coords_e

orbit_coords_mars = np.vstack((xpos_list_m, ypos_list_m, zpos_list_m))
rotated_coords_mars = np.dot(rotationalMatrixM, orbit_coords_mars)

x_rotated_m, y_rotated_m, z_rotated_m = rotated_coords_mars

orbit_coords_J = np.vstack((xpos_list_j, ypos_list_j, zpos_list_j))
rotated_coords_J = np.dot(rotationalMatrixJ, orbit_coords_J)

x_rotated_j, y_rotated_j, z_rotated_j = rotated_coords_J

orbit_coords_sat = np.vstack((xpos_list_sat, ypos_list_sat, zpos_list_sat))
rotated_coords_sat = np.dot(rotationalMatrixS, orbit_coords_sat)

x_rotated_sat, y_rotated_sat, z_rotated_sat = rotated_coords_sat

orbit_coords_ura = np.vstack((xpos_list_ura, ypos_list_ura, zpos_list_ura))
rotated_coords_ura = np.dot(rotationalMatrixU, orbit_coords_ura)

x_rotated_u, y_rotated_u, z_rotated_u = rotated_coords_ura

orbit_coords_nep = np.vstack((xpos_list_nep, ypos_list_nep, zpos_list_nep))
rotated_coords_nep = np.dot(rotationalMatrixN, orbit_coords_nep)

x_rotated_nep, y_rotated_nep, z_rotated_nep = rotated_coords_nep

orbit_coords_pluto = np.vstack((xpos_list_p, ypos_list_p, zpos_list_p))
rotated_coords_pluto = np.dot(rotationalMatrixP, orbit_coords_pluto)

x_rotated_p, y_rotated_p, z_rotated_p = rotated_coords_pluto

fig = plt.figure(figsize=(10,10))
ax = plt.axes(projection='3d')
ax.axis("auto")

axis_size = 4
ax.set_xlim(-axis_size*astronomical_unit,axis_size*astronomical_unit)
ax.set_ylim(-axis_size*astronomical_unit,axis_size*astronomical_unit)
ax.set_zlim(-axis_size*astronomical_unit,axis_size*astronomical_unit)

dataset_dict = {}

dataset_mercury = [x_rotated_mer, y_rotated_mer, z_rotated_mer]
dataset_venus = [x_rotated_ven, y_rotated_ven, z_rotated_ven]
dataset_earth = [x_rotated_earth, y_rotated_earth, z_rotated_earth]
dataset_mars = [x_rotated_m, y_rotated_m, z_rotated_m]
dataset_jupiter = [x_rotated_j, y_rotated_j, z_rotated_j]
dataset_saturn = [x_rotated_sat, y_rotated_sat, z_rotated_sat]
dataset_uranus = [x_rotated_u, y_rotated_u, z_rotated_u]
dataset_neptune = [x_rotated_nep, y_rotated_nep, z_rotated_nep]
dataset_pluto = [x_rotated_p, y_rotated_p, z_rotated_p]

dataset_dict["mercury"] = dataset_mercury
dataset_dict["venus"] = dataset_venus
dataset_dict["earth"] = dataset_earth
dataset_dict["mars"] = dataset_mars
dataset_dict["jupiter"] = dataset_jupiter
dataset_dict["saturn"] = dataset_saturn
dataset_dict["uranus"] = dataset_uranus
dataset_dict["neptune"] = dataset_neptune
dataset_dict["pluto"] = dataset_pluto

graphics_dict = {}

line_mer, = ax.plot([0], [0], [0], "-g", lw = 1)
point_mer, = ax.plot([69.818e6*1000], [0], [0], marker="o", markersize=7, markeredgecolor="gray", markerfacecolor="gray")

graphics_dict["mercury"] = [line_mer, point_mer]

line_ven, = ax.plot([0], [0], [0], "-g", lw = 1)
point_ven, = ax.plot([108.941e6*1000], [0], [0], marker="o", markersize=7, markeredgecolor="red", markerfacecolor="red")

graphics_dict["venus"] = [line_ven, point_ven]

line_e, = ax.plot([0], [0], [0], "-g", lw = 1)
point_e, = ax.plot([152.100e6*1000], [0], [0], marker="o", markersize=7, markeredgecolor="blue", markerfacecolor="blue")

graphics_dict["earth"] = [line_e, point_e]

line_m, = ax.plot([0], [0], [0], "-g", lw = 1)
point_m, = ax.plot([249.261e6*1000], [0], [0], marker="o", markersize=7, markeredgecolor="green", markerfacecolor="green")

graphics_dict["mars"] = [line_m, point_m]

line_j, = ax.plot([0], [0], [0], "-g", lw = 1)
point_j, = ax.plot([816.363e6*1000], [0], [0], marker="o", markersize=7, markeredgecolor="red", markerfacecolor="red")

graphics_dict["jupiter"] = [line_j, point_j]

line_sat, = ax.plot([0], [0], [0], "-g", lw = 1)
point_sat, = ax.plot([1506.527e6*1000], [0], [0], marker="o", markersize=7, markeredgecolor="yellow", markerfacecolor="yellow")

graphics_dict["saturn"] = [line_sat, point_sat]

line_u, = ax.plot([0], [0], [0], "-g", lw = 1)
point_u, = ax.plot([3001.390e6*1000], [0], [0], marker="o", markersize=7, markeredgecolor="gray", markerfacecolor="gray")

graphics_dict["uranus"] = [line_u, point_u]

line_nep, = ax.plot([0], [0], [0], "-g", lw = 1)
point_nep, = ax.plot([4514.953e6*1000], [0], [0], marker="o", markersize=7, markeredgecolor="blue", markerfacecolor="blue")

graphics_dict["neptune"] = [line_nep, point_nep]

line_p, = ax.plot([0], [0], [0], "-g", lw = 1)
point_p, = ax.plot([7304.326e6*1000], [0], [0], marker="o", markersize=7, markeredgecolor="green", markerfacecolor="green")

graphics_dict["pluto"] = [line_p, point_p]

def update_position(frame, dataDict, graphicDict):
     #Mercury
     dataset_mer = dataDict["mercury"]
     line_mer = graphicDict["mercury"][0]
     point_mer = graphicDict["mercury"][1]
     line_mer.set_data_3d(dataset_mer[0][:frame], dataset_mer[1][:frame], dataset_mer[2][:frame])
     point_mer.set_data_3d(dataset_mer[0][frame], dataset_mer[1][frame], dataset_mer[2][frame])

     #Venus
     dataset_ven = dataDict["venus"]
     line_ven = graphicDict["venus"][0]
     point_ven = graphicDict["venus"][1]
     line_ven.set_data_3d(dataset_ven[0][:frame], dataset_ven[1][:frame], dataset_ven[2][:frame])
     point_ven.set_data_3d(dataset_ven[0][frame], dataset_ven[1][frame], dataset_ven[2][frame])

     #Earth
     dataset_e = dataDict["earth"]
     line_e = graphicDict["earth"][0]
     point_e = graphicDict["earth"][1]
     line_e.set_data_3d(dataset_e[0][:frame], dataset_e[1][:frame], dataset_e[2][:frame])
     point_e.set_data_3d(dataset_e[0][frame], dataset_e[1][frame], dataset_e[2][frame])

     #Mars
     dataset_m = dataDict["mars"]
     line_m = graphicDict["mars"][0]
     point_m = graphicDict["mars"][1]
     line_m.set_data_3d(dataset_m[0][:frame], dataset_m[1][:frame], dataset_m[2][:frame])
     point_m.set_data_3d(dataset_m[0][frame], dataset_m[1][frame], dataset_m[2][frame])
     
     #Jupiter
     dataset_j = dataDict["jupiter"]
     line_j = graphicDict["jupiter"][0]
     point_j = graphicDict["jupiter"][1]
     line_j.set_data_3d(dataset_j[0][:frame], dataset_j[1][:frame], dataset_j[2][:frame])
     point_j.set_data_3d(dataset_j[0][frame], dataset_j[1][frame], dataset_j[2][frame])

     #Saturn
     dataset_s = dataDict["saturn"]
     line_sat = graphicDict["saturn"][0]
     point_sat = graphicDict["saturn"][1]
     line_sat.set_data_3d(dataset_s[0][:frame], dataset_s[1][:frame], dataset_s[2][:frame])
     point_sat.set_data_3d(dataset_s[0][frame], dataset_s[1][frame], dataset_s[2][frame])

     #Uranus
     dataset_u = dataDict["uranus"]
     line_u = graphicDict["uranus"][0]
     point_u = graphicDict["uranus"][1]
     line_u.set_data_3d(dataset_u[0][:frame], dataset_u[1][:frame], dataset_u[2][:frame])
     point_u.set_data_3d(dataset_u[0][frame], dataset_u[1][frame], dataset_u[2][frame])

     #Neptune
     dataset_n = dataDict["neptune"]
     line_nep = graphicDict["neptune"][0]
     point_nep = graphicDict["neptune"][1]
     line_nep.set_data_3d(dataset_n[0][:frame], dataset_n[1][:frame], dataset_n[2][:frame])
     point_nep.set_data_3d(dataset_n[0][frame], dataset_n[1][frame], dataset_n[2][frame])

     #Pluto
     dataset_p = dataDict["pluto"]
     line_p = graphicDict["pluto"][0]
     point_p = graphicDict["pluto"][1]
     line_p.set_data_3d(dataset_p[0][:frame], dataset_p[1][:frame], dataset_p[2][:frame])
     point_p.set_data_3d(dataset_p[0][frame], dataset_p[1][frame], dataset_p[2][frame])

#Fix Mercury, put this in separate file
#Add labels for axes

ax.scatter(0, 0, 0, color='orange', marker='o', s=30)
ani = FuncAnimation(fig, update_position, len(x_rotated_earth), fargs=(dataset_dict, graphics_dict), interval = 0.000000001)
plt.show()

#5. Use Simpson’s numeric integration method to determine how orbital time varies with polar angle. Hence code-up a function which outputs orbit polar angle from orbit time. Update your models with this function, and contrast how polar angle varies with time for Pluto, compared to a circular motion example with the same 248.348 year period. 


orbital_time = []
orbital_angle = np.linspace(0, 20, 1000)

circular_times = []
circular_angles =[]

def orbitalEq(theta):
    orbit_time = 1/(1-(0.2488*(math.cos(theta))))**2
    return orbit_time

def SimpsonsIntegral(lowerlim, upperlim, noOfIntervals):
    change_in_x = (upperlim-lowerlim)/noOfIntervals

    time_even = []
    time_odd = []
    Sum_Even = 0
    Sum_odd = 0

    for i in range(1, noOfIntervals):
        theta = lowerlim + (i*change_in_x)
        if i % 2 == 0:
            time_even.append(orbitalEq(theta))
        else:
            time_odd.append(orbitalEq(theta))

    for times in time_even:
        Sum_Even += times*2
    for times2 in time_odd:
        Sum_odd += times2*4

    First_Term = orbitalEq(lowerlim)
    Last_Term = orbitalEq(upperlim)

    Sum = (First_Term+Sum_odd+Sum_Even+Last_Term)*(1/(2*math.pi))*(248.348*(1-(0.2488)**2)**(3/2))*change_in_x/3
    orbital_time.append(Sum)

for j in range(0, 800):
    circular_times.append(j)


for theta in orbital_angle:
    SimpsonsIntegral(0, theta, 1000)

def circularOrbit(time):
    angle = (2*math.pi*time)/248.348
    circular_angles.append(angle)

for times in circular_times:
    circularOrbit(times)

plt.plot(orbital_time, orbital_angle, label = "Pluto")
plt.plot(circular_times, circular_angles, label = "Circular Orbit")
plt.xlabel("Orbital Time / Years")
plt.ylabel("Orbital Period / Radians")
plt.legend()
plt.grid(True)
plt.show()

#6. Solar System spirograph! Choose a pair of planets and determine their orbits vs time. At fixed time intervals, draw a line between the planets and plot their positions. Keep going for 10 orbits of the outermost planet.

import math
import pygame

pygame.init()
WIDTH, HEIGHT = 1080, 1080
window3 = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Animation of the First Four Inner Planets of the Solar System")
font3 = pygame.font.SysFont("Helvetica", 16)
background3 = r"C:\Users\veerg\Documents\Coding\Algorithms, Programming and Logic\Python\Simulation_BG.jpg"
bg3 = pygame.image.load(background3)

#inititalize all variables
#draw the planet initially
#calculate the gravitational forces
#update the position


class Planet3: 
    gravity_constant3 = 6.67430e-11
    astronomical_unit3 = 149597870.7 *1000
    scale3 = 500/astronomical_unit3 #1AU = 100px
    time_step3 = 24*60*60
    counter3 = 0
    def __init__(self, xpos, ypos, xvel, yvel, mass, radius, color):
          self.xpos = xpos
          self.ypos = ypos
          self.xvel = xvel
          self.yvel = yvel
          self.mass = mass
          self.radius = radius
          self.Sun = False
          self.distanceToSun = 0
          self.positionVal = []
          self.color = color
          self.lines = []
          self.timer = 0
          self.draw_interval = 5
    def draw(self, window3):
         x = self.xpos*self.scale3 + (WIDTH/2)
         y = self.ypos*self.scale3 + (HEIGHT/2)
         if len(self.positionVal) > 2:
              updated_orbit = []
              for position in self.positionVal:
                   x,y = position
                   x = x*self.scale3 + (WIDTH/2)
                   y = y*self.scale3 + (HEIGHT/2)
                   updated_orbit.append((x,y))
              pygame.draw.lines(window3, self.color, False, updated_orbit, 2)
         if not self.Sun:
              distance_text = font3.render(f"{round(self.distanceToSun/1000,1)}km", 1, (255,255,255))
              window3.blit(distance_text, (x-(distance_text.get_width()/2), y-(distance_text.get_width()/2)))
         pygame.draw.circle(window3, self.color, (x,y), self.radius)
         for lines in self.lines:
               pygame.draw.line(window3, (255,255,255), lines[0], lines[1], 1)

    def Gravitation2(self, other):
        other_x, other_y = other.xpos, other.ypos
        distance_x = other_x - self.xpos
        distance_y = other_y - self.ypos
        distance_final = ((distance_x)**2+(distance_y)**2)**0.5
        if other.Sun:
             self.distanceToSun = distance_final
        force = (self.gravity_constant3*self.mass*other.mass)/(distance_final**2)
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta)*force
        force_y = math.sin(theta)*force
        return force_x, force_y
    def update_pos(self, planets, planetsOnly):
        totalForceX, totalForceY = 0,0
        for planet in planets:
            if self == planet:
                 continue
            forceX, forceY = self.Gravitation2(planet)
            totalForceX += forceX
            totalForceY += forceY
        self.xvel += (totalForceX/self.mass)*self.time_step3
        self.yvel += (totalForceY/self.mass)*self.time_step3
        self.xpos += (self.xvel*self.time_step3)
        self.ypos += (self.yvel*self.time_step3)
        self.positionVal.append((self.xpos, self.ypos))
        self.timer+=1e6
        if (self.timer >= self.draw_interval*1e6) and self.counter3<600:
          for planet2 in planetsOnly:
               if (self==planet2) or (self.Sun):   
                    continue
               xpos_s = self.xpos*self.scale3 + (WIDTH/2)   
               ypos_s = self.ypos*self.scale3 + (HEIGHT/2)
               xpos_o = planet2.xpos*self.scale3 + (WIDTH/2)   
               ypos_o = planet2.ypos*self.scale3 + (HEIGHT/2)    
               self.lines.append(((xpos_s, ypos_s), (xpos_o, ypos_o)))
          self.timer = 0
          self.counter3+=1
    

def Main():
    run = True
    clock = pygame.time.Clock()
    Sun3 = Planet3(0,0,0,0,1.989e+30,30,(253, 184, 19))
    Sun3.Sun = True
    Venus3 = Planet3(108.941e6*1000, 0, 0, -34780, 4.8673e+24, 16, (139, 125, 130))
    Earth3 = Planet3(-152.100e6*1000, 0, 0, 29290, 5.9722e+24, 18, (100, 149, 237))
    
    #initialize all planet data
    #while loop to run

    planets = [Sun3, Venus3, Earth3]
    planetsOnly = [Venus3, Earth3]
    while run:
         clock.tick(60)
         window3.fill((0,0,0))
         window3.blit(bg3, (0,0))
         for event in pygame.event.get():
              if event.type == pygame.QUIT:
                run = False
         for planet in planets:
              planet.update_pos(planets, planetsOnly)
              planet.draw(window3)
         pygame.display.update()
    pygame.quit()
            
Main()

#7. Be like Ptolemy! Use your orbital models to plot the orbits of the other bodies in the solar system, with a chosen object (e.g. Earth) at a fixed position at the origin of a Cartesian coordinate system. i.e. choose a coordinate system where your chosen object is at (0,0,0)

#Change number of iterations

x_final_1 = []
y_final_1 = []

x_final_2 = []
y_final_2 = []

x_final_3 = []
y_final_3 = []

x_final_4 = []
y_final_4 = []

for i in range(len(xpos_list_e)):
     plotxMer = xpos_list_e[i] - xpos_list_mer[i]
     plotxVen = xpos_list_e[i] - xpos_list_v[i]
     plotXMars = xpos_list_m[i] - xpos_list_e[i]
     plotyMer = ypos_list_e[i] - ypos_list_mer[i]
     plotyVen = ypos_list_e[i] - ypos_list_v[i]
     plotyMars = ypos_list_m[i] - ypos_list_e[i]
     plotxSun = xpos_list_e[i]-xpos_sun
     plotySun = ypos_list_e[i]-ypos_sun
     x_final_1.append(plotxMer)
     x_final_2.append(plotxVen)
     x_final_3.append(plotXMars)
     y_final_1.append(plotyMer)
     y_final_2.append(plotyVen)
     y_final_3.append(plotyMars)
     x_final_4.append(plotxSun)
     y_final_4.append(plotySun)


plt.plot(x_final_1, y_final_1, "-r", label = "Mercury")
plt.plot(x_final_2, y_final_2, "orange", label = "Venus")
plt.plot(x_final_3, y_final_3, "-g", label = "Mars")
plt.plot(x_final_4, y_final_4, "-y", label = "Sun")
plt.xlabel("x / m")
plt.ylabel("y / m")
plt.scatter(0, 0, color='blue', marker='o', s=30, label = "Earth")
plt.legend()
plt.axis("equal")
plt.show()

x_final_6 = []
y_final_6 = []

x_final_7 = []
y_final_7 = []

x_final_8 = []
y_final_8 = []

x_final_9 = []
y_final_9 = []

x_final_10 = []
y_final_10 = []

for i in range(len(xpos_list_sat)):
     plotxJup = xpos_list_sat[i] - xpos_list_j[i]
     plotxUra = xpos_list_ura[i] - xpos_list_sat[i]
     plotXNep = xpos_list_nep[i] - xpos_list_sat[i]
     plotyJup = ypos_list_sat[i] - ypos_list_j[i]
     plotyUra = ypos_list_ura[i] - ypos_list_sat[i]
     plotyNep = ypos_list_nep[i] - ypos_list_sat[i]
     plotxPluto = xpos_list_p[i] - xpos_list_sat[i]
     plotyPluto = ypos_list_p[i] - ypos_list_sat[i]
     plotxSun = xpos_list_sat[i]-xpos_sun
     plotySun = ypos_list_sat[i]-ypos_sun
     x_final_6.append(plotxJup)
     x_final_7.append(plotxUra)
     x_final_8.append(plotXNep)
     y_final_6.append(plotyJup)
     y_final_7.append(plotyUra)
     y_final_8.append(plotyNep)
     x_final_9.append(plotxSun)
     y_final_9.append(plotySun)
     x_final_10.append(plotxPluto)
     y_final_10.append(plotyPluto)


plt.plot(x_final_6, y_final_6, "-r", label = "Jupiter")
plt.plot(x_final_7, y_final_7, "orange", label = "Uranus")
plt.plot(x_final_8, y_final_8, "-g", label = "Neptune")
plt.plot(x_final_9, y_final_9, "-b", label = "Sun")
plt.plot(x_final_10, y_final_10, "violet", label = "Pluto")
plt.xlabel("x / m")
plt.ylabel("y / m")
plt.scatter(0, 0, color='yellow', marker='o', s=30, label = "Saturn")
plt.legend()
plt.axis("equal")
plt.show()

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

fig5 = plt.figure(figsize=(10,10))
ax5 = plt.axes(projection='3d')
ax5.axis("auto")

ax5.set_xlim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)
ax5.set_ylim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)
ax5.set_zlim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)



for i in range(len(xpos_list_e)):
     plotxMer = x_rotated_earth[i] - x_rotated_mer[i]
     plotxVen = x_rotated_earth[i] - x_rotated_ven[i]
     plotXMars = x_rotated_m[i] - x_rotated_earth[i]
     plotyMer = y_rotated_earth[i] - y_rotated_mer[i]
     plotyVen = y_rotated_earth[i] - y_rotated_ven[i]
     plotyMars = y_rotated_m[i] - y_rotated_earth[i]
     plotzMer = z_rotated_earth[i] - z_rotated_mer[i]
     plotzVen = z_rotated_earth[i] - z_rotated_ven[i]
     plotzMars = z_rotated_m[i] - z_rotated_earth[i]
     plotxSun = x_rotated_earth[i]-xpos_sun
     plotySun = y_rotated_earth[i]-ypos_sun
     plotzSun = z_rotated_earth[i]-zpos_sun
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
ax5.scatter(0, 0, 0, color='orange', marker='o', s=30)
ax5.legend()
plt.show()

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

fig2 = plt.figure(figsize=(10,10))
ax2 = plt.axes(projection='3d')
ax2.axis("auto")

ax2.set_xlim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)
ax2.set_ylim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)
ax2.set_zlim(-axis_size*astronomical_unit*10,axis_size*astronomical_unit*10)

for i in range(len(xpos_list_sat)):
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
     plotxSun = x_rotated_sat[i]-xpos_sun
     plotySun = y_rotated_sat[i]-ypos_sun
     plotzSun = z_rotated_sat[i]-zpos_sun
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
ax2.scatter(0, 0, 0, color='orange', marker='o', s=30)
ax2.legend()
plt.show()

#8. Extension Task --> Plotting a 3D Orbit of Gliese 876 Planetary System, with Gl 876 d, Gl 876 c, Gl 876 b, Gl 876 e

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


fig4 = plt.figure(figsize=(10,10))
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
plt.show()
