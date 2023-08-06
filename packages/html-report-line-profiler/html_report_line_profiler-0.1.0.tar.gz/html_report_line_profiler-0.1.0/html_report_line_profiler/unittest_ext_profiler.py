import os
import io
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


def names2basename(
        file_name:str,
        class_name:str,
        method_name:str
):
    class_name_t = class_name.lower().replace('test',"")
    class_name_t = class_name_t if not class_name_t[0] == "_" else class_name_t[1:]
    return f"{os.path.basename(file_name).replace('.py','')}_{class_name_t}_{method_name}"


def tearDown_profiler(profiler, proffile_basename="file", output_folder="./profile", delete_profiling_env:bool=False):
    if profiler is None:
        return
    #
    # Code executé après chaque test
    #del self.my_class_instance
    output_folder = os.path.abspath(output_folder)
    profiler.disable_by_count()
    os.makedirs(output_folder, exist_ok=True)  # Creer si necessaire le dossier

    binary_file = f"{proffile_basename}.lprof"
    outfile = os.path.join(output_folder, binary_file)
    profiler.dump_stats(outfile)
    print(f">> WRITE {outfile}")
    #

    text_file = f"{proffile_basename}.dat"
    output_stream = io.StringIO()
    profiler.print_stats(stream=output_stream)
    stats_output = output_stream.getvalue()

    with open(os.path.join(output_folder, text_file), "w") as f:
        f.write(stats_output)
    #

    print(f">> WRITE {text_file}")

    profiler.print_stats()
    if delete_profiling_env and os.environ.get("PROFILING", False):
        del os.environ["PROFILING"]
    #
#
