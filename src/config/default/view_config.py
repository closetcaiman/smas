from pydantic import (
    BaseModel,
    Field,
    NonNegativeInt,
    PositiveFloat,
    PositiveInt,
    model_validator,
)

from config.errors import RangeError


class ViewConfig(BaseModel):
    """Configuration for the view component of the application."""

    # Window
    WINDOW_WIDTH: PositiveInt = Field(default=1000, ge=1000, le=2000)
    WINDOW_HEIGHT: PositiveInt = Field(default=700, ge=700, le=1400)

    # Grid
    GRID_LINE_COLOR: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt] = Field(
        default=(65, 65, 65)
    )
    GRID_BORDER_COLOR: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt] = Field(
        default=(70, 70, 70)
    )
    GRID_PADDING: PositiveInt = Field(default=8)

    ## Barrier
    BARRIER_COLOR: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt] = Field(
        default=(90, 90, 90)
    )

    # Sidebar
    SIDEBAR_WIDTH: PositiveInt = Field(default=280, ge=200, le=400)
    SIDEBAR_BG_COLOR: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt] = Field(
        default=(22, 22, 22)
    )
    SIDEBAR_BORDER_COLOR: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt] = Field(
        default=(90, 90, 90)
    )
    SIDEBAR_BORDER_WIDTH: PositiveInt = Field(default=2, ge=1)
    SIDEBAR_WIDTH: PositiveInt = Field(default=280, ge=200, le=400)
    SIDEBAR_MARGIN: PositiveInt = Field(default=15, ge=0)

    # Agents
    AGENT_BASE_RADIUS: PositiveInt = Field(default=10, ge=5, le=30)
    AGENT_OUTLINE_COLOR: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt] = Field(
        default=(255, 255, 255)
    )
    AGENT_OUTLINE_WIDTH: PositiveInt = Field(default=1, ge=1)
    AGENT_SIZE_MIN: PositiveInt = Field(default=20, ge=10)
    AGENT_SIZE_MAX: PositiveInt = Field(default=60, ge=10)

    METABOLIC_RANGE_MIN: PositiveInt = Field(default=10, ge=0)
    METABOLIC_RANGE_MAX: PositiveInt = Field(default=30, ge=0)
    IDEAL_TEMP_RANGE_MIN: PositiveInt = Field(default=0, ge=0)
    IDEAL_TEMP_RANGE_MAX: PositiveInt = Field(default=27, ge=0)
    TEMP_TOL_RANGE_MIN: PositiveInt = Field(default=4, ge=0)
    TEMP_TOL_RANGE_MAX: PositiveInt = Field(default=10, ge=0)
    RADIUS_FACTOR_MIN: PositiveFloat = Field(default=0.6, ge=0.1, le=10.0)
    RADIUS_FACTOR_MAX: PositiveFloat = Field(default=1.3, ge=0.1, le=10.0)

    ## Enlarged agent display
    ENLARGED_MAX_DISPLAY: PositiveInt = Field(default=5, ge=1)
    ENLARGED_AGENT_SPACING: PositiveInt = Field(default=22, ge=10)
    ENLARGED_AGENT_SCALE: PositiveFloat = Field(default=0.8, ge=0.1, le=2.0)
    ENLARGED_MIN_RADIUS: PositiveInt = Field(default=4, ge=1)
    ENLARGED_BG_COLOR: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt] = Field(
        default=(45, 45, 45)
    )
    ENLARGED_SIZE: PositiveInt = Field(default=160, ge=100, le=300)

    # Typography
    TEXT_COLOR: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt] = Field(
        default=(255, 255, 255)
    )
    LABEL_COLOR: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt] = Field(
        default=(150, 150, 150)
    )
    HEALTH_COLOR: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt] = Field(
        default=(120, 220, 120)
    )
    WARNING_COLOR: tuple[NonNegativeInt, NonNegativeInt, NonNegativeInt] = Field(
        default=(220, 180, 120)
    )
    TITLE_FONT_SIZE: PositiveInt = Field(default=28, ge=10)
    HUD_FONT_SIZE: PositiveInt = Field(default=22, ge=10)
    SMALL_FONT_SIZE: PositiveInt = Field(default=16, ge=10)

    @model_validator(mode="after")
    def check_range_consistency(self) -> "ViewConfig":
        """Validate that all min values are less than their corresponding max values."""
        if self.METABOLIC_RANGE_MIN >= self.METABOLIC_RANGE_MAX:
            raise RangeError(
                "METABOLIC_RANGE_MIN",
                self.METABOLIC_RANGE_MIN,
                "METABOLIC_RANGE_MAX",
                self.METABOLIC_RANGE_MAX,
            )
        if self.IDEAL_TEMP_RANGE_MIN >= self.IDEAL_TEMP_RANGE_MAX:
            raise RangeError(
                "IDEAL_TEMP_RANGE_MIN",
                self.IDEAL_TEMP_RANGE_MIN,
                "IDEAL_TEMP_RANGE_MAX",
                self.IDEAL_TEMP_RANGE_MAX,
            )
        if self.TEMP_TOL_RANGE_MIN >= self.TEMP_TOL_RANGE_MAX:
            raise RangeError(
                "TEMP_TOL_RANGE_MIN",
                self.TEMP_TOL_RANGE_MIN,
                "TEMP_TOL_RANGE_MAX",
                self.TEMP_TOL_RANGE_MAX,
            )
        if self.RADIUS_FACTOR_MIN >= self.RADIUS_FACTOR_MAX:
            raise RangeError(
                "RADIUS_FACTOR_MIN",
                self.RADIUS_FACTOR_MIN,
                "RADIUS_FACTOR_MAX",
                self.RADIUS_FACTOR_MAX,
            )
        return self
