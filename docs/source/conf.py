# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute.

import os
import sys
sys.path.insert(0, os.path.abspath('../../src/'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'MetPyRad'
copyright = '2025, Xandra Campo'
author = 'Xandra Campo'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.napoleon', 'sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx_design']

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_title = f'{project} {release}'
html_theme_options = {
    "show_nav_level": 2,
    "icon_links": [
        {
            "name": "GitHub",  # Label for this link
            "url": "https://github.com/lmri-met/metpyrad>",  # URL where the link will redirect
            "icon": "fa-brands fa-github",  # Icon class (if "type": "fontawesome"), or path to local image (if "type": "local")
            "type": "fontawesome",  # The type of image to be used (see below for details)
        }
   ]
}