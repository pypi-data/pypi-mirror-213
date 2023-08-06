import os

from ._find_test_functions import find_test_functions, testfunctions_to_dict
from ._find_profiled_files import find_profiled_files

from ._profilefile2htmlfile import functions2profilfile

from ..__version__ import __pkg_name__
def generate_html_report(the_dir:str="./", out_dir=None, build_tree:bool=True):
    """
:param str the_dir: Name of the directory
:param str out_dir: Name of the out directory for html pages
:param bool build_tree: Build a tree : /out_dir/module/function/test.html
"""

    if out_dir is None:
        out_dir = the_dir
    #endIf

    # Recuperer tous les fichiers de profilage
    list_files = find_test_functions(os.path.join(the_dir, ".."))
    list_prof = find_profiled_files(the_dir)

    ordered_files = testfunctions_to_dict(list_files)


    list_mod = []
    total_time_mod = 0.0

    a = functions2profilfile(ordered_files, list_prof, ext=".dat", out_dir=out_dir, build_tree=build_tree)

    # Copie du fichier css
    with open(f"../{__pkg_name__}/template/style.css", "r") as f:
        css = f.read()
    # endWith
    with open(os.path.join(out_dir, "style.css"), "w") as f:
        f.write(css)
    # endWith

    # Creer index des fichiers du module :
    #
    # module 1
    # - fonction1
    # - fonction2
#
