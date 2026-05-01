from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

from .world_map_sample import WorldMapSample


class HSVImageSampler:
    """
    Sampler that converts an image into HSV color space and samples it into a grid.

    Methods:
        sample_grid(image_path: Path, width: int, height: int) -> WorldMapSample

    """

    @staticmethod
    def sample_grid(image_path: Path, width: int, height: int) -> WorldMapSample:
        """
        Sample the image into a `width` by `height` grid by averaging pixel blocks.

        Each block corresponds to a region in the simulation,
        and the average hue, saturation, and value of the block are stored
        for later use in determining the properties of that region.
        """
        absolute_path = image_path.resolve()
        image = Image.open(absolute_path).convert("HSV")
        img_array = np.array(image)
        px_height, px_width, _ = img_array.shape

        block_h = px_height // height
        block_w = px_width // width

        if block_h == 0 or block_w == 0:
            raise ValueError(
                f"Grid size {width} x {height} is too large for image dimensions ({px_width}x{px_height})."
            )

        # crop to full increments of block_h / block_w
        cropped_array = img_array[: block_h * height, : block_w * width]
        # Reshape the array to isolate the blocks
        # Shape becomes: (grid_rows, block_height, grid_cols, block_width, rgb_channels)
        reshaped = cropped_array.reshape(height, block_h, width, block_w, 3)
        averaged_hsv: np.ndarray = reshaped.mean(axis=(1, 3))

        return WorldMapSample(averaged_hsv)
