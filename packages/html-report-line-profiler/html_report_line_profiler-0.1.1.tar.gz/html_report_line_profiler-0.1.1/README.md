[![Latest Release](https://framagit.org/1sixunhuit/html_report_line_profiler/badges/main/release.svg)](https://framagit.org/1sixunhuit/html_report_line_profiler/-/releases)
[![pipeline status](https://framagit.org/1sixunhuit/html_report_line_profiler/badges/main/pipeline.svg)](https://framagit.org/1sixunhuit/html_report_line_profiler/-/commits/main)
[![coverage report](https://framagit.org/1sixunhuit/html_report_line_profiler/badges/main/coverage.svg)](https://1sixunhuit.frama.io/html_report_line_profiler/coveragepy_report/)
[![PEP8-Critical](https://img.shields.io/endpoint?url=https://1sixunhuit.frama.io/html_report_line_profiler/badges/pep8-critical.json)](https://1sixunhuit.frama.io/html_report_line_profiler/flake8_report/)
[![PEP8-NonCritical](https://img.shields.io/endpoint?url=https://1sixunhuit.frama.io/html_report_line_profiler/badges/pep8-noncritical.json)](https://1sixunhuit.frama.io/html_report_line_profiler/flake8_report/)
[![PEP8-Rate](https://img.shields.io/endpoint?url=https://1sixunhuit.frama.io/html_report_line_profiler/badges/pep8-rate.json)](https://1sixunhuit.frama.io/html_report_line_profiler/flake8_report/)

---

[![Downloads](https://pepy.tech/badge/html_report_line_profiler/month)](https://pepy.tech/project/html_report_line_profiler)
[![Supported Versions](https://img.shields.io/pypi/pyversions/html_report_line_profiler.svg)](https://pypi.org/project/html_report_line_profiler)

---


# Intro

Crée un rapport HTML (avec une arborescence), en se basant sur line_profiler : https://github.com/pyutils/line_profiler, fork de https://github.com/rkern/line_profiler


# TODO
- [ ] Several classes in one file : bug...

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