===============
voevent-parse
===============

A bare-bones, lightweight library for parsing, manipulating, and generating 
`VOEvent <http://wiki.ivoa.net/twiki/bin/view/IVOA/IvoaVOEvent>`_ XML packets.

(Note: Still under active development. The current feature set is limited,
but growing - and easy to add to if, you'd like to get involved.
Update: As of 28/12/12 subroutines for easy creation of all major elements 
are in place.)

Rationale
---------------
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


Prerequisites
---------------

- `lxml <http://lxml.de/>`_ (version >= 2.3).  
  For recent Ubuntu versions this is as simple as ``sudo apt-get install python-lxml`` - 
  check the version number though! 
  Otherwise, you might try ``pip install lxml --upgrade`` or something similar.

Installation
-------------
At this stage, I'm assuming that only developers will want to install the 
package. In which case, I recommend ``python setup.py develop --user``,
which effectively adds the checked out copy of the code to your python path
via symlinks. 
To uninstall after using this method, simply:
``rm ~/.local/lib/python2.7/site-packages/voevent-parse.egg-link``.

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

For some more examples, you might also try `here 
<http://www.saltycrane.com/blog/2011/07/example-parsing-xml-lxml-objectify/>`_. 
 
