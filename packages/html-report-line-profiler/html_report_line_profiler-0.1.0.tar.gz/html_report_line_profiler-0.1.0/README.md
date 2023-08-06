# Utilisation dans les tests unitaires :

A ajouter a un test unittaire unittest, et à lancer avec $ coverage run -m unittest test_str.py 

Dans :
```
[...]

import html_report_line_profiler as hr


class Test_CeciEstUnTest(unittest.TestCase):
    def setUp(self):
        # Code execute avant chaque test
        [...] # ce que l'on veut

        # Profiler :
        self.profiler, self.delete_profiling_env = hr.setUp_profiler(castList)

    #endDef

    # ...

    def tearDown(self):
        # Code executé après chaque test
        # Terminer le profiler en premier

        # Create basename
        hr.proffile_basename = classname2basename(
            file_name = __file__,
            class_name = self.__class__.__name__,
            method_name = self._testMethodName
        )

        # Launch the profiler out
        hr.tearDown_profiler(
            profiler=self.profiler,
            proffile_basename=proffile_basename,
            output_folder=output_folder,
            delete_profiling_env=self.delete_profiling_env
        )
        #
	# [...] # Les autres commandes
    #endDef
#endClass
```


# Rapport HTML
Pour lancer ensuite le post-traitement (rapport html) :
```
$ profiler_html_report.py
```

Remarques

* `-d = --input-dir` (default : './profile')
* `-o = --output-dir` (default : './profile_html')