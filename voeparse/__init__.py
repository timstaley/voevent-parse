"""Convenience routines allowing easy access to information in VOEvent packets."""
#Tim Staley, <timstaley337@gmail.com>, 2012

from __future__ import absolute_import
from voeparse.definitions import cite_values, coord_system, coord_units
from voeparse.misc import SimpleParam, Reference, Inference, Position2D
from voeparse.voevent import *


###########################################################
# Various convenience routines...
###########################################################

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

#def get_param_names(voevent):
#    '''
#    Grabs the "what" section of a voevent, and produces a list of tuples of group name and param name.
#    For a bare param, the group name is the empty string.
#    
#    NB. This replicates functionality from VOEventLib - but the inbuilt version is broken as of v0.3.
#    '''
#    list = []
#    w = voevent.What
#    if not w: return list
#    for p in voevent.What.Param:
#        list.append(('', p.name))
#    for g in voevent.What.Group:
#        for p in g.Param:
#            list.append((g.name, p.name))
#    return list
#


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
