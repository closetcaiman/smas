class RangeError(ValueError):
    """Error class for invalid range values."""

    def __init__(
        self, low_name: str, low_value: float, high_name: str, high_value: float
    ):
        """
        Initialize the RangeError with details about the invalid range.

        Args:
            low_name (str): The name of the lower bound parameter.
            low_value (float): The value of the lower bound parameter.
            high_name (str): The name of the upper bound parameter.
            high_value (float): The value of the upper bound parameter.

        """
        message = (
            f"{low_name} ({low_value}) must be less than {high_name} ({high_value})."
        )
        super().__init__(message)
