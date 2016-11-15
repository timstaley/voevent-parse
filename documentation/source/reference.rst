.. _api:

voevent-parse API reference
===========================

.. warning::
   Much of the content within assumes the reader has at least a summary
   understanding of the
   `VOEvent <http://en.wikipedia.org/wiki/VOEvent>`_
   `specifications <http://www.ivoa.net/Documents/VOEvent/>`_.

.. note::
    The top-level ``__init__.py`` file `imports key classes and subroutines
    <imports_>`_
    into the top-level ``voeventparse`` namespace, for brevity.


:mod:`voeventparse.voevent` - Basic VOEvent packet manipulation
---------------------------------------------------------------

.. automodule:: voeventparse.voevent
    :members: 
    :undoc-members:


:mod:`voeventparse.misc` - Subtree-elements and other helpers
-------------------------------------------------------------

.. automodule:: voeventparse.misc
    :members:
    :undoc-members:

      
:mod:`voeventparse.convenience` - Convenience routines
------------------------------------------------------

.. automodule:: voeventparse.convenience
    :members:
    :undoc-members:

:mod:`voeventparse.definitions` - Standard or common string values
------------------------------------------------------------------

.. automodule:: voeventparse.definitions
   :members:
   :undoc-members:
   :exclude-members: v2_0_schema_str, v2_0_skeleton_str



.. _imports: https://github.com/timstaley/voevent-parse/blob/master/src/voeventparse/__init__.py