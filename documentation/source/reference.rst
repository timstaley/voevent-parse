.. _api:

===========================
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
    into the top-level ``voeparse`` namespace, for brevity.


:mod:`voeparse.voevent` - Basic VOEvent packet manipulation
-----------------------------------------------------------

.. automodule:: voeparse.voevent
    :members: 
    :undoc-members:


:mod:`voeparse.misc` - Sub-elements and other helpers
-----------------------------------------------------

.. automodule:: voeparse.misc
    :members:
    :undoc-members:

      
:mod:`voeparse.convenience` - Convenience routines
--------------------------------------------------

.. automodule:: voeparse.convenience
    :members:
    :undoc-members:

:mod:`voeparse.definitions` - Standard values as defined by VOEvent specification
---------------------------------------------------------------------------------

.. automodule:: voeparse.definitions
   :members:
   :undoc-members:
   :exclude-members: v2_0_schema_str, v2_0_skeleton_str



.. _imports: https://github.com/timstaley/voevent-parse/blob/master/voeparse/__init__.py#L17