from pydantic import BaseModel, Field


class MetricsConfig(BaseModel):
    """Configuration for the metrics component of the application."""

    BHATTACHARYYA_TRAIT: str = Field(default="agent_size")
