"""Type definitions for simulation data structures."""

from typing import TypedDict

from pandera.typing import DataFrame

from metrics.types.agent_dataframe import PCADataSchema
from model.agent.genome import FullGenome
from model.world.elements.food import FoodResources
from model.world.types import PopulationType

type RegionCoordinates = tuple[int, int]


class AgentData(TypedDict):
    """Data about an agent at a specific epoch."""

    energy: int
    age: int
    temperature: int
    time_since_last_breeding: int
    genome: FullGenome


class RegionData(TypedDict):
    """Data about a region at a specific epoch."""

    agent_data: list[AgentData]
    region_coordinates: RegionCoordinates

    current_agents: int
    born_agents: int
    dead_agents: int

    temperature: int
    food_resources: FoodResources

    is_barrier: bool
    max_agents: int
    migrate_in_cost: int
    migrate_out_cost: int
    population_type: PopulationType


class SimulationData(TypedDict):
    """Data about the entire simulation at a specific epoch."""

    epoch: int
    region_data: dict[RegionCoordinates, RegionData]


class SimulationMetrics(TypedDict):
    """Metrics calculated for a specific epoch."""

    epoch: int
    fst: float
    bhattacharyya_distance: float
    pca: DataFrame[PCADataSchema]
