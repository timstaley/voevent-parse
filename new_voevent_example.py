import datetime
import voeparse as vp
from lxml import etree

v = vp.Voevent(stream='astronomy.physics.science.org/super_exciting_events',
               stream_id=123, role=vp.roles.test)

vp.set_who(v, date=datetime.datetime.now(),
           author_ivorn="www.4pisky.soton.ac.uk")

vp.set_author(v, title="4PiSky Testing Node",
              shortName="Tim"
              )

p_flux = vp.Param(name='peak_flux',
                        value=1.5e-3,
                        unit='Janskys',
                        ucd='em.radio.100-200MHz'
                        )

p_flux.Description = 'Peak Flux'
int_flux = vp.Param(name='int_flux',
                          value=2.0e-3,
                        unit='Janskys',
                        ucd='em.radio.100-200MHz')
int_flux.Description = 'Integrated Flux'

v.What.append(vp.Group(params=[p_flux, int_flux], name='source_flux'))

v.What.append(vp.Param(name="amb_temp",
                       value=15.5,
                       unit='degrees',
                       ucd='phys.temperature',
                       dataType='float'))
v.What[-1].Description = "Ambient temperature at telescope"

vp.set_where_when(v,
                  coords=vp.Position2D(ra=123.5, dec=45, err=0.1,
                                             units='deg',
                                             system=vp.sky_coord_system.fk5),
                  obs_time=datetime.datetime(2013, 1, 31, 12, 05, 30),
                  observatory_location=vp.observatory_location.geosurface)

print "\n***Here is your WhereWhen:***\n"
print vp.prettystr(v.WhereWhen)

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
                     cite_type=vp.cite_types.followup))


vp.assert_valid_as_v2_0(v)

with open('new_voevent_example.xml', 'w') as f:
    vp.dump(v, f, validate=True)

