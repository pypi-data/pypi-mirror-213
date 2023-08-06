import os
import sys

from ._tools_profile import extract_profpath, profilefile2htmlfile, html2file
from ._generate_html_page import generate_html_page
from ..__version__ import __pkg_name__


def functions2profilfile(ordered_files, list_prof, ext=".dat", out_dir="./", build_tree:bool=True):

    if ext[0] == "." and len(ext)>1:
        ext = ext[1:]
    #

    listprof_basename = [os.path.basename(e) for e in list_prof]
    len_listprof = len(list_prof)
    rl_listprof = range(len_listprof)

    index_page = []

    for file_name, d_file in ordered_files.items():

        total_time_mod = 0.0

        for class_name, d_class in d_file.items():

            total_time_fct = 0.0
            list_fct = []

            for each_fct in d_class["functions"]:

                basename = f"{class_name}_{each_fct['name']}.{ext}"
                path_prof = extract_profpath(
                    basename=basename,
                    list_prof=list_prof,
                    rangelen_listprof=rl_listprof
                )

                if not path_prof:
                    continue
                # endIf

                each_fct["profile_in"] = path_prof

                path_html, total_time = profilefile2htmlfile(
                    file_in=path_prof,
                    ext_in=".dat",
                    out_dir=out_dir,
                    class_name=class_name,
                    file_name=file_name,
                    build_tree=build_tree
                )

                total_time_fct +=  float(str(total_time).strip().split(" ")[0])

                list_fct.append(
                    {
                        "line": 0, "hits": 1, "per hit": None, "% time": None,
                        "time": total_time,
                        "line content":f"<a href={os.path.abspath(path_html)}>{os.path.basename(path_html)}</a>"
                    }
                )
            # endFor each_fct

            for elt in list_fct:
                elt["% time"] = float(str(elt["time"]).strip().split(" ")[0]) / total_time_fct * 100.0
            # endFor

            # Creer index des tests du fichier :
            #
            # fonction1
            # - test1
            # - test2

            datas = {"timer unit":None,
                     "total time": total_time_fct,
                     "file":f"{file_name}"  ,# nom du fichier source module/function.py
                     "function":class_name, # nom de la classe
                     "report":list_fct
                     }

            total_time_mod +=  float(str(datas["total time"]).strip().split(" ")[0])

            html = generate_html_page(
                datas,
                path_css=out_dir,
                header=f"<h1>INDEX : {class_name}</h1>"
            )

            basename = f'index.html'

            dirout1 = "/".join([e for e in out_dir.split("/") if e])

            index_class_html = html2file(
                html,
                basename=basename,
                out_dir=dirout1,
                mod_name=class_name,
                fct_name=None,
                build_tree=build_tree
            )

            index_page.append(
                {
                    "line": 0,
                    "line content":f"<a href={os.path.abspath(index_class_html)}>{class_name}</a>"
                    }
                )

            sys.stdout.write(f"write file> {os.path.abspath(index_class_html)}\n")
        # endFor classname
    # endFor filename

    datas = {"timer unit":None,
             "total time": None,
             "file":f"{file_name}"  ,# nom du fichier source module/function.py
             "function":None, # nom de la classe
             "report":index_page
             }


    html = generate_html_page(
        datas,
        path_css=out_dir,
        header=f"<h1>INDEX</h1>"
    )


    basename = f'index.html'

    html_page = html2file(
        html,
        basename=basename,
        out_dir=out_dir,
        mod_name=None,
        fct_name=None,
        build_tree=build_tree
    )
    sys.stdout.write(f"write file> {os.path.abspath(html_page)}\n")
#
