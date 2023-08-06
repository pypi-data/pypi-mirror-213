# -*- coding: utf-8 -*-

"""
Python project Ops automation.
"""


from ._version import __version__

__short_description__ = "Python project Ops automation."
__license__ = "MIT"
__author__ = "Sanhe Hu"
__author_email__ = "husanhe@gmail.com"
__maintainer__ = "Sanhe Hu"
__maintainer_email__ = "husanhe@gmail.com"
__github_username__ = "MacHu-GWU"

try:
    from . import api
except ImportError:  # pragma: no cover
    pass
