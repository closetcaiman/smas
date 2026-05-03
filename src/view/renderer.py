from config.default import MetricsConfig, ViewConfig
from controller.handlers.sampling.world_map_sample import WorldMapSample
from model.world import World
from view.renderers.metrics import MetricsRenderer
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
        view_config: ViewConfig,
        metrics_config: MetricsConfig,
    ) -> None:
        """
        Initialize the main renderer.

        Args:
            viewport: The viewport for rendering.
            world: The world to render.
            sample: The world map sample.
            cell_size: The size of each grid cell.
            view_config: The view configuration containing settings for rendering.
            metrics_config: The metrics configuration containing settings for metrics rendering.

        """
        self.__grid_renderer = GridRenderer(viewport, world, sample, view_config)
        self.__agent_renderer = AgentRenderer(viewport, world, view_config)
        self.__sidebar_renderer = SidebarRenderer(viewport, world, view_config)
        self.__metrics_renderer = MetricsRenderer(viewport, view_config, metrics_config)

        self.__main_pipeline = [
            self.__metrics_renderer.render,
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
            is_barrier: A flag indicating whether to render the post-barrier pipeline (metrics) after the main rendering steps.

        Returns:
            None

        """
        for render_step in self.__main_pipeline:
            render_step(context)
