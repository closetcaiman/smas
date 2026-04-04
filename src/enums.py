from enum import Enum


class FoodType(Enum):
    GRASS = 0
    TALL_GRASS = 1
    FRUIT = 2


class Action(Enum):
    EAT = 0
    MIGRATE = 1
    REPRODUCE = 2
