# -*- coding: utf-8 -*-

"""
AWS related automation.
"""

import typing as T
import dataclasses
from pathlib_mate import Path


if T.TYPE_CHECKING:
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectAWS:
    """
    Namespace class for AWS related automation.
    """
    @property
    def path_bin_aws(self: "PyProjectOps") -> Path:
        """
        The AWS CLI executable path.
        """
        return self.get_path_dynamic_bin_cli("aws")
