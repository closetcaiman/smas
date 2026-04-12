import math
from typing import List, Tuple

import numpy as np

from model.agent.agent import Agent
from model.map.grid import Grid


def extract_genome_values(agents: List[Agent]) -> np.ndarray:
    if not agents:
        return np.array([])

    values = []
    for agent in agents:
        genome = agent.genome
        values.append(
            [
                float(genome.min_energy_to_reproduce.value),
                float(genome.ideal_temperature.value),
                float(genome.temperature_tolerance.value),
                float(genome.metabolic_rate.value),
                float(genome.maturity_age.value),
                float(genome.size.value),
                float(genome.breeding_interval.value),
            ]
        )
    return np.array(values)


def calculate_fst(pop_a: np.ndarray, pop_b: np.ndarray) -> float:
    if len(pop_a) < 2 or len(pop_b) < 2:
        return 0.0

    n_loci = pop_a.shape[1]
    if n_loci == 0:
        return 0.0

    var_within = 0.0
    var_between = 0.0

    for i in range(n_loci):
        mean_a: np.ndarray = np.mean(pop_a[:, i])
        mean_b: np.ndarray = np.mean(pop_b[:, i])
        var_within: float = float(np.var(pop_a[:, i]) + np.var(pop_b[:, i]))
        var_between: float = pow(mean_a - mean_b, 2.0)

    var_within /= n_loci
    var_between /= n_loci

    total_var = var_within + var_between
    if total_var == 0:
        return 0.0

    fst = var_between / total_var
    return float(max(0.0, min(1.0, fst)))


def calculate_bhattacharyya(pop_a: np.ndarray, pop_b: np.ndarray) -> float:
    if len(pop_a) < 2 or len(pop_b) < 2:
        return 0.0

    n_loci = pop_a.shape[1]
    bc_sum = 0.0

    for i in range(n_loci):
        mean_a = np.mean(pop_a[:, i])
        mean_b = np.mean(pop_b[:, i])
        var_a = np.var(pop_a[:, i]) + 0.001
        var_b = np.var(pop_b[:, i]) + 0.001

        bc = 0.5 * math.log(0.5 * (var_a / var_b + var_b / var_a + 2)) - 0.25 * (
            (mean_a - mean_b) ** 2
        ) / (var_a + var_b)
        bc_sum += max(0, bc)

    return float(bc_sum / n_loci)


def _calculate_agent_fitness(agent: Agent) -> float:
    genome = agent.genome
    return float(
        (100 - abs(genome.ideal_temperature.value - 20))
        + genome.size.value
        + (100 - genome.metabolic_rate.value)
        + genome.temperature_tolerance.value
    )


def calculate_hybrid_inviability(
    pop_a: np.ndarray, pop_b: np.ndarray
) -> Tuple[float, float, float]:
    if len(pop_a) < 1 or len(pop_b) < 1:
        return 0.0, 0.0, 1.0

    hybrid_genome = (pop_a[0] + pop_b[0]) / 2

    parent_fitness = float(np.mean(pop_a[0] + pop_b[0]))
    hybrid_fitness = float(np.mean(hybrid_genome))

    fitness_ratio = hybrid_fitness / np.max([1, parent_fitness])

    return hybrid_fitness, parent_fitness, fitness_ratio


class MASEvolutionStats:
    def __init__(self) -> None:
        self.barrier_introduced = False
        self.barrier_step = 0
        self.barrier_col = 0
        self.fst: float = 0.0
        self.bhattacharyya: float = 0.0
        self.hybrid_fitness_ratio: float = 1.0

    def record_barrier_introduction(self, step: int, barrier_col: int) -> None:
        self.barrier_introduced = True
        self.barrier_step = step
        self.barrier_col = barrier_col

    def calculate_stats(
        self, grid: Grid, barrier_col: int, sample_size: int = 20
    ) -> None:
        if not self.barrier_introduced:
            return

        pop_a: List[Agent] = []
        pop_b: List[Agent] = []

        for row_idx, row in enumerate(grid._data):
            for col_idx, region in enumerate(row):
                if region.is_barrier:
                    continue
                if col_idx < barrier_col:
                    pop_a.extend(region.agents)
                else:
                    pop_b.extend(region.agents)

                if len(pop_a) > sample_size:
                    pop_a = pop_a[:sample_size]
                if len(pop_b) > sample_size:
                    pop_b = pop_b[:sample_size]

        if len(pop_a) < 2 or len(pop_b) < 2:
            return

        values_a = extract_genome_values(pop_a)
        values_b = extract_genome_values(pop_b)

        self.fst = calculate_fst(values_a, values_b)
        self.bhattacharyya = calculate_bhattacharyya(values_a, values_b)

        _, _, self.hybrid_fitness_ratio = calculate_hybrid_inviability(
            values_a, values_b
        )
