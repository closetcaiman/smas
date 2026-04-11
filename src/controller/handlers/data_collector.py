"""
Data collector - gathers simulation data.
"""

from model.map.grid import Grid


class DataCollector:
    """Collects simulation data for export."""

    def __init__(self, grid: Grid) -> None:
        self.__grid = grid

    def collect(self, epoch: int) -> dict:
        """Collect snapshot data."""
        agents = []
        barriers = []

        for y, row in enumerate(self.__grid._data):
            for x, region in enumerate(row):
                if region.agents and not region.is_barrier:
                    for agent in region.agents:
                        agents.append(
                            {
                                "cell": (x, y),
                                "energy": agent.energy,
                                "age": agent.age,
                                "size": agent.genome.size.value,
                                "metabolic": agent.genome.metabolic_rate.value,
                                "ideal_temp": agent.genome.ideal_temperature.value,
                                "temp_tolerance": agent.genome.temperature_tolerance.value,
                            }
                        )
                if region.is_barrier:
                    barriers.append((x, y))

        return {
            "epoch": epoch,
            "total_agents": len(agents),
            "agents": agents,
            "barriers": barriers,
        }

    def count_agents(self) -> int:
        """Count total non-barrier agents."""
        return sum(len(r.agents) for r in self.__grid.regions if not r.is_barrier)
