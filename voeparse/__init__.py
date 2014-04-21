"""Convenience routines allowing easy access to information in VOEvent packets."""
#Tim Staley, <timstaley337@gmail.com>, 2012

from __future__ import absolute_import
import os
from pkg_resources import get_distribution, DistributionNotFound

import lxml.objectify
import lxml.etree
from voeparse.definitions import *
from voeparse.misc import Param, Group, Reference, Inference, Position2D, Citation
from voeparse.voevent import *
from voeparse.convenience import *


###########################################################
# Versioning; see also
# http://stackoverflow.com/questions/17583443
###########################################################
try:
    _dist = get_distribution('voevent-parse')
    if not __file__.startswith(os.path.join(_dist.location, 'voeparse')):
        # not installed, but there is another version that *is*
        raise DistributionNotFound
except DistributionNotFound:
    __version__ = 'Local import @ '+os.path.dirname(os.path.abspath(__file__))
else:
    __version__ = _dist.version

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


