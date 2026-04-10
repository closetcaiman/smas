import random
from typing import List

from model.agent.action import Action
from model.agent.agent import Agent
from model.agent.genome.genome_factory import create_genome, crossover_genomes
from model.map.food_type import FoodType
from model.map.grid import Grid
from model.map.region import Region


class Simulation:
    def __init__(self, grid_width: int, grid_height: int, num_agents_per_region: int):
        self.grid = Grid(grid_width, grid_height)
        regions = list(self.grid.regions)
        self._initialize_agents(num_agents_per_region, regions)
        self.step_count = 0

    def _initialize_agents(self, num_agents_per_region: int, regions: List[Region]):
        for region in regions:
            agents = []
            for _ in range(num_agents_per_region):
                agents.append(
                    Agent(
                        energy=random.randrange(100, 150),
                        age=0,
                        time_since_last_breeding=0,
                        genome=create_genome(),
                        temperature=20,
                    )
                )
            region.agents = agents

    def run(self, num_steps: int, print_stats: bool = False):
        for _ in range(num_steps):
            if print_stats:
                print(self.step())
            else:
                self.step()

    def step(self):
        self.step_count += 1
        return self._step()

    def _step(self):
        stats: dict[str, int] = {}
        for region in self.grid.regions:
            region_stats = self._perform_agent_actions(region)
            stats["born"] = stats.get("born", 0) + region_stats.get("born", 0)
            stats["dead"] = stats.get("dead", 0) + region_stats.get("dead", 0)
            region.step_simulation()
        return {
            "step": self.step_count,
            "born": stats.get("born", 0),
            "dead": stats.get("dead", 0),
        }

    def _perform_agent_actions(self, region: Region) -> dict[str, int]:
        reproducing_agents = [
            agent
            for agent in region.agents
            if agent.get_wanted_action() == Action.REPRODUCE
        ]
        migrating_agents = [
            agent
            for agent in region.agents
            if agent.get_wanted_action() == Action.MIGRATE
        ]
        eating_agents = [
            agent for agent in region.agents if agent.get_wanted_action() == Action.EAT
        ]

        new_agents = []
        if len(reproducing_agents) > 1:
            new_agents = self._breed_agents(reproducing_agents)
            region.agents.extend(new_agents)
        self._migrate_agents(region, migrating_agents)
        self._feed_agents(region, eating_agents)
        dead_agents = self._remove_dead_agents(region)
        return {"born": len(new_agents), "dead": len(dead_agents)}

    def _breed_agents(self, reproducing_agents: List[Agent]) -> List[Agent]:
        random.shuffle(reproducing_agents)
        a = reproducing_agents[: len(reproducing_agents) // 2]
        b = reproducing_agents[len(a) :]
        new_agents = []
        if len(a) < len(b):
            a.append(a[-1])
        for i in range(len(a)):
            new_agents.append(
                Agent(
                    energy=(a[i].energy + b[i].energy) // 2,
                    age=0,
                    time_since_last_breeding=0,
                    genome=crossover_genomes(a[i].genome, b[i].genome),
                    temperature=a[i].temperature,
                )
            )
        return new_agents

    def _migrate_agents(self, current_region: Region, migrating_agents: List[Agent]):
        for agent in migrating_agents:
            available_regions = [
                r
                for r in current_region.neighbors
                if current_region.migrate_out_cost + r.migrate_in_cost < agent.energy
            ]
            if len(available_regions) > 0:
                selected_region = random.choice(available_regions)
                agent.energy -= (
                    current_region.migrate_out_cost + selected_region.migrate_in_cost
                )
                current_region.agents.remove(agent)
                selected_region.agents.append(agent)

    def _feed_agents(self, region: Region, eating_agents: List[Agent]):
        for agent in eating_agents:
            for pref in agent.genome.preferred_food.value:
                if pref == FoodType.GRASS.value and region.food.grass_amount > 0:
                    agent.energy += FoodType.GRASS.energy_amount()
                elif (
                    pref == FoodType.TALL_GRASS.value
                    and region.food.tall_grass_amount > 0
                ):
                    agent.energy += FoodType.TALL_GRASS.energy_amount()
                elif (
                    pref == FoodType.FRUIT.value
                    and agent.genome.size.value >= 40
                    and region.food.fruit_amount > 0
                ):
                    agent.energy += FoodType.FRUIT.energy_amount()

    def _remove_dead_agents(self, region: Region) -> List[Agent]:
        living_agents = []
        dead_agents = []
        for agent in region.agents:
            if agent.energy > 0:
                living_agents.append(agent)
            else:
                dead_agents.append(agent)
        if len(living_agents) > region.max_agents:
            living_agents.sort(key=lambda agent: -agent.energy)
            living_agents = living_agents[: region.max_agents]
            dead_agents.extend(living_agents[region.max_agents :])
        region.agents = living_agents
        return dead_agents
