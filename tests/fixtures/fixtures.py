from unittest.mock import MagicMock

import numpy as np
import pytest


@pytest.fixture
def mock_sampler():
    mock = MagicMock()

    fake_hsv = np.full((5, 5, 3), [120, 200, 150], dtype=np.uint8)
    mock.hsv = fake_hsv

    mock.hue.side_effect = lambda x, y: int(mock.hsv[y, x, 0])
    mock.saturation.side_effect = lambda x, y: int(mock.hsv[y, x, 1])
    mock.value.side_effect = lambda x, y: int(mock.hsv[y, x, 2])

    mock.rgb.return_value = [34, 139, 34]

    return mock
