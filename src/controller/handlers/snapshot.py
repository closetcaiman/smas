"""
Snapshot handler - exports data to files.
"""

import json
import os
from datetime import datetime

import pygame


class SnapshotHandler:
    """Handles saving simulation data."""

    def __init__(self, results_dir: str) -> None:
        self._results_dir = results_dir

    def save(self, epoch: int, data: dict, screen: pygame.Surface) -> None:
        """Save data to timestamped directory."""
        os.makedirs(self._results_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_dir = os.path.join(self._results_dir, f"run_{timestamp}")
        os.makedirs(run_dir, exist_ok=True)

        pygame.image.save(screen, os.path.join(run_dir, "final_state.png"))
        self.__write_csv(run_dir, epoch, data)
        self.__write_json(run_dir, "genome_dump.json", data)
        self.__write_json(run_dir, "barriers.json", {"barriers": data["barriers"]})

    def __write_csv(self, run_dir: str, epoch: int, data: dict) -> None:
        path = os.path.join(run_dir, "simulation_stats.csv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(
                "epoch,total_agents,cell_x,cell_y,energy,age,size,metabolic,ideal_temp,temp_tolerance\n"
            )
            for agent in data["agents"]:
                f.write(
                    f"{epoch},{data['total_agents']},{agent['cell'][0]},{agent['cell'][1]},"
                )
                f.write(f"{agent['energy']},{agent['age']},{agent['size']},")
                f.write(
                    f"{agent['metabolic']},{agent['ideal_temp']},{agent['temp_tolerance']}\n"
                )

    def __write_json(self, run_dir: str, filename: str, data: dict) -> None:
        path = os.path.join(run_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
