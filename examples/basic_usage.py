#!/usr/bin/python
"""A quick usage example. 

Once voeventparse is installed, this should tell you most of what you need to know
in order to start doing things with VOEvent packets.

The attributes are built from the structure of the XML file, 
so the best way to understand where the variable names come from is to simply 
open the XML packet in your favourite web browser and dig around.

See also:
* lxml documentation at http://lxml.de/objectify.html
* VOEvent standard at http://www.ivoa.net/documents/VOEvent/
* VOEvent schema file at http://www.ivoa.net/xml/VOEvent/VOEvent-v2.0.xsd
"""
import copy
import voeventparse
from voeventparse.tests.resources.datapaths import swift_bat_grb_pos_v2

with open(swift_bat_grb_pos_v2) as f:
    v = voeventparse.load(f)

#Basic attribute access
print "Ivorn:", v.attrib['ivorn']
print "Role:", v.attrib['role']
print "AuthorIVORN:", v.Who.AuthorIVORN
print "Short name:", v.Who.Author.shortName
print "Contact:", v.Who.Author.contactEmail

#Copying by value, and validation:
print "Original valid as v2.0? ", voeventparse.valid_as_v2_0(v)
v_copy = copy.copy(v)
print "Copy valid? ", voeventparse.valid_as_v2_0(v_copy)

#Changing values:
v_copy.Who.Author.shortName = 'BillyBob'
v_copy.attrib['role'] = voeventparse.definitions.roles.test
print "Changes valid? ", voeventparse.valid_as_v2_0(v_copy)

v_copy.attrib['role'] = 'flying circus'
print "How about now? ", voeventparse.valid_as_v2_0(v_copy)
print "But the original is ok, because we copied? ", voeventparse.valid_as_v2_0(v)

v.Who.BadPath = "This new attribute certainly won't conform with the schema."
assert voeventparse.valid_as_v2_0(v) == False
del v.Who.BadPath
assert voeventparse.valid_as_v2_0(v) == True
#######################################################
# And now, SCIENCE
#######################################################
c = voeventparse.pull_astro_coords(v)
print "Coords:", c
