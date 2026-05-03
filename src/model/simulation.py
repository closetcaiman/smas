import random
from typing import List

from config.default import BehaviourConfig, ModelConfig
from controller.handlers.sampling import WorldMapSample
from controller.mediator import SimulationMediator
from model.agent import Breeder, GenomeFactory
from model.agent.action import Action
from model.agent.agent import Agent
from model.world import FoodType, Region, World


class Simulation:
    """
    Class representing the entire simulation, including the grid of regions and the agents within them.

    The Simulation class is responsible for initializing the world state, managing the progression of time (epochs),
    and coordinating the actions of agents within their respective regions. It interacts with the SimulationMediator
    to record significant events such as births and deaths for data tracking and analysis.

    Methods:
        step: Advances the simulation by one epoch, performing all agent actions and updating the world state.

    """

    def __init__(
        self,
        config: ModelConfig,
        behaviour: BehaviourConfig,
        controller_mediator: SimulationMediator,
        sample: WorldMapSample,
    ) -> None:
        """
        Initialize the simulation with a grid of regions and agents.

        The simulation is initialized with a grid of specified width and height, where each cell represents a region.
        Each region is populated with a specified number of agents, and the initial state of the world is recorded
        in the simulation data bank for historical tracking and analysis.

        Args:
            config (ModelConfig): The configuration for the model component.
            behaviour (BehaviourConfig): The configuration for how the simulation behaves.
            controller_mediator (SimulationMediator): The mediator for communication between simulation components.
            sample (WorldMapSample): The sampled seed data for initializing the world state.

        Returns:
            None

        """
        self.world = World(config.GRID_WIDTH, config.GRID_HEIGHT, sample)
        self.mediator = controller_mediator

        self.__config = config
        self.__behaviour = behaviour
        self.__epoch = 0
        self.__barrier_placed = False
        self.__initialize_agents(list(self.world.regions))

    @property
    def epoch(self) -> int:
        """Get the current epoch of the simulation."""
        return self.__epoch

    @property
    def barrier_placed(self) -> bool:
        """Check if the barrier has been placed in the simulation."""
        return self.__barrier_placed

    def step(self):
        """Advance the simulation by one epoch, performing all agent actions and updating the world state."""
        self.__epoch += 1
        self.mediator.databank.record_epoch(
            self.world, self.__epoch, self.__barrier_placed
        )
        for region in self.world.regions:
            if not region.is_barrier:
                self.__perform_agent_actions(region)
                region.step_simulation()

    def place_barrier(self, y: int) -> None:
        """
        Place a vertical barrier in the middle of the grid at the specified y-coordinate.

        Args:
            y (int): The y-coordinate at which to place the barrier. The barrier will be placed vertically across the grid.

        Returns:
            None

        """
        self.__barrier_placed = True
        col = self.world.grid_width // 2
        for region in self.world.regions:
            if region.coordinates[0] == col:
                region.make_barrier()

    def __initialize_agents(self, regions: List[Region]):
        for region in regions:
            agents = []
            for _ in range(self.__config.AGENTS_PER_REGION):
                agents.append(
                    Agent(
                        energy=random.randrange(
                            self.__config.AGENT_INITIAL_ENERGY_LOW,
                            self.__config.AGENT_INITIAL_ENERGY_HIGH,
                        ),
                        age=random.randrange(
                            self.__config.AGENT_INITIAL_AGE_LOW,
                            self.__config.AGENT_INITIAL_AGE_HIGH,
                        ),
                        temperature=random.randrange(
                            self.__config.AGENT_INITIAL_TEMP_LOW,
                            self.__config.AGENT_INITIAL_TEMP_HIGH,
                        ),
                        time_since_last_breeding=self.__config.AGENT_INITIAL_TIME_SINCE_LAST_BREEDING,
                        genome=GenomeFactory.create_genome(self.__config),
                    )
                )
            region.agents = agents

    def __perform_agent_actions(self, region: Region) -> None:
        """
        Perform actions for all agents in the region and return stats on births and deaths.

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
            if agent.get_wanted_action(self.__behaviour.agent) == Action.REPRODUCE
        ]
        migrating_agents = [
            agent
            for agent in region.agents
            if agent.get_wanted_action(self.__behaviour.agent) == Action.MIGRATE
        ]
        eating_agents = [
            agent
            for agent in region.agents
            if agent.get_wanted_action(self.__behaviour.agent) == Action.EAT
        ]

        self.__breed_agents(region, reproducing_agents)
        self.__migrate_agents(region, migrating_agents)
        self.__feed_agents(region, eating_agents)
        self.__remove_dead_agents(region)

    def __breed_agents(self, region: Region, reproducing_agents: List[Agent]) -> None:
        """
        Breed agents in pairs.

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
            region (Region): The region where the new agents will be added.
            reproducing_agents (List[Agent]): A list of agents that want to reproduce.

        Returns:
            None

        """
        if len(reproducing_agents) < 2:
            return

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
                    genome=Breeder.crossover_genomes(
                        a[i].genome, b[i].genome, self.__config
                    ),
                    temperature=a[i].temperature,
                )
            )

        region.agents.extend(new_agents)

        # Notify the mediator about the births for logging and data tracking
        self.mediator.record_birth(self.epoch, len(new_agents), region.coordinates)

    def __migrate_agents(
        self, current_region: Region, migrating_agents: List[Agent]
    ) -> None:
        """
        Try to migrate each agent to a random neighboring region if they have enough energy.

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
                and not r.is_barrier
            ]
            if len(available_regions) > 0:
                selected_region = random.choice(available_regions)
                agent.energy -= (
                    current_region.migrate_out_cost + selected_region.migrate_in_cost
                )
                current_region.agents.remove(agent)
                selected_region.agents.append(agent)

    def __feed_agents(self, region: Region, eating_agents: List[Agent]) -> None:
        """
        Feed agents based on their genome preferences and available food in the region.

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

    def __remove_dead_agents(self, region: Region) -> None:
        """
        Remove agents with energy <= 0 from the region and return them.

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

        # Notify the mediator about the deaths for logging and data tracking
        self.mediator.record_death(self.epoch, len(dead_agents), region.coordinates)
