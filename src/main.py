from model.simulation import Simulation


def main():
    sim = Simulation(grid_width=12, grid_height=8, num_agents_per_region=5)
    sim.run(num_steps=100, print_stats=True)


if __name__ == "__main__":
    main()
