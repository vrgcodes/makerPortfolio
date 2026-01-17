import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy import sparse
from scipy.sparse import linalg as ln

class WavePacket:
    def __init__(
        self, n_points, dt, sigma0=5, p0=1, x0=-150,
        x_begin=-200, x_end=200, barrier_height=1, barrier_width=1
    ):
        # Initial parameters
        self.n_points = n_points
        self.sigma0 = sigma0
        self.p0 = p0
        self.x0 = x0
        self.x_begin = x_begin
        self.dt = dt
        self.probability = np.zeros(n_points)
        self.barrier_height = barrier_height
        self.barrier_width = barrier_width

        # Discrete space
        self.x, self.dx = np.linspace(x_begin, x_end, n_points, retstep=True)

        # Initial Gaussian wave packet
        gaussian = (2 * np.pi * (sigma0 ** 2)) ** (-1 / 4)
        self.waveFunction = (
            gaussian
            * np.exp(-(((self.x - x0) / (2 * sigma0)) ** 2))
            * np.exp(1j * p0 * self.x)
        )

        # Potential barrier: V(x) = barrier_height for 0 < x < barrier_width else 0
        self.potential = np.array(
            [barrier_height if (0 < x < barrier_width) else 0.0 for x in self.x],
            dtype=np.float64
        )

        # Hamiltonian (finite difference Laplacian + potential)
        H_diagonal = (np.ones(n_points) / (self.dx ** 2)) + self.potential
        H_non_diagonal = np.ones(n_points - 1) * (-0.5 / (self.dx ** 2))
        hamiltonian = sparse.diags(
            [H_diagonal, H_non_diagonal, H_non_diagonal],
            [0, 1, -1],
            format="csc"
        )

        # Crank–Nicolson time evolution matrix
        I = sparse.eye(self.n_points, format="csc")
        forward = (I - ((dt / (2j)) * hamiltonian)).tocsc()
        backward = (I + ((dt / (2j)) * hamiltonian)).tocsc()
        self.evolution_matrix = ln.inv(forward).dot(backward).tocsr()

    def evolve(self):
        self.waveFunction = self.evolution_matrix.dot(self.waveFunction)
        self.probability = np.abs(self.waveFunction) ** 2

        # Normalize
        normalized = np.sum(self.probability)
        self.probability /= normalized
        self.waveFunction /= np.sqrt(normalized)

        return self.probability


class Animator:
    def __init__(self, wave_packet):
        self.time = 0.0
        self.wave_packet = wave_packet

        self.fig, self.ax = plt.subplots()
        self.ax.plot(self.wave_packet.x, self.wave_packet.potential * 0.1, color="r")

        self.time_text = self.ax.text(
            0.05, 0.95, "",
            horizontalalignment="left",
            verticalalignment="top",
            transform=self.ax.transAxes
        )

        self.line, = self.ax.plot(self.wave_packet.x, self.wave_packet.evolve())
        self.ax.set_ylim(0, 0.2)
        self.ax.set_xlabel("Position (a$_0$)")
        self.ax.set_ylabel("Probability density (a$_0^{-1}$)")

    def update(self, data):
        self.line.set_ydata(data)
        return (self.line,)

    def advance_time(self):
        while True:
            self.time += self.wave_packet.dt
            self.time_text.set_text(f"Elapsed Time: {self.time * 2.419e-2:6.2f} fs")
            yield self.wave_packet.evolve()

    def animate(self):
        self.animation = animation.FuncAnimation(
            self.fig, self.update, self.advance_time, interval=25, blit=False
        )


wave_packet = WavePacket(n_points=500, dt=0.5, barrier_height=1, barrier_width=1)
animator = Animator(wave_packet)
animator.animate()
plt.show()
