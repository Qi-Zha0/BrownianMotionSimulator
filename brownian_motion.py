"""
Author: Meiqi "Qi" Zhao
Created Mar 24, 2023
This python module supports simulation of one or more Brownian particles within an arena
 """

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class BrownianRobot:
    def __init__(self, mass, radius, position, velocity, color='blue'):
        self.mass = mass
        self.radius = radius
        self.position = position
        self.velocity = velocity
        self.color = color


class BrownianMotion:
    def __init__(self, arena_size, robots):
        self.arena_size = arena_size
        self.robots = robots
        self.eps = 1e-5

    def check_collision(self, r1, r2):
        distance = np.linalg.norm(r1.position - r2.position)
        return distance <= (r1.radius + r2.radius) + self.eps

    def collide_robots(self, r1, r2):
        # referencee: https://en.wikipedia.org/wiki/Elastic_collision
        v_rel = r1.velocity - r2.velocity
        n = r1.position - r2.position
        n_hat = n / np.linalg.norm(n)
        r1.velocity -= 2 * r2.mass / (r1.mass + r2.mass) * np.dot(v_rel, n_hat) * n_hat
        r2.velocity -= 2 * r1.mass / (r1.mass + r2.mass) * np.dot(-1.0*v_rel, -1.0*n_hat) * -1.0*n_hat

    def collide_boundary(self, robot):
        # elastic collision
        # for i in range(2):      
        #     if (robot.position[i] - robot.radius <= self.eps and robot.velocity[i] < 0) or (
        #         robot.position[i] + robot.radius >= self.arena_size[i] - self.eps and robot.velocity[i] > 0
        #     ):
        #         robot.velocity[i] = -robot.velocity[i]

        # randomly rotate an angle when reaching boundary
        speed = np.linalg.norm(robot.velocity)
        for i in range(2):
            if (robot.position[i] - robot.radius <= self.eps and robot.velocity[i] < 0) or (
                robot.position[i] + robot.radius >= self.arena_size[i] - self.eps and robot.velocity[i] > 0
            ):
                rand_vel_i = np.random.uniform(0, speed)
                robot.velocity[i] = rand_vel_i if robot.velocity[i] < 0 else -1.0 * rand_vel_i
                robot.velocity[1-i] = np.random.choice([-1.0, 1.0]) * np.sqrt(speed * speed - robot.velocity[i] * robot.velocity[i])



    def step(self, dt):
        for robot in self.robots:
            # Update positions
            robot.position += robot.velocity * dt

            # Handle collisions with arena boundaries
            self.collide_boundary(robot)

        # Handle collisions between robots
        for i in range(len(self.robots)):
            for j in range(i + 1, len(self.robots)):
                r1, r2 = self.robots[i], self.robots[j]
                if self.check_collision(r1, r2):
                    self.collide_robots(r1, r2)

    def plot_arena(self, ax):
        ax.set_xlim(0, self.arena_size[0])
        ax.set_ylim(0, self.arena_size[1])
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])

    def simulate(self, num_steps, time_step):
        print("Simulating...")
        self.history = []
        for _ in range(num_steps):
            self.history.append([np.copy(robot.position) for robot in self.robots])
            self.step(time_step)
        return self.history

    def visualize(self, num_steps, time_step, show_plot=True, filename=None):
        fig, ax = plt.subplots(figsize=(10, self.arena_size[0]*self.arena_size[1]/10))
        self.plot_arena(ax)

        def animate(i):
            ax.clear()
            self.plot_arena(ax)
            for j, robot in enumerate(self.robots):
                self.history[i][j][0] = np.maximum(self.history[i][j][0], robot.radius+self.eps)
                self.history[i][j][1] = np.maximum(self.history[i][j][1], robot.radius+self.eps)
                self.history[i][j][0] = np.minimum(self.history[i][j][0], self.arena_size[0]-self.eps)
                self.history[i][j][1] = np.minimum(self.history[i][j][1], self.arena_size[1]-self.eps)
                circle = plt.Circle(self.history[i][j], robot.radius, fc=robot.color)
                ax.add_artist(circle)

        ani = animation.FuncAnimation(fig, animate, frames=len(self.history), interval=100, blit=False)
        if show_plot:
            plt.show()
        plt.close(fig)
        if filename:
            print("Generating gif...it will take a minute")
            ani.save(filename, writer='pillow', fps=int(1 / time_step))
            print("Done")