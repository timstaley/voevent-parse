
import sys, os
import voeventparse

# -- General configuration -----------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.3'

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.intersphinx', 'sphinx.ext.todo',
               'sphinx.ext.coverage', 'sphinx.ext.viewcode',
               'sphinx.ext.napoleon']


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix of source filenames.
source_suffix = '.rst'


# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'voevent-parse'
copyright = u'2013,2014 Tim Staley'

# The short X.Y version.
version = voeventparse._nominal_version
# The full version, including alpha/beta/rc tags.
release = version

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'


# on_rtd is whether we are on readthedocs.org
import os
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if not on_rtd:  # only import and set the theme if we're building docs locally
    import sphinx_rtd_theme
    html_theme = 'sphinx_rtd_theme'
    html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# otherwise, readthedocs.org uses their theme by default, so no need to specify it

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# Output file base name for HTML help builder.
htmlhelp_basename = 'VOEvent-parsedoc'


# -- Options for LaTeX output --------------------------------------------------

latex_elements = {
# The paper size ('letterpaper' or 'a4paper').
#'papersize': 'letterpaper',

# The font size ('10pt', '11pt' or '12pt').
#'pointsize': '10pt',

# Additional stuff for the LaTeX preamble.
#'preamble': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
  ('index', 'VOEvent-parse.tex', u'VOEvent-parse Documentation',
   u'Tim Staley', 'manual'),
]


# -- Options for manual page output --------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ('index', 'voevent-parse', u'VOEvent-parse Documentation',
     [u'Tim Staley'], 1)
]

# If true, show URL addresses after external links.
#man_show_urls = False


# -- Options for Texinfo output ------------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
  ('index', 'VOEvent-parse', u'VOEvent-parse Documentation',
   u'Tim Staley', 'VOEvent-parse', 'One line description of project.',
   'Miscellaneous'),
]


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'http://docs.python.org/': None}

# -- Custom options ----------------------
autodoc_member_order = 'bysource'
todo_include_todos = True

nitpicky=True
nitpick_ignore = [
    ("py:obj", "lxml.etree.DocumentInvalid"),
    ("py:obj", "lxml.etree"),
    ("py:obj", "bytes"),

]
