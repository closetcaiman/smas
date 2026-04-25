import random
from typing import List

from model.agent.action import Action
from model.agent.agent import Agent
from model.agent.genome.genome_factory import create_genome, crossover_genomes
from model.map.food_type import FoodType
from model.map.grid import Grid
from model.map.map_image_sampler import MapImageSampler
from model.map.region import Region


class Simulation:
    def __init__(
        self,
        grid_width: int,
        grid_height: int,
        num_agents_per_region: int,
        sampler: MapImageSampler,
    ):
        self.grid = Grid(sampler, grid_width, grid_height)
        regions = list(self.grid.regions)
        self.__initialize_agents(num_agents_per_region, regions)
        self.step_count = 0

    def __initialize_agents(self, num_agents_per_region: int, regions: List[Region]):
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

    def step(self):
        self.step_count += 1
        return self.__step()

    def __step(self):
        stats: dict[str, int] = {}
        for region in self.grid.regions:
            region_stats = self.__perform_agent_actions(region)
            stats["born"] = stats.get("born", 0) + region_stats.get("born", 0)
            stats["dead"] = stats.get("dead", 0) + region_stats.get("dead", 0)
            region.step_simulation()
        return {
            "step": self.step_count,
            "born": stats.get("born", 0),
            "dead": stats.get("dead", 0),
        }

    def __perform_agent_actions(self, region: Region) -> dict[str, int]:
        """Perform actions for all agents in the region and return stats on births and deaths.

        The method categorizes agents based on their desired actions (reproduce, migrate, eat) and processes each category accordingly:
        - Reproducing agents are paired up to create new agents through the `__breed_agents` method.
        - Migrating agents attempt to move to neighboring regions if they have enough energy, using the `__migrate_agents` method.
        - Eating agents consume available food in the region based on their genome preferences, handled by the `__feed_agents` method.
        - After processing the actions, the method removes any agents that have died (energy <= 0)
          using the `__remove_dead_agents` method and returns a dictionary containing the count of new agents born and agents that died during this step.

        Args:
            region (Region): The region in which to perform agent actions.

        Returns:
            dict[str, int]: A dictionary with keys "born" and "dead" indicating the number of agents born and died in this step.

        """
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
            new_agents = self.__breed_agents(reproducing_agents)
            region.agents.extend(new_agents)

        self.__migrate_agents(region, migrating_agents)
        self.__feed_agents(region, eating_agents)

        dead_agents = self.__remove_dead_agents(region)

        return {"born": len(new_agents), "dead": len(dead_agents)}

    def __breed_agents(self, reproducing_agents: List[Agent]) -> List[Agent]:
        """Breed agents in pairs and return the list of new agents.

        The method takes a list of agents that want to reproduce and creates new agents by pairing them up.
        The list of reproducing agents is shuffled randomly to ensure random pairing.
        If there is an odd number of agents, the last one is duplicated to make an even number of agents for pairing.
        For each pair of agents, a new agent is created with the following properties:
        - Energy: The average of the two parent agents' energy.
        - Age: 0 (newborn).
        - Time since last breeding: 0 (newborn).
        - Genome: A new genome created by crossing over the genomes of the two parent agents using the `crossover_genomes` function.
        - Temperature: The same as the first parent agent's temperature.

        Args:
            reproducing_agents (List[Agent]): A list of agents that want to reproduce.

        Returns:
            List[Agent]: A list of new agents created from the reproducing agents.

        """
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

    def __migrate_agents(self, current_region: Region, migrating_agents: List[Agent]):
        """Try to migrate each agent to a random neighboring region if they have enough energy.

        The migration cost is the sum of the current region's `r_out.migrate_out_cost`
        and the target region's `r_in.migrate_in_cost`. The agent's energy cannot
        drop below 0 after paying the migration cost. If multiple neighboring
        regions are available, one is chosen via `random.choice()`.

        Args:
            current_region (Region): The region from which agents are migrating.
            migrating_agents (List[Agent]): The list of agents attempting to migrate.

        Returns:
            None

        """
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

    def __feed_agents(self, region: Region, eating_agents: List[Agent]):
        """Feed agents based on their genome preferences and available food in the region.

        Each agent has a list of preferred food types in their genome.
        The method iterates through each eating agent and checks their preferences in order.
        If the preferred food type is available in the region, the agent consumes it and gains energy accordingly.
        The method handles three food types: `GRASS`, `TALL_GRASS`, and `FRUIT`. For `FRUIT`,
        there is an additional requirement that the agent's size must be at least 40 to consume it.

        Args:
            region (Region): The region where the agents are located and food is available.
            eating_agents (List[Agent]): The list of agents attempting to eat.

        Returns:
            None

        """
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

    def __remove_dead_agents(self, region: Region) -> List[Agent]:
        """Remove agents with energy <= 0 from the region and return them.

        The method iterates through all agents in the region and separates them into two lists:
        - `living_agents` for those with energy greater than 0,
        - `dead_agents` for those with energy less than or equal to 0.

        If the number of living agents exceeds the region's `max_agents` limit,
        the living agents are sorted by energy in descending order,
        and only the top `max_agents` are kept as living agents,
        while the rest are moved to the dead agents list.

        Finally, the region's agents are updated to only include the living
        agents, and the method returns the list of dead agents.

        Args:
            region (Region): The region from which to remove dead agents.

        Returns:
            List[Agent]: A list of agents that have died (energy <= 0)
            or were removed due to overpopulation.

        """
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
