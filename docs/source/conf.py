# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../../search'))
sys.path.insert(0, os.path.abspath('../../maze'))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'search module'
copyright = '2024, javrui'
author = 'javrui'
release = '1.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',       # Automatically document Python modules
    'sphinx.ext.autosummary',   # Generate summary tables for modules
    'sphinx.ext.napoleon',      # Parse Google/NumPy-style docstrings
    'sphinx_autodoc_typehints', # Add type hints to documentation
    'sphinx.ext.viewcode',      # Optional: Adds source code links
    'sphinxcontrib.video',      # Add video support (pip install sphinxcontrib-video)
    'myst_parser',              # Support Markdown files

]

templates_path = ['_templates']
exclude_patterns = []
source_suffix = ['.rst', '.md']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    "collapse_navigation": False,  # Keep the sidebar expanded
    "navigation_depth": 4,     # Show up to 4 levels in the sidebar
    "sticky_navigation": True,     # Keep the sidebar visible while scrolling
}
html_static_path = ['_static']


# This disables the module index in the HTML output.
html_use_modindex = False


# Autodoc settings
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'show-inheritance': True,
}

autosummary_generate = True  # Enable autosummary
napoleon_google_docstring = True  # Parse Google-style docstrings

# Configure autodoc:
autodoc_member_order = 'bysource'  # Order by appearance in code
autodoc_typehints = 'description'  # Include type hints in descriptions




# Napoleon settings
napoleon_google_docstring = True  # Enable parsing of Google-style docstrings
napoleon_numpy_docstring = False  # Disable NumPy-style docstrings (optional)
napoleon_include_init_with_doc = True  # Include `__init__` docstrings
napoleon_include_private_with_doc = False  # Exclude private members
napoleon_use_param = True  # Use `:param` for parameters in the output
napoleon_use_rtype = True  # Use `:rtype` for return types
napoleon_preprocess_types = True  # Preprocess type hints for better formatting
