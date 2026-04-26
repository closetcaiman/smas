from unittest.mock import MagicMock

import numpy as np
import pytest

from controller.handlers import WorldMapSample
from controller.mediator import SimulationMediator


@pytest.fixture
def mock_sample():
    data = np.zeros((5, 5, 3), dtype=np.uint8)
    data[:, :, 0] = 120
    data[:, :, 1] = 100
    data[:, :, 2] = 255
    return WorldMapSample(hsv_data=data)


@pytest.fixture
def mock_mediator():
    mock_db = MagicMock()
    mock_logger = MagicMock()
    mediator = SimulationMediator(databank=mock_db, logger=mock_logger)
    return mediator
