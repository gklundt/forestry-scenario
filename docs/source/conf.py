# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Forestry Scenario'
copyright = '2023, Gordon Klundt'
author = 'Gordon Klundt'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    'sphinxcontrib.plantuml',
    'sphinxcontrib.openapi',
    'sphinxcontrib.httpdomain',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# -- Options for PlantUML Output ---------------------------------------------
plantuml_path = os.environ.get("PLANTUML_PATH")
plantuml = f'java -jar {plantuml_path}'

# -- Options for Myst Parser -------------------------------------------------
# https://myst-parser.readthedocs.io/en/latest/configuration.html#global-configuration

myst_gfm_only = True
myst_title_to_header = True
