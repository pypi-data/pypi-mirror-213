import os
import io

#
# class_name_t = class_name.lower().replace('test',"")
# class_name_t = class_name_t if not class_name_t[0] == "_" else class_name_t[1:]
# proffile_basename = os.path.join(dirout, f"{class_name_t}_{test_method_name}")
def tearDown_profiler(proffile_basename="file", output_folder="./profile"):
    # Code executé après chaque test
    #del self.my_class_instance
    self.profiler.disable_by_count()
    os.makedirs(output_folder, exist_ok=True)  # Creer si necessaire le dossier

    test_method_name = self._testMethodName

    binary_file = f"{proffile_basename}.lprof"
    output_folder = "./profile/"
    outfile = os.path.join(output_folder, binary_file)
    self.profiler.dump_stats(outfile)
    print(f">> WRITE {outfile}")
    #

    text_file = f"{proffile_basename}.lprof"
    output_stream = io.StringIO()
    self.profiler.print_stats(stream=output_stream)
    stats_output = output_stream.getvalue()

    with open(text_file, "w") as f:
        f.write(stats_output)
    #

    print(f">> WRITE {text_file}")

    self.profiler.print_stats()
    if self.delete_profiling_env:
        del os.environ["PROFILING"]
    #
#
