from pydantic import BaseModel, Field, PositiveInt


class AgentBehaviourConfig(BaseModel):
    """Configuration for the simulation behaviour component of the application."""

    MOST_PREFERRED_ACTION_WEIGHT: PositiveInt = Field(default=6, ge=1)
    ACTION_WEIGHT_DECAY: PositiveInt = Field(default=2, ge=1)
