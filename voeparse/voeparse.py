#pysovo VOEvent Tools
#Convenience functions allowing easy access to information in VOEvent packets. 
#Tim Staley, <timstaley337@gmail.com>, 2012

from lxml import objectify, etree
#from astropysics.coords.coordsys import FK5Coordinates

import schema
voevent_v2_0_schema = etree.XMLSchema(
                        etree.fromstring(schema.v2_0_str))

#NB this is not really used as a class but a namespace, 
# so we use lowercase_with_underscores name convention.
class build(object):
    @staticmethod
    def from_string(s, validate=False):
        """
        Wrapper to parse a VOEvent tree, taking care of some subtleties.
        
        Currently pretty basic, but we can imagine using this function to 
        homogenise or at least identify different VOEvent versions, etc.
        
        NB The namespace is removed from the root element tag to make 
        objectify access work as expected, so we must re-add it with 
        <output function to be determined> when we want to conform to schema.  
        """
        v = objectify.fromstring(s)
        build._remove_root_tag_prefix(v)
        return v

    @staticmethod
    def from_file(path):
        s = open(path, 'rb').read()
        return build.from_string(s)

    @staticmethod
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

    @staticmethod
    def _reinsert_root_tag_prefix(v):
        """
        Returns 'voe' namespace prefix to root tag.
        """
        v.tag = ''.join(('{', v.nsmap['voe'], '}VOEvent'))
        return

class output(object):
    @staticmethod
    def to_string(v, validate=False, pretty_print=True, xml_declaration=True):
        """Converts voevent 'v' to string.
        
        NB Encoding is UTF-8, in line with V2 schema.
        Declaring the encoding can cause diffs with the original loaded VOEvent,
        but I think it's probably the right thing to .
        """
        objectify.deannotate(v)
        build._reinsert_root_tag_prefix(v)
        s = etree.tostring(v, pretty_print=pretty_print,
                           xml_declaration=xml_declaration,
                           encoding='UTF-8')
        build._remove_root_tag_prefix(v)
        return s

class validate(object):
    @staticmethod
    def as_v2_0(v):
        objectify.deannotate(v)
        build._reinsert_root_tag_prefix(v)
        valid_bool = voevent_v2_0_schema.validate(v)
        build._remove_root_tag_prefix(v)
        return valid_bool


#
#def get_param_names(v):
#    '''
#    Grabs the "what" section of a voevent, and produces a list of tuples of group name and param name.
#    For a bare param, the group name is the empty string.
#    
#    NB. This replicates functionality from VOEventLib - but the inbuilt version is broken as of v0.3.
#    '''
#    list = []
#    w = v.What
#    if not w: return list
#    for p in v.What.Param:
#        list.append(('', p.name))
#    for g in v.What.Group:
#        for p in g.Param:
#            list.append((g.name, p.name))
#    return list
#

class CoordSystemIDs(object):
    fk5 = 'UTC-FK5-GEO'
#
#def pull_astro_coords(v):
#    """Attempts to determine coords system and convert to corresponding
#       astropysics class.
#    """
#    ac = v.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoords
#    ac_sys = v.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoordSystem
#
#    if ac_sys.attrib['id'] != CoordSystemIDs.fk5:
#        raise ValueError("Cannot extract astro_coords, unrecognised coord system")
#
#    try:
#        assert ac.Position2D.Name1 == 'RA'
#        ra_deg = ac.Position2D.Value2.C1
#        dec_deg = ac.Position2D.Value2.C2
#        err_deg = ac.Position2D.Error2Radius
#    except AttributeError:
#        raise ValueError("Unrecognised AstroCoords type")
#    return FK5Coordinates(ra=ra_deg, dec=dec_deg,
#                          raerror=err_deg, decerror=err_deg)


#def get_isotime(v):
#    assert isinstance(v, voe.VOEvent)
#    try:
#        ol = v.WhereWhen.ObsDataLocation.ObservationLocation
#        return ol.AstroCoords.Time.TimeInstant.ISOTime
#    except:
#        return None
#
#def make_Who(names, emails):
#    names = listify(names)
#    emails = listify(emails)
#    w = voe.Who()
#    w.Author = voe.Author()
#    w.Author.contactName = names
#    w.Author.contactEmail = emails
#    return w
