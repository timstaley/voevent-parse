import unittest
from unittest import TestCase
from voeparse.tests.resources import datapaths

from lxml import objectify, etree
#from astropysics.coords.coordsys import FK5Coordinates
from copy import copy
import datetime

import voeparse as voe

class TestValidation(TestCase):
    def shortDescription(self):
        return None
    def test_schema_valid_for_test_data(self):
        """
        First, let's check everything is in order with the test data
        and the schema.

        Here we directly access the lxml validate routine.
        """
        v = objectify.parse(datapaths.swift_bat_grb_pos_v2).getroot()
        self.assertTrue(voe.voevent_v2_0_schema.validate(v))
        Who = v['{}Who']
        Who.BadChild = 42
        self.assertFalse(voe.voevent_v2_0_schema.validate(v))
        del Who.BadChild
        self.assertTrue(voe.voevent_v2_0_schema.validate(v))

        #NB dropping the namespace from root element invalidates packet:
        # This is why we must re-insert it before output.
        v.tag = 'VOEvent'
        self.assertFalse(voe.voevent_v2_0_schema.validate(v))

    def test_validation_routine(self):
        """
        Now we perform the same validation tests, but applied via the
        convenience functions.
        """
        with open(datapaths.swift_bat_grb_pos_v2) as f:
            v = voe.load(f)
        self.assertTrue(voe.valid_as_v2_0(v))
        v.Who.BadChild = 42
        self.assertFalse(voe.valid_as_v2_0(v))
        del v.Who.BadChild
        self.assertTrue(voe.valid_as_v2_0(v))

    def test_invalid_error_reporting(self):
        with self.assertRaises(etree.DocumentInvalid):
            v = voe.Voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id='001',
                             role='DeadParrot')
            voe.assert_valid_as_v2_0(v)



class TestIO(TestCase):
    def shortDescription(self):
        return None
    def test_load_of_voe_v2(self):
        with open(datapaths.swift_bat_grb_pos_v2) as f:
            vff = voe.load(f)
        with open(datapaths.swift_bat_grb_pos_v2) as f:
            vfs = voe.loads(f.read())
        self.assertEqual(objectify.dump(vff), objectify.dump(vfs))
        self.assertEqual(vfs.tag, 'VOEvent')
        self.assertEqual(vfs.attrib['ivorn'],
                         'ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_532871-729')

    def test_dumps(self):
        """
        Note, the processed output does not match the raw input -
        because I have added the UTF-8 encoding declaration.
        So we match the convenience routines against an
        etree.tostring processed version of the original.
        """
        swift_grb_v2_raw = objectify.parse(
                                  datapaths.swift_bat_grb_pos_v2).getroot()
        with open(datapaths.swift_bat_grb_pos_v2) as f:
            swift_grb_v2_voeparsed = voe.load(f)
        raw = etree.tostring(swift_grb_v2_raw,
                             pretty_print=False,
                             xml_declaration=True,
                             encoding='UTF-8')
        processed = voe.dumps(swift_grb_v2_voeparsed)
        self.assertEqual(raw, processed)

class TestMinimalVOEvent(TestCase):
    def test_make_minimal_voevent(self):
        v1 = voe.Voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id='100',
                             role='test')
        self.assertTrue(voe.valid_as_v2_0(v1))
        v2 = voe.Voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id=100,
                             role='test')
        self.assertEqual(v1.attrib['ivorn'], v2.attrib['ivorn'])

class TestWho(TestCase):
    def setUp(self):
        self.v = voe.Voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id=100,
                             role='test')
        self.date = datetime.datetime.now()



    def test_set_who_date(self):
        voe.set_who(self.v, self.date)
        self.assertTrue(voe.valid_as_v2_0(self.v))

    def test_set_who_minimal(self):
        voe.set_who(self.v, self.date, author_ivorn='voevent.soton.ac.uk/TEST')
        self.assertTrue(voe.valid_as_v2_0(self.v))

    def test_set_author(self):
        voe.set_author(self.v, title='4 Pi Sky Project',
                       shortName='4PiSky',
                       contactName='Tim Staley',
                       contactEmail='tim.staley@soton.ac.uk',
                       contactPhone='123456789',
                       contributor='Bob')
        self.assertTrue(voe.valid_as_v2_0(self.v))
        self.assertEqual(self.v.Who.Author.shortName, '4PiSky')

class TestWhat(TestCase):
    def shortDescription(self):
        return None
    def setUp(self):
        self.v = voe.Voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id='100',
                             role='test')

    def test_autoconvert_off(self):
        """Param values can only be strings..."""
        self.v.What.append(voe.Param(name='Dead Parrot', ac=False))
        self.v.What.append(voe.Param(name='The Answer', value=str(42), ac=False))
        self.assertTrue(voe.valid_as_v2_0(self.v))
        
        with self.assertRaises(TypeError):
            self.v.What.append(voe.Param(name='IntValue', value=42, ac=False))


    def test_autoconvert_on(self):
        """...but we provide some python smarts to alleviate this."""
        self.v.What.append(voe.Param(name='Dead Parrot'))
        self.v.What.append(voe.Param(name='The Answer', value=42))
        self.v.What.append(voe.Param(name='What is the time?',
                                     value=datetime.datetime.now()))
        self.v.What.append(voe.Param(name='This is a lie',
                                     value=False))
        self.assertTrue(voe.valid_as_v2_0(self.v))
#         print
#         print voe.prettystr(self.v.What)


class TestWhereWhen(TestCase):
    def setUp(self):
        self.v = voe.Voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id='100',
                             role='test')
    def test_set_wherewhen(self):
        c = voe.Position2D(ra=123.456, dec=45.678,
                       err=0.1,
                       units='deg', system='UTC-FK5-GEO'
                       )
        voe.set_where_when(self.v, coords=c,
                           obs_time=datetime.datetime.now(),
                           observatory_location=voe.definitions.observatory_location.geosurface)
        self.assertTrue(voe.valid_as_v2_0(self.v))
        self.assertEqual(c, voe.pull_astro_coords(self.v))

class TestHow(TestCase):
    def setUp(self):
        self.v = voe.Voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id='100',
                             role='test')
    def test_add_How(self):
        descriptions = ['One sentence.', 'Another.']
        voe.add_how(self.v, descriptions)
        self.assertEqual(len(self.v.How.Description), 2)
        self.assertEqual(descriptions,
                         [self.v.How.Description[0], self.v.How.Description[1]])
        refs = [voe.Reference('http://www.saltycrane.com/blog/2011/07/'
                              'example-parsing-xml-lxml-objectify/'),
                voe.Reference('http://github.com/timstaley/voevent-parse')]
        voe.add_how(self.v, references=refs)
        self.assertEqual(len(self.v.How.Reference), len(refs))
        self.assertEqual([r.attrib['uri'] for r in refs],
                         [r.attrib['uri'] for r in self.v.How.Reference])

        self.assertTrue(voe.valid_as_v2_0(self.v))

class TestWhy(TestCase):
    def setUp(self):
        self.v = voe.Voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id='100',
                             role='test')

    def test_add_why(self):
        inferences = [voe.Inference(probability=0.5, relation=None,
                                    name='Toin Coss', concept='Probability')]
        voe.add_why(self.v, importance=0.6,
                    expires=datetime.datetime(2013, 1, 1),
                    inferences=inferences)
        self.assertTrue(voe.valid_as_v2_0(self.v))
        self.assertEqual(self.v.Why.attrib['importance'], str(0.6))
        self.assertEqual(self.v.Why.Inference[0].attrib['probability'], str(0.5))
        self.assertEqual(self.v.Why.Inference[0].Name, 'Toin Coss')

class TestCitations(TestCase):
    def setUp(self):
        self.v = voe.Voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id='100',
                             role='test')
    def test_followup_citation(self):
        ref = 'ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_532871-729'
        voe.add_citations(self.v,
                          voe.Citation('ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_532871-729',
                               cite_type=voe.cite_types.followup)
                          )
        self.assertTrue(voe.valid_as_v2_0(self.v))
        self.assertEqual(len(self.v.Citations.getchildren()), 1)
#         print voe.prettystr(self.v.Citations)
        voe.add_citations(self.v,
                          voe.Citation('ivo://nasa.gsfc.gcn/SWIFT#BAT_GRB_Pos_532871-730',
                               cite_type=voe.cite_types.followup)
                          )
        self.assertTrue(voe.valid_as_v2_0(self.v))
#         print voe.prettystr(self.v.Citations)
        self.assertEqual(len(self.v.Citations.getchildren()), 2)

class TestConvenienceRoutines(TestCase):
    def setUp(self):
        with open(datapaths.swift_bat_grb_pos_v2) as f:
            self.swift_grb_v2_packet = voe.load(f)
        self.blank = voe.Voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id='100',
                             role='test')
    def test_pull_astro_coords(self):
        known_swift_grb_posn = voe.Position2D(ra=74.741200, dec= -9.313700,
                                             err=0.05,
                                             units='deg',
                                             system='UTC-FK5-GEO')
        p = voe.pull_astro_coords(self.swift_grb_v2_packet)
        self.assertEqual(p, known_swift_grb_posn)
        self.assertIsInstance(p.ra, float)

    def test_pull_params(self):
        params = voe.pull_params(self.swift_grb_v2_packet)

        self.assertEqual(params[None]['Packet_Type']['value'], '61')
        self.assertEqual(params['Misc_Flags']['Values_Out_of_Range']['value'],
                         'false')

        params = voe.pull_params(self.blank)
        self.assertEqual(params, {})

        single_par = copy(self.blank)
        single_par.What.append(voe.Param(name="test_param", value=123))
        params = voe.pull_params(single_par)
        self.assertEqual(len(params), 1)
    
    def test_pull_isotime(self):
        isotime = voe.pull_isotime(self.swift_grb_v2_packet)
        self.assertIsInstance(isotime, datetime.datetime)

        null_result = voe.pull_isotime(self.blank)
        self.assertIsNone(null_result)
