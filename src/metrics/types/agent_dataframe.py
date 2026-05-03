import pandera.pandas as pa
from pandera.typing import Series


class AgentSchema(pa.DataFrameModel):
    """Schema for validating agent data in the DataFrame."""

    epoch: Series[int]
    agent_min_energy_to_reproduce: Series[int]
    agent_preferred_food: Series[int]
    agent_preferred_action: Series[int]
    agent_ideal_temperature: Series[int]
    agent_temperature_tolerance: Series[int]
    agent_metabolic_rate: Series[int]
    agent_maturity_age: Series[int]
    agent_size: Series[int]
    agent_breeding_interval: Series[int]
    agent_dna: Series[str]
    population_type: Series[str]


class PCADataSchema(pa.DataFrameModel):
    """Schema for validating PCA data in the DataFrame."""

    population_type: Series[str]
    pc1: Series[float]
    pc2: Series[float]
