"""Convenience routines allowing easy access to information in VOEvent packets."""
#Tim Staley, <timstaley337@gmail.com>, 2012

from __future__ import absolute_import
import lxml.objectify
import lxml.etree
from voeparse.definitions import *
from voeparse.misc import Param, Group, Reference, Inference, Position2D, Citation
from voeparse.voevent import *
from voeparse.convenience import *
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


