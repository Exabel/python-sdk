import abc
import argparse
import logging
import sys
from typing import Sequence, TextIO


class CommandLineScript(abc.ABC):
    """Abstract base class for command line scripts."""

    def __init__(self, argv: Sequence[str], description: str):
        self.argv = argv
        self.parser = argparse.ArgumentParser(description=description)

    def parse_arguments(self) -> argparse.Namespace:
        """Parse arguments input"""
        return self.parser.parse_args(self.argv[1:])

    def setup_logging(
        self,
        format: str = "%(message)s",  # pylint: disable=redefined-builtin
        level: int = logging.INFO,
        stream: TextIO = sys.stdout,
    ) -> None:
        """Setup logging"""
        logging.basicConfig(format=format, level=level, stream=stream)
        logging.captureWarnings(True)

    @abc.abstractmethod
    def run(self) -> None:
        """Runs the script."""
