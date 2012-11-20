===============
voevent-parse
===============

A bare-bones, lightweight library for parsing, manipulating, and generating 
`VOEvent <http://wiki.ivoa.net/twiki/bin/view/IVOA/IvoaVOEvent>`_ XML packets.


Rationale:
---------------
The python library `lxml.objectify <http://lxml.de/objectify.html>`_ provides very elegant, 
attribute-style access to data stored in XML packets. 
However, dealing with the vagaries of its namespace handling requires some careful reading of the documentation. 
This library takes care of the details for you, so that accessing those vital data elements is as simple as:: 

  v = voeparse.load(xml_filename)
  print "AuthorIVORN:", v.Who.AuthorIVORN   #Prints ivo://nasa.gsfc.tan/gcn
  v.Who.AuthorIVORN = 'ivo://i.heart.python/lxml' #Alters the XML value.

It also provides convenience routines for common data access tasks, 
saving you the hassle of typing out very long attribute chains.


Prerequisites:
---------------

- `lxml <http://lxml.de/>`_ (version >= 2.3).  
  For recent Ubuntu versions this is as simple as ``sudo apt-get install python-lxml`` - 
  check the version number though! 
  Otherwise, you might try ``pip install lxml --upgrade`` or something similar.
