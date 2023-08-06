import os
from line_profiler import LineProfiler

def setUp_profiler(function, delete_profiling_env:bool = False):
    """
    :param function: nom de la fonction
    :param bool delete_profiling_env: supprimer la variable d'environnement a la fin, si cree ici
    """
    if not os.environ.get("PROFILING", False):
        os.environ["PROFILING"] = "1"
        delete_profiling_env = True
    #endIf

    profiler = LineProfiler()
    profiler.add_function(function)
    profiler.enable_by_count()

    return profiler, delete_profiling_env

#endDef
