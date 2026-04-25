"""Data bank for storing simulation data."""

from controller.types import AgentData, RegionData, SimulationData
from model.world import World


class SimulationDataBank:
    """Stores historical simulation data for analysis and visualization."""

    def __init__(self) -> None:
        """Initialize an empty data bank."""
        self.simulation_history: dict[int, SimulationData] = {}

    def get_total_agents(self, epoch: int) -> int:
        """Calculate the total number of agents in the world for a specific epoch."""
        epoch_data = self.get_epoch_data(epoch)
        return sum(
            region["current_agents"] for region in epoch_data["region_data"].values()
        )

    def get_epoch_data(self, epoch: int) -> SimulationData:
        """Retrieve the data for a specific epoch."""
        if epoch not in self.simulation_history:
            raise ValueError(f"Epoch {epoch} not found in data bank.")
        return self.simulation_history[epoch]

    def record_epoch(self, world_state: World, epoch: int) -> None:
        """Record the state of the world at a specific epoch."""
        self.simulation_history[epoch] = self.__initialize_data(world_state, epoch)

    def record_births(self, epoch, region_coordinates, count):
        """Record births in the specified region and epoch."""
        if epoch not in self.simulation_history:
            raise ValueError(f"Epoch {epoch} not found in data bank.")

        region_data = self.simulation_history[epoch]["region_data"].get(
            region_coordinates
        )
        if not region_data:
            raise ValueError(
                f"Region {region_coordinates} not found in epoch {epoch} data."
            )

        region_data["born_agents"] += count

    def record_deaths(self, epoch, region_coordinates, count):
        """Record deaths in the specified region and epoch."""
        if epoch not in self.simulation_history:
            raise ValueError(f"Epoch {epoch} not found in data bank.")

        region_data = self.simulation_history[epoch]["region_data"].get(
            region_coordinates
        )
        if not region_data:
            raise ValueError(
                f"Region {region_coordinates} not found in epoch {epoch} data."
            )

        region_data["dead_agents"] += count

    def __initialize_data(self, world_state: World, epoch: int) -> SimulationData:
        """Map the current state of the World/Regions into the TypedDict format."""
        region_map: dict[tuple[int, int], RegionData] = {}

        for region in world_state.regions:
            # Create the AgentData list for this region
            agents_list: list[AgentData] = [
                {
                    "energy": a.energy,
                    "age": a.age,
                    "temperature": a.temperature,
                    "time_since_last_breeding": a.time_since_last_breeding,
                    "genome": a.genome,
                }
                for a in region.agents
            ]

            # Create the RegionData entry
            region_map[region.coordinates] = {
                "agent_data": agents_list,
                "region_coordinates": region.coordinates,
                "current_agents": len(region.agents),
                "born_agents": 0,  # Zero at start
                "dead_agents": 0,
                "temperature": region.temperature,
                "food_resources": region.food,
                "is_barrier": region.is_barrier,
                "max_agents": region.max_agents,
                "migrate_in_cost": region.migrate_in_cost,
                "migrate_out_cost": region.migrate_out_cost,
            }

        return {"epoch": epoch, "region_data": region_map}
