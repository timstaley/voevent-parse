Change history
===============


Unreleased - 2016/11
--------------------
API Changes
~~~~~~~~~~~~
Some routines have been renamed, with the old aliases preserved for backwards
compatibility for now:

 - ``pull_isotime`` is now deprecated in favour of the alias
   ``pull_event_time_as_utc``.
 - ``Citation`` is now deprecated in favour of the alias ``EventIvorn``.


0.9.8 - 2016/11/09
-------------------
Enhancement to ``pull_isotime`` convenience function: Add support for 
conversion of event-timestamps to UTC from the TDB (Barycentric Dynamical 
Time) format. This is now in use 'in the wild' for the GAIA VOEvent
stream.
(Support for remaining VOEvent timescales 'GPS' and 'TT' has been 
considered but needs a motivating use-case, see 
https://github.com/timstaley/voevent-parse/issues/5 )

0.9.7 - 2016/10/31 
------------------
Identical to 0.96, fixes a packaging issue most likely due to temporary
files / dev installation confusing the packager.

0.9.6 - 2016/10/31 
------------------
Minor bugfix to ``pull_params``: Don't bork on missing Param name.
However, note that if multiple Params are present without a `name`
attribute then this convenience routine doesn't really make sense - see
warning in docs.

0.9.5 - 2016/05/03
------------------
Switch to versioneer for version numbering / release tagging.
CF https://github.com/warner/python-versioneer