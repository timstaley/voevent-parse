Change history
==============

1.0.2 - 2018/02/10
--------------------
Fixes
~~~~~
Fix some minor issues with the the 'prettystr' routine:

* Ensure return of a string type in Python3 (was bytes).
* Fix printing of whole packet (#6, with thanks to @henrilouvin).

1.0.1 - 2016/11/28
--------------------
Fixes
~~~~~
Minor bugfix - bring back importing of deprecated 'pull_astro_coords'
function into the package-root namespace.


1.0.0 - 2016/11/28
--------------------
API Changes
~~~~~~~~~~~
Some routines have been renamed, with the old aliases preserved for backwards
compatibility for now:

- ``add_where_when`` now has an extra boolean parameter,
  'allow_tz_naive_datetime' which defaults to False - so by default you
  must supply a **timezone-aware** datetime (this should help to avoid
  mistakenly supplying a timezone-naive datetime which is non-UTC).
- ``Citation`` is now deprecated in favour of the alias ``EventIvorn``.
- ``pull_isotime`` is now deprecated in favour of the alias
  ``get_event_time_as_utc``.
- ``pull_astro_coords`` is now deprecated in favour of the alias
  ``get_event_position``.
- ``pull_params`` is now deprecated in favour of the improved replacement
  functions ``get_grouped_params`` and ``get_toplevel_params``. Separating
  this functionality into two routines ensures return of datastructures with
  sensible nesting-depth (i.e. ``toplevel[ParamName][AttrName]`` or
  ``grouped[GroupName][ParamName][AttrName]``), and avoids problems with
  GroupNames clashing with top-level ParamNames, etc. The returned
  datastructures are of type
  `orderedmultidict.omdict <https://github.com/gruns/orderedmultidict>`_,
  which provides robust handling of duplicated names.

Docs
~~~~
Documentation now includes tutorial material which was previously hosted in
a separate GitHub repo.

Fixes
~~~~~
Fix a regression from 0.9.8: Switching from from iso8601 library to astropy
for ISO-format timestamp parsing introduced a failure case, as astropy does
not parse timestamps with the '+0' timezone-signifier suffix. Timestamps of
this style are now parsed correctly. In addition, ``add_where_when`` will
now generate ISO-format timestamps that do not include the suffix (since
strictly speaking the VOEvent standard specifies the UTC timezone - or something
altogether non-terrestial, e.g. TDB - already).

General refactoring
~~~~~~~~~~~~~~~~~~~
Library code now resides under /src, which provides more reliable testing
cf
https://blog.ionelmc.ro/2014/05/25/python-packaging/,
https://hynek.me/articles/testing-packaging/.


0.9.8 - 2016/11/09
------------------
Enhancement to ``pull_isotime`` convenience function: Add support for 
conversion of event-timestamps to UTC from the TDB (Barycentric Dynamical 
Time) format. This is now in use 'in the wild' for the GAIA VOEvent
stream.
(Support for remaining VOEvent timescales 'GPS' and 'TT' has been 
considered but needs a motivating use-case, see 
https://github.com/timstaley/voevent-parse/issues/5 )
NB this functionality introduces a dependence on Astropy>=1.2. (While this
seems a little like using a sledgehammer to crack a nut, it's likely to be a
useful library for anyone handling VOEvents anyway, and barycentric time
correction codes are hard to find).

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
