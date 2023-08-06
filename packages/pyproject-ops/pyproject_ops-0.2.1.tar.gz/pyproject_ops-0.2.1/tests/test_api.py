# -*- coding: utf-8 -*-


def test():
    from pyproject_ops import api


if __name__ == "__main__":
    from pyproject_ops.tests import run_cov_test

    run_cov_test(__file__, "pyproject_ops.api", preview=False)
