"""
Generate html pages from line_parser profiler
"""

from .generate_html_report import generate_html_report_fct
from .unittest_ext_profiler import setUp_profiler, tearDown_profiler, names2basename

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
    "generate_html_report_fct",
    "setUp_profiler",
    "tearDown_profiler",
    "names2basename"
]
