from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class RenderContext:
    """Context object to pass rendering state and data to the Renderer and its sub-renderers."""

    hovered_cell: Tuple[int, int] | None
    selected_cell: Tuple[int, int] | None
    epoch: int
    total_agents: int
    speed_label: str
