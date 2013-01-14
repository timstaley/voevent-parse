"""Routines for handling etrees representing VOEvent packets."""

from __future__ import absolute_import
import lxml
from lxml import objectify, etree
from collections import Iterable
import types

import voeparse.definitions
voevent_v2_0_schema = etree.XMLSchema(
                        etree.fromstring(voeparse.definitions.v2_0_schema_str))


def Voevent(stream, stream_id, role):
    """Create an empty VOEvent packet with specified identifying properties.

    **Args:**
      - stream and stream_id: Strings, used to construct the IVORN:
        ``ivorn = 'ivo://' + stream + '#' + stream_id``
      - role: String conforming to VOEvent spec.
        (See also  :py:class:`.definitions.roles`)

    **Returns:**
     Instance of lxml.objectify.Element representing root-node of the VOEvent
     etree.
    """
    v = objectify.fromstring(voeparse.definitions.v2_0_skeleton_str)
    _remove_root_tag_prefix(v)
    v.attrib['ivorn'] = ''.join(('ivo://', stream, '#', stream_id))
    v.attrib['role'] = role
    #Presumably we'll always want the following children:
    #(NB, valid to then leave them empty)
    etree.SubElement(v, 'Who')
    etree.SubElement(v, 'What')
    etree.SubElement(v, 'WhereWhen')
    return v
####################################################
# And finally, lots of utility functions...

def loads(s, validate=False):
    """Load VOEvent from string.

    This parses a VOEvent XML packet string, taking care of some subtleties.

    Currently pretty basic, but we can imagine using this function to
    homogenise or at least identify different VOEvent versions, etc.
    """
#    .. note::
#
#        The namespace is removed from the root element tag to make
#        objectify access work as expected,
#        (see  :py:func:`._remove_root_tag_prefix`)
#        so we must re-insert it when we want to conform to schema.
    v = objectify.fromstring(s)
    _remove_root_tag_prefix(v)
    return v


def load(path):
    """Load VOEvent from file.

    See also: :py:func:`.loads`
    """
    s = open(path, 'rb').read()
    return loads(s)


def _remove_root_tag_prefix(v):
    """
    Removes 'voe' namespace prefix from root tag.

    When we load in a VOEvent, the root element has a tag prefixed by
     the VOE namespace, e.g. {http://www.ivoa.net/xml/VOEvent/v2.0}VOEvent
    Because objectify expects child elements to have the same namespace as
    their parent, this breaks the python-attribute style access mechanism.
    We can get around it without altering root, via e.g
     who = v['{}Who']

    Alternatively, we can temporarily ditch the namespace altogether.
    This makes access to elements easier, but requires care to reinsert
    the namespace upon output.

    I've gone for the latter option.
    """
    v.tag = v.tag.replace(''.join(('{', v.nsmap['voe'], '}')), '')
    # Now v.tag = '{}VOEvent'
    return


def _reinsert_root_tag_prefix(v):
    """
    Returns 'voe' namespace prefix to root tag.
    """
    v.tag = ''.join(('{', v.nsmap['voe'], '}VOEvent'))
    return

def _return_to_standard_xml(v):
    #Remove lxml.objectify DataType namespace prefixes:
    objectify.deannotate(v)
    #Put the default namespace back:
    _reinsert_root_tag_prefix(v)
    etree.cleanup_namespaces(v)

def dumps(voevent, validate=False, pretty_print=True, xml_declaration=True):
    """Converts voevent to string.

    .. note:: Encoding is UTF-8, in line with VOE2.0 schema.
        Declaring the encoding can cause diffs with the original loaded VOEvent,
        but I think it's probably the right thing to do.
    """
    _return_to_standard_xml(voevent)
    s = etree.tostring(voevent, pretty_print=pretty_print,
                       xml_declaration=xml_declaration,
                       encoding='UTF-8')
    _remove_root_tag_prefix(voevent)
    return s

def dump(voevent, file, validate=False, pretty_print=True, xml_declaration=True):
    """Dumps voevent to file."""
    file.write(dumps(voevent, validate, pretty_print, xml_declaration))

def valid_as_v2_0(voevent):
    """Tests if a voevent conforms to the schema.

    **Returns** a bool.
    """
    _return_to_standard_xml(voevent)
    valid_bool = voevent_v2_0_schema.validate(voevent)
    _remove_root_tag_prefix(voevent)
    return valid_bool

def assert_valid_as_v2_0(voevent):
    """Raises an :py:obj:`lxml.etree.DocumentInvalid` exception if voevent
    does not conform to schema.

    Especially useful for debugging,
    since the stack trace contains a reason for the invalidation.
    """
    _return_to_standard_xml(voevent)
    voevent_v2_0_schema.assertValid(voevent)
    _remove_root_tag_prefix(voevent)



def set_who(v, date=None, author_stream=None, description=None, reference=None):
    """For setting the basics of the Who component, e.g. AuthorIVORN.

    **Args**
      - v: Voevent instance to update.
      - date: A datetime object. Can be None if the voevent already
        has a date set. Microseconds are ignored, as per the VOEvent spec.
      - author_ivorn, description, reference: Should be strings.

    .. todo:: Implement description & reference parameters.

    """
    if author_stream is not None:
        v.Who.AuthorIVORN = ''.join(('ivo://', author_stream))
    if date is not None:
        v.Who.Date = date.replace(microsecond=0).isoformat()

def set_author(voevent, title=None, shortName=None, logoURL=None,
               contactName=None, contactEmail=None, contactPhone=None,
               contributor=None):
    """For adding author details.

    .. note:: Unusually for this library,
        the args here use CamelCase naming convention,
        since there's a direct mapping to the ``Author.*``
        attributes to which they will be assigned.
    """
    # We inspect all local variables except the voevent packet,
    # Cycling through and assigning them on the Who.Author element.
    AuthChildren = locals()
    AuthChildren.pop('voevent')
    if not voevent.xpath('Who/Author'):
        etree.SubElement(voevent.Who, 'Author')
    for k, v in AuthChildren.iteritems():
        if v is not None:
            voevent.Who.Author[k] = v




def set_where_when(voevent, coords, obs_time,
                   observatory_location):
    """Set up a basic WhereWhen for an observed sky position.

    **Args**:
         - voevent
         - coords: Should be instance of voeparse.Position2D
         - obs_time: Nominal DateTime of the observation.
         - observatory_location: Telescope locale, see VOEvent spec.

    .. todo:: Implement TimeError using datetime.timedelta
    """

    obs_data = etree.SubElement(voevent.WhereWhen, 'ObsDataLocation')
    etree.SubElement(obs_data, 'ObservatoryLocation', id=observatory_location)
    ol = etree.SubElement(obs_data, 'ObservationLocation')
    etree.SubElement(ol, 'AstroCoordSystem', id=coords.system)
    ac = etree.SubElement(ol, 'AstroCoords',
                          coord_system_id=coords.system)
    time = etree.SubElement(ac, 'Time', unit='s')
    instant = etree.SubElement(time, 'TimeInstant')
    instant.ISOTime = obs_time.isoformat()
#    iso_time = etree.SubElement(instant, 'ISOTime') = obs_time.isoformat()

    pos2d = etree.SubElement(ac, 'Position2D', unit=coords.units)
    pos2d.Name1 = 'RA'
    pos2d.Name2 = 'Dec'
    pos2d_val = etree.SubElement(pos2d, 'Value2')
    pos2d_val.C1 = coords.ra
    pos2d_val.C2 = coords.dec
    pos2d.Error2Radius = coords.err



def add_how(voevent, descriptions=None, references=None):
    """Add entries to the How section.

    **Args**:
      - voevent
      - descriptions: list of description strings.
      - references: list of :py:class:`.Reference` elements.
    """
    if not voevent.xpath('How'):
        etree.SubElement(voevent, 'How')
    if descriptions is not None:
        for desc in descriptions:
            #d = etree.SubElement(voevent.How, 'Description')
            #voevent.How.Description[voevent.How.index(d)] = desc
            ##Simpler:
            etree.SubElement(voevent.How, 'Description')
            voevent.How.Description[-1] = desc
    if references is not None:
        voevent.How.extend(references)

def add_why(voevent, importance=None, expires=None, inferences=None):
    """
    NB. importance / expires are 'Why' attributes, therefore setting them
    will overwrite previous values.
    On the other hand, inferences are appended to the list.

    **Args**:
      - voevent
      - importance: Float from 0.0 to 1.0
      - expires: Datetime. (See voevent spec).
      - inferences: list of Inference elements.
    """
    if not voevent.xpath('Why'):
        etree.SubElement(voevent, 'Why')
    if importance is not None:
        voevent.Why.attrib['importance'] = str(importance)
    if expires is not None:
        voevent.Why.attrib['expires'] = expires.replace(microsecond=0).isoformat()
    if inferences is not None:
        voevent.Why.extend(inferences)

def set_citations(voevent, ivorns, citation_type, description=None):
    """
    (Overwrites any previous citations set.)

    This is the logical behaviour, since there are carefully defined
    meanings associated with single or multiple EventIVORN references;
    see the VOEvent spec for details.

    **Args**:
      - voevent
      - ivorns: A list of ivorn strings. In keeping with the rest of this library,
        the 'ivo://' prefix should be omitted.
      - citation_type: Should be one of the pre-defined ``cite_values``.
      - description: Free text - should not contain any html tags
        since this will upset the XML spec.

    .. todo:: Implement CDATA escaping, if anyone actually requires it.
    """
    if not voevent.xpath('Citations'):
        etree.SubElement(voevent, 'Citations')
    while voevent.Citations.xpath('EventIvorn'):
        del voevent.Citations.EventIvorn
    for ivn in ivorns:
        etree.SubElement(voevent.Citations, 'EventIVORN', cite=citation_type)
        voevent.Citations.EventIVORN[-1] = ''.join(('ivo://', ivn))
    if description is not None:
        voevent.Citations.Description = description

