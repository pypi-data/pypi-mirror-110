from .typed_flags import TypedFlags

__version__ = "1.1.4"

import logging
from collections import namedtuple

logging.getLogger(__name__).addHandler(logging.NullHandler())
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=1, minor=1, micro=4, releaselevel="final", serial=0)
