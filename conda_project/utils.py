# Copyright (C) 2022 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause

import itertools
import os
import sys
import threading
import time
from collections.abc import Generator
from contextlib import contextmanager
from inspect import Traceback
from pathlib import Path
from typing import Optional, Type

from .exceptions import CondaProjectError


@contextmanager
def env_variable(key: str, value: str) -> Generator:
    """Temporarily set environment variable in a context manager."""
    old = os.environ.get(key, None)
    os.environ[key] = value

    yield

    if old is None:
        os.environ.pop(key, None)
    else:
        os.environ[key] = old


class Spinner:
    """Multithreaded CLI spinner context manager

    Attributes:
        prefix: Text to display at the start of the line

    Args:
        prefix: Text to display at the start of the line

    """

    def __init__(self, prefix: str):
        self.prefix = prefix
        self._event = threading.Event()
        self._thread = threading.Thread(target=self._spin)

    def _spin(self) -> None:
        spinner = itertools.cycle(["◜", "◠", "◝", "◞", "◡", "◟"])

        while not self._event.is_set():
            sys.stdout.write("\r")
            sys.stdout.write("\033[K")
            sys.stdout.write(f"{self.prefix}: {next(spinner)} ")
            sys.stdout.flush()
            time.sleep(0.10)

    def start(self) -> None:
        self._thread.start()

    def stop(self) -> None:
        self._event.set()
        self._thread.join()
        sys.stdout.write("\r")
        sys.stdout.write("\033[K")
        sys.stdout.write(f"{self.prefix}: done\n")
        sys.stdout.flush()

    def __enter__(self) -> None:
        self.start()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_tb: Optional[Traceback],
    ) -> None:
        self.stop()


def find_file(directory: Path, options: tuple) -> Optional[Path]:
    """Search for a file in a directory from a tuple of variants.

    Returns:
        The path to the file if found else None

    Raises:
        CondaProjectError if more than one of the options is found

    """
    found = []

    for filename in options:
        path = directory / filename
        if path.exists():
            found.append(path.resolve())

    if len(found) == 1:
        return found[0]
    elif len(found) > 1:
        _found_files = "\n".join([str(p) for p in found])
        raise CondaProjectError(
            f"Multiple variants of the same file were found.\n{_found_files}\nConsider using one of them."
        )
    else:
        return None
