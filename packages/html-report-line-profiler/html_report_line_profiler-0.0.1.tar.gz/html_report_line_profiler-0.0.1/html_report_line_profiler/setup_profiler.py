import os
from line_profiler import LineProfiler

def setUp_profiler(function):
    if not os.environ.get("PROFILING", False):
        os.environ["PROFILING"] = "1"
        self.delete_profiling_env = True
        self.profiler = LineProfiler()
        self.profiler.add_function(function)
        self.profiler.enable_by_count()
    #endIf
#endDef
