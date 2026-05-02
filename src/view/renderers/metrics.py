import io

import matplotlib.pyplot as plt
import pygame

from config.default import MetricsConfig, ViewConfig
from view.types import RenderContext
from view.viewport import Viewport

from .ui_renderer import UIRenderer


class MetricsRenderer(UIRenderer):
    """Renders visualizations of simulation metrics such as FST, PCA, and Bhattacharyya distance."""

    def __init__(
        self, viewport: Viewport, view_config: ViewConfig, metrics_config: MetricsConfig
    ):
        """
        Initialize the metrics renderer for visualizing simulation metrics like FST, PCA, and B-distance.

        Args:
            viewport: The viewport to render on.
            view_config: Configuration for view settings.
            metrics_config: Configuration for metrics rendering.

        """
        self.__viewport = viewport
        self.__view_config = view_config
        self.__metrics_config = metrics_config
        self.__cached_surface = None
        self.__last_epoch = -1
        self.__sidebar_x = viewport.sidebar_x

    def render(self, context: RenderContext):
        """
        Render the metrics visualization on the screen.

        Overrides: UIRenderer.render

        Args:
            context: The rendering context containing the current epoch and metrics data.

        """
        if not context.metrics_data:
            return

        if (
            context.epoch - self.__last_epoch
            >= self.__view_config.METRICS_UPDATE_INTERVAL
        ):
            self.__update_cache(context.metrics_data)
            self.__last_epoch = context.epoch

        if self.__cached_surface:
            padding = 10
            draw_x = self.__sidebar_x + padding
            draw_y = 550
            self.__viewport.screen.blit(self.__cached_surface, (draw_x, draw_y))

    def __update_cache(self, data):
        width_in_inches = (self.__view_config.SIDEBAR_WIDTH - 20) / 100
        fig, axes = plt.subplots(3, 1, figsize=(width_in_inches, 6), dpi=100)
        self.__plot_fst(axes[0], data)
        self.__plot_pca(axes[1], data[-1])
        self.__plot_bhattacharyya(axes[2], data)

        fig.tight_layout(pad=1.0)
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        self.__cached_surface = pygame.image.load(buf)
        plt.close(fig)

    def __plot_fst(self, ax, data):
        epochs = [m["epoch"] for m in data]
        fst = [m["fst"] for m in data]
        ax.plot(epochs, fst, color="blue")
        ax.set_title("FST over Time", fontsize=10)

    def __plot_pca(self, ax, latest):
        if "pca" in latest:
            df = latest["pca"]
            for pop, color in [("A", "red"), ("B", "blue")]:
                subset = df[df["population_type"] == pop]
                ax.scatter(
                    subset["pc1"],
                    subset["pc2"],
                    c=color,
                    label=f"{pop}",
                    s=5,
                    alpha=0.6,
                )
            ax.set_title("PCA: Population Divergence", fontsize=10)
            ax.legend(fontsize=7)

    def __plot_bhattacharyya(self, ax, data):
        epochs = [m["epoch"] for m in data]
        b_dist = [m["bhattacharyya_distance"] for m in data]
        ax.plot(epochs, b_dist, color="purple")
        ax.set_title(
            f"Bhattacharyya Distance over \n{self.__metrics_config.BHATTACHARYYA_TRAIT}",
            fontsize=10,
        )
