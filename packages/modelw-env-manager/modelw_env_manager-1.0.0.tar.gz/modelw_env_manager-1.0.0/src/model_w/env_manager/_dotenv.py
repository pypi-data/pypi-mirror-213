import inspect
import os
import re
import sys
from pathlib import Path
from typing import Iterator, Optional, Tuple, Union

from dotenv.main import DotEnv
from dotenv.parser import parse_stream

SET_A = re.compile(r"^\s*set\s+-a\s*$")


class WDotEnv(DotEnv):
    """
    We override the default DotEnv class in order to alter error reporting.
    First of all, we want to allow `set -a` in files without getting an error.
    And then we want the option to be able to look at the list of errors and
    to report them through a different channel than the default warning from
    the lib.
    """

    def parse(self) -> Iterator[Tuple[str, Optional[str]]]:
        """
        Same as the parent but ignoring errors on `set -a`.
        """

        with self._get_stream() as stream:
            setattr(self, "_error_lines", [])

            for binding in parse_stream(stream):
                if binding.error:
                    if not SET_A.match(binding.original.string):
                        self.error_lines.append(binding.original)
                elif binding.key:
                    yield binding.key, binding.value

    @property
    def error_lines(self):
        """
        A shortcut to get error lines reported during parsing
        """

        return getattr(self, "_error_lines", [])


def find_dotenv(file_name: str = ".env") -> Optional[Path]:
    """
    The algorithm from the original find_dotenv is not working for our case so
    we're coding it again here.

    The idea is to move up the stack trace and find all files that are not
    children of the virtual environment. For each of those "developer files" we
    go up until the root, looking for the closest .env file we can find.

    Notes
    -----
    In order to find the "closest" file we look at the length of the file's
    path. The longest path wins. If there are several locations of "developer
    files" that's how we decide which "root" to pick from. All this is
    entirely heuristic and definitely not recommended in production.

    Parameters
    ----------
    file_name
        Name of the `.env` file you're looking for. Defaults to `.env` but can
        be anything.
    """

    prefixes = [Path(sys.prefix).absolute()]

    if py_path := os.getenv("DOTENV_IGNORE_PATH"):
        prefixes.extend(Path(p).absolute() for p in py_path.split(os.pathsep))

    candidates = set()

    for frame in inspect.stack(0):
        file = Path(frame.filename).absolute()

        if not any(file.is_relative_to(p) for p in prefixes):
            for parent in file.parents:
                if parent not in candidates:
                    candidates.add(parent)

    for candidate in sorted(candidates, key=lambda c: (len(f"{c}"), c), reverse=True):
        if (out := candidate / file_name).is_file():
            return out


def load_dotenv(dotenv_path: Union[str, Path, None] = None) -> bool:
    """
    Finds, parses and loads as default the .env file for this project.

    If the path is not specified, it will use find_dotenv() which looks along
    the stack trace to find the code root and find the .env file associated.

    Parameters
    ----------
    dotenv_path
        Optional path to the dotenv file, which will otherwise be guessed
    """

    if dotenv_path is None:
        dotenv_path = find_dotenv()

    if dotenv_path:
        return WDotEnv(dotenv_path=dotenv_path).set_as_environment_variables()
    else:
        return True
