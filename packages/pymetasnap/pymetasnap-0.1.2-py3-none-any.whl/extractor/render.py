"""This module contains Requirements class, which is the core of the current process."""

import re
from typing import List, Tuple


class Requirements:
    """
    A class that handles parsing and rendering requirements data.

    Attributes:
        None

    Methods:
        _read_file_contents: Read the contents of a file.
        _from_pip_freeze: Parse data in the pip freeze format.
        _from_pip_list: Parse data in the pip list format.
        render: Render the requirements data based on the specified format.
    """

    def _read_file_contents(self, source_path: str) -> str:
        """
        Read the contents of a file.

        Args:
            source_path: The path to the file to be read.

        Returns:
            The contents of the file as a string.
        """
        return open(source_path, "r").read()

    def _from_pip_freeze(self, data: str) -> List[Tuple[str, str]]:
        """
        Parse data in the pip freeze format.

        Args:
            data: The pip freeze formatted data to be parsed.

        Returns:
            A list of tuples containing package names and versions.
        """
        lines = data.strip().split("\n")
        pattern = r"(==|<=|>=|<|>)"
        package_data = [re.split(pattern, line) for line in lines]
        return [
            (package[0], package[2]) if len(package) > 1 else package
            for package in package_data
        ]

    def _from_pip_list(self, data: str) -> List[Tuple[str, str]]:
        """
        Parse data in the pip list format.

        Args:
            data: The pip list formatted data to be parsed.

        Returns:
            A list of tuples containing package names and versions.
        """
        lines = data.strip().split("\n")
        package_data = [tuple(line.split()) for line in lines[2:]]
        return [(package[0], package[1]) for package in package_data]  # pylint

    def render(self, source_path: str, format: str) -> List[Tuple[str, str]]:
        """
        Render the requirements data based on the specified format.

        Args:
            source_path: The path to the requirements file.
            format: The format of the requirements file (e.g., "pip_freeze", "pip_list"). # noqa

        Returns:
            A list of tuples containing package names and versions.
        """
        data = self._read_file_contents(source_path)
        if format == "pip_freeze":
            return self._from_pip_freeze(data)
        if format == "pip_list":
            return self._from_pip_list(data)
