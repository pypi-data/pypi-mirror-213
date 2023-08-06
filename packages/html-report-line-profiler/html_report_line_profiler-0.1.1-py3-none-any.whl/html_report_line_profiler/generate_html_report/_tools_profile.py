import sys
import os

from ._extract_profiled_data import extract_profiled_data
from ._generate_html_page import generate_html_page
from ._extract_with_mask  import extractWithMask


def names_file_class_fct2path(
        base_path: str = "./",
        file_name: str = None,
        class_name: str = None,
        fct_name: str = None,
        build_tree: bool = True
):

    if build_tree:

        ldirname = [
            file_name.replace("/", "_").replace(".", "_") if file_name is not None else "",
            class_name.replace("/", "_").replace(".", "_") if class_name is not None else ""
        ]

        dirname = "_".join([e for e in ldirname if e]).lower()
        path = os.path.join(base_path, dirname)

    else:

        path = base_path

    #endIf

    # Creer le dossier si n'existe pas et ecrire le fichier
    os.makedirs(path, exist_ok=True)

    return path
#

def profilefile2htmlfile(
        file_in:str="file.dat",
        ext_in:str=".dat",
        out_dir:str="./",
        file_name:str="file_name",
        class_name:str="class_name",
        fct_name:str="function_name",
        build_tree:bool=True
        ):

    datas = extract_profiled_data(file_name=file_in)

    datas["function"] = f"{file_name}.py: {class_name}: {fct_name}: {datas['function']}"

    path_html_dir = names_file_class_fct2path(
        base_path=out_dir,
        file_name=file_name,
        class_name=class_name,
        fct_name=fct_name,
        build_tree=build_tree
    )

    html = generate_html_page(
        datas,
        path_css=os.path.relpath(out_dir, path_html_dir),
        index_same_dir=True
    )

    #basename_html = os.path.basename(file_in).replace(ext_in, ".html")
    basename_html = f"{fct_name}.html".lower()

    path_html = html2file(
        html,
        basename=basename_html,
        path=path_html_dir
    )

    sys.stdout.write(f"write file> {os.path.abspath(path_html)}\n")

    return path_html, datas["total time"]
#

def extract_profpath(basename, list_prof, rangelen_listprof):
    basenamelow = basename.lower()
    mask = [basenamelow == os.path.basename(e).lower() for e in list_prof]

    fileprof = extractWithMask(
        the_list=list_prof,
        the_mask=mask,
        rangelen_list=rangelen_listprof
    )

    if len(fileprof) == 1:
        return fileprof[0]
    elif len(fileprof) > 1:
        sys.stderr.write(f">unexpected, trop : {fileprof}\n\n")
        return fileprof[0]
    # endIf

    return ""
#


def html2file(html, basename="out.html", path="./"):
    """Write HTML file from string (html)

:param str html: HTML content
:param str basename: Name of the html file
:param str path: Path of the html file

:return: the path to the html file
:rtypes: str
"""

    path_html = os.path.join(path, basename)

    with open(path_html, "w") as f:
        f.write(html)
    #endWith

    return path_html
#end
