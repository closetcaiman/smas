import random
from typing import List

from agent import Agent
from enums import Action, Food
from genome import cross_genomes, make_starting_genome
from grid import Grid
from region import Region, energy_amount_from_food


def run_simulation(num_steps):
    print("Initializing...", end="")
    grid = Grid(10, 10)
    regions = list(grid.regions())
    initialize_agents(20, random.sample(regions, 20))
    print("Done")

    print("Simulation start")
    for i in range(num_steps):
        print(
            f"---\nStep #{i + 1} num of agents: {sum([len(region.agents) for region in grid.regions()])}"
        )
        stats = {"born": 0, "dead": 0}
        for region in grid.regions():
            region_stats = perform_agent_actions(region)
            update_region(region)
            stats["born"] += region_stats["born"]
            stats["dead"] += region_stats["dead"]
        print(stats)


def initialize_agents(num_agents_per_region: int, regions: List[Region]):
    for region in regions:
        agents = []
        for _ in range(num_agents_per_region):
            agents.append(
                Agent(
                    energy=random.randrange(100, 150),
                    age=0,
                    time_since_last_breeding=0,
                    genome=make_starting_genome(),
                    temperature=20,
                )
            )
        region.agents = agents


def perform_agent_actions(region: Region):
    reproducing_agents = [
        agent for agent in region.agents if agent.wants_action() == Action.REPRODUCE
    ]
    migrating_agents = [
        agent for agent in region.agents if agent.wants_action() == Action.MIGRATE
    ]
    eating_agents = [
        agent for agent in region.agents if agent.wants_action() == Action.EAT
    ]

    new_agents = []
    if len(reproducing_agents) > 1:
        new_agents = breed_agents(reproducing_agents)
        region.agents.extend(new_agents)
    migrate_agents(region, migrating_agents)
    feed_agents(region, eating_agents)
    dead_agents = remove_dead_agents(region)
    return {"born": len(new_agents), "dead": len(dead_agents)}


def breed_agents(reproducing_agents: List[Agent]) -> List[Agent]:
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
                genome=cross_genomes(a[i].genome, b[i].genome),
                temperature=a[i].temperature,
            )
        )
    return new_agents


def migrate_agents(current_region: Region, migrating_agents: List[Agent]):
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


def feed_agents(region: Region, eating_agents: List[Agent]):
    for agent in eating_agents:
        for pref in agent.genome.preferred_food.value:
            if pref == Food.GRASS.value and region.grass_amount > 0:
                agent.energy += energy_amount_from_food(Food.GRASS)
            elif pref == Food.TALL_GRASS.value and region.tall_grass_amount > 0:
                agent.energy += energy_amount_from_food(Food.TALL_GRASS)
            elif (
                pref == Food.FRUIT
                and agent.genome.size.value >= 40
                and region.fruit_amount > 0
            ):
                agent.energy += energy_amount_from_food(Food.FRUIT)


def remove_dead_agents(region: Region):
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


def update_region(region: Region):
    region.step_simulation()
