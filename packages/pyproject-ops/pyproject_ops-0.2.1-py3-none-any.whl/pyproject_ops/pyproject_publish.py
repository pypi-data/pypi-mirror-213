# -*- coding: utf-8 -*-

"""
Publish to Python repository related automation.
"""

import typing as T
import subprocess
import dataclasses


if T.TYPE_CHECKING:
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectPublish:
    """
    Namespace class for publishing to Python repository related automation.
    """

    def twine_upload(self: "PyProjectOps"):
        """
        Publish to PyPI repository using
        `twine upload <https://twine.readthedocs.io/en/stable/index.html>`_.
        """
        args = [
            f"{self.path_bin_twine}",
            "upload",
            f"{self.dir_dist}/*",
        ]
        with self.dir_project_root.temp_cwd():
            subprocess.run(args, check=True)

    def poetry_publish(self: "PyProjectOps"):
        """
        Publish to PyPI repository using
        `poetry publish <https://python-poetry.org/docs/libraries/#publishing-to-pypi>`_.`
        """
        args = [
            f"{self.path_bin_poetry}",
            "publish",
        ]
        with self.dir_project_root.temp_cwd():
            subprocess.run(args, check=True)
