"""Simulation state handler.
"""

from model.simulation.mas_stats import MASEvolutionStats
from model.simulation.simulation import Simulation

from .. import config


class SimulationState:
    """Manages simulation state and stepping.
    """

    def __init__(
        self,
        grid_width: int,
        grid_height: int,
        num_agents: int,
    ) -> None:
        self.__grid_width = grid_width
        self.__grid_height = grid_height
        self.__num_agents = num_agents

        self.__simulation = Simulation(
            self.__grid_width,
            self.__grid_height,
            self.__num_agents,
        )
        self.__mas_stats = MASEvolutionStats()
        self.__last_step_time = 0
        self.__paused = False
        self.__speed_index = 1
        self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]

    @property
    def simulation(self) -> Simulation:
        return self.__simulation

    @property
    def grid(self):
        return self.simulation.grid

    @property
    def step_count(self) -> int:
        return self.simulation.step_count

    @property
    def mas_stats(self) -> MASEvolutionStats:
        return self.__mas_stats

    def reset(self) -> None:
        """Reset simulation to initial state."""
        self.__simulation = Simulation(
            self.__grid_width,
            self.__grid_height,
            self.__num_agents,
        )
        self.__mas_stats = MASEvolutionStats()
        self.__last_step_time = 0
        self.__paused = False
        self.__speed_index = 1
        self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]

    def toggle_pause(self) -> None:
        self.__paused = not self.__paused

    def step(self, current_time: int) -> bool:
        """Step simulation if interval passed. Returns True if stepped."""
        if self.__paused:
            return False
        if current_time - self.__last_step_time >= self.__step_interval:
            self.__simulation.step()
            if self.__mas_stats.barrier_introduced:
                barrier_col = self.__grid_width // 2
                self.__mas_stats.calculate_stats(self.grid, barrier_col)
            self.__last_step_time = current_time
            return True
        return False

    def speed_up(self) -> bool:
        """Increase speed. Returns True if changed."""
        if self.__speed_index < len(config.STEP_INTERVAL_MS) - 1:
            self.__speed_index += 1
            self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]
            return True
        return False

    def speed_down(self) -> bool:
        """Decrease speed. Returns True if changed."""
        if self.__speed_index > 0:
            self.__speed_index -= 1
            self.__step_interval = config.STEP_INTERVAL_MS[self.__speed_index]
            return True
        return False

    def place_barrier_split(self, grid_width: int, grid_height: int) -> None:
        """Place vertical barrier line."""
        col = grid_width // 2
        for row in range(grid_height):
            region = self.__simulation.grid._data[row][col]
            region.is_barrier = True
            region.agents.clear()
        self.__mas_stats.record_barrier_introduction(self.step_count, col)

    @property
    def speed_label(self) -> str:
        return config.SPEED_LABELS[self.__speed_index]
