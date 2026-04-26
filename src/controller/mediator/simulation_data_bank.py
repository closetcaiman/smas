"""Data bank for storing simulation data."""

import os
from collections import deque
from pathlib import Path

import pyarrow as pa
import pyarrow.parquet as pq

from controller.types import AgentData, RegionData, SimulationData
from model.world import World


class SimulationDataBank:
    """Stores historical simulation data for analysis and visualization."""

    def __init__(
        self, storage_dir: Path | str, active_limit: int = 10, dump_data: bool = False
    ) -> None:
        """Initialize an empty data bank."""
        self.simulation_history: dict[int, SimulationData] = {}
        self.__storage_dir = Path(storage_dir)
        self.__active_limit = active_limit
        self.__dump_data = dump_data

        self.epoch_keys = deque()

        if not os.path.exists(self.__storage_dir) and self.__dump_data:
            os.makedirs(self.__storage_dir)

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
        epoch_data = self.__initialize_data(world_state, epoch)
        print(
            f"len of simulation history before recording: {len(self.simulation_history)}"
        )
        # 2. Update RAM Cache
        self.simulation_history[epoch] = epoch_data
        self.epoch_keys.append(epoch)

        # 3. If we hit the limit, flush the OLDEST to Parquet and remove from RAM
        if len(self.epoch_keys) > self.__active_limit:
            oldest_epoch = self.epoch_keys.popleft()
            data_to_flush = self.simulation_history.pop(oldest_epoch)

            if self.__dump_data:
                self.__save_to_parquet(data_to_flush)
            self.__flush_epoch(oldest_epoch)

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

    def __save_to_parquet(self, data: SimulationData):
        """Purely saves data to disk without modifying the original dictionary."""
        rows = []
        epoch = data["epoch"]

        # Non-destructive iteration
        for coords, region in data["region_data"].items():
            base_row: dict[str, int | float | str] = {
                "epoch": epoch,
                "region_x": coords[0],
                "region_y": coords[1],
                "region_temp": region["temperature"],
                "grass": region["food_resources"].grass_amount,
                "tall_grass": region["food_resources"].tall_grass_amount,
                "fruit": region["food_resources"].fruit_amount,
                "born_agents": region["born_agents"],
                "dead_agents": region["dead_agents"],
                "is_barrier": region["is_barrier"],
            }

            if not region["agent_data"]:
                rows.append(base_row)
            else:
                for agent in region["agent_data"]:
                    agent_row = base_row.copy()
                    agent_row.update(
                        {
                            "agent_energy": agent["energy"],
                            "agent_age": agent["age"],
                            "agent_time_breed": agent["time_since_last_breeding"],
                            "agent_temperature": agent["temperature"],
                            "agent_genome_dna": agent["genome"].to_dna(),
                        }
                    )
                    rows.append(agent_row)

        file_path = self.__storage_dir / f"epoch_{epoch:06d}.parquet"
        table = pa.Table.from_pylist(rows)
        pq.write_table(table, file_path, compression="snappy")

    def __flush_epoch(self, epoch: int):
        """Centralized memory destruction. Ensures data is completely cleared."""
        if epoch not in self.simulation_history:
            return

        data = self.simulation_history.pop(epoch)

        # Explicitly clear internal lists to break references for the GC
        for region in data["region_data"].values():
            region["agent_data"].clear()

        data["region_data"].clear()
        del data
