import os
from ._tool_find import find_files, find_in_files

def find_test_functions(the_dir="./", prefix="test_", ext=".py"):
    """
rechercher dans le dossier tous les fichiers qui commencent par "test_" et qui se terminent en ".py"

:param str the_dir:
:param str prefix: the prefix of the tests
"""

    list_files = find_files(
        the_dir=the_dir,
        prefix="*",
        ext=ext
    )

    list_files, _ = find_in_files(
        list_files=list_files,
        string="import unittest",
        hard=False
    )

    return list_files
# endDef


def testfunctions_to_dict(list_files):
    """ Convertir fichier sources des tests unitaires (test_X.py) en un dictionnaire

    :param list list_file: list of python files used to do the test
    :return: {file_name: {Test_X (class_name):({name:fct_name}, {name:fct_name}, ...)}}
    :rtypes: dict
    """

    ordered_files = {}
    for each_file in list_files:
        with open(each_file, "r") as f:
            content = f.readlines()
        #endWith

        file_name = os.path.basename(each_file).split(".py")[0]

        module_name = ""

        for line in content:

            if "class test" in line[0:len("class Test")].lower():

                module_name = line.replace("class Test", "").split("(")[0]

                if module_name[0] == "_":
                    module_name = module_name[1:]
                #endIf

                ordered_files[file_name] = {module_name:{"functions":[], "path_in":each_file}}
            elif not module_name:
                continue
            elif line.strip()[:4] == "def ":
                ordered_files[file_name][module_name]["functions"].append(
                    {
                        "name"
                        :
                        line.strip()[4:].split("(")[0]
                    }
                )
            #endIf
        #endFor line

    # endFor file
    return ordered_files
