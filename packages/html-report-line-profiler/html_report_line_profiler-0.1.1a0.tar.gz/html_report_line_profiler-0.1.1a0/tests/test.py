# -*- coding: utf-8 -*-
import unittest  # python -m unittest discover
import sys
import os

# sys.path.insert(0, '../')
from html_report_line_profiler import generate_html_report

if __name__=="__main__":
    generate_html_report(
        the_dir="/home/pierre/Documents/Projets/catho/module_toolkit/tests/profile",
        out_dir="./reports",
        build_tree=True
    )
