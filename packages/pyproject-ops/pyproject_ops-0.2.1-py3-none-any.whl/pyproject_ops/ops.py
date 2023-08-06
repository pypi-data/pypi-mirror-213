# -*- coding: utf-8 -*-

"""
The namespace for all the pyproject_ops automation methods.
"""

import dataclasses

from .pyproject_paths import PyProjectPaths
from .pyproject_venv import PyProjectVenv
from .pyproject_deps import PyProjectDeps
from .pyproject_tests import PyProjectTests
from .pyproject_docs import PyProjectDocs
from .pyproject_build import PyProjectBuild
from .pyproject_publish import PyProjectPublish
from .pyproject_config_management import PyProjectConfigManagement
from .pyproject_aws import PyProjectAWS
from .pyproject_aws_lambda import PyProjectAWSLambda


@dataclasses.dataclass
class PyProjectOps(
    PyProjectPaths,
    PyProjectVenv,
    PyProjectDeps,
    PyProjectTests,
    PyProjectDocs,
    PyProjectBuild,
    PyProjectPublish,
    PyProjectConfigManagement,
    PyProjectAWS,
    PyProjectAWSLambda,
):
    """
    The namespace for all the pyproject_ops automation methods.
    """
    def __post_init__(self):
        self._validate_paths()
        self._validate_python_version()
