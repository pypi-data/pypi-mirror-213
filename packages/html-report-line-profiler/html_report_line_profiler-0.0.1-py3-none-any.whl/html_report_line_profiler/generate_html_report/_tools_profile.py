import sys
import os

from ._extract_profiled_data import extract_profiled_data
from ._generate_html_page import generate_html_page
from ._extract_with_mask  import extractWithMask

def profilefile2htmlfile(
        file_in:str="file.dat",
        ext_in:str=".dat",
        out_dir:str="./",
        class_name:str="class_name",
        file_name:str="file_name",
        build_tree:bool=True
        ):

    datas = extract_profiled_data(file_name=file_in)

    html = generate_html_page(datas, path_css=out_dir)

    basename_html = os.path.basename(file_in).replace(ext_in, ".html")

    path_html = html2file(
        html,
        basename=basename_html,
        out_dir=out_dir,
        mod_name=class_name,
        fct_name=file_name,
        build_tree=build_tree
    )

    sys.stdout.write(f"write file> {os.path.abspath(path_html)}\n")

    return path_html, datas["total time"]
#

def extract_profpath(basename, list_prof, rangelen_listprof):
    mask = [basename == os.path.basename(e) for e in list_prof]

    fileprof = extractWithMask(
        the_list=list_prof,
        the_mask=mask,
        rangelen_list=rangelen_listprof
    )

    if len(fileprof) == 1:
        return fileprof[0]
    elif len(fileprof) > 1:
        print("unexpected, trop : ", fileprof)
        print()
        return  fileprof[0]
    # endIf
    return ""
#


def html2file(html, basename="out.html", out_dir="./", mod_name:str=None, fct_name:str=None, build_tree:bool=True):
    """Write HTML file from string (html)

:param str html: HTML content
:param basename: Name of the html file
:param mod_name: Name of the module
:param fct_name: Name of the function
:param bool build_tree: Build the tree directories

:return: the path to the html file
:rtypes: str
"""

    if build_tree:

        path = os.path.join(
            out_dir,
            (mod_name.replace("/", "_").replace(".", "_") if mod_name is not None else ""),
            (fct_name.replace("/", "_").replace(".", "_") if fct_name is not None else "")
        )

    else:

        path = out_dir

    #endIf

    # Creer le dossier si n'existe pas et ecrire le fichier
    os.makedirs(path, exist_ok=True)
    path_html = os.path.join(path, basename)
    with open(path_html, "w") as f:
        f.write(html)
    #endWith
    return path_html
#end
