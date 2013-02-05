"""Routines for creating sub-elements of the VOEvent tree,
and a few other helper classes."""
#Tim Staley, <timstaley337@gmail.com>, 2012

from __future__ import absolute_import
from collections import namedtuple
from lxml import objectify, etree


Position2D = namedtuple('Position2D', 'ra dec err units system')
""""A namedtuple for simple representation of a 2D position as described
by the VOEvent spec."""

####################################
#A few small 'classes' - really just wrapper functions about
# element creation routines.
def Param(name, value=None, unit=None, ucd=None, dataType=None,
                utype=None):
    """Creates an element representing a Param

      NB name is not mandated by schema, but *is* mandated in full spec.

      **Args:**
       - value: A string, int, or float.
         This is converted to a string for storage.
       - unit: string, e.g. 'deg' for degrees.
       - ucd: string denoting `unified content descriptor
         <http://arxiv.org/abs/1110.0525>`_.
         For a list of valid UCDs, see  http://vocabularies.referata.com/wiki/Category:IVOA_UCD.
       - dataType: String denoting type of ``value`` - ``string``, ``int`` or ``float``.
    """
    #We use locals() to allow concise looping over the arguments.
    atts = locals()
    for k in atts.keys():
        if atts[k] is None:
            del atts[k]
    if 'value' in atts and type(value) != str:
        atts['value'] = repr(atts['value'])
    return objectify.Element('Param', attrib=atts)

def Group(params, name=None, type=None):
    """Creates an element representing a group of Params.

    """
    atts = {}
    if name:
        atts['name'] = name
    if type:
        atts['type'] = type
    g = objectify.Element('Group', attrib=atts)
    for p in params:
        g.append(p)
    return g

def Reference(uri, meaning=None):
    """Foolproof wrapper function to create a 'Reference' element"""
    attrib = {'uri': uri}
    if meaning is not None:
        attrib['meaning'] = meaning
    return objectify.Element('Reference', attrib)

def Inference(probability=None, relation=None, name=None, concept=None):
    """Create an inference element.

    NB VOEvent spec allows for multiple name / concepts per Inference,
    but I have implemented the simpler case of one each for now -
    I expect this will be sufficient for most purposes.
    """
    atts = {}
    if probability is not None:
        atts['probability'] = str(probability)
    if relation is not None:
        atts['relation'] = relation
    inf = objectify.Element('Inference', attrib=atts)
    if name is not None:
        inf.Name = name
    if concept is not None:
        inf.Concept = concept
    return inf