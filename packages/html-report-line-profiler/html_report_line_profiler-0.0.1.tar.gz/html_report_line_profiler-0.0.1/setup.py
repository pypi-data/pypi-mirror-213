from setuptools import setup
import os
import sys

# Variables ##########################################
package_name = "html_report_line_profiler"
# packages = Components of the package to add
packages = [package_name, f"{package_name}.generate_html_report"]
url_page = "https://1sixunhuit.frama.io"
url_git = "https://framagit.org"
package_data = {'template': ['page.html', 'style.css']}  # non py files
# #####################################################
#
# THEN : DO NOT MODIFY
# --------------------
# #####################################################

def parse_version(path:str='./modulename/__version__.py'):
    about = {}
    with open(path, "r") as f:
        exec(f.read(), about)
    #endWith
    return about
#endDef

def parse_requirements(path:str='./requirements.txt'):
    """    Parser le fichier requirements.txt

- Nommer les categories de modules pour separer l'indispensable au package de ceux pour le deploiement et la doc
- Les tags qui ne sont pas indiques ici seront consideres comme principaux
> # tag
> package == X.Y.Z

- Pour creer une nouvelle categorie :
-- ajouter "CATEGORIE_TAG" (1)
-- ajouter un indicateur "CAT" (4) et init le dico "extra_requires" avec cet indicateur
-- Ajouter dans (5) :
--- "elif line.lower() in CATEGORIE_tags: ..."
--- "elif add_to == _CAT: ..."

:param str path: Chemin/fichier.txt a parser
:return: packages, extras_require
:rtypes: (list, dict)
    """

    # (1) Categories
    doc_tags = [
        '# doc', '# document', '# documentation',
        '#doc', '#document', '#documentation',
    ]

    test_tags = [
        '# cover', '# coverage', '# test', '# tests', '# unit test', '# unit-test', '# unit tests', '# unit-tests',
        '#cover', '#coverage', '#test', '#tests', '#unit test', '#unit-test', '#unit tests', '#unit-tests',
    ]

    pypi_tags = [
        '# twine', '# pypi',
        '#twine', '#pypi',
    ]
    ## (2) Lire le contenu du fichier requirements.txt
    if not os.path.exists(path):
        return [], {}
    #
    with open(path, 'r') as file:
        lines = file.readlines()
    #endWith

    ## (3) Variables pour stocker les lignes dans les sections appropriées
    packages_lines = []
    doc_lines = []
    extras_pkg = {}

    ## (4) Indicateur pour déterminer si les lignes doivent être ajoutées à la section "packages" ou "doc"
    _packages = "packages"
    _doc = "doc"
    _test = "test"
    _pypi = "upload"

    extras_pkg[_doc] = []
    extras_pkg[_test] = []
    extras_pkg[_pypi] = []

    add_to = _packages # Valeur par defaut

    ## (5) Parcourir les lignes du fichier requirements.txt
    for line in lines:

        line = line.strip()

        if line.lower() in doc_tags:

            add_to = _doc

        elif line.lower() in test_tags:

            add_to = _test

        elif line.lower() in pypi_tags:

            add_to = _pypi

        elif line.startswith('#'):

            add_to = _packages

        elif add_to == _packages:

            packages_lines.append(line.split("#")[0].strip())

        elif add_to == _doc:

            extras_pkg[_doc].append(line.split("#")[0].strip())

        elif add_to == _test:

            extras_pkg[_test].append(line.split("#")[0].strip())

        elif add_to == _pypi:

            extras_pkg[_pypi].append(line.split("#")[0].strip())

        else:

            raise ValueError(f"{add_to} not in [{_packages}, {_doc}]")

        #endIf
    #endFor

    ## Convertir les lignes en arguments de setup()
    packages = [line.split(' ')[0] for line in packages_lines]
    extras_require = {k:[e for e in v if e] for k,v in extras_pkg.items() if k}

    return packages, extras_require
#endDef


if __name__ == '__main__':

    try:
        import sphinx
    except ImportError:
        sphinxInstalled=False
    else:
        sphinxInstalled=True
    #endTry

    if not sphinxInstalled:
        sys.stderr.write(f"> Warning, Sphinx is not installed ; I'll try it.\n")
    #endIf

    # Chemin du repertoire ...........................................
    here = os.path.abspath(os.path.dirname(__file__))

    # Lecture du requirements.txt ....................................
    packages_requirements, extras_require = parse_requirements(path=os.path.join(here, 'requirements.txt'))

    # Lecture du __version__.py ......................................
    path_about = os.path.join(here, package_name, "__version__.py")
    if os.path.exists(path_about):
        about = parse_version(path=path_about)
    else:
        raise ValueError(f"Path not exists: {path_about}")
    #

    ## Creation de variables
    url = f'{url_page}/{about["__git_name__"]}'
    project_urls = {
        'Source Code': f'{url_git}/{about["__git_group__"]}/{about["__git_name__"]}',
    }

    # Setup ..........................................................
    setup(
        name = str(about["__pkg_name__"]),
        version = str(about["__version__"]),
        license = str(about["__license__"]),
        copyright = str(about["__copyright__"]),
        url = url,
        project_url = project_urls,
        author = str(about["__author__"]),
        author_email = str(about["__author_email__"]),
        description = str(about["__description__"]),
        keywords=str(about["__keywords__"]),
        packages=packages+packages_requirements,
        extras_require=extras_require,
        package_data=package_data,
    )

#endIf
