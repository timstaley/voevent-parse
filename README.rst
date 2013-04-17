=============
voevent-parse
=============

A bare-bones, lightweight library for parsing, manipulating, and generating 
`VOEvent <http://wiki.ivoa.net/twiki/bin/view/IVOA/IvoaVOEvent>`_ XML packets.

**Update: I've now designated a version 0.1.0 and uploaded to PyPI.** You can install this using:

``pip install voevent-parse``.

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

API reference docs
------------------
While currently quite minimal, these can be found at 
http://voevent-parse.readthedocs.org,  
or can be built from the source if you prefer the traditional python docs 
colour-scheme. 
 
