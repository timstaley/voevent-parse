"""
A package for concise manipulation of VOEvent XML packets.
"""

from __future__ import absolute_import
import os
from pkg_resources import get_distribution, DistributionNotFound

from voeparse.voevent import (
    Voevent,
    voevent_v2_0_schema,
    load, loads, dump, dumps,
    valid_as_v2_0, assert_valid_as_v2_0,
    set_who, set_author, set_where_when,
    add_how, add_why, add_citations
)
import voeparse.definitions as definitions
from voeparse.misc import (Param, Group, Reference, Inference, Position2D,
                           Citation)
from voeparse.convenience import (pull_astro_coords, pull_params, pull_isotime,
                                  prettystr)



###########################################################
# Versioning; see also
# http://stackoverflow.com/questions/17583443
###########################################################
try:
    _dist = get_distribution('voevent-parse')
    #The version number according to Pip:
    _nominal_version = _dist.version
    if not __file__.startswith(os.path.join(_dist.location, 'voeparse')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    #The actual copy in use if a custom PYTHONPATH or local dir import is used
    __version__ = 'Local import @ ' + os.path.dirname(os.path.abspath(__file__))
else:
    __version__ = _nominal_version


