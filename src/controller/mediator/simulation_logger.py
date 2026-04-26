"""A simple logger for recording simulation events."""


class SimulationLogger:
    """
    A simple logger for recording simulation events.

    Methods:
        info: Log informational messages.
        debug: Log debugging messages.
        error: Log error messages.

    """

    @staticmethod
    def info(message: str):
        """Log informational messages."""
        print(f"[INFO] {message}")

    @staticmethod
    def debug(message: str):
        """Log debugging messages."""
        print(f"[DEBUG] {message}")

    @staticmethod
    def error(message: str):
        """Log error messages."""
        print(f"[ERROR] {message}")
