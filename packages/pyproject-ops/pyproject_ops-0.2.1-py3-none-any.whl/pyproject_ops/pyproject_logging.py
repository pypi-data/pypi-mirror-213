# -*- coding: utf-8 -*-

import typing as T
import dataclasses
from pathlib_mate import Path

from .compat import cached_property
from .logger import logger

if T.TYPE_CHECKING:
    from .pyproject_ops import PyProjectOps


@dataclasses.dataclass
class PyProjectLogging:
    print_func: T.Callable = dataclasses.field(default=logger.info)
