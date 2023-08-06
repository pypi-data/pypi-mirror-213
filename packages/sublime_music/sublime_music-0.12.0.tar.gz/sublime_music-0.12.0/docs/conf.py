# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

# -- Project information -----------------------------------------------------

import datetime
import importlib.util
from pathlib import Path

project = "Sublime Music"
copyright = f"{datetime.datetime.today().year}, Sumner Evans"
author = "Sumner Evans"
github_url = "https://github.com/sublime-music/sublime-music/"

# Get the version from the package.
module_name = "sublime_music"
init_file = Path(__file__).parent.parent.joinpath("sublime_music/__init__.py").resolve()
spec = importlib.util.spec_from_file_location(module_name, str(init_file))
sublime_music = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sublime_music)

version = release = f"v{sublime_music.__version__}"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.intersphinx",
    "sphinx.ext.mathjax",
    "sphinx.ext.viewcode",
]

autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
    "special-members": "__init__",
}
autodoc_typehints = "description"

autosectionlabel_prefix_document = True
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "gtk": ("https://lazka.github.io/pgi-docs/Gtk-3.0/", None),
}

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The master toctree document.
master_doc = "index"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_logo = "../logo/logo.png"
html_theme_options = {
    "logo_only": True,
}

# Edit on GitHub integration
html_context = {
    "display_github": True,
    "github_user": "sublime-music",
    "github_repo": "sublime-music",
    "github_version": "master",
    "conf_py_path": "/docs/",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for manual page output ---------------------------------------

man_pages = [
    (
        "manpages/sublime-music",
        "sublime-music",
        "native GTK *sonic client",
        "Louis-Philippe Véronneau",
        1,
    )
]
