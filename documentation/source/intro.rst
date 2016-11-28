.. _intro:

Introduction
============

What is voevent-parse?
----------------------
A lightweight library for parsing, manipulating, and generating
VOEvent_ XML packets,
built atop  `lxml.objectify`_ and compatible with Python 2 and 3.

voevent-parse provides convenience routines to take care of many
common tasks, so that accessing those vital data elements is as simple as::

    import voeventparse
    with open(xml_filename, 'rb') as f:
        v = voeventparse.load(f)
    print "AuthorIVORN:", v.Who.AuthorIVORN  #Prints e.g. ivo://nasa.gsfc.tan/gcn
    v.Who.AuthorIVORN = 'ivo://i.heart.python/lxml' #Alters the XML value.


Rationale
---------
voevent-parse aims to make dealing with VOEvent packets easy, while remaining
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
voevent-parse is pip_ installable, try running::

    pip install voevent-parse

Note that voevent-parse depends upon lxml_, and pip will attempt to install lxml
first if not already present. lxml may be installed as a system package
if the version distributed with your package manager is sufficiently up-to-date
(version >= 2.3).
If you're working with pip / virtualenv_ and not making use of system packages,
then note that lxml has some prerequisites for compilation that can cause a
standard ``pip install``
to fail with somewhat cryptic errors.
On a typical Debian / Ubuntu machine you can satisfy those requirements using::

    sudo apt-get install libxml2-dev libxslt-dev



Documentation
-------------
Reference documentation can be found at
http://voevent-parse.readthedocs.org,
or generated directly from the repository using Sphinx_.


Source, Issues, Development etc.
--------------------------------
I intend to mark any updates by bumping the version number accordingly.
That said, if you find yourself using voevent-parse in any serious context,
do drop me an email so I can keep you informed of any updates or critical bugs.

Bug reports (or even better, pull requests) are welcomed.
The source code and issue tracker may be found at
https://github.com/timstaley/voevent-parse.

voevent-parse also has a suite of unit-tests which may be run in the usual
manner, typically using nose_ from the repository root directory.


lxml.objectify 'gotchas'
------------------------

.. note::
    See also the `tutorial <https://github.com/timstaley/voevent-parse-tutorial>`_,
    which includes a basic introduction to lxml.objectify.

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

Another 'gotcha' is that *creating* multiple child elements of the same
name is a bit unintuitive. Essentially, ``objectify`` works implicitly
if each element has only one child::

    from lxml import objectify, etree
    simple_root = objectify.Element('simple_root')
    simple_root.layer1 = None
    simple_root.layer1.layer2 = 5
    print etree.tostring(simple_root, pretty_print=True)

But if there are multiple children then each child must be explicitly declared
as an lxml ``Element`` in order to co-exist with its siblings::

    from lxml import objectify, etree
    import math
    siblings_root = objectify.Element('siblings')
    siblings_root.bars = None
    siblings_root.bars.append(objectify.Element('bar'))
    siblings_root.bars.append(objectify.Element('bar'))
    siblings_root.bars.bar[0] = math.pi
    siblings_root.bars.bar[1] = 42
    print etree.tostring(siblings_root, pretty_print=True)

... which is another reason to use voevent-parse as a user-friendly interface
for common operations.

For some more examples, you might also try:
http://www.saltycrane.com/blog/2011/07/example-parsing-xml-lxml-objectify/.


See also
--------

Brokers
~~~~~~~
In order to receive VOEvent packets, you will require a utility capable of
connecting to the VOEvent backbone. Two such tools are
`Comet <http://comet.transientskp.org/>`_ and
`Dakota <http://voevent.dc3.com/>`_.

Associated utility routines
~~~~~~~~~~~~~~~~~~~~~~~~~~~
Depending on what you want to use your VOEvents for, you may be interested
`fourpiskytools <https://github.com/4pisky/fourpiskytools>`_, which provides
a minimum working example of a broker / event-handler setup,
and basic routines for submitting VOEvents to a broker for publication.

Experienced users may also want to take a look at
`fourpisky-core <https://github.com/4pisky/fourpisky-core>`_, which is much less
easy-to-read but provides extensive examples of handling VOEvent data for
real-time alerting purposes.

Further information
~~~~~~~~~~~~~~~~~~~
The 4PiSky project page at https://4pisky.org/voevents/ provides links to more
information on using VOEvents for scientific work, and other VOEvent related
tools.

Acknowledgement
---------------
If you make use of voevent-parse in work leading to a publication, we ask
that you cite the `ASCL entry <http://ascl.net/1411.003>`_.



.. _VOEvent: http://voevent.readthedocs.org/
.. _lxml: http://lxml.de/installation.html
.. _lxml.objectify: http://lxml.de/objectify.html
.. _Sphinx: http://sphinx-doc.org/
.. _pip: https://pip.readthedocs.org/en/latest/
.. _virtualenv: http://virtualenv.readthedocs.org/en/latest/virtualenv.html
.. _nose: https://nose.readthedocs.org/en/latest/