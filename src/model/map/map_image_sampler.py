from colorsys import hsv_to_rgb

import numpy as np
from PIL import Image


class MapImageSampler:
    def __init__(self, image_path: str):
        self.image = Image.open(image_path).convert("HSV")
        self.img_array = np.array(self.image)
        self.px_height, self.px_width, _ = self.img_array.shape
        self.hsv: np.ndarray | None = None

    def sample_grid(self, width: int, height: int):
        """
        Samples the image into a `width` by `height` grid by averaging pixel blocks.
        Returns a (height, width, 3) numpy array of HSV values.
        """
        block_h = self.px_height // height
        block_w = self.px_width // width

        if block_h == 0 or block_w == 0:
            raise ValueError(
                f"Grid size {width} x {height} is too large for image dimensions ({self.px_width}x{self.px_height})."
            )

        # crop to full increments of block_h / block_w
        cropped_array = self.img_array[: block_h * height, : block_w * width]
        # Reshape the array to isolate the blocks
        # Shape becomes: (grid_rows, block_height, grid_cols, block_width, rgb_channels)
        reshaped = cropped_array.reshape(height, block_h, width, block_w, 3)
        averaged_hsv = reshaped.mean(axis=(1, 3))

        self.hsv = averaged_hsv.astype(np.uint8)

    def hue(self, x, y):
        if self.hsv is None:
            raise ValueError("no HSV data; run sample_grid() first")
        return int(self.hsv[y, x, 0])

    def saturation(self, x, y):
        if self.hsv is None:
            raise ValueError("no HSV data; run sample_grid() first")
        return int(self.hsv[y, x, 1])

    def value(self, x, y):
        if self.hsv is None:
            raise ValueError("no HSV data; run sample_grid() first")
        return int(self.hsv[y, x, 2])

    def rgb(self, x, y):
        if self.hsv is None:
            raise ValueError("no HSV data; run sample_grid() first")
        return [int(v * 255) for v in hsv_to_rgb(*(self.hsv[y, x, :] / 255))]
