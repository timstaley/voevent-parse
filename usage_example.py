#!/usr/bin/python
"""A quick usage example. 

Once voeparse is installed, this should tell you most of what you need to know
in order to start doing things with VOEvent packets.

The attributes are built from the structure of the XML file, 
so the best way to understand where the variable names come from is to simply 
open the XML packet in your favourite web browser and dig around.

See also: the slightly terse documentation at http://lxml.de/objectify.html
"""
import copy
import voeparse

xml_filename = 'tests/resources/SWIFT_bat_position_v2.0_example.xml'

v = voeparse.load(xml_filename)

#Basic attribute access
print "Ivorn:", v.attrib['ivorn']
print "Role:", v.attrib['role']
print "AuthorIVORN:", v.Who.AuthorIVORN
print "Short name:", v.Who.Author.shortName
print "Contact:", v.Who.Author.contactEmail

#Copying by value, and validation:
print "Original valid as v2.0? ", voeparse.valid_as_v2_0(v)
v_copy = copy.copy(v)
print "Copy valid? ", voeparse.valid_as_v2_0(v_copy)

#Changing values:
v_copy.Who.Author.shortName = 'BillyBob'
v_copy.attrib['role'] = 'test'
print "Changes valid? ", voeparse.valid_as_v2_0(v_copy)

v_copy.attrib['role'] = 'flying circus'
print "How about now? ", voeparse.valid_as_v2_0(v_copy)
print "But the original is ok, because we copied? ", voeparse.valid_as_v2_0(v)

v.Who.BadPath = "This new child certainly won't conform with the schema."
assert voeparse.valid_as_v2_0(v) == False
del v.Who.BadPath
assert voeparse.valid_as_v2_0(v) == True
#######################################################
# And now, SCIENCE
#######################################################
c = voeparse.pull_astro_coords(v)
print "Coords:", c
