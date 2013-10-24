=======================
:mod:`voeparse` Package
=======================

A package for elegant and concise manipulation of VOEvent XML packets.

.. warning::
   Much of the content within assumes the reader has at least a summary 
   understanding of the
   `VOEvent <http://en.wikipedia.org/wiki/VOEvent>`_ 
   `specifications <http://www.ivoa.net/Documents/VOEvent/>`_. 

.. hint:: 

   Currently, we import all the sub-package module members to ``voeparse.*``,
   for brevity (see ``voeparse/__init__.py``).
   

:mod:`.voevent` - Basic VOEvent packet manipulation
---------------------------------------------------

.. automodule:: voeparse.voevent
    :members: 
    :undoc-members:


:mod:`.misc` - Sub-elements and other helpers
---------------------------------------------

.. automodule:: voeparse.misc
    :members:
    :undoc-members:

      
:mod:`.convenience` - Convenience routines
------------------------------------------

.. automodule:: voeparse.convenience
    :members:
    :undoc-members:

:mod:`.definitions`
-------------------

.. automodule:: voeparse.definitions
   :members:
   :undoc-members:
   :exclude-members: v2_0_schema_str, v2_0_skeleton_str



