# -*- coding: utf-8 -*-

"""
Virtualenv management related automation.
"""

import typing as T
import shutil
import subprocess
import dataclasses


if T.TYPE_CHECKING:  # pragma: no cover
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectVenv:
    """
    Namespace class for Virtualenv management related automation.

    :param python_version: example "3.7", "3.8", ...
    """

    python_version: str = dataclasses.field()

    def _validate_python_version(self: "PyProjectOps"):
        value_error = ValueError(
            f"'python_version' has to be in format of '3.7', '3.8', ..."
        )
        if self.python_version[0] not in ["3"]:
            raise value_error
        if self.python_version[1] != ".":
            raise value_error
        if not self.python_version[2:].isdigit():
            raise value_error
        if int(self.python_version[2:]) < 7:
            raise ValueError("python_version has to be >= 3.7")

    def create_virtualenv(self: "PyProjectOps") -> bool:
        """
        Run:

        .. code-block:: bash

            $ virtualenv -p python${X}.${Y} ./.venv

        :return: a boolean flat to indicate whether a creation is performed.
        """
        if self.dir_venv.exists():
            return False
        else:
            subprocess.run(
                [
                    f"{self.path_bin_virtualenv}",
                    "-p",
                    f"python{self.python_version}",
                    f"{self.dir_venv}",
                ],
                check=True,
            )
            return True

    def remove_virtualenv(self: "PyProjectOps") -> bool:
        """
        Run:

        .. code-block:: bash

            $ rm -r /path/to/.venv

        :return: a boolean flat to indicate whether a deletion is performed.
        """
        if self.dir_venv.exists():
            shutil.rmtree(f"{self.dir_venv}", ignore_errors=True)
            return True
        else:
            return False
