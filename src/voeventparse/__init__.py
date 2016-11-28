"""
A package for concise manipulation of VOEvent XML packets.
"""

from __future__ import absolute_import

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

from voeventparse.voevent import (
    Voevent,
    voevent_v2_0_schema,
    load, loads, dump, dumps,
    valid_as_v2_0, assert_valid_as_v2_0,
    set_who, set_author, add_where_when,
    add_how, add_why, add_citations
)
import voeventparse.definitions as definitions
from voeventparse.misc import (
    Citation,
    EventIvorn,
    Group,
    Inference,
    Param,
    Position2D,
    Reference,
)
from voeventparse.convenience import (
    get_event_time_as_utc,
    get_grouped_params,
    get_toplevel_params,
    get_event_position,
    pull_astro_coords,
    pull_isotime,
    pull_params,
    prettystr,
)
