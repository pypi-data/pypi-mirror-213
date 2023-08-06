# -*- coding: utf-8 -*-

"""
Testing related automation.
"""

import typing as T
import subprocess
import dataclasses

from .operation_system import OPEN_COMMAND

if T.TYPE_CHECKING:  # pragma: no cover
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectTests:
    """
    Namespace class for testing related automation.
    """

    def run_unit_test(self: "PyProjectOps"):
        """
        A wrapper of ``pytest`` command to run unit test.
        """
        args = [
            f"{self.path_venv_bin_pytest}",
            f"{self.dir_tests}",
            "-s",
            f"--rootdir={self.dir_project_root}",
        ]
        with self.dir_project_root.temp_cwd():
            subprocess.run(args, check=True)

    def run_cov_test(self: "PyProjectOps"):
        """
        A wrapper of ``pytest`` command to run code coverage test.
        """
        args = [
            f"{self.path_venv_bin_pytest}",
            "-s",
            "--tb=native",
            f"--rootdir={self.dir_project_root}",
            f"--cov={self.package_name}",
            "--cov-report",
            "term-missing",
            "--cov-report",
            f"html:{self.dir_htmlcov}",
            f"{self.dir_tests}",
        ]
        with self.dir_project_root.temp_cwd():
            subprocess.run(args, check=True)

    def view_cov(self: "PyProjectOps"):
        """
        View coverage test output html file locally in web browser.

        It is usually at the ``${dir_project_root}/htmlcov/index.html``
        """
        subprocess.run([OPEN_COMMAND, f"{self.path_htmlcov_index_html}"])

    def run_int_test(self: "PyProjectOps"):
        """
        A wrapper of ``pytest`` command to run integration test.
        """
        args = [
            f"{self.path_venv_bin_pytest}",
            f"{self.dir_tests_int}",
            "-s",
            f"--rootdir={self.dir_project_root}",
        ]
        with self.dir_project_root.temp_cwd():
            subprocess.run(args, check=True)

    def run_load_test(self: "PyProjectOps"):
        """
        A wrapper of ``pytest`` command to run load test.
        """
        args = [
            f"{self.path_venv_bin_pytest}",
            f"{self.dir_tests_load}",
            "-s",
            f"--rootdir={self.dir_project_root}",
        ]
        with self.dir_project_root.temp_cwd():
            subprocess.run(args, check=True)
