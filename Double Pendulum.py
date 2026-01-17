import matplotlib
matplotlib.use('tkAgg') # 'tkAgg' if Qt not present 
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import scipy as sp
import numpy as np
import math

class DoublePendulum:
    def __init__(self, theta1, theta2, dt):
        self.theta1 = theta1	
        self.theta2 = theta2
        
        self.dt = dt
        
        self.p1 = 0.0
        self.p2 = 0.0

        self.gravity = 9.81
        self.length = 1.0

        self.trajectory = [self.polar_to_cartesian()]
    def polar_to_cartesian(self):
        x1 = self.length*math.sin(self.theta1)
        y1 = -1*self.length*math.cos(self.theta1)

        x2 = x1+(self.length*math.sin(self.theta2))
        y2 = y1-(self.length*math.cos(self.theta2))

        return np.array([[0.0,0.0], [x1,y1], [x2,y2]])
    def numericalSol(self):
        theta1 = self.theta1
        theta2 = self.theta2
        p1 = self.p1
        p2 = self.p2
        g = self.gravity
        l = self.length

        expr1 = (1+(math.sin(theta1-theta2))**2)
        theta1_dot = (p1-(p2*math.cos(theta1-theta2)))/expr1
        theta2_dot = ((2*p2)-(p1*math.cos(theta1-theta2)))/expr1
        expr2 = -2*g*math.sin(theta1)*l
        expr3 = -1*g*math.sin(theta2)*l
        expr4 = (p1*p2*math.sin(theta1-theta2))/expr1
        expr5 = (((p1**2)+(2*(p2**2))-(p1*p2*math.cos(theta1-theta2)))*math.sin(2*(theta1-theta2)))/(2*(expr1**2))
        p1_dot = expr2-(expr4-expr5)
        p2_dot = expr3+(expr4-expr5)
        self.theta1 += self.dt*theta1_dot
        self.theta2 += self.dt*theta2_dot
        self.p1 += self.dt*p1_dot
        self.p2 += self.dt*p2_dot

        updated_pos = self.polar_to_cartesian()
        self.trajectory.append(updated_pos)
        return updated_pos
    
class Animator:
    def __init__(self, pendulum, draw_trace=False):
        self.pendulum = pendulum
        self.draw_trace = draw_trace
        self.time = 0.0

        self.fig, self.ax = plt.subplots()
        self.ax.set_ylim(-2.5, 2.5)
        self.ax.set_xlim(-2.5,2.5)

        self.time_text = self.ax.text(0.05,0.95,'',horizontalalignment='left', verticalalignment='top', transform=self.ax.transAxes)

        self.line, = self.ax.plot(self.pendulum.trajectory[-1][:,0], self.pendulum.trajectory[-1][:, 1], marker='o')

        if self.draw_trace:
            self.trace, = self.ax.plot([a[2,0] for a in self.pendulum.trajectory], [a[2,1] for a in self.pendulum.trajectory])

    def advance_time(self):
        while True:
            self.time += self.pendulum.dt
            yield self.pendulum.numericalSol()

    def update(self,data):
        self.time_text.set_text("Elapsed Time: {:6.2f}s".format(self.time))

        self.line.set_xdata(data[:,0])
        self.line.set_ydata(data[:,1])

        if self.draw_trace:
            self.trace.set_xdata([a[2,0] for a in self.pendulum.trajectory])
            self.trace.set_ydata([a[2,1] for a in self.pendulum.trajectory])
        return self.line,

    def animate(self):
        self.animation = animation.FuncAnimation(self.fig, self.update, self.advance_time, interval = 25, blit=False)

pendulum = DoublePendulum(theta1=sp.constants.pi, theta2=sp.constants.pi-0.01, dt=0.01)
animator = Animator(pendulum=pendulum, draw_trace=True)
animator.animate()
plt.show()