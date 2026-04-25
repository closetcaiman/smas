from abc import ABC

from view.types import RenderContext


class UIRenderer(ABC):
    """Base class for UI renderers, providing common functionality and interface for rendering different UI components."""

    def render(self, context: RenderContext) -> None:
        """Render the element with optional parameters."""
        raise NotImplementedError("Subclasses must implement render()")
