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

    def test_step_simulation_increases_metabolic_cost_with_age(self):
        genome = create_genome()
        genome.from_dna(genome.to_dna())

        ideal_temp = genome.ideal_temperature.value
        agent_young = Agent(
            energy=200,
            age=0,
            temperature=ideal_temp,
            time_since_last_breeding=0,
            genome=genome,
        )
        agent_old = Agent(
            energy=200,
            age=500,
            temperature=ideal_temp,
            time_since_last_breeding=0,
            genome=genome,
        )
        metabolic_rate = genome.metabolic_rate.value
        young_cost = round(metabolic_rate * (1 + 0))
        old_cost = round(metabolic_rate * (1 + 500 / 500))
        agent_young.step_simulation()
        agent_old.step_simulation()
        assert agent_young.energy == 200 - young_cost
        assert agent_old.energy == 200 - old_cost

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

    def test_reproduce_only_when_energy_and_age_sufficient(self):
        genome = create_genome()
        genome.min_energy_to_reproduce.value = 80
        genome.maturity_age.value = 50
        genome.breeding_interval.value = 10

        young_low_energy = Agent(
            energy=50,
            age=10,
            temperature=20,
            time_since_last_breeding=100,
            genome=genome,
        )
        for _ in range(100):
            action = young_low_energy.get_wanted_action()
            assert action != Action.REPRODUCE
