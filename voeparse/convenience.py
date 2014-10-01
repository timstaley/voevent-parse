"""Convenience routines for common actions on VOEvent objects"""

from __future__ import absolute_import
import datetime
import lxml
from voeparse.misc import (Param, Group, Reference, Inference, Position2D, 
                           Citation)
def pull_astro_coords(voevent):
    """Extracts the `AstroCoords` from the first `WhereWhen.ObservationLocation`.

    Args:
        voevent (:class:`voeparse.voevent.Voevent`): Root node of the VOevent etree.
    Returns:
        :py:class:`.Position2D`: The position defined by the first
            ObservationLocation element under the WhereWhen section.
    """
    ac = voevent.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoords
    ac_sys = voevent.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoordSystem
    sys = ac_sys.attrib['id']

    try:
        assert ac.Position2D.Name1 == 'RA' and ac.Position2D.Name2 == 'Dec'
        posn = Position2D(ra=float(ac.Position2D.Value2.C1),
                          dec=float(ac.Position2D.Value2.C2),
                          err=float(ac.Position2D.Error2Radius),
                          units=ac.Position2D.attrib['unit'],
                          system=sys)
    except AttributeError:
        raise ValueError("Unrecognised AstroCoords type")
    return posn


def pull_params(voevent):
    """Attempts to load the `What` section of a voevent as a nested dictionary.

    Args:
        voevent (:class:`voeparse.voevent.Voevent`): Root node of the VOevent etree.
    Returns:
        Nested dict: Mapping of ``Group->Param->Attribs``. Access like so::

            foo_param_val = what_dict['GroupName']['ParamName']['value']

        .. note::

          Parameters without a group are indexed under the key 'None' - otherwise,
          we might get name-clashes between `params` and `groups` (unlikely but
          possible) so for ungrouped Params you'll need something like::

            what_dict[None]['ParamName']['value']

    """
    result = {}
    w = voevent.What
    if w.countchildren() == 0:
        return result
    toplevel_params = {}
    result[None] = toplevel_params
    if hasattr(voevent.What, 'Param'):
        for p in voevent.What.Param:
            toplevel_params[p.attrib['name']] = p.attrib
    if hasattr(voevent.What, 'Group'):
        for g in voevent.What.Group:
            g_params = {}
            result[g.attrib['name']] = g_params
            for p in g.Param:
                g_params[p.attrib['name']] = p.attrib
    return result


def pull_isotime(voevent):
    """Extract the event time from the WhereWhen section, if present.

    Accesses the first `WhereWhere.ObsDataLocation.ObservationLocation`
    element and returns the AstroCoords.Time.TimeInstant.ISOTime element,
    converted to a datetime.

    Args:
        voevent (:class:`voeparse.voevent.Voevent`): Root node of the VOevent
            etree.
    Returns:
        :class:`datetime.datetime`: Specifically, we return a standard library
            datetime object, i.e. one that is **timezone-naive** (that is,
            agnostic about its timezone, see python docs).
            This avoids an added dependency on pytz.

    The details of the reference system for time and space are provided
    in the AstroCoords object, but typically time reference is UTC.

    """
    try:
        ol = voevent.WhereWhen.ObsDataLocation.ObservationLocation
        isotime_str = str(ol.AstroCoords.Time.TimeInstant.ISOTime)
        return datetime.datetime.strptime(isotime_str, "%Y-%m-%dT%H:%M:%S.%f")
    except AttributeError:
        return None


def prettystr(subtree):
    """Print an element tree with nice indentation.

    Prettyprinting a whole VOEvent often doesn't seem to work, probably for
    issues relating to whitespace cf.
    http://lxml.de/FAQ.html#why-doesn-t-the-pretty-print-option-reformat-my-xml-output
    This function is a quick workaround for prettyprinting a subsection
    of a VOEvent, for easier desk-checking.

    Args:
        subtree(lxml.etree): A node in the VOEvent element tree.
    Returns:
        string: Prettyprinted string representation of the raw XML.
    """
    lxml.objectify.deannotate(subtree)
    lxml.etree.cleanup_namespaces(subtree)
    return lxml.etree.tostring(subtree, pretty_print=True)


