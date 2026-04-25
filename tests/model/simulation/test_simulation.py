from model.simulation import Simulation


class TestSimulation:
    def test_initialization(self, mock_sample, mock_mediator):
        sim = Simulation(
            grid_width=5,
            grid_height=5,
            num_agents_per_region=3,
            controller_mediator=mock_mediator,
            sample=mock_sample,
        )
        assert sim.world.width == 5
        assert sim.world.height == 5
        total_agents = sum(len(r.agents) for r in sim.world.regions)
        assert total_agents == 75

    def test_initialization_creates_agents(self, mock_sample, mock_mediator):
        sim = Simulation(
            grid_width=2,
            grid_height=2,
            num_agents_per_region=2,
            controller_mediator=mock_mediator,
            sample=mock_sample,
        )
        for region in sim.world.regions:
            if not region.is_barrier:
                assert len(region.agents) == 2

    def test_run_completes_without_error(self, mock_sample, mock_mediator):
        sim = Simulation(
            grid_width=2,
            grid_height=2,
            num_agents_per_region=5,
            controller_mediator=mock_mediator,
            sample=mock_sample,
        )
        for _ in range(5):
            sim.step()

    def test_run_updates_agents(self, mock_sample, mock_mediator):
        sim = Simulation(
            grid_width=2,
            grid_height=2,
            num_agents_per_region=5,
            controller_mediator=mock_mediator,
            sample=mock_sample,
        )
        initial_total_age = sum(a.age for r in sim.world.regions for a in r.agents)
        sim.step()
        final_total_age = sum(a.age for r in sim.world.regions for a in r.agents)
        assert final_total_age > initial_total_age

    def test_step_increments_count(self, mock_sample, mock_mediator):
        sim = Simulation(
            grid_width=2,
            grid_height=2,
            num_agents_per_region=2,
            controller_mediator=mock_mediator,
            sample=mock_sample,
        )
        assert sim.epoch == 0
        sim.step()
        assert sim.epoch == 1
