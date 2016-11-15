
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
copyright = u'2013-2016 Tim Staley'

# The short X.Y version.
version = voeventparse.__version__
# The full version, including alpha/beta/rc tags.
release = version

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = []

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# otherwise, readthedocs.org uses their theme by default, so no need to specify it

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
# Output file base name for HTML help builder.
htmlhelp_basename = 'VOEvent-parsedoc'



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
