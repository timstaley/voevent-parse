=======================
:mod:`voeparse` Package
=======================

.. hint:: 

   Currently, we import all the sub-module members to ``voeparse.*``,
   for brevity (see ``__init__.py``).
   

:mod:`voeparse` - top level convenience routines
------------------------------------------------

.. automodule:: voeparse
    :members:
    :undoc-members:


:mod:`.voevent` - VOEvent packet manipulation
---------------------------------------------

.. automodule:: voeparse.voevent
    :members: 
    :undoc-members:


:mod:`.misc` - Sub-Elements and other helpers
---------------------------------------------

.. automodule:: voeparse.misc
    :members:
    :undoc-members:
    :show-inheritance:
    :exclude-members: Position2D
    
    .. autoclass:: Position2D
    
      A ``namedtuple`` used to collect together attributes of the commonly used
      *Position2D* element type.

:mod:`.definitions`
-------------------

.. automodule:: voeparse.definitions
   :members:
   :undoc-members:
   :exclude-members: v2_0_schema_str, v2_0_skeleton_str



