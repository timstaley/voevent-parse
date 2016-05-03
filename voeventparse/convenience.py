"""Convenience routines for common actions on VOEvent objects"""

from __future__ import absolute_import
import iso8601
import lxml
from collections import OrderedDict
from voeventparse.misc import (Param, Group, Reference, Inference, Position2D,
                               Citation)
from copy import deepcopy



def pull_astro_coords(voevent, index=0):
    """Extracts the `AstroCoords` from a given `WhereWhen.ObsDataLocation`.

    Note that a packet may include multiple 'ObsDataLocation' entries
    under the 'WhereWhen' section, for example giving locations of an object
    moving over time. Most packets will have only one, however, so the
    default is to just return co-ords extracted from the first.

    Args:
        voevent (:class:`voeventparse.voevent.Voevent`): Root node of the
            VOEvent etree.
        index (int): Index of the ObsDataLocation to extract AstroCoords from.

    Returns:
        Position (:py:class:`.Position2D`): The sky position defined in the
        ObsDataLocation.
    """
    od = voevent.WhereWhen.ObsDataLocation[index]
    ac = od.ObservationLocation.AstroCoords
    ac_sys = voevent.WhereWhen.ObsDataLocation.ObservationLocation.AstroCoordSystem
    sys = ac_sys.attrib['id']


    if hasattr(ac.Position2D, "Name1"):
        assert ac.Position2D.Name1 == 'RA' and ac.Position2D.Name2 == 'Dec'
    posn = Position2D(ra=float(ac.Position2D.Value2.C1),
                      dec=float(ac.Position2D.Value2.C2),
                      err=float(ac.Position2D.Error2Radius),
                      units=ac.Position2D.attrib['unit'],
                      system=sys)
    return posn


def pull_isotime(voevent, index=0):
    """Extracts the event time from a given `WhereWhen.ObsDataLocation`.

    Accesses a `WhereWhere.ObsDataLocation.ObservationLocation`
    element and returns the AstroCoords.Time.TimeInstant.ISOTime element,
    converted to a (UTC-timezoned) datetime.

    Note that a packet may include multiple 'ObsDataLocation' entries
    under the 'WhereWhen' section, for example giving locations of an object
    moving over time. Most packets will have only one, however, so the
    default is to access the first.

    .. warning::

        This function currently only works with UTC time-system coords.
        Future updates may implement conversion from other systems (TT, GPS)
        using astropy functionality.

    Args:
        voevent (:class:`voeventparse.voevent.Voevent`): Root node of the VOevent
            etree.
        index (int): Index of the ObsDataLocation to extract an ISOtime from.

    Returns:
        isotime (:class:`datetime.datetime`): Datetime object as parsed by
        `iso8601`_ (with UTC timezone).

    .. _iso8601: https://pypi.python.org/pypi/iso8601/

    """
    try:
        od = voevent.WhereWhen.ObsDataLocation[index]
        ol = od.ObservationLocation
        coord_sys = ol.AstroCoords.attrib['coord_system_id']
        if coord_sys.split('-')[0] != 'UTC':
            raise NotImplementedError(
                'Loading from time-systems other than UTC not yet implemented'
            )
        isotime_str = str(ol.AstroCoords.Time.TimeInstant.ISOTime)
        return iso8601.parse_date(isotime_str)
    except AttributeError:
        return None


def pull_params(voevent):
    """Attempts to load the `What` section of a voevent as a nested dictionary.

    Args:
        voevent (:class:`voeventparse.voevent.Voevent`): Root node of the VOevent etree.
    Returns:
        Nested dict (dict): Mapping of ``Group->Param->Attribs``.
        Access like so::

            foo_param_val = what_dict['GroupName']['ParamName']['value']

        .. note::

          Parameters without a group are indexed under the key 'None' - otherwise,
          we might get name-clashes between `params` and `groups` (unlikely but
          possible) so for ungrouped Params you'll need something like::

            what_dict[None]['ParamName']['value']

    """
    result = OrderedDict()
    w = voevent.What
    if w.countchildren() == 0:
        return result
    toplevel_params = OrderedDict()
    result[None] = toplevel_params
    if hasattr(voevent.What, 'Param'):
        for p in voevent.What.Param:
            toplevel_params[p.attrib['name']] = p.attrib
    if hasattr(voevent.What, 'Group'):
        for g in voevent.What.Group:
            g_params = {}
            result[g.attrib['name']] = g_params
            if hasattr(g, 'Param'):
                for p in g.Param:
                    g_params[p.attrib['name']] = p.attrib
    return result


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
    subtree = deepcopy(subtree)
    lxml.objectify.deannotate(subtree)
    lxml.etree.cleanup_namespaces(subtree)
    return lxml.etree.tostring(subtree, pretty_print=True)


