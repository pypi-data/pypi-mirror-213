"""Configuration file for the Sphinx documentation builder"""
# -*- coding: utf-8 -*-

from anybadge import Badge
import os
import inspect

def _query_badges_values():
    badges = dict()
    keywords = zip(["pypi package", 'license'], ["VERSION", "LICENSE"])
    ignore_chars = ['=', "'", '"', ',', "::"]
    root = os.path.abspath(inspect.getfile(inspect.currentframe()))
    root = os.path.dirname(root)

    with open("%s/../setup.py" %root) as fin:
        lines = fin.readlines()

    for key, keyword in keywords:
        keyword = keyword.strip()
        try:
            badges[key] = [line.strip() for line in lines
                           if line.strip().startswith(keyword)]
            badges[key] = badges[key][-1]
        except IndexError:
            raise RuntimeError("Cannot find 'keyword' %s" %keyword)
        _ignor = [keyword]
        _ignor.extend(ignore_chars)
        for string in _ignor:
            badges[key] = badges[key].replace(string, "").strip()

    keywords = zip(["python", 'status'],
                   ["Programming Language :: Python", "Development Status"])
    for key, keyword in keywords:
        keyword = keyword.strip()
        badges[key] = [line.strip().split(keyword)[-1] for line in lines
                       if keyword in line.strip()]
        _ignor = [keyword]
        _ignor.extend(ignore_chars)
        for string in _ignor:
            badges[key] = [line.replace(string, "").strip()
                           for line in badges[key]]
    badges['python'] = '|'.join(badges['python'])
    badges['status'] = badges['status'][-1].split("-")[-1].strip().lower()
    return badges

def update_badges():
    """Create badges for pyhip package"""
    root = os.path.abspath(inspect.getfile(inspect.currentframe()))
    root = os.path.join(os.path.dirname(root), '_badges')

    badges = _query_badges_values()
    colors = dict()
    colors["python"] = '#107dc8'
    colors["license"] = "yellow"
    colors["pypi package"] = "green"
    for key in badges:
        if key != "status":
            badge = Badge(key, badges[key], default_color=colors[key])
        else:
            thresholds = {"pre-alpha": 'red',
                          "alpha": 'orange',
                          "beta": 'yellow',
                          "production/stable": 'green'}
            badge = Badge(key, badges[key], thresholds=thresholds)
        fname = "%s/%s.svg" %(root, key.replace(' ', "_"))
        badge.write_badge(fname, overwrite=True)


def _get_version():
    version = ""
    release = ''

    with open('../setup.py', "r") as fin:
        for line in fin.readlines():
            if all([key in line for key in ["VERSION", "=", "."]]):
                ver = line.split('=')[-1].replace('"', '').replace("'", "").strip()
                ver_split = [key for key in ver.split('.') if key]
                if len(ver_split) >= 3:
                    release = ".".join(ver.split('.')[:3])
                    version = ".".join(ver.split('.')[:2])
                elif len(ver_split) == 2:
                    release = "%s.0" %ver
                    version = ver
                elif len(ver_split) == 1:
                    release = "%s.0.0" %ver.replace('.', '')
                    version = "%s.0" %ver.replace('.', '')
                break
    return release, version
# -- Path setup --------------------------------------------------------------
import os
import sys
import sphinx_rtd_theme
sys.path.insert(0, os.path.abspath('../pyhip/'))


# -- Project information -----------------------------------------------------

project = 'PyHip'
copyright = '2019, Jens-Dominik Mueller and CERFACS'
author = 'Jens-Dominik Mueller and CERFACS'

release, version = _get_version()

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.coverage',
    'sphinx.ext.viewcode',
    "sphinx_rtd_theme"
]

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'


# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_title = 'PyHip Documentation'
html_short_title = 'PyHip Documentation'

html_logo = "./_logo/PyHip_logo.svg"
html_favicon = "./_logo/PyHip_favicon.ico"
html_show_sourcelink = False

html_theme_options = {}

html_static_path = ['_static']

html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

htmlhelp_basename = 'PyHipdoc'


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_documents = [
    (master_doc, 'PyHip.tex', 'PyHip Documentation',
     'Jens-Dominik Mueller and CERFACS', 'manual'),
]


# -- Options for manual page output ------------------------------------------

man_pages = [
    (master_doc, 'pyhip', 'PyHip Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [
    (master_doc, 'PyHip', 'PyHip Documentation',
     author, 'PyHip', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------
update_badges()