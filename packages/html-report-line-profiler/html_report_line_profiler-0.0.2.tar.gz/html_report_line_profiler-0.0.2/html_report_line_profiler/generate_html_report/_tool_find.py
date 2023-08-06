import glob
import os
import re

def find_files(the_dir="./", prefix="test_", ext=".dat"):
    """
rechercher dans le dossier tous les fichiers qui commencent par "test_" et qui se terminent en ".py"

:param str the_dir:
:param str prefix: the prefix of the tests
:param str ext: the extension of the files

:return: list of files
:rtypes: list
"""


    if ext == ".":
        raise ValueError("ext can not be a dot !")
    elif "." in ext:
        ext = ".".join(ext.split(".")[1:])
    #endIf

    the_dir = os.path.abspath(the_dir)

    # Lister les fichiers
    if prefix == "*":
        prefix = ""
    # endIf
    model = f"{prefix}*"

    if ext != "*" and ext:
        model = f"{model}.{ext}"
    # endIf

    list_files = glob.glob(os.path.join(the_dir, model))

    return list_files
# end


def find_in_files(list_files: list, string: str, hard: bool = False):
    """Split list of files, between those where string is find and not

:param list list_files: list of files
:param str string: the searched string
:param bool hard: if True, the string must be exactly equal ; if False, comparison without case and multiple spaces

:return: (found, not found)
:rtypes: tuple(list, list)
"""

    i = len(list_files) - 1

    string_present = False
    not_present = []

    while i >= 0:

        with open(list_files[i]) as myfile:

            if hard:
                string_present = string in myfile
            else:
                string_present = re.sub(' +', ' ', string.lower()) in re.sub(' +', ' ', myfile.read().lower())
            # endIf

        # endWith

        if not string_present:
            not_present += [list_files[i],]
            del list_files[i]
        # end If

        i -= 1
    # end

    return list_files, not_present
# end
