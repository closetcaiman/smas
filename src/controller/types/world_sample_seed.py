from typing import TypedDict


class GrassSeed(TypedDict):
    """Seed data for initializing grass resources in a region."""

    grass_amount: int
    grass_growth: int
    grass_max_amount: int


class TallGrassSeed(TypedDict):
    """Seed data for initializing tall grass resources in a region."""

    tall_grass_amount: int
    tall_grass_growth: int
    tall_grass_max_amount: int


class FruitSeed(TypedDict):
    """Seed data for initializing fruit resources in a region."""

    fruit_amount: int
    fruit_growth: int
    fruit_max_amount: int


class MigrationCostSeed(TypedDict):
    """Seed data for initializing migration costs in a region."""

    migrate_in_cost: int
    migrate_out_cost: int
