"""
Generate html pages from line_parser profiler
"""

from .generate_html_report import generate_html_report
from .setup_profiler import setUp_profiler
from .teardown_profiler import tearDown_profiler

from .__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __version__,
    __pkg_name__,
)

# requirements are in requirements.txt


__all__ = [
    '__author__', '__author_email__',
    '__copyright__', '__description__', '__license__',
    '__title__', '__version__', '__pkg_name__',
    "generate_html_report",
    "setUp_profiler",
    "tearDown_profiler"
]
