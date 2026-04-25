from enum import Enum, auto


class UserAction(Enum):
    """Enumeration of possible user actions in the simulation."""

    QUIT = auto()
    TOGGLE_PAUSE = auto()
    RESET = auto()
    PLACE_BARRIER = auto()
    SPEED_UP = auto()
    SPEED_DOWN = auto()
    CLICK = auto()
    HOVER = auto()
