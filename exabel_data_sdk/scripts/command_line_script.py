import abc
import argparse
from typing import Sequence


class CommandLineScript(abc.ABC):
    """Abstract base class for command line scripts."""

    def __init__(self, argv: Sequence[str], description: str):
        self.argv = argv
        self.parser = argparse.ArgumentParser(description=description)

    def parse_arguments(self) -> argparse.Namespace:
        """Parse arguments input"""
        return self.parser.parse_args(self.argv[1:])

    @abc.abstractmethod
    def run(self) -> None:
        """Runs the script."""
