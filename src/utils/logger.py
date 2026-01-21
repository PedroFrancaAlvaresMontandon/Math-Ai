"""
Logging configuration module using rich for beautiful console output.
"""
import logging
from rich.logging import RichHandler
from rich.console import Console

from .config import LOG_LEVEL


def setup_logger(name: str = "Assistente IA") -> logging.Logger:
    """
    Configures and returns a logger with rich formatting.

    Args:
        name: Logger name

    Returns:
        Configured logger instance
    """
    console = Console()

    logging.basicConfig(
        level=LOG_LEVEL,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[
            RichHandler(
                console=console,
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                markup=True,
            )
        ],
    )

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)

    return logger


def get_logger(name: str = "Assistente IA") -> logging.Logger:
    """
    Gets a logger with the specified name.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return setup_logger(name)


# Create default logger instance
logger = setup_logger()
