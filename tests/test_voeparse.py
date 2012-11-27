import unittest
from unittest import TestCase
from resources import datapaths

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
        v = voe.load(datapaths.swift_bat_grb_pos_v2)
        self.assertTrue(voe.valid_as_v2_0(v))
        v.Who.BadChild = 42
        self.assertFalse(voe.valid_as_v2_0(v))
        del v.Who.BadChild
        self.assertTrue(voe.valid_as_v2_0(v))

    def test_invalid_error_reporting(self):
        with self.assertRaises(etree.DocumentInvalid):
            voe.make_voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id='001',
                             role='DeadParrot')



class TestIO(TestCase):
    def shortDescription(self):
        return None
    def test_load_of_voe_v2(self):
        vff = voe.load(datapaths.swift_bat_grb_pos_v2)
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
        swift_grb_v2_voeparsed = voe.load(datapaths.swift_bat_grb_pos_v2)
        raw = etree.tostring(swift_grb_v2_raw,
                             pretty_print=True,
                             xml_declaration=True,
                             encoding='UTF-8')
        processed = voe.dumps(swift_grb_v2_voeparsed)
        self.assertEqual(raw, processed)


class TestMake(TestCase):
    def setUp(self):
        self.v = voe.make_voevent(stream='voevent.soton.ac.uk/TEST',
                             stream_id='100',
                             role='test')
        self.date = datetime.datetime.now()

    def test_make_minimal_voevent(self):
        self.assertTrue(voe.valid_as_v2_0(self.v))

    def test_set_who_date(self):
        voe.set_who(self.v, self.date)
        self.assertTrue(voe.valid_as_v2_0(self.v))

    def test_set_who_minimal(self):
        voe.set_who(self.v, self.date, author_stream='voevent.soton.ac.uk/TEST')
        self.assertTrue(voe.valid_as_v2_0(self.v))

    def test_add_author(self):
        voe.set_who(self.v, self.date)
        voe.set_author(self.v, title='4 Pi Sky Project',
                       short_name='4PiSky',
                       contact_name='Tim Staley',
                       contact_email='tim.staley@soton.ac.uk',
                       contact_phone='123456789',
                       contributor='Bob')
        self.assertTrue(voe.valid_as_v2_0(self.v))

class TestAstroCoords(TestCase):
    def test_swift_grb_v2(self):
        swift_grb_v2_packet = voe.load(datapaths.swift_bat_grb_pos_v2)
        known_swift_grb_posn = voe.Coords(ra=74.741200, dec= -9.313700,
                                             ra_err=0.05, dec_err=0.05,
                                             units='degrees',
                                             system='UTC-FK5-GEO')
        p = voe.pull_astro_coords(swift_grb_v2_packet)
        self.assertEqual(p, known_swift_grb_posn)






