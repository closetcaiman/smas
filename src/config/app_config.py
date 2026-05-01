import tomllib
from pathlib import Path

from pydantic import BaseModel

from .default import (
    BehaviourConfig,
    ControllerConfig,
    ModelConfig,
    ViewConfig,
)


class AppConfig(BaseModel):
    """Application configuration class that holds the configurations for the model, view, and controller components."""

    model: ModelConfig = ModelConfig()
    view: ViewConfig = ViewConfig()
    controller: ControllerConfig = ControllerConfig()
    behaviour: BehaviourConfig = BehaviourConfig()

    @staticmethod
    def from_file(file_path: str):
        """
        Load the configuration from the specified file path.

        Args:
            file_path (str): The path to the configuration file.

        Returns:
            AppConfig: The loaded application configuration.

        """
        config = AppConfig().model_dump()

        path = Path(file_path)
        if path.exists():
            with open(path, "rb") as f:
                user_data = tomllib.load(f)
                config = AppConfig(**user_data)

        return config
