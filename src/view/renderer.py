from config.default import ViewConfig
from controller.handlers.sampling.world_map_sample import WorldMapSample
from model.world import World
from view.renderers.ui_renderer import UIRenderer
from view.viewport import Viewport

from .renderers.agent import AgentRenderer
from .renderers.grid import GridRenderer
from .renderers.sidebar import SidebarRenderer
from .types import RenderContext


class Renderer(UIRenderer):
    """Main renderer that composes the grid, agents, and sidebar renderers."""

    def __init__(
        self,
        viewport: Viewport,
        world: World,
        sample: WorldMapSample,
        config: ViewConfig,
    ) -> None:
        """
        Initialize the main renderer.

        Args:
            viewport: The viewport for rendering.
            world: The world to render.
            sample: The world map sample.
            cell_size: The size of each grid cell.
            config: The view configuration containing settings for rendering.

        """
        self.__grid_renderer = GridRenderer(viewport, world, sample, config)
        self.__agent_renderer = AgentRenderer(viewport, world, config)
        self.__sidebar_renderer = SidebarRenderer(viewport, world, config)

        self.__pipeline = [
            self.__grid_renderer.render,
            self.__agent_renderer.render,
            self.__sidebar_renderer.render,
        ]

    def render(self, context: RenderContext) -> None:
        """
        Render the entire scene by calling each renderer in the pipeline.

        Overrides:
            UIRenderer.render: Executes the rendering pipeline, which includes rendering the grid, agents, and sidebar in sequence.

        Args:
            context: The rendering context containing dynamic information for rendering.

        Returns:
            None

        """
        for render_step in self.__pipeline:
            render_step(context)
