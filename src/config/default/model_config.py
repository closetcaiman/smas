from pydantic import BaseModel, Field, PositiveInt, model_validator

from config.errors import RangeError


class ModelConfig(BaseModel):
    """Configuration for the model component of the application."""

    # Agent
    ## Agent inital values

    ### Agent.initial.energy
    AGENT_INITIAL_ENERGY_LOW: PositiveInt = Field(default=50, ge=1)
    AGENT_INITIAL_ENERGY_HIGH: PositiveInt = Field(default=150, ge=1)

    ### Agent.initial.temperature
    AGENT_INITIAL_TEMP_LOW: PositiveInt = Field(default=15, ge=0)
    AGENT_INITIAL_TEMP_HIGH: PositiveInt = Field(default=25, ge=0)

    ### Agent.initial.age
    AGENT_INITIAL_AGE_LOW: PositiveInt = Field(default=0, ge=0)
    AGENT_INITIAL_AGE_HIGH: PositiveInt = Field(default=50, ge=0)

    ### Agent.initial.time_since_last_breeding
    AGENT_INITIAL_TIME_SINCE_LAST_BREEDING: PositiveInt = Field(default=0, ge=0)

    ## Agent.genome

    ### Agent.genome.min_energy_to_reproduce
    MIN_ENERGY_TO_REPRODUCE_LOW: PositiveInt = Field(default=40, ge=1)
    MIN_ENERGY_TO_REPRODUCE_HIGH: PositiveInt = Field(default=80, ge=1)

    ### Agent.genome.ideal_temperature
    IDEAL_TEMPERATURE_LOW: PositiveInt = Field(default=0, ge=0)
    IDEAL_TEMPERATURE_HIGH: PositiveInt = Field(default=28, ge=0)

    ### Agent.genome.temperature_tolerance
    TEMPERATURE_TOLERANCE_LOW: PositiveInt = Field(default=4, ge=1)
    TEMPERATURE_TOLERANCE_HIGH: PositiveInt = Field(default=10, ge=1)

    ### Agent.genome.metabolic_rate
    METABOLIC_RATE_LOW: PositiveInt = Field(default=10, ge=1)
    METABOLIC_RATE_HIGH: PositiveInt = Field(default=30, ge=1)

    ### Agent.genome.maturity_age
    MATURITY_AGE_LOW: PositiveInt = Field(default=20, ge=1)
    MATURITY_AGE_HIGH: PositiveInt = Field(default=40, ge=1)

    ### Agent.genome.size
    SIZE_LOW: PositiveInt = Field(default=20, ge=1)
    SIZE_HIGH: PositiveInt = Field(default=60, ge=1)

    ### Agent.genome.breeding_interval
    BREEDING_INTERVAL_LOW: PositiveInt = Field(default=2, ge=1)
    BREEDING_INTERVAL_HIGH: PositiveInt = Field(default=20, ge=1)

    # Region
    AGENTS_PER_REGION: PositiveInt = Field(default=3, ge=1)

    # World
    GRID_WIDTH: PositiveInt = Field(default=20, ge=1, le=50)
    GRID_HEIGHT: PositiveInt = Field(default=20, ge=1, le=50)

    @model_validator(mode="after")
    def check_ranges_valid(self) -> "ModelConfig":
        """Validate that all low values are less than their corresponding high values."""
        if self.AGENT_INITIAL_ENERGY_LOW >= self.AGENT_INITIAL_ENERGY_HIGH:
            raise RangeError(
                "AGENT_INITIAL_ENERGY_LOW",
                self.AGENT_INITIAL_ENERGY_LOW,
                "AGENT_INITIAL_ENERGY_HIGH",
                self.AGENT_INITIAL_ENERGY_HIGH,
            )
        if self.AGENT_INITIAL_TEMP_LOW >= self.AGENT_INITIAL_TEMP_HIGH:
            raise RangeError(
                "AGENT_INITIAL_TEMP_LOW",
                self.AGENT_INITIAL_TEMP_LOW,
                "AGENT_INITIAL_TEMP_HIGH",
                self.AGENT_INITIAL_TEMP_HIGH,
            )
        if self.AGENT_INITIAL_AGE_LOW >= self.AGENT_INITIAL_AGE_HIGH:
            raise RangeError(
                "AGENT_INITIAL_AGE_LOW",
                self.AGENT_INITIAL_AGE_LOW,
                "AGENT_INITIAL_AGE_HIGH",
                self.AGENT_INITIAL_AGE_HIGH,
            )
        if self.MIN_ENERGY_TO_REPRODUCE_LOW >= self.MIN_ENERGY_TO_REPRODUCE_HIGH:
            raise RangeError(
                "MIN_ENERGY_TO_REPRODUCE_LOW",
                self.MIN_ENERGY_TO_REPRODUCE_LOW,
                "MIN_ENERGY_TO_REPRODUCE_HIGH",
                self.MIN_ENERGY_TO_REPRODUCE_HIGH,
            )

        if self.IDEAL_TEMPERATURE_LOW >= self.IDEAL_TEMPERATURE_HIGH:
            raise RangeError(
                "IDEAL_TEMPERATURE_LOW",
                self.IDEAL_TEMPERATURE_LOW,
                "IDEAL_TEMPERATURE_HIGH",
                self.IDEAL_TEMPERATURE_HIGH,
            )
        if self.TEMPERATURE_TOLERANCE_LOW >= self.TEMPERATURE_TOLERANCE_HIGH:
            raise RangeError(
                "TEMPERATURE_TOLERANCE_LOW",
                self.TEMPERATURE_TOLERANCE_LOW,
                "TEMPERATURE_TOLERANCE_HIGH",
                self.TEMPERATURE_TOLERANCE_HIGH,
            )
        if self.METABOLIC_RATE_LOW >= self.METABOLIC_RATE_HIGH:
            raise RangeError(
                "METABOLIC_RATE_LOW",
                self.METABOLIC_RATE_LOW,
                "METABOLIC_RATE_HIGH",
                self.METABOLIC_RATE_HIGH,
            )
        if self.MATURITY_AGE_LOW >= self.MATURITY_AGE_HIGH:
            raise RangeError(
                "MATURITY_AGE_LOW",
                self.MATURITY_AGE_LOW,
                "MATURITY_AGE_HIGH",
                self.MATURITY_AGE_HIGH,
            )
        if self.SIZE_LOW >= self.SIZE_HIGH:
            raise RangeError(
                "SIZE_LOW",
                self.SIZE_LOW,
                "SIZE_HIGH",
                self.SIZE_HIGH,
            )
        if self.BREEDING_INTERVAL_LOW >= self.BREEDING_INTERVAL_HIGH:
            raise RangeError(
                "BREEDING_INTERVAL_LOW",
                self.BREEDING_INTERVAL_LOW,
                "BREEDING_INTERVAL_HIGH",
                self.BREEDING_INTERVAL_HIGH,
            )
        return self
