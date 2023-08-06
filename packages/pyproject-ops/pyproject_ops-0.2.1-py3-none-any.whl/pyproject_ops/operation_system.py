# -*- coding: utf-8 -*-

from .vendor.os_platform import IS_WINDOWS


if IS_WINDOWS:
    OPEN_COMMAND = "start"
else:
    OPEN_COMMAND = "open"
