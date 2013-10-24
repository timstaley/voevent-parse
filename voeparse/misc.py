"""Routines for creating sub-elements of the VOEvent tree,
and a few other helper classes."""
#Tim Staley, <timstaley337@gmail.com>, 2012

from __future__ import absolute_import
from collections import namedtuple
import datetime
from lxml import objectify, etree


class Position2D(namedtuple('Position2D', 'ra dec err units system')):
    """"A namedtuple for simple representation of a 2D position as described
    by the VOEvent spec.

    **Args**:
     - ra
     - dec
     - err
     - units
     - system
    """

_datatypes_autoconversion = {
         bool:('string', lambda b: str(b)),
         int: ('int', lambda i: str(i)),
         float: ('float', lambda f: str(f)),
         datetime.datetime: ('string', lambda dt: dt.isoformat()),
         }

def Param(name, value=None, unit=None, ucd=None, dataType=None, utype=None,
          ac=True):
    """Create a Param element.

      NB name is not mandated by schema, but *is* mandated in full spec.

      **Args:**
       - value: A string representing your value. Or, if ``ac=True``, can also
         be an instance of one of the following:

          - ``bool``
          - ``int``
          - ``float``
          - ``datetime``

         Always stored as a string representation, as per VO spec.
       - unit: string e.g. 'deg' for degrees.
       - ucd: string denoting `unified content descriptor
         <http://arxiv.org/abs/1110.0525>`_.
         For a list of valid UCDs, see:
         http://vocabularies.referata.com/wiki/Category:IVOA_UCD.
       - dataType: String denoting type of ``value``; restricted to 3 options:
         ``string`` (default), ``int`` , or ``float``.
         (NB *not* to be confused with standard XML Datatypes, which have many
         more possible values.)
       - utype: string. See http://wiki.ivoa.net/twiki/bin/view/IVOA/Utypes
       - ac: bool. Attempt automatic conversion of passed value to
         string, and set ``dataType`` accordingly (only attempted
         if dataType is the default, i.e. None).
         (NB only supports types listed in _datatypes_autoconversion dict)
    """
    #We use locals() to allow concise looping over the arguments.
    atts = locals()
    atts.pop('ac')
    for k in atts.keys():
        if atts[k] is None:
            del atts[k]
    if (ac
        and value is not None
        and (not isinstance(value, basestring))
        and dataType is None
        ):
        if type(value) in _datatypes_autoconversion:
            datatype, func = _datatypes_autoconversion[type(value)]
            atts['dataType'] = datatype
            atts['value'] = func(value)
    return objectify.Element('Param', attrib=atts)

def Group(params, name=None, type=None):
    """Create an element representing a group of Params.

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
    """Create a 'Reference' element"""
    attrib = {'uri': uri}
    if meaning is not None:
        attrib['meaning'] = meaning
    return objectify.Element('Reference', attrib)

def Inference(probability=None, relation=None, name=None, concept=None):
    """Create an Inference element.

    **Args**:
      - probability: float of value 0.0 to 1.0.
      - relation: string, e.g. 'associated' (see VOEvent spec).
      - name: string
      - concept: string, one of a
        'formal UCD-like vocabulary of astronomical concepts' - see VOEvent spec.
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

def Citation(ivorn, cite_type):
    """Create a Citation element.

    **Args**:
     - ivorn: string. It is assumed this will be copied verbatim from elsewhere,
       and so these should have any prefix (e.g. 'ivo://','http://') already
       in place - the function will not alter the value.
     - cite_type: String. Should be one of the pre-defined
       :py:class:`.definitions.cite_types`.
    """
    # This is an ugly hack around the limitations of the  lxml.objectify API:
    c = objectify.StringElement(cite=cite_type)
    c._setText(ivorn)
    c.tag = "EventIVORN"
    return c

