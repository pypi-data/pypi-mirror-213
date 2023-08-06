# -*- coding: utf-8 -*-

from .vendor.nested_logger import NestedLogger

logger = NestedLogger(
    name="pyproject_ops",
    log_format="%(message)s",
)
