.. VOEvent-parse documentation master file, created by
   sphinx-quickstart on Mon Jan 14 15:58:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

VOEvent-parse
=============
A lightweight library for parsing, manipulating, and generating
`VOEvent <http://wiki.ivoa.net/twiki/bin/view/IVOA/IvoaVOEvent>`_ XML packets,
built atop  `lxml.objectify`_.

VOEvent-parse provides convenience routines to take care of many
common tasks, so that accessing those vital data elements is as simple as::

    import voeparse
    with open(xml_filename) as f:
        v = voeparse.load(f)
    print "AuthorIVORN:", v.Who.AuthorIVORN  #Prints e.g. ivo://nasa.gsfc.tan/gcn
    v.Who.AuthorIVORN = 'ivo://i.heart.python/lxml' #Alters the XML value.

Rationale
---------
Voevent-parse aims to make dealing with VOEvent packets easy, while remaining
small, flexible, and stable enough to be suitable for use as a dependency in a
range of larger projects.
To achieve this, we add a user-friendly layer on top of
`lxml.objectify`_ which attempts to hide the messy details of working with the
sometimes lengthy VOEvent schema, and also take care of some rather obscure
lxml namespace handling.
However, since the objects created are just regular lxml classes, the user
is free to utilise the full power of the lxml library when required.


Installation
------------
Voevent-parse is pip_ installable, try running::

    pip install voevent-parse

Note that voevent-parse depends upon lxml_, and pip will attempt to install lxml
first if not already present. lxml may be installed as a system package
if the version distributed with your package manager is sufficiently up-to-date
(version >= 2.3).
If you're working with pip / virtualenv_ and not making use of system packages,
then note that lxml has some prerequisites for compilation that can cause a
standard ``pip install``
to fail with somewhat cryptic errors.
On Ubuntu you can satisfy those requirements using::

    apt-get install libxml2-dev libxslt-dev

I intend to mark any updates by bumping the version number accordingly.
That said, if you find yourself using voevent-parse in any serious context,
do drop me an email so I can keep you informed of any updates or bugs.


Documentation
-------------
Reference documentation can be found at
http://voevent-parse.readthedocs.org,
or generated directly from the repository using Sphinx_.

Source, Issues, Contributions
-----------------------------
Bug reports (or even better, pull requests) are welcomed. The source code and
issue tracker may be found at https://github.com/timstaley/voevent-parse.


lxml.objectify tips
-------------------
The objectify library has a few syntactic quirks which can trip up new users.
Firstly, you should be aware that the line ``root.foo`` actually returns
an object that acts like a *list* of all the children  of the ``root`` element
with the name `foo`.
What's confusing is that objectify has syntactic sugar applied so that
``root.foo`` is a shortcut alias for the more explicit
``root.foo[0]``.
This can be very confusing to the uninitiated, since it overrides some
attributes of the the actual element values. To get around this, you should
be aware of the accessor to the text representation of the value; ``.text``,
e.g.::

  import lxml.objectify
  root = lxml.objectify.Element('root')
  root.foo = 'sometext' # Adds a child called 'foo' with value 'sometext'
  print root.foo # 'sometext'
  print len(root.foo) #  1. Wait, what?
  # The string value clearly does not have length==1,
  # the list of children called 'foo' does.
  print root.foo.text # 'sometext'
  print len(root.foo.text) # 8. Sanity prevails!

For some more examples, you might also try:
http://www.saltycrane.com/blog/2011/07/example-parsing-xml-lxml-objectify/.


See also
--------

Alternative parsing libraries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
voevent-parse was preceded by
`VOEventLib <http://lib.skyalert.org/VOEventLib/>`_, which has similar aims
but a different stylistic approach
(see http://lib.skyalert.org/VOEventLib/VOEventLib/doc/index.html ).

Brokers
~~~~~~~
In order to receive VOEvent packets, you will require a utility capable of
connecting to the VOEvent backbone. Two such tools are
`Comet <http://comet.transientskp.org/>`_ and
`Dakota <http://voevent.dc3.com/>`_.

Associated utility routines
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Depending on what you want to use your VOEvents for, you may be interested
in `pysovo <https://github.com/timstaley/pysovo>`_,
a collection of routines for dealing with VOEvents and
responding to them accordingly.


Reference material
------------------

.. toctree::
    :maxdepth: 2

    examples
    reference


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _lxml: http://lxml.de/installation.html
.. _lxml.objectify: http://lxml.de/objectify.html
.. _Sphinx: http://sphinx-doc.org/
.. _pip: https://pip.readthedocs.org/en/latest/
.. _virtualenv: http://virtualenv.readthedocs.org/en/latest/virtualenv.html