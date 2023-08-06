# -*- coding: utf-8 -*-

"""
Config management related automation.
"""

import typing as T
import dataclasses
from pathlib_mate import Path


if T.TYPE_CHECKING:
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectConfigManagement:
    """
    Namespace class for config management related automation.
    """
    @property
    def dir_config(self: "PyProjectOps") -> Path:
        """
        The folder that stores the config files.

        Example: ``${dir_project_root}/config``
        """
        return self.dir_project_root.joinpath("config")

    @property
    def path_config_json(self) -> Path:
        """
        Path to the JSON file that stores the non-sensitive config.

        Example: ``${dir_project_root}/config/config.json``
        """
        return self.dir_config.joinpath("config.json")

    @property
    def path_secret_config_json(self: "PyProjectOps") -> Path:
        """
        Path to the JSON file that stores the secret config such as password.

        Example: ``${HOME}/.projects/${package_name}/secret-config.json``
        """
        return self.dir_home.joinpath(
            ".projects", self.package_name, "secret-config.json"
        )
