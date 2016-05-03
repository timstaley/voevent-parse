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
    Param, Group,
    Reference, Inference,
    Position2D,
    Citation)
from voeventparse.convenience import (
    pull_astro_coords, pull_params, pull_isotime,
    prettystr)
