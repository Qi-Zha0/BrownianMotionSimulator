from brownian_motion import BrownianRobot, BrownianMotion
import numpy as np
import matplotlib.colors as mcolors
import argparse

def generate_random_robots(num, arena_size, radius=0.1, mass=1, max_vel=1.5):
	num_robots = num
	radius = radius
	mass = mass
	max_vel_abs = max_vel
	arena_size = arena_size

	robots = []
	colors = list(mcolors.CSS4_COLORS.keys())

	# Evenly divide arena into n x n grid
	grid_n = np.floor(np.sqrt(num_robots)) + 1 
	grid_size = arena_size / grid_n
	positions = np.arange(0, grid_n*grid_n, 1, dtype=int)

	# Randomize positions
	np.random.shuffle(positions)

	for i in range(num_robots):
		# Set robot velocity
		vel = np.array(np.random.uniform(-1.0*max_vel_abs, max_vel_abs, 2))

		# Set robot color
		color = np.random.choice(colors)

		# Set robot position
		idx = positions[i]
		grid_r = idx // grid_n
		grid_c = idx % grid_n
		pos = np.array([
						np.random.uniform(grid_c * grid_size[0]+radius, grid_c * grid_size[0] - radius + grid_size[0]),
						arena_size[1] - np.random.uniform(grid_r * grid_size[1]+radius, grid_r * grid_size[1] - radius + grid_size[1])
						])

		robot = BrownianRobot(mass, radius, pos, vel, color=color)
		robots.append(robot)
	return robots


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--filename", help="Enter a filename to save to, e.g. brownian.gif", required=True)
	parser.add_argument("-n", "--num", help="Enter the number of particles to simulate", required=False, default=120, type=int)
	args = parser.parse_args()
	filename = args.filename
	N = args.num
	
	# Randomly generate 100 small circle/robots
	arena_size = np.array([8, 8])
	robots = generate_random_robots(N, arena_size)

	# Clear a patch and place some bigger circles
	# for robot in robots:
	# 	if (3.5 < robot.position[0] < 4.5) and (3.5 < robot.position[1] < 4.5):
	# 		robots.remove(robot)
	# 	if (1.0 < robot.position[0] < 2.0) and (3.0 < robot.position[1] < 4.0):
	# 		robots.remove(robot)
	# 	if (5.0 < robot.position[0] < 6.0) and (1.0 < robot.position[1] < 2.0):
	# 		robots.remove(robot)
	# robots.append(BrownianRobot(5, 0.2, np.array([4.0, 4.0]), np.array([0.0, 0.1]), color='royalblue'))
	# robots.append(BrownianRobot(5, 0.2, np.array([1.5, 3.5]), np.array([0.0, 0.1]), color='royalblue'))
	# robots.append(BrownianRobot(5, 0.2, np.array([5.5, 1.5]), np.array([0.0, 0.1]), color='royalblue'))

	# Create simulation
	simulation = BrownianMotion(arena_size, robots)

	# Configure simulation
	num_steps = 500
	time_step = 0.01

	# Simulate the motion and save the positions history
	simulation.simulate(num_steps, time_step)

	# Save the animation as a GIF
	simulation.visualize(num_steps, time_step, show_plot=False, filename=filename)