import datetime
import voeparse as vp
from lxml import etree

v = vp.Voevent(stream='astronomy.physics.science.org/super_exciting_events',
               stream_id=123, role=vp.definitions.roles.test)

vp.set_who(v, date=datetime.datetime.utcnow(),
           author_ivorn="www.4pisky.soton.ac.uk")

vp.set_author(v, title="4PiSky Testing Node",
              shortName="Tim"
              )


#Strictly speaking, parameter values should be strings,
# with a manually specified dataType;
# `string` (default), `int` , or `float`.
int_flux = vp.Param(name='int_flux',
                          value="2.0e-3",
                        unit='Janskys',
                        ucd='em.radio.100-200MHz',
                        dataType='float',
                        ac=False)
int_flux.Description = 'Integrated Flux'

# But with ac=True (autoconvert) we switch on some logic to take care
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

vp.set_where_when(v,
              coords=vp.Position2D(ra=123.5, dec=45, err=0.1,
                                   units='deg',
                                   system=vp.definitions.sky_coord_system.fk5),
              obs_time=datetime.datetime(2013, 1, 31, 12, 05, 30),
              observatory_location=vp.definitions.observatory_location.geosurface)

print "\n***Here is your WhereWhen:***\n"
print vp.prettystr(v.WhereWhen)

print "\n***And your What:***\n"
print vp.prettystr(v.What)

vp.add_how(v, descriptions='Discovered via 4PiSky',
           references=vp.Reference('http://www.4pisky.soton.ac.uk/'))

vp.add_why(v, importance=0.5,
           inferences=vp.Inference(probability=0.1,
                                 relation='identified',
                                 name='GRB121212A',
                                 concept='process.variation.burst;em.radio')
           )

vp.add_citations(v,
         vp.Citation(ivorn='ivo://astronomy.physics.science.org/super_exciting_events#101',
                     cite_type=vp.definitions.cite_types.followup))


vp.assert_valid_as_v2_0(v)

with open('new_voevent_example.xml', 'w') as f:
    vp.dump(v, f, validate=True)

