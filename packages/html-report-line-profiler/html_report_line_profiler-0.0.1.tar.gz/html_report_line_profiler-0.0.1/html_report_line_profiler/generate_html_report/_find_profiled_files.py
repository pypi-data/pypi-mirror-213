from ._tool_find import find_files, find_in_files

def find_profiled_files(the_dir="./profile", ext=".dat"):
    """
rechercher dans le dossier tous les fichiers qui commencent par "test_" et qui se terminent en ".py"

:param str the_dir:
:param str ext: the extension of the files
"""

    list_files = find_files(
        the_dir=the_dir,
        prefix="*",
        ext=ext
    )

    list_files, _ = find_in_files(
        list_files=list_files,
        string="Line #      Hits         Time  Per Hit   % Time  Line Contents",
        hard=False
    )

    return list_files
# endDef
