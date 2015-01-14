"""Routines for creating sub-elements of the VOEvent tree,
and a few other helper classes."""

from __future__ import absolute_import
from six import string_types
from collections import namedtuple
import datetime
from lxml import objectify, etree


class Position2D(namedtuple('Position2D', 'ra dec err units system')):
    """A namedtuple for simple representation of a 2D position as described
    by the VOEvent spec.

    Args:
        ra (float): Right ascension.
        dec (float): Declination
        err (float): Error radius.
        units (:class:`.definitions.coord_units`): Coordinate units
            e.g. degrees, radians.
        system (:class:`.definitions.sky_coord_system`): Co-ordinate system
            e.g. UTC-FK5-GEO
    """
    pass  # Just wrapping a namedtuple so we can assign a docstring.


_datatypes_autoconversion = {
    bool: ('string', lambda b: str(b)),
    int: ('int', lambda i: str(i)),
    float: ('float', lambda f: str(f)),
    datetime.datetime: ('string', lambda dt: dt.isoformat()),
}


def Param(name, value=None, unit=None, ucd=None, dataType=None, utype=None,
          ac=True):
    """
    'Parameter', used as a general purpose key-value entry in the 'What' section.

    May be assembled into a :class:`Group`.

    NB ``name`` is not mandated by schema, but *is* mandated in full spec.

    Args:
        value(string): String representing parameter value.
            Or, if ``ac`` is true, then 'autoconversion' is attempted, in which case
            ``value`` can also be an instance of one of the following:

             * :py:obj:`bool`
             * :py:obj:`int`
             * :py:obj:`float`
             * :py:class:`datetime.datetime`

            This allows you to create Params without littering your code
            with string casts, or worrying if the passed value is a float or a
            string, etc.
            NB the value is always *stored* as a string representation,
            as per VO spec.
        unit(string): e.g. 'deg' for degrees.
        ucd(string): `unified content descriptor <http://arxiv.org/abs/1110.0525>`_.
            For a list of valid UCDs, see:
            http://vocabularies.referata.com/wiki/Category:IVOA_UCD.
        dataType(string): Denotes type of ``value``; restricted to 3 options:
            ``string`` (default), ``int`` , or ``float``.
            (NB *not* to be confused with standard XML Datatypes, which have many
            more possible values.)
        utype(string): See http://wiki.ivoa.net/twiki/bin/view/IVOA/Utypes
        ac(bool): Attempt automatic conversion of passed ``value`` to string,
            and set ``dataType`` accordingly (only attempted if ``dataType``
            is the default, i.e. ``None``).
            (NB only supports types listed in _datatypes_autoconversion dict)

    """
    # We use locals() to allow concise looping over the arguments.
    atts = locals()
    atts.pop('ac')
    temp_dict={}
    temp_dict.update(atts)
    for k in temp_dict.keys():
        if atts[k] is None:
            del atts[k]
    if (ac
        and value is not None
        and (not isinstance(value, string_types))
        and dataType is None
    ):
        if type(value) in _datatypes_autoconversion:
            datatype, func = _datatypes_autoconversion[type(value)]
            atts['dataType'] = datatype
            atts['value'] = func(value)
    return objectify.Element('Param', attrib=atts)


def Group(params, name=None, type=None):
    """Groups together Params for adding under the 'What' section.

    Args:
        params(list of :func:`Param`): Parameter elements to go in this group.
        name(string): Group name. NB ``None`` is valid, since the group may be
            best identified by its type.
        type(string): Type of group, e.g. 'complex' (for real and imaginary).
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
    """
    Represents external information, typically original obs data and metadata.

    Args:
        uri(string): Uniform resource identifier for external data, e.g. FITS file.
        meaning(string): The nature of the document referenced, e.g. what
            instrument and filter was used to create the data?
    """
    attrib = {'uri': uri}
    if meaning is not None:
        attrib['meaning'] = meaning
    return objectify.Element('Reference', attrib)


def Inference(probability=None, relation=None, name=None, concept=None):
    """Represents a probable cause / relation between this event and some prior.

    Args:
        probability(float): Value 0.0 to 1.0.
        relation(string): e.g. 'associated' or 'identified' (see Voevent spec)
        name(string): e.g. name of identified progenitor.
        concept(string): One of a 'formal UCD-like vocabulary of astronomical
            concepts', e.g. http://ivoat.ivoa.net/stars.supernova.Ia - see
            VOEvent spec.
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
    """Used to cite earlier VOEvents.

    Args:
        ivorn(string): It is assumed this will be copied verbatim from elsewhere,
            and so these should have any prefix (e.g. 'ivo://','http://')
            already in place - the function will not alter the value.
        cite_type (:class:`.definitions.cite_types`): String conforming to one
            of the standard citation types.

    """
    # This is an ugly hack around the limitations of the  lxml.objectify API:
    c = objectify.StringElement(cite=cite_type)
    c._setText(ivorn)
    c.tag = "EventIVORN"
    return c

