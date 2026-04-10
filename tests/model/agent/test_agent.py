from model.agent.action import Action
from model.agent.agent import Agent
from model.agent.genome.genome_factory import create_genome


class TestAgent:
    def test_initialization(self):
        genome = create_genome()
        agent = Agent(
            energy=100,
            age=0,
            temperature=20,
            time_since_last_breeding=0,
            genome=genome,
        )
        assert agent.energy == 100
        assert agent.age == 0
        assert agent.temperature == 20

    def test_get_wanted_action_returns_valid_action(self):
        genome = create_genome()
        agent = Agent(
            energy=100,
            age=50,
            temperature=20,
            time_since_last_breeding=100,
            genome=genome,
        )
        action = agent.get_wanted_action()
        assert action in [Action.EAT, Action.MIGRATE, Action.REPRODUCE]

    def test_step_simulation_decreases_energy(self):
        genome = create_genome()
        agent = Agent(
            energy=100,
            age=0,
            temperature=20,
            time_since_last_breeding=0,
            genome=genome,
        )
        initial_energy = agent.energy
        agent.step_simulation()
        assert agent.energy < initial_energy
        assert agent.age == 1
        assert agent.time_since_last_breeding == 1

    def test_apply_reproduction_cost(self):
        genome = create_genome()
        initial_energy = 100
        agent = Agent(
            energy=initial_energy,
            age=50,
            temperature=20,
            time_since_last_breeding=100,
            genome=genome,
        )
        agent.apply_reproduction_cost()
        assert agent.energy < initial_energy
        assert agent.time_since_last_breeding == 0
