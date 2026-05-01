import tomllib
from pathlib import Path

import tomlkit
from pydantic import BaseModel

from .default import (
    BehaviourConfig,
    ControllerConfig,
    ModelConfig,
    ViewConfig,
)

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
APP_DIR = ROOT_DIR / "src" / "app"


class AppConfig(BaseModel):
    """Application configuration class that holds the configurations for the model, view, and controller components."""

    model: ModelConfig = ModelConfig()
    view: ViewConfig = ViewConfig()
    controller: ControllerConfig = ControllerConfig()
    behaviour: BehaviourConfig = BehaviourConfig()

    @staticmethod
    def from_file(file_path: str | Path) -> "AppConfig":
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
            print(f"Loading configuration from {file_path}")
            with open(path, "rb") as f:
                user_data = tomllib.load(f)
                config = AppConfig(**user_data)

            if not config.controller.SAMPLING_MAP_PATH.is_absolute():
                config.controller.SAMPLING_MAP_PATH = (
                    APP_DIR / config.controller.SAMPLING_MAP_PATH
                )

            return config
        else:
            return AppConfig()

    def save_to_file(self, file_path: str | Path) -> None:
        """
        Save the current configuration to the specified file path.

        Args:
            file_path (str): The path to the configuration file.

        """
        data = self.model_dump()

        # Create the TOML document
        doc = tomlkit.document()
        doc.add(tomlkit.comment("Auto-generated default configuration from AppConfig"))

        # Iterate through each section (e.g., 'view', 'model', 'controller')
        for section_name, section_data in data.items():
            # Create a table for each high-level config section
            table = tomlkit.table()
            # Add the items into the table
            table.update(section_data)
            # Add the table to the document with the section name
            doc.add(section_name, table)

        with open(file_path, "w") as f:
            f.write(tomlkit.dumps(doc))
