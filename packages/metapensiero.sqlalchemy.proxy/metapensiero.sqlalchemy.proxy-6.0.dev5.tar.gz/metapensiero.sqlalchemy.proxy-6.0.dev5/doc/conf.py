# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.proxy -- Sphinx configuration
# :Created:   ven 30 dic 2016 18:41:24 CET
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2016, 2017, 2022 Lele Gaifax
#

from __future__ import unicode_literals

from io import open
import os
import sys

from tomli import load


sys.path.insert(0, os.path.abspath('../src'))


# -- General configuration ------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
]

master_doc = 'index'

project = 'metapensiero.sqlalchemy.proxy'
copyright = '2009—2022, Lele Gaifax'
author = 'Lele Gaifax'

with open('../pyproject.toml', 'rb') as f:
    version = release = load(f)['project']['version']

language = 'en'

exclude_patterns = ['_build']

pygments_style = 'sphinx'


# -- Options for HTML output ----------------------------------------------

html_theme = 'haiku'
html_show_sourcelink = False
html_copy_source = False
