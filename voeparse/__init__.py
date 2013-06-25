"""Convenience routines allowing easy access to information in VOEvent packets."""
#Tim Staley, <timstaley337@gmail.com>, 2012

from __future__ import absolute_import
import lxml.objectify
import lxml.etree
from voeparse.definitions import *
from voeparse.misc import Param, Group, Reference, Inference, Position2D, Citation
from voeparse.voevent import *

__version__ = version
###########################################################
# Various convenience routines...
###########################################################

def prettystr(subtree):
    """Print an element tree with nice indentation.

    Prettyprinting a whole VOEvent doesn't seem to work - possibly this is
    due to whitespacing issues in the skeleton string definition.
    This function is a quick workaround for easily desk-checking
    what you're putting together.
    """
    lxml.objectify.deannotate(subtree)
    lxml.etree.cleanup_namespaces(subtree)
    return lxml.etree.tostring(subtree, pretty_print=True)

def pull_astro_coords(voevent):
    """Returns a Position2D namedtuple."""
    ac = voevent.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoords
    ac_sys = voevent.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoordSystem
    sys = ac_sys.attrib['id']

    try:
        assert ac.Position2D.Name1 == 'RA' and ac.Position2D.Name2 == 'Dec'
        posn = Position2D(ra=ac.Position2D.Value2.C1,
                          dec=ac.Position2D.Value2.C2,
                          err=ac.Position2D.Error2Radius,
                          units=ac.Position2D.attrib['unit'],
                          system=sys)
    except AttributeError:
        raise ValueError("Unrecognised AstroCoords type")
    return posn

def pull_params(voevent):
    """Attempts to load the 'What' section of a voevent as a nested dictionary.

    Parameters without a group are indexed under the key 'None' - otherwise,
    we might get name-clashes between params and groups (unlikely but possible).

    Note that the dictionaries returned represent the 'attrib' accessor,
    so to get to the values you'll need to use something like::

      result[None]['ParamName']['value']

    Which is a bit tedious - but giving direct access means throwing away
    other attrib values such as the units and UCD. Of course, it's
    easy to manipulate the resulting dict as you wish.
    """
    result = {}
    w = voevent.What
    if not w: return result
    toplevel_params = {}
    result[None] = toplevel_params
    for p in voevent.What.Param:
        toplevel_params[p.attrib['name']] = p.attrib
    for g in voevent.What.Group:
        g_params = {}
        result[g.attrib['name']] = g_params
        for p in g.Param:
            g_params[p.attrib['name']] = p.attrib
    return result



#def get_isotime(voevent):
#    assert isinstance(voevent, voe.VOEvent)
#    try:
#        ol = voevent.WhereWhen.ObsDataLocation.ObservationLocation
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
