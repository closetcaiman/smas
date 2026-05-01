from pathlib import Path

from pydantic import BaseModel, Field, PositiveInt, model_validator


class ControllerConfig(BaseModel):
    """Configuration for the controller component of the application."""

    FPS: PositiveInt = Field(default=30, ge=1, le=120)
    STEP_INTERVAL_MS: list[PositiveInt] = Field(
        default=[500, 200, 100, 50, 20], min_length=1
    )
    SPEED_LABELS: list[str] = Field(
        default=["Slow", "Normal", "Fast", "Faster", "Max"], min_length=1
    )
    RESULTS_DIR: str = Field(default="results")
    SAMPLING_MAP_PATH: Path = Field(default=Path("assets/sample-map-1.png"))

    @model_validator(mode="after")
    def check_list_lengths_match(self) -> "ControllerConfig":
        """Ensure that STEP_INTERVAL_MS and SPEED_LABELS have the same length."""
        if len(self.STEP_INTERVAL_MS) != len(self.SPEED_LABELS):
            raise ValueError(
                f"Configuration mismatch: STEP_INTERVAL_MS has {len(self.STEP_INTERVAL_MS)} items, "
                f"but SPEED_LABELS has {len(self.SPEED_LABELS)}. They must be the same length."
            )
        return self
