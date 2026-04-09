from model.simulation import Simulation

if __name__ == "__main__":
    sim = Simulation(grid_width=10, grid_height=10, num_agents_per_region=20)
    sim.run(200)
