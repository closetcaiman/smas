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

        self.__cached_surfaces = []

    def render(self, context: RenderContext):
        """
        Render the metrics visualization on the screen.

        Overrides: UIRenderer.render

        Args:
            context: The rendering context containing the current epoch and metrics data.

        """
        pygame.draw.rect(
            self.__viewport.screen,
            self.__view_config.METRICS_BG_COLOR,
            (
                0,
                0,
                self.__view_config.METRICS_PANEL_WIDTH,
                self.__viewport.screen.get_height(),
            ),
        )

        font = pygame.font.SysFont(None, self.__view_config.HUD_FONT_SIZE)
        text_surface = font.render(
            "Metrics (FST, PCA, B-distance)", True, self.__view_config.TEXT_COLOR
        )
        text_hint = font.render(
            "(?) Place the barrier to start",
            True,
            self.__view_config.METRICS_ACCENT_COLOR,
        )

        self.__viewport.screen.blit(text_surface, (5, 10))
        self.__viewport.screen.blit(text_hint, (5, 40))

        if not context.metrics_data:
            return

        if (
            context.epoch - self.__last_epoch
            >= self.__view_config.METRICS_UPDATE_INTERVAL
        ):
            self.__update_cache(context.metrics_data)
            self.__last_epoch = context.epoch

        if self.__cached_surfaces:
            font = pygame.font.SysFont(None, 24)
            latest = context.metrics_data[-1]

            y_pos = 70
            spacing = 250

            self.__viewport.screen.blit(self.__cached_surfaces[0], (0, y_pos))
            val_text = font.render(
                f"Current FST: {latest['fst']:.4f}", True, (255, 255, 255)
            )
            self.__viewport.screen.blit(val_text, (10, y_pos + 200))

            y_pos += spacing
            self.__viewport.screen.blit(self.__cached_surfaces[2], (0, y_pos))
            b_text = font.render(
                f"B-Dist: {latest['bhattacharyya_distance']:.4f}", True, (255, 255, 255)
            )
            self.__viewport.screen.blit(b_text, (10, y_pos + 200))

            y_pos += spacing
            self.__viewport.screen.blit(self.__cached_surfaces[1], (0, y_pos))

    def __update_cache(self, data):
        self.__cached_surfaces = []
        width_in_inches = (self.__view_config.METRICS_PANEL_WIDTH - 20) / 100

        # Helper to create a single plot image
        def _save_plot(plot_func, *args):
            fig, ax = plt.subplots(figsize=(width_in_inches, 2.0), dpi=100)
            plot_func(ax, *args)
            fig.tight_layout(pad=1.0)
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            surf = pygame.image.load(buf).convert_alpha()
            plt.close(fig)
            return surf

        self.__cached_surfaces.append(_save_plot(self.__plot_fst, data))
        self.__cached_surfaces.append(_save_plot(self.__plot_pca, data[-1]))
        self.__cached_surfaces.append(_save_plot(self.__plot_bhattacharyya, data))

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
