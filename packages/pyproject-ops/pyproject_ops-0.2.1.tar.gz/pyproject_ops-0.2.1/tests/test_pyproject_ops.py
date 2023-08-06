# -*- coding: utf-8 -*-

import inspect
from pathlib_mate import Path
from pyproject_ops.api import PyProjectOps


pyops = PyProjectOps(
    dir_project_root=Path.dir_here(__file__).parent,
    package_name="pyproject_ops",
    python_version="3.8",
)


class TestPyprojectPaths:
    def test(self):
        for name, type_ in inspect.getmembers(PyProjectOps):
            if isinstance(type_, property):
                if name.startswith("dir_") or name.startswith("path_"):
                    getattr(pyops, name)


class PyProjectVenv:
    def test(self):
        _ = pyops.create_virtualenv
        _ = pyops.remove_virtualenv


class PyProjectDeps:
    def test(self):
        _ = pyops.poetry_lock
        _ = pyops.poetry_install
        _ = pyops.poetry_install_dev
        _ = pyops.poetry_install_test
        _ = pyops.poetry_install_doc
        _ = pyops.poetry_install_all
        _ = pyops._do_we_need_poetry_export
        _ = pyops._poetry_export_group
        _ = pyops._poetry_export
        _ = pyops.poetry_export
        _ = pyops._try_poetry_export
        _ = pyops.pip_install
        _ = pyops.pip_install_dev
        _ = pyops.pip_install_test
        _ = pyops.pip_install_doc
        _ = pyops.pip_install_automation
        _ = pyops.pip_install_all


class PyProjectTests:
    def test(self):
        _ = pyops.run_unit_test
        _ = pyops.run_cov_test


class PyProjectDocs:
    def test(self):
        _ = pyops.build_doc
        _ = pyops.view_doc
        _ = pyops.deploy_versioned_doc
        _ = pyops.deploy_latest_doc
        _ = pyops.view_latest_doc


if __name__ == "__main__":
    from pyproject_ops.tests import run_cov_test

    run_cov_test(__file__, "pyproject_ops", preview=False)
