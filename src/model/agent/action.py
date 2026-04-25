from enum import Enum


class Action(Enum):
    """
    Defines the possible actions an agent can take in the simulation.

    EAT: The agent will attempt to consume available food in its current region to gain energy.
    MIGRATE: The agent will attempt to move to a neighboring region, incurring energy costs based on the migration cost of the regions involved.
    REPRODUCE: The agent will attempt to reproduce, creating a new agent with a genome derived from its own and possibly another agent's genome. This action can only be taken if the agent has sufficient energy and meets the breeding conditions defined in its genome.

    """

    EAT = 0
    MIGRATE = 1
    REPRODUCE = 2
