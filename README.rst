=============
voevent-parse
=============

A bare-bones, lightweight library for parsing, manipulating, and generating 
`VOEvent <http://wiki.ivoa.net/twiki/bin/view/IVOA/IvoaVOEvent>`_ XML packets.

**voevent-parse is available via PyPI.** 
See below for details on installation.


Rationale
---------
The python library `lxml.objectify <http://lxml.de/objectify.html>`_ 
provides very elegant, 
attribute-style access to data stored in XML packets. 
However, dealing with the vagaries of its namespace handling requires 
some careful reading of the documentation. 
This library takes care of the details for you, 
so that accessing those vital data elements is as simple as:: 

  v = voeparse.load(xml_filename)
  print "AuthorIVORN:", v.Who.AuthorIVORN   #Prints ivo://nasa.gsfc.tan/gcn
  v.Who.AuthorIVORN = 'ivo://i.heart.python/lxml' #Alters the XML value.

It also provides convenience routines for common data access tasks, 
saving you the hassle of typing out very long attribute chains and dealing 
with varying formats of VOEvent.

Installation
------------
Take your pick; options are:

- ``pip install voevent-parse``    
  (with a virtualenv, recommended)
- ``pip install voevent-parse --user``    
  (to install for current user only)
- Other development tricks e.g. symlink into ``~/.local/lib/python2.7/site-packages``.

If you're working with pip/virtualenv, then note that lxml has some 
prerequisites for compilation that can cause a standard ``pip install`` 
to fail with somewhat cryptic errors.
On Ubuntu you can satisfy those requirements using::

	apt-get install libxml2-dev libxslt-dev

I intend to mark any updates by bumping the version number accordingly.
That said, if you find yourself using voevent-parse in any serious context,
do drop me an email so I can keep you informed of any updates or bugs.


API reference docs
------------------
While currently quite minimal, these can be found at 
http://voevent-parse.readthedocs.org,  
or can be built from the source if you prefer the traditional python docs 
colour-scheme. 


lxml.objectify tips
-------------------
The objectify library has a few syntactic quirks which can trip up new users.
Firstly, you should be aware that the line ``root.foo`` actually returns 
an object that acts like a list of all the children  with the name 'foo'. 
What's confusing is that objectify has syntactic sugar applied so that 
``print root.foo`` is effectively identical to ``print root.foo[0]``.
Furthermore, this can confuse access to the actual leaf values, so you should 
be aware of the accessor to the text representation of the value; ``.text``, 
e.g.::
  
  >root = lxml.objectify.Element('root')
  >root.foo = 'sometext'
  >root.foo
  'sometext'
  >len(root.foo)
  1
  >#The string clearly does not have length==1 - it's the list.
  >root.foo.text
  'sometext'
  >print len(root.foo.text)
  8
  >#Ah, that's better!

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
 

