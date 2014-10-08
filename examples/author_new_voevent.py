#!/usr/bin/python
import datetime
import os
import voeventparse as vp
from lxml import etree


# Set the basic packet ID and Author details

v = vp.Voevent(stream='astronomy.physics.science.org/super_exciting_events',
               stream_id=123, role=vp.definitions.roles.test)

vp.set_who(v, date=datetime.datetime.utcnow(),
           author_ivorn="voevent.4pisky.org")

vp.set_author(v, title="4PiSky Testing Node",
              shortName="Tim"
)


# Now create some Parameters for entry in the 'What' section.

# Strictly speaking, parameter values should be strings,
# with a manually specified dataType; one of
# `string` (default), `int` , or `float`.
# e.g.
int_flux = vp.Param(name='int_flux',
                    value="2.0e-3",
                    unit='Janskys',
                    ucd='em.radio.100-200MHz',
                    dataType='float',
                    ac=False)
int_flux.Description = 'Integrated Flux'

# But with ac=True (autoconvert) we switch on some magic to take care
# of this for us automatically.
# See ``Param`` docstring for details.
p_flux = vp.Param(name='peak_flux',
                  value=1.5e-3,
                  unit='Janskys',
                  ucd='em.radio.100-200MHz',
                  ac=True
)
p_flux.Description = 'Peak Flux'

v.What.append(vp.Group(params=[p_flux, int_flux], name='source_flux'))

#Note ac=True (autoconvert) is the default setting if dataType=None (the default)
amb_temp = vp.Param(name="amb_temp",
                    value=15.5,
                    unit='degrees',
                    ucd='phys.temperature')

amb_temp.Description = "Ambient temperature at telescope"
v.What.append(amb_temp)


# Now we set the sky location of our event:
vp.add_where_when(v,
                  coords=vp.Position2D(ra=123.5, dec=45, err=0.1,
                                       units='deg',
                                       system=vp.definitions.sky_coord_system.fk5),
                  obs_time=datetime.datetime(2013, 1, 31, 12, 05, 30),
                  observatory_location=vp.definitions.observatory_location.geosurface)

# Prettyprint some sections for desk-checking:
print "\n***Here is your WhereWhen:***\n"
print vp.prettystr(v.WhereWhen)

print "\n***And your What:***\n"
print vp.prettystr(v.What)

# You would normally describe or reference your telescope / instrument here:
vp.add_how(v, descriptions='Discovered via 4PiSky',
           references=vp.Reference('http://4pisky.org'))

# The 'Why' section is optional, allows for speculation on probable
# astrophysical cause
vp.add_why(v, importance=0.5,
           inferences=vp.Inference(probability=0.1,
                                   relation='identified',
                                   name='GRB121212A',
                                   concept='process.variation.burst;em.radio')
)

# We can also cite earlier VOEvents:
vp.add_citations(v,
                 vp.Citation(
                     ivorn='ivo://astronomy.physics.science.org/super_exciting_events#101',
                     cite_type=vp.definitions.cite_types.followup))

# Check everything is schema compliant:
vp.assert_valid_as_v2_0(v)

output_filename = 'new_voevent_example.xml'
with open(output_filename, 'w') as f:
    vp.dump(v, f)

print "Wrote your voevent to ", os.path.abspath(output_filename)