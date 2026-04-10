from model.simulation import Simulation


class TestSimulation:
    def test_initialization(self):
        sim = Simulation(grid_width=5, grid_height=5, num_agents_per_region=3)
        assert sim.grid._width == 5
        assert sim.grid._height == 5
        total_agents = sum(len(r.agents) for r in sim.grid.regions)
        assert total_agents == 75

    def test_initialization_creates_agents(self):
        sim = Simulation(grid_width=2, grid_height=2, num_agents_per_region=2)
        for region in sim.grid.regions:
            assert len(region.agents) == 2

    def test_run_completes_without_error(self):
        sim = Simulation(grid_width=2, grid_height=2, num_agents_per_region=5)
        sim.run(num_steps=3)

    def test_run_updates_agents(self):
        sim = Simulation(grid_width=2, grid_height=2, num_agents_per_region=5)
        initial_total_age = sum(a.age for r in sim.grid.regions for a in r.agents)
        sim.run(num_steps=1)
        final_total_age = sum(a.age for r in sim.grid.regions for a in r.agents)
        assert final_total_age > initial_total_age
