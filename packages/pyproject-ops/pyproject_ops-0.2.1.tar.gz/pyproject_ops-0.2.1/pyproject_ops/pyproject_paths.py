# -*- coding: utf-8 -*-

"""
Enumeration of important paths on local file system.
"""

import typing as T
import sys
import subprocess
import dataclasses
from pathlib_mate import Path

from .compat import cached_property

if T.TYPE_CHECKING:  # pragma: no cover
    from .ops import PyProjectOps


@dataclasses.dataclass
class PyProjectPaths:
    """
    Namespace class for accessing important paths.

    :param dir_project_root: The root directory of the project, it is usually
        the git root directory. It has to have a ``pyproject.toml`` file or
        ``setup.py`` in it.
    :param package_name: The name of the Python package you are working on.
        There has to be a folder with the same name under ``dir_project_root``,
        And it has to have a ``__init__.py`` file in it.
    """

    dir_project_root: Path = dataclasses.field()
    package_name: str = dataclasses.field()

    def _validate_paths(self):
        if (self.dir_project_root.joinpath("pyproject.toml").exists() is False) and (
            self.dir_project_root.joinpath("setup.py").exists() is False
        ):
            raise ValueError(
                f"{self.dir_project_root} does not have a pyproject.toml or setup.py file "
                f"it might not be a valid project root directory."
            )
        dir_python_lib = self.dir_project_root.joinpath(self.package_name)
        if dir_python_lib.joinpath("__init__.py").exists() is False:
            raise ValueError(
                f"{dir_python_lib} does not have a __init__.py file, "
                f"the package name {self.package_name} might be invalid."
            )

    @cached_property
    def dir_home(self) -> Path:
        """
        The user home directory.

        Example: ``${HOME}``
        """
        return Path.home()

    # --------------------------------------------------------------------------
    # Virtualenv
    # --------------------------------------------------------------------------
    _VENV_RELATED = None

    @property
    def dir_venv(self) -> Path:
        """
        The virtualenv directory.

        Example: ``${dir_project_root}/.venv``
        """
        return self.dir_project_root.joinpath(".venv")

    @property
    def dir_venv_bin(self) -> Path:
        """
        The bin folder in virtualenv.

        Example: ``${dir_project_root}/.venv/bin``
        """
        return self.dir_venv.joinpath("bin")

    def get_path_venv_bin_cli(self, cmd: str) -> Path:
        """
        Get the path of a command in virtualenv bin folder.

        Example: ``${dir_project_root}/.venv/bin/${cmd}``
        """
        return self.dir_venv_bin.joinpath(cmd)

    @property
    def path_venv_bin_python(self) -> Path:
        """
        The python executable in virtualenv.

        Example: ``${dir_project_root}/.venv/bin/python``
        """
        return self.get_path_venv_bin_cli("python")

    @property
    def path_venv_bin_pip(self) -> Path:
        """
        The pip command in virtualenv.

        Example: ``${dir_project_root}/.venv/bin/pip``
        """
        return self.get_path_venv_bin_cli("pip")

    @property
    def path_venv_bin_pytest(self) -> Path:
        """
        The pytest command in virtualenv.

        Example: ``${dir_project_root}/.venv/bin/pytest``
        """
        return self.get_path_venv_bin_cli("pytest")

    @property
    def path_sys_executable(self) -> Path:
        """
        The current Python interpreter path.
        """
        return Path(sys.executable)

    def get_path_dynamic_bin_cli(self, cmd: str) -> Path:
        """
        Search multiple locations to get the absolute path of the CLI command.
        It search the following locations in order:

        1. the bin folder in virtualenv.
        2. the global Python's bin folder.
        3. Then use the raw command name (string) as the path.

        Example: ``${dir_project_root}/.venv/bin/${cmd}`` or ``${global_python_bin}/${cmd}``
        """
        p = self.dir_venv_bin.joinpath(cmd)
        if p.exists():
            return p
        p = self.path_sys_executable.parent.joinpath(cmd)
        if p.exists():
            return p
        return Path(cmd)

    @property
    def path_bin_virtualenv(self) -> Path:
        """
        The virtualenv CLI command path.

        Example: ``${dir_project_root}/.venv/bin/virtualenv``
        """
        return self.get_path_dynamic_bin_cli("virtualenv")

    @property
    def path_bin_poetry(self) -> Path:
        """
        The poetry CLI command path.

        Example: ``${dir_project_root}/.venv/bin/poetry``
        """
        return self.get_path_dynamic_bin_cli("poetry")

    @property
    def path_bin_twine(self) -> Path:
        """
        The twine CLI command path.

        Example: ``${dir_project_root}/.venv/bin/twine``
        """
        return self.get_path_dynamic_bin_cli("twine")

    # --------------------------------------------------------------------------
    # Source code
    # --------------------------------------------------------------------------
    @property
    def dir_python_lib(self) -> Path:
        """
        The current Python library directory.

        Example: ``${dir_project_root}/${package_name}``
        """
        return self.dir_project_root.joinpath(self.package_name)

    @property
    def path_version_py(self) -> Path:
        """
        Path to the ``_version.py`` file where the package version is defined.

        Example: ``${dir_project_root}/${package_name}/_version.py``
        """
        return self.dir_python_lib.joinpath("_version.py")

    @cached_property
    def package_version(self) -> str:
        """
        Version of the current Python library defined in ``_version.py`` file.
        """
        args = ["python", f"{self.path_version_py}"]
        res = subprocess.run(args, check=True, capture_output=True)
        return res.stdout.decode("utf-8").strip()

    # --------------------------------------------------------------------------
    # Pytest
    # --------------------------------------------------------------------------
    _PYTEST_RELATED = None

    @property
    def dir_tests(self) -> Path:
        """
        Unit test folder.

        Example: ``${dir_project_root}/tests``
        """
        return self.dir_project_root.joinpath("tests")

    @property
    def dir_tests_int(self) -> Path:
        """
        Integration test folder.

        Example: ``${dir_project_root}/tests_int``
        """
        return self.dir_project_root.joinpath("tests_int")

    @property
    def dir_tests_load(self) -> Path:
        """
        Load test folder.

        Example: ``${dir_project_root}/tests_load``
        """
        return self.dir_project_root.joinpath("tests_load")

    @property
    def dir_htmlcov(self) -> Path:
        """
        The code coverage test results HTML output folder.

        Example: ``${dir_project_root}/htmlcov``
        """
        return self.dir_project_root.joinpath("htmlcov")

    @property
    def path_htmlcov_index_html(self) -> Path:
        """
        The code coverage test results HTML file.

        Example: ``${dir_project_root}/htmlcov/index.html``
        """
        return self.dir_htmlcov.joinpath("index.html")

    # --------------------------------------------------------------------------
    # Sphinx doc
    # --------------------------------------------------------------------------
    _SPHINX_DOC_RELATED = None

    @property
    def dir_sphinx_doc(self) -> Path:
        """
        Sphinx docs folder.

        Example: ``${dir_project_root}/docs``
        """
        return self.dir_project_root.joinpath("docs")

    @property
    def dir_sphinx_doc_source(self) -> Path:
        """
        Sphinx docs source code folder.

        Example: ``${dir_project_root}/docs/source``
        """
        return self.dir_sphinx_doc.joinpath("source")

    @property
    def dir_sphinx_doc_source_conf_py(self) -> Path:
        """
        Sphinx docs ``conf.py`` file path.

        Example: ``${dir_project_root}/docs/source/conf.py``
        """
        return self.dir_sphinx_doc_source.joinpath("conf.py")

    @property
    def dir_sphinx_doc_source_python_lib(self) -> Path:
        """
        The generated Python library API reference Sphinx docs folder.

        Example: ``${dir_project_root}/docs/source/${package_name}``
        """
        return self.dir_sphinx_doc_source.joinpath(self.package_name)

    @property
    def dir_sphinx_doc_build(self) -> Path:
        """
        The temp Sphinx doc build folder.

        Example: ``${dir_project_root}/docs/build
        """
        return self.dir_sphinx_doc.joinpath("build")

    @property
    def dir_sphinx_doc_build_html(self) -> Path:
        """
        The built Sphinx doc build HTML folder.

        Example: ``${dir_project_root}/docs/build/html
        """
        return self.dir_sphinx_doc_build.joinpath("html")

    @property
    def path_sphinx_doc_build_index_html(self) -> Path:  # pragma: no cover
        """
        The built Sphinx doc site entry HTML file path.

        Example: ``${dir_project_root}/docs/build/html/index.html or README.html
        """
        if self.dir_sphinx_doc_source.joinpath("index.rst").exists():
            return self.dir_sphinx_doc_build_html.joinpath("index.html")

        if self.dir_sphinx_doc_source.joinpath("README.rst").exists():
            return self.dir_sphinx_doc_build_html.joinpath("README.html")

        raise FileNotFoundError(
            str(self.dir_sphinx_doc_build_html.joinpath("index.html"))
        )

    # --------------------------------------------------------------------------
    # Poetry
    # --------------------------------------------------------------------------
    _POETRY_RELATED = None

    @property
    def path_requirements(self) -> Path:
        """
        The requirements.txt file path.

        Example: ``${dir_project_root}/requirements.txt``
        """
        return self.dir_project_root.joinpath("requirements.txt")

    @property
    def path_requirements_dev(self) -> Path:
        """
        The requirements-dev.txt file path.

        Example: ``${dir_project_root}/requirements-dev.txt``
        """
        return self.dir_project_root.joinpath("requirements-dev.txt")

    @property
    def path_requirements_test(self) -> Path:
        """
        The requirements-test.txt file path.

        Example: ``${dir_project_root}/requirements-test.txt``
        """
        return self.dir_project_root.joinpath("requirements-test.txt")

    @property
    def path_requirements_doc(self) -> Path:
        """
        The requirements-doc.txt file path.

        Example: ``${dir_project_root}/requirements-doc.txt``
        """
        return self.dir_project_root.joinpath("requirements-doc.txt")

    @property
    def path_requirements_automation(self) -> Path:
        """
        The requirements-automation.txt file path.

        Example: ``${dir_project_root}/requirements-automation.txt``
        """
        return self.dir_project_root.joinpath("requirements-automation.txt")

    @property
    def path_poetry_lock(self) -> Path:
        """
        The poetry.lock file path.

        Example: ``${dir_project_root}/poetry.lock``
        """
        return self.dir_project_root.joinpath("poetry.lock")

    @property
    def path_poetry_lock_hash_json(self) -> Path:
        """
        The poetry-lock-hash.json file path. It is the cache of the poetry.lock file hash.

        Example: ``${dir_project_root}/poetry-lock-hash.json``
        """
        return self.dir_project_root.joinpath("poetry-lock-hash.json")

    # ------------------------------------------------------------------------------
    # Build Related
    # ------------------------------------------------------------------------------
    _BUILD_RELATED = None

    @property
    def path_pyproject_toml(self) -> Path:
        """
        The pyproject.toml file path.

        Example: ``${dir_project_root}/pyproject.toml``
        """
        return self.dir_project_root.joinpath("pyproject.toml")

    @property
    def dir_build(self) -> Path:
        """
        The build folder for Python or artifacts build.

        Example: ``${dir_project_root}/build``
        """
        return self.dir_project_root.joinpath("build")

    @property
    def dir_dist(self) -> Path:
        """
        The dist folder for Python package distribution (.whl file).

        Example: ``${dir_project_root}/dist``
        """
        return self.dir_project_root.joinpath("dist")
